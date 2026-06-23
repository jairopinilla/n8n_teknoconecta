# Reglas accionables de renta corta (para agentes)

> Convierte las recomendaciones de `documentacion/playbook_renta_corta.md` y `documentacion/insights_airbnb_2026-06-22.md` en reglas ejecutables con las APIs reales (PriceLabs y Stays).
> Lo leen tanto el agente de OpenCode como Chitara (Hermes).
> Version: 2026-06-23

---

## Como usar este documento

Cada regla tiene: disparador -> como medir (tool real) -> umbral -> accion -> tipo de ejecucion -> verificacion -> que NO hacer.

Etiquetas de accion:
- 🟢 **API**: ejecutable con las herramientas MCP (PriceLabs/Stays).
- 🟡 **UI**: solo configurable en el panel web de PriceLabs (la API no lo expone). La regla genera una ALERTA con los pasos.
- 🔴 **Humano**: requiere accion fuera de API (fotos, titulo, promos de Airbnb, soporte). La regla NOTIFICA (ej. Telegram).

Tipo de ejecucion:
- **AUTO**: el diagnostico (solo lecturas) se puede correr sin pedir permiso.
- **GATED**: cualquier cambio de precio o escritura requiere aprobacion explicita del usuario y `confirmed=True`. Sigue el "PROTOCOLO DE CAMBIOS DE PRECIOS" de AGENTS.md (10 pasos). Nunca aplicar sin OK.

---

## Herramientas disponibles (lo que SI permite cada API)

### PriceLabs (MCP)
| Tool | Tipo | Uso |
|------|------|-----|
| `pricelabs_get_listings()` | lectura | Lista todos los listings (id, base_price, min_price, max_price, currency) |
| `pricelabs_get_listing(listing_id)` | lectura | Un listing (base/min/max actuales) |
| `pricelabs_fetch_prices(listing_id, pms)` | lectura | Precios por fecha ya refrescados |
| `pricelabs_update_listings(listings, confirmed)` | escritura GATED | Actualiza SOLO base_price/min_price/max_price |
| `pricelabs_push_prices(listing_id, pms, confirmed)` | escritura GATED | Empuja precios al PMS (Stays) |

`pms="stays"` para nuestras unidades.

**La API de PriceLabs NO expone** (esto es solo UI -> etiqueta 🟡): ocupacion propia, datos de mercado/vecindario, descuentos de ultimo minuto, reglas de estadia minima, ajustes por ocupacion, perfiles de temporada, overrides por fecha.

### Stays (MCP)
| Tool | Tipo | Uso |
|------|------|-----|
| `stays_get_reservations(from_date, to_date, date_type, listing_id, limit, offset)` | lectura | Reservas por rango (para calcular ocupacion propia) |
| `stays_search_listings(from_date, to_date, guests, rooms, ...)` | lectura | Disponibilidad / listings |

**Stays API es solo lectura util.** Escritura (promo codes, checkout, pagos) responde 404: NO usar para acciones.

### Unidades
901, 902, 709, 702 (Tarapaca 1140). Obtener los `listing_id` de PriceLabs con `pricelabs_get_listings()`; las reservas por unidad con `stays_get_reservations(..., listing_id)`. Mapeo Stays `_idlisting` <-> Directus `AlojamientoStayslistingIdLargo`.

### Como medir ocupacion propia (fórmula)
Ocupacion (%) = noches ocupadas / noches disponibles * 100 (ver `05_finanzas_y_pricing/kpis.md`).
Para una ventana: `stays_get_reservations(from=hoy, to=hoy+N, date_type="arrival", listing_id)` -> contar noches reservadas dentro de la ventana / N.
Ventana de conversion del negocio: **7 dias** (la mayoria de reservas entra en ese rango).

> Limitacion: la **ocupacion de MERCADO** (para comparar "estoy por encima/debajo del mercado") NO esta en la API; se lee del UI de PriceLabs (Datos del Vecindario / Market Dashboard). Cuando una regla la requiera, va como 🟡UI.

---

## Reglas

### R1 — Sin reservas en la ventana de conversion (7 dias)
- **Disparador:** 0 reservas en los proximos 7 dias en una unidad.
- **Medir (AUTO):** `stays_get_reservations(from=hoy, to=hoy+7, date_type="arrival", listing_id)` -> noches reservadas. `pricelabs_get_listing(listing_id)` -> base/min actuales.
- **Umbral:** ocupacion 7d = 0 (alerta). Reforzar si el mercado 7d tiene ocupacion (ver 🟡UI Datos del Vecindario).
- **Accion:**
  - 🟢 GATED: acercar el precio al minimo viable -> `pricelabs_update_listings([{id, base_price, min_price}], confirmed=True)` + `pricelabs_push_prices(listing_id, "stays", confirmed=True)`.
  - 🟡 UI: activar/ajustar "descuento de ultimo minuto" (no hay API).
  - 🔴 Humano: si el precio ya es competitivo y no convierte -> alertar "revisar fotos/titulo".
- **Verificacion:** `pricelabs_get_listing(listing_id)` (nuevos base/min) + `pricelabs_fetch_prices` para ver precio por fecha.
- **NO hacer:** tocar precios en Stays (PriceLabs los sobrescribe); bajar bajo el minimo viable.

### R2 — Bajo el mercado / sin reservas a 30 dias
- **Disparador:** ocupacion propia a 30d por debajo del mercado.
- **Medir (AUTO):** `stays_get_reservations(from=hoy, to=hoy+30, ...)` -> ocupacion 30d. `pricelabs_get_listing` -> precios.
- **Umbral:** ocupacion 30d < mercado (🟡UI) o muy baja en absoluto.
- **Accion:**
  - 🟡 UI: crear/ajustar descuentos por duracion en la estadia que el mercado reserva (3-4 noches), no solo semanal.
  - 🟢 GATED: si el precio esta sobre el mercado, bajar base/min -> `pricelabs_update_listings(..., confirmed=True)` + push.
- **Ejecucion:** diagnostico AUTO; cambios GATED.
- **NO hacer:** descuentos en duraciones que el mercado no reserva.

### R3 — Cobrando barato a futuro (60 dias)
- **Disparador:** ocupacion propia a 60d MUY por encima del mercado (te reservan barato con mucha antelacion).
- **Medir (AUTO):** `stays_get_reservations(from=hoy, to=hoy+60, ...)` -> ocupacion 60d. Comparar con mercado (🟡UI Datos del Vecindario a 60d).
- **Umbral:** ocupacion propia 60d >> mercado 60d (ej. 42% vs 17% en el caso real).
- **Accion:**
  - 🟢 GATED: SUBIR base (y min si aplica) para fechas lejanas -> `pricelabs_update_listings([{id, base_price}], confirmed=True)` + push.
  - 🟡 UI: configurar "ajuste por ocupacion" para subir precio cuando la ocupacion futura es alta.
- **Verificacion:** `pricelabs_get_listing` (nuevo base) + `last_date_pushed`.
- **NO hacer:** subir sin validar; recordar que en temporada alta se protege precio (R6).

### R4 — Noches huerfanas (1-2 noches entre reservas)
- **Disparador:** hueco de 1-2 noches entre dos reservas.
- **Medir (AUTO):** `stays_get_reservations(from, to, ...)` -> detectar huecos en el calendario por unidad.
- **Accion:**
  - 🟡 UI: configurar "descuento para periodos huerfanos" (semana ~20% / finde ~10%) en PriceLabs.
  - 🟢 GATED (proxy via API): para esas fechas no hay override por API; alternativa = bajar min temporalmente (con cuidado, afecta todo el rango). Preferir 🟡UI.
- **NO hacer:** bloquear la noche si se puede resolver con precio.

### R5 — Subir precio por escalones (alta ocupacion / buena conversion)
- **Disparador:** ocupacion alta y reservas frecuentes a precio actual.
- **Medir (AUTO):** ocupacion 7/30d alta via `stays_get_reservations`; precio actual via `pricelabs_get_listing`.
- **Accion:** 🟢 GATED: subir base un escalon pequeno -> `pricelabs_update_listings([{id, base_price}], confirmed=True)` + push. Esperar y medir; si baja la conversion, volver al escalon anterior.
- **NO hacer:** subir de golpe; perseguir 100% ocupacion destruyendo margen.

### R6 — Temporada alta (proteger precio)
- **Disparador:** periodo de alta demanda (ej. mediados de octubre, eventos).
- **Medir (AUTO):** fechas-objetivo; ocupacion del sector (🟡UI). `pricelabs_get_listing` precios.
- **Accion:** 🟢 GATED: subir base/max de las fechas alta demanda -> `pricelabs_update_listings([{id, base_price, max_price}], confirmed=True)` + push. Ser el ultimo en reservarse; bajar hacia el mercado solo si no se vende al acercarse la fecha.
- 🟡 UI: perfil de temporada para esas fechas.
- **NO hacer:** regalar fechas de alta demanda con mucha anticipacion.

### R7 — Temporada baja (capturar temprano)
- **Disparador:** se acerca un mes de baja demanda.
- **Accion:**
  - 🟡 UI: programar descuentos ANTES de entrar al mes; perfil de temporada con min/base mas bajos.
  - 🟢 GATED: bajar base/min del periodo bajo -> `pricelabs_update_listings(..., confirmed=True)` + push.
- **NO hacer:** esperar a estar vacio para reaccionar.

### R8 — Evento / pico de demanda
- **Disparador:** evento que dispara demanda (concierto, feria, festivo).
- **Medir (AUTO):** fecha del evento; ocupacion del sector (🟡UI Datos del Vecindario, franjas magenta).
- **Accion:** 🟢 GATED: subir base/max de esas fechas + push. 🟡 UI: si PriceLabs no detecto el evento, reportarlo manualmente en el panel; poner min-stay si la ocupacion es extrema.
- **NO hacer:** dejar que una reserva de 1 noche dane un fin de semana de alta demanda (min-stay = 🟡UI).

### R9 — Validacion de base/min/max y refresco
- **Disparador:** revision periodica o tras cambios.
- **Medir (AUTO):** `pricelabs_get_listing(listing_id)` -> base/min/max por unidad.
- **Reglas de coherencia:**
  - Minimo ~35-40% por debajo del base.
  - Maximo ~2 a 3x el base.
  - Minimo nunca bajo el costo operativo real.
- **Accion:** 🟢 GATED: corregir valores fuera de rango -> `pricelabs_update_listings(..., confirmed=True)` + push.
- **Nota:** refrescar precios a diario mejora el ranking en Airbnb; PriceLabs ya lo hace automatico (~medianoche) si la sincronizacion esta activa.

### R10 — Impresiones altas pero pocos clics/reservas (conversion)
- **Disparador:** el anuncio aparece pero no convierte (dato de Airbnb: impresiones ok, conversion de clic baja).
- **Medir:** 🔴 Humano/UI (Airbnb stats; no hay API). Cruzar con precio competitivo via `pricelabs_get_listing`.
- **Accion:** 🔴 Humano: ALERTA "el cuello de botella es fotos/titulo, no precio". Acciones: rehacer fotos (horizontales, tecnica), titulo con ubicacion (<=50 car). Ver `documentacion/insights_airbnb_2026-06-22.md`.
- **NO hacer:** bajar precio si el precio ya es competitivo (no es el problema).

### R11 — Anuncio nuevo
- **Disparador:** publicar o republicar una unidad.
- **Accion:** 🔴 Humano: usar `08_playbooks/checklist_pre_publicacion.md` (fotos, titulo, descripcion, reglas, precio listos antes de publicar). Al publicar, dejar SOLO la promo "3 primeras reservas -20%" (boost Airbnb). 🟢 API: setear base/min/max iniciales via `pricelabs_update_listings`.
- **NO hacer:** publicar incompleto (contamina la data inicial).

### R12 — Calificacion baja
- **Disparador:** unidad con calificacion <= 4.6.
- **Medir:** 🔴 Humano (Airbnb; no hay API).
- **Accion:** 🔴 Humano: 4.6 o menos -> evaluar eliminar y recrear el anuncio. 4.7 -> recuperar bajando precio temporal (🟢 GATED via PriceLabs) para generar reservas + resenas frecuentes hacia 4.85.
- **NO hacer:** subir precio mientras la calificacion esta castigada.

### R13 — Huesped problematico / riesgo de mala resena
- **Disparador:** huesped exigente o conflicto durante la estadia.
- **Medir:** 🔴 Humano (mensajes; ver `stays_get_reservations` para datos de la reserva).
- **Accion:** 🔴 Humano: proteger la resena dando beneficios (sabanas/aseo) aunque cueste; llamar a soporte Airbnb en modo informativo para dejar precedente; mantener todo en el chat de la plataforma como evidencia.
- **NO hacer:** discutir en caliente.

### R14 — Post-reserva larga / calendario debil
- **Disparador:** termina una reserva larga y quedan noches proximas vacias.
- **Medir (AUTO):** `stays_get_reservations` -> detectar el hueco tras la reserva larga.
- **Accion:** 🟢 GATED: bajar base/min de las noches proximas para reactivar -> `pricelabs_update_listings(..., confirmed=True)` + push; volver gradual al precio normal cuando entren reservas. 🟡 UI: descuento de ultimo minuto.
- **NO hacer:** dejar calendario vacio prolongado.

---

## Flujo recomendado al disparar una regla
1. **Diagnostico (AUTO):** correr las lecturas (Stays + PriceLabs) y reportar el estado por unidad.
2. **Propuesta:** si toca precio, elaborar propuesta con valores y justificacion (no aplicar todavia).
3. **Aprobacion:** esperar OK explicito del usuario.
4. **Ejecucion (GATED):** `pricelabs_update_listings(..., confirmed=True)` + `pricelabs_push_prices(..., confirmed=True)`.
5. **Verificacion:** `pricelabs_get_listing` (valores) + `last_date_pushed` / `push_enabled`.
6. **Registro:** documentar en `memory-bank/activeContext.md` y `memory-bank/progress.md`.

## Referencias
- Know-how completo: `documentacion/playbook_renta_corta.md`.
- Caso real: `documentacion/insights_airbnb_2026-06-22.md`.
- Protocolo de cambios de precio (obligatorio): seccion "PROTOCOLO DE CAMBIOS DE PRECIOS" en `AGENTS.md`.
- APIs: `documentacion/Pricelabs_API.md`, `documentacion/APIStaysDoc.md`.
