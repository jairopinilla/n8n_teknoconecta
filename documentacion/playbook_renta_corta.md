# Playbook de Renta Corta — SandiegoApart

> Documento consolidado y fuente unica para agentes de IA. Reune en un solo lugar Pack Maestro, eBooks y transcripciones de asesorias pagadas 1-on-1. No existen archivos legacy paralelos.
>
> Fuentes originales:
> - Pack Maestro Airbnb (Bonos 1-6), EBook Airbnb Host Summit 2025, Asesoria_Renta_Corta.pdf → `documentacion/Asesorias/`
> - Transcripciones de asesorias pagadas → `G:\Mi unidad\asesoria pagada\Transcripcion`
> - Asesorias 1-on-1 procesadas → `documentacion/` (ej: insights_airbnb_2026-06-22.md)
>
> Version: 2026-06-22

---

## Como debe usar este documento un LLM

Cuando el usuario pregunte por un problema de renta corta, **no responder con una sugerencia aislada**. Responder con diagnostico, causa probable, prioridad y acciones.

Formato recomendado para respuestas:

1. Diagnostico probable.
2. Que datos revisar.
3. Acciones inmediatas.
4. Acciones de seguimiento.
5. Que NO hacer.
6. Senal de que la estrategia funciono.

El criterio general es: primero entender el contexto, luego tocar la variable correcta.

> Para reglas ejecutables con las APIs de PriceLabs y Stays (diagnosticos automaticos, cambios de precio con aprobacion, alertas UI/humano), ver `06_automatizacion/reglas_accionables_renta_corta.md`.

---

## Reglas de comportamiento del agente

Cuando un agente (bot, asistente, automatizacion) actua como asesor operativo o atiende huespedes:

**Tono:** claro, profesional, directo, humano, sin exagerar, sin prometer lo no confirmado.

**Prohibiciones:** no inventar amenities, disponibilidad, distancias ni politicas; no recomendar cancelar reservas sin advertir consecuencias; no prometer reembolsos sin validacion humana; no entregar claves, codigos de acceso o datos sensibles sin verificacion de reserva; no ocultar reglas importantes para lograr una reserva.

**Ante la duda, usar una de estas formulas:**

```
No tengo ese dato confirmado. Puedo ayudarte con la informacion disponible y dejar este punto como pendiente de validacion.
```

```
Para evitar entregarte informacion incorrecta, este dato debe validarse con administracion antes de confirmarlo.
```

---

## Tesis central

La renta corta no se administra como un precio fijo publicado en internet. Se administra como un negocio vivo, donde cada fecha, temporada, plataforma, huesped y propiedad puede necesitar una estrategia distinta.

La rentabilidad aparece cuando se alinean: mercado, precio, visibilidad, fotos, configuracion, resenas, experiencia del huesped, plataforma y seguimiento constante.

El error comun es tratar de resolver todo bajando precio. La metodologia ensena que bajar precio puede ser correcto, pero solo si se hace en el momento, duracion y contexto adecuados.

---

## Glosario operativo

### ADR
Precio promedio diario que se intenta cobrar. No necesariamente es lo que finalmente entra de dinero. Es una intencion de precio. Ejemplo: si un alojamiento tiene todos los dias del mes a 300.000, su ADR es 300.000, aunque no haya vendido todas las noches.

### RevPAR (Reppar, Redpar, Refpar)
Rentabilidad diaria distribuida sobre todos los dias del periodo, ocupados o no. Formula practica: **Ingresos del mes / dias del mes = RevPAR aproximado**. Usar para comparar contra costo fijo diario. Si RevPAR > costo fijo, hay utilidad. Si RevPAR < costo fijo, hay perdida aunque algunas noches se hayan vendido bien.

### Ocupacion
Porcentaje de noches ocupadas. Es importante, pero no basta. Una propiedad puede tener alta ocupacion y baja rentabilidad si vendio demasiado barato.

### Ventana de reserva
Anticipacion promedio con la que los huespedes reservan. Si la ventana es 7 dias, la mayor parte de reservas llega dentro de los proximos 7 dias. Si no tienes reservas en ese rango, estas en zona de alerta.

### Duracion de estadia
Cantidad promedio de noches por reserva. Sirve para definir descuentos por 2, 3, 4, 7 o mas noches. Si el mercado convierte principalmente entre 3 y 4 noches, los descuentos importantes deberian disenarse alrededor de 3 y 4 noches.

### Dias o noches huerfanas
Noches sueltas entre dos reservas. Suelen tener menor probabilidad de venderse porque limitan la combinacion de fechas disponibles para el huesped. Conviene tratarlas con una tarifa o descuento especifico.

### Temporada alta
Periodo con alta demanda. La estrategia recomendada es proteger el precio y ser de los ultimos en reservar, siempre que el mercado lo soporte.

### Temporada baja
Periodo con menos demanda. La estrategia recomendada es captar reservas antes que la competencia, incluso sacrificando algo de ADR para asegurar ocupacion.

### Evento unicornio
Evento que dispara demanda de forma excepcional, incluso en temporada baja. Puede permitir cobrar multiplos del precio normal si se detecta a tiempo.

### OTA
Plataforma de venta como Airbnb, Booking o similares.

### PMS
Sistema centralizado para administrar calendarios, precios, disponibilidad y reservas en varias plataformas.

### PriceLabs
Herramienta de pricing dinamico. Ayuda, pero no reemplaza el criterio humano. Puede no captar calidad del anuncio, malas resenas, mejoras fisicas, eventos extremos o problemas especificos de posicionamiento.

---

## Principios base

### 1. El mercado manda, no el evento
No basta con subir precios porque existe un concierto, feria, feriado o evento. La decision debe basarse en senales reales del mercado: competidores comparables ya reservados, disminucion de disponibilidad en el sector, aumento de ocupacion futura, cambios en precios promedio, comportamiento historico de la zona, picos detectados por PriceLabs.

**Regla:** Nunca recomendar subir precios solo porque existe un evento. Primero revisar demanda, ocupacion, disponibilidad y competencia.

### 2. La visibilidad es el motor del negocio
Mas reservas no dependen solamente de tener mejor propiedad. Dependen de que la plataforma muestre el anuncio, de que el huesped haga clic y de que luego convierta. La visibilidad se ve afectada por: disponibilidad, precio, calidad del anuncio, resenas, conversion, flexibilidad, calendario y rentabilidad que el anuncio le genera a la plataforma.

### 3. Las plataformas muestran lo que les genera dinero
Airbnb, Booking y similares tienen incentivos claros: mostrar alojamientos que convierten, dejan comision y generan buena experiencia. Si el anuncio no convierte, puede empezar a mostrarse menos → recibe menos interacciones → convierte menos → la plataforma lo muestra menos. Ese ciclo puede hundir un anuncio si no se interviene.

### 4. El precio correcto depende del momento correcto
Una oferta agresiva puede funcionar si se lanza en la ventana correcta. La misma oferta puede fracasar si se aplica demasiado tarde. Si tu alojamiento normalmente convierte 15 o 20 dias antes de la llegada, bajar precio el dia anterior puede no rescatar la ocupacion. El descuento llego tarde.

### 4b. La conversion depende de cuatro pilares
1. **Ocupacion:** entender como se comporta el mercado.
2. **Precio:** definir tarifa segun valor real del alojamiento y competencia.
3. **Visibilidad:** reducir restricciones y crear ofertas atractivas.
4. **Conversion:** mejorar fotos, titulo, descripcion, reglas y experiencia.

Si un alojamiento no reserva, diagnosticar cual de estos cuatro pilares esta fallando.

### 5. Coherencia entre expectativa y realidad
La experiencia debe coincidir con lo prometido. No editar fotos de forma exagerada, no prometer lujo si el espacio es funcional, no ocultar restricciones importantes, no exagerar distancias, no usar textos genericos que no describan el alojamiento real.

### 6. No tocar todo al mismo tiempo sin medir
Cambiar titulo, fotos, precio, politicas y descuentos el mismo dia puede mover el anuncio, pero luego no se sabe que funciono. La metodologia recomienda: diagnosticar → ajustar → esperar una ventana razonable → medir → volver a calibrar.

### 7. Las herramientas automaticas ayudan, pero no piensan por ti
PriceLabs puede leer demanda, ocupacion, reservas y comportamiento de mercado. Pero puede no saber que: recibiste una mala resena, cambiaste las fotos, compraste mejor lenceria, remodelaste la cocina, la propiedad se ve peor que la competencia, aparecio un evento que puede desbordar la ciudad, tu anuncio esta perdiendo traccion por calidad o posicionamiento.

---

## Marco general de diagnostico

Antes de sugerir cualquier accion, revisar en orden:

1. ¿La propiedad tiene disponibilidad real?
2. ¿Esta visible en la plataforma?
3. ¿Esta recibiendo visitas?
4. ¿Esta recibiendo clics?
5. ¿Esta convirtiendo?
6. ¿Esta alineada en precio con la competencia directa?
7. ¿Tiene fotos competitivas?
8. ¿Tiene buenas resenas recientes?
9. ¿Esta demasiado restrictiva?
10. ¿El mercado esta en temporada alta, baja o evento?
11. ¿La ventana de reserva permite esperar o exige accion inmediata?
12. ¿El problema es de Airbnb, Booking, PriceLabs, PMS o configuracion propia?

---

## Revenue management

Revenue management es la gestion estrategica de precios, disponibilidad y restricciones para maximizar ingresos.

### Variables que se deben revisar
- Ocupacion futura e historica
- ADR: tarifa diaria promedio
- RevPAR: ingreso por noche disponible
- Competencia directa
- Temporada alta, media o baja
- Anticipacion de reserva (ventana)
- Huecos entre reservas y noches huerfanas
- Cantidad de resenas y calidad del anuncio
- Restricciones activas (minimo de noches, cancelacion, etc.)
- Costos fijos, fee de limpieza, comisiones de plataforma

---

## Estrategia de precios por temporada

### Temporada alta
**Objetivo:** ser de los ultimos en reservarse.

- Proteger fechas con precios mas altos
- No bajar demasiado temprano
- Ajustar progresivamente al acercarse la fecha
- Observar si la competencia se reserva antes
- Reducir precio solo si la ocupacion esperada no se materializa
- Si la ocupacion del mercado supera 80%, 90% o 95%, se puede cobrar muy por encima del promedio
- No todas las noches de temporada alta valen igual. La tarifa debe comportarse como montana, no como linea plana
- Si el pico es viernes y sabado, esos dias llevan el precio mas alto; jueves y domingo precio alto pero menor

**Regla:** En temporada alta no se debe competir por precio desde el inicio. Primero se protege margen; luego se ajusta segun ocupacion y cercania de la fecha.

### Temporada baja
**Objetivo:** ser de los primeros en reservarse.

- Activar precios competitivos con anticipacion
- Programar descuentos ANTES de entrar en temporada baja
- No esperar a estar vacio para reaccionar
- Captar reservas con antelacion aunque sea una o dos
- Usar descuentos por duracion de estadia donde realmente convierte el mercado
- Reducir restricciones
- Aumentar atractivo visual del anuncio
- Monitorear conversion semanalmente

**Regla:** En temporada baja, la prioridad es asegurar ocupacion temprana. Un calendario vacio cerca de la fecha requiere accion agresiva.

### Entre semana
Ser mas agresivo en precio, usar descuentos de ultima hora, incentivar reservas de trabajo, destacar escritorio, Wi-Fi y ubicacion.

### Fines de semana
Ser menos agresivo, proteger tarifa, evaluar minimos de estadia solo si no perjudican visibilidad, usar narrativa de escapada o descanso.

---

## Casos de uso

### Caso 1: No tengo reservas en los proximos 7 dias

**Lectura:** Si la ventana de reserva de tu mercado es de 7 dias y no tienes reservas, estas en alerta. La alerta es mas fuerte si: el mercado si tiene ocupacion para los proximos 7 dias, tu estas por debajo, tu precio esta por encima, tienes restricciones de minimo de noches o noches huerfanas, el anuncio es nuevo o tiene pocas resenas.

**Datos a revisar:** ocupacion propia 7 dias, ocupacion del mercado 7 dias, precio propio contra competencia directa, precio minimo configurado, si PriceLabs esta sincronizando, descuentos de ultimo minuto activos, noches huerfanas, minimo de estadia, foto principal y primeras cinco fotos.

**Accion recomendada:**
1. Aplicar descuento de ultimo minuto (10% a 15% dentro de 7 dias)
2. Comparar precio final con competencia directa
3. Si estas arriba del mercado, bajar precio de inmediato
4. Si estas igual o abajo y no conviertes, revisar fotos, titulo, restricciones y resenas
5. Revisar que el precio minimo no este bloqueando a PriceLabs
6. Si hay noches huerfanas, aplicar tarifa especial
7. Sincronizar cambios y verificar que se actualizan

**Que NO hacer:** bajar precio sin revisar mercado, asumir que el problema es solo PriceLabs, esperar pasivamente si el dashboard marca rojo, mantener minimo de dos noches si el mercado reserva una noche.

**Senal de mejora:** aparecen consultas o reservas dentro de la ventana, la ocupacion se acerca al mercado, el anuncio recibe mas clics.

### Caso 2: No tengo reservas en los proximos 30 dias

**Lectura:** 30 dias sin reservas no siempre significa crisis, pero si exige comparar contra el mercado. Si el mercado tambien esta lento, puede ser temporada baja. Si el mercado esta ocupandose y tu no, el problema es de oferta, precio, visibilidad, calidad o configuracion.

**Accion:** si tu ocupacion esta por debajo del mercado, generar oferta mas competitiva. Si la duracion promedio del mercado es 3 o 4 noches, crear descuentos en 3 y 4 noches. Si solo tienes descuentos semanales, puedes estar perdiendo el punto dulce. Si la propiedad tiene mala traccion, hacer oferta de choque durante 20 a 30 dias.

**Ejemplo:** La competencia convierte a 110 USD. Tu alojamiento esta a 150 y no vende. Si tu costo fijo es 60-70, no tiene sentido insistir en 150. Estrategia: mantener precio visible en 130 si quieres preservar percepcion, crear descuento para 3 o 4 noches que deje el precio efectivo en 105-110. Si aun no convierte, bajar efectivo a 95-100. Conseguir primeras reservas y resenas, luego subir por escalones.

### Caso 3: Mi anuncio esta en rojo contra el mercado

Si el dashboard muestra que el mercado esta mas ocupado que tu en 7, 30 o 60 dias, tu anuncio esta perdiendo contra la referencia.

**Como interpretar:**
- **7 dias:** problema urgente. Exige accion rapida.
- **30 dias:** problema de calendario proximo. Permite estrategia, pero no mucha espera.
- **60 dias:** oportunidad de prevenir. Si estas muy por debajo, ajusta antes de entrar en urgencia.

**Accion:** revisar precio contra mercado, verificar si PriceLabs esta bajando hasta el minimo, si el minimo es demasiado alto ajustarlo, aplicar descuento temporal, revisar restricciones, si el precio ya esta bien revisar conversion visual y titulo.

### Caso 4: Tengo muchas noches ocupadas pero aun me quedan huecos

Cuando una propiedad ya tiene reservas, las noches disponibles restantes pueden perder visibilidad. Las plataformas prefieren mostrar alojamientos con mas disponibilidad.

**Accion:** identificar noches huerfanas, crear precio o descuento especifico para esas noches, ser mas agresivo entre semana, proteger fin de semana si aun tiene demanda.

### Caso 5: Anuncio nuevo sin reservas

**Regla principal:** No abrir un anuncio si no esta listo. Debe estar listo en: fotos, diseno, limpieza, lenceria, descripcion, amenidades, reglas, precio, calendario, descuentos, disponibilidad.

El objetivo inicial no es maximizar rentabilidad. Es conseguir reservas, buenas resenas y datos positivos para la plataforma. Salir con una oferta mas atractiva que la competencia, ser flexible al inicio, no pretender cobrar como un anuncio con 50 resenas si no tienes prueba social. Una vez ganada traccion, subir precio gradualmente.

### Caso 6: Anuncio que antes funcionaba y dejo de vender

**Causas probables:** perdida de posicionamiento, malas resenas recientes, calendario bloqueado, exceso de restricciones, precio desfasado, fotos menos atractivas que la competencia, competencia nueva mas fuerte, sobreoferta en la zona, mala configuracion de descuentos, el anuncio acumulo mala data.

**Diagnostico:** revisar si el anuncio se muestra, si recibe visitas, si recibe clics, si convierte, precio contra competencia, resenas recientes, bloqueos, fotos y titulo.

**Acciones:** normalizar oferta y precio, mejorar fotos, ajustar titulo, crear descuentos segun duracion real del mercado, hacer la propiedad mas flexible, dar 10 a 15 dias para observar. Si el anuncio lleva muchos meses con metricas intoxicadas, puede ser mejor crear un anuncio nuevo.

### Caso 7: Temporada baja

En temporada baja debes intentar ser de los primeros en reservar. Hay menos demanda y mas alojamientos compitiendo por menos huespedes. Programar descuentos antes de entrar en temporada baja. Si la temporada baja es octubre, no esperar a octubre para bajar. El descuento debe estar configurado antes.

### Caso 8: Temporada alta

En temporada alta conviene proteger el precio y buscar ser de los ultimos en reservar, siempre que el mercado tenga alta demanda real. No regalar fechas de alta demanda con demasiada anticipacion. Inflar o proteger precio al inicio. A medida que se acerca la fecha, bajar progresivamente hacia el mercado si no se vende.

### Caso 9: Evento unicornio

Evento de demanda extraordinaria que puede desbordar una ciudad. Puede permitir multiplicar el precio normal si la ciudad se queda sin disponibilidad.

**Como detectarlo:** revisar ocupacion futura del mercado, picos anormales en dashboard, comparar con anos anteriores, observar si competidores empiezan a llenarse antes, revisar noticias y agenda cultural, verificar si la ocupacion supera 90%.

**Estrategia:** proteger fechas, no bloquear si puedes vender caro (mejor poner precio alto que bloquear), si alguien reserva a precio altisimo aceptar, poner minimos de estadia si la ocupacion es extrema, no dejar que una reserva de una noche dane un fin de semana de alta demanda.

**Criterio de montana:** si el pico es viernes y sabado → viernes y sabado precio mas alto, jueves y domingo alto pero menor, dias alrededor suben para incentivar estadias mas largas.

### Caso 10: Precio alto y reservas de ultima hora

Si las reservas llegan muy encima, puede significar que el ADR estaba demasiado alto y solo convertiste cuando ajustaste o cuando quedaba poca disponibilidad. Crear registro historico, identificar el precio donde si conviertes, no esperar al ultimo dia para ajustar si el mercado convierte antes.

### Caso 11: Tengo visitas pero no reservas

Si el anuncio se ve pero no convierte, el problema suele estar en: precio final, fotos, primeras cinco imagenes, titulo, descripcion, resenas, reglas, tarifa de limpieza, costo por persona adicional o falta de diferenciacion. Revisar precio total que paga el huesped (no solo precio base), comparar con competencia directa.

### Caso 12: Tengo reservas pero poca rentabilidad

Puede haber ocupacion, pero la tarifa estar demasiado baja. Hay que mirar RevPAR y costo fijo. Si hay ocupacion alta y RevPAR bajo, subir precio gradualmente. Revisar si descuentos se estan acumulando. No perseguir 100% ocupacion si destruye margen.

### Caso 13: Quiero subir precio sin matar la conversion

**Estrategia de escalones:**
1. Encontrar precio en el que el anuncio si convierte
2. Conseguir varias reservas
3. Mantener excelente servicio
4. Subir un escalon pequeno (ej: de 90 a 95)
5. Esperar mas reservas
6. Si no convierte, volver al escalon anterior
7. Reintentar con punto intermedio

El precio se calibra con el mercado, no con orgullo.

---

## Pricing y estrategia de calendario

Cada fecha tiene un valor diferente. No es lo mismo: lunes que sabado, temporada baja que alta, fecha sin evento que con evento, noche huerfana que noche abierta, 7 dias antes que 60 dias antes.

### Que debe tener una estrategia de calendario
- Precio base (valor normal en condiciones promedio)
- Precio minimo (debe cubrir costos operativos, limpieza, comisiones, desgaste, margen minimo)
- Rango de temporada alta y baja
- Descuentos por duracion de estadia
- Reglas para noches huerfanas
- Ajustes de ultimo minuto
- Ajustes por ocupacion
- Reglas para eventos

### Regla de oro
Siempre mirar el precio final que ve el huesped y el neto que recibes tu. Las promociones acumuladas pueden convertir una reserva en perdida.

---

## Descuentos por duracion de estadia

Ayudan a mejorar visibilidad, incentivar reservas mas largas, llenar huecos y competir sin bajar el precio base visible.

**Como definirlos:** no definir por costumbre, sino segun duracion promedio de estadia del mercado. Si el mercado reserva 3 y 4 noches, crear descuentos para 3 y 4 noches. Si solo haces descuento semanal, puedes estar perdiendo el grueso de la demanda.

**Ejemplo de rule set:**

| Duracion | Descuento sugerido |
|---|---:|
| 1 noche | 0% |
| 2 noches | 20% |
| 3 noches | 25% |
| 4+ noches | 30% |

**Regla:** No bloquear una noche si se puede resolver con precio. La restriccion reduce visibilidad; el precio controla rentabilidad.

---

## Flexibilidad y restricciones

### Restricciones que bajan visibilidad
- Minimo de noches alto
- No aceptar reserva inmediata
- Calendario abierto pocos meses
- Cobro alto por persona adicional
- Tarifa de limpieza demasiado alta
- Politica de cancelacion poco competitiva
- No aceptar reservas de ultimo minuto
- Bloqueos frecuentes por otras plataformas

### Como ser mas flexible sin perder control
Permitir una noche pero hacerla cara. Luego aplicar descuento desde dos noches para quedar al nivel de mercado.

**Ejemplo:** mercado a 800 CLP por noche. Quieres evitar una sola noche pero no restringir Airbnb. Estrategia: precio visible 2.000, minimo 1 noche, descuento desde 2 noches 60%, precio efectivo desde 2 noches = 800.

**Regla:** Mientras mas restricciones, menor visibilidad. Mientras mas estricta la politica de cancelacion, menor atractivo. Usar flexibilidad cuando se necesita visibilidad.

---

## PriceLabs

PriceLabs es un Revenue Management System (RMS), distinto y complementario a un PMS. Se conecta directo a Airbnb/VRBO o via PMS. Productos: Dynamic Pricing (precios + reglas de estadia minima), Portfolio Analytics (KPIs propios), Market Dashboard (KPIs de un mercado por direccion+radio, util para decidir inversion), Revenue Estimator Pro (proyeccion futura de ingresos, ocupacion y ADR por direccion). Costo desde ~USD 9.99/mes la 1a unidad, baja con mas unidades. Impacto tipico: +10% a +40% de ingresos.

Revenue management = moneda de dos caras: (1) precios dinamicos que fluctuan con el mercado y (2) reglas de estadia minima. Ambas se gestionan juntas.

> Esta seccion es el know-how accionable (fuente unica). Para referencia tecnica oficial detallada, ver `documentacion/pricelabs-academy/` (scraping de 365 articulos de la base de conocimiento de PriceLabs).

### Precio base
Es el promedio por noche a lo largo de todo el ano (ej. 6 meses a 80 + 6 meses a 120 = base 100). Es el punto de partida del algoritmo; se define manual por propiedad antes de encender la sincronizacion. No es el precio minimo. No recomendar un base sin revisar: tipo, calidad, ubicacion, capacidad, amenities, franja de competidores, ocupacion, resenas, estacionalidad.

**Sugerencia de base por mercado (3 criterios):** (1) area geografica (dibujar perimetro), (2) categoria/percentil de precio, (3) categoria de habitaciones (comparar manzanas con manzanas: 2 dorm con 2 dorm).

**Percentiles de precio del mercado:** economico = 25-50, medio = 50-75, alto = 75-90. Son las franjas (gris / rosada) del grafico de Datos del Vecindario; ubican tu precio frente al mercado.

### Precio minimo
Red de seguridad: ninguna noche por debajo de ese valor. Debe cubrir costos operativos, limpieza, comisiones, desgaste y margen minimo. Criterio: el precio bajo el cual prefieres dejar vacio antes que perder dinero. **Regla practica:** ubicarlo 35-40% por debajo del base (mas margen base-minimo = mejor optimizacion en baja demanda). El precio atrae el segmento: bajar demasiado atrae huespedes no deseados. Nunca bajar del costo operativo real salvo estrategia puntual y justificada.

### Precio maximo
Controla expectativas del huesped. **Regla practica:** 2 a 3 veces el base (ej. base x2.5). Cobrar de mas tiene 3 efectos negativos: (1) el huesped no cuida la propiedad, (2) mayor carga operacional (mas exigente), (3) peor calificacion. Debe ser realista, no fantasioso.

### Reglas de estadia minima (cascada)
La "otra cara de la moneda". El motor recomienda segun "cortas" o "medianas" estadias y arma una cascada por antelacion, por ejemplo:
- Ultima hora (0-2 dias): 1 noche (flexibiliza).
- 2-6 noches de antelacion: 2 noches.
- 6-29 noches: 4 noches.
- 29+ noches: regla general (ej. 7 noches).
- 90+ noches (fechas lejanas): mayor a 7 noches.
Mas tratamiento especifico de noches huerfanas (mas estricto o mas flexible).

### Descuentos
- **Ultimo minuto (gradual):** ej. 35% si reservan para hoy, decreciendo dia a dia hasta 0% al dia 17.
- **Periodos huerfanos (1-2 noches):** diferenciar entre semana (ej. 20%) vs fin de semana (ej. 10%); puede ser descuento o incremento.

### Ajustes por ocupacion y perfiles de temporada
- **Ajustes por ocupacion:** sube/baja el precio segun la ocupacion para distintas ventanas de reserva (una de las funciones mas utiles). Mas agresivo en la ventana corta (tu ventana de conversion).
- **Perfiles de temporada:** definir base/minimo y reglas de estadia minima distintos por rango de fechas (ej. ene-jun minimo 75 en baja; jul-dic minimo 100 en alta).
- **Ajuste manual por fechas:** override por valor fijo o % sobre el recomendado + min-stay propio (ej. evento/grupo => +25%, min 6 noches). Aparece como banda negra en el calendario.

### Datos del vecindario y eventos
Herramienta clave: grafico de tu precio (linea negra) vs percentiles del mercado a futuro; franjas magenta = eventos/festivos que suben demanda (detectados por integraciones + ML). Resumen de mercado por mes: ocupacion, ventana de reserva, LOS promedio, ADR. Si PriceLabs no detecta un evento (ej. concierto), reportarlo manualmente.

### Sincronizacion y ranking
El sistema empuja precios cada 24h (~medianoche); se puede forzar manual. Refrescar precios con frecuencia mejora el ranking: Airbnb te detecta como anfitrion activo (es su "SEO interno") y te posiciona mas arriba.

### Smart Pricing de Airbnb: NO usar (velocidad vs calidad)
El precio inteligente de Airbnb NO es realmente inteligente. Airbnb (OTA) busca VELOCIDAD: vender rapido y barato (negocio de volumen, compite con Booking/Expedia), por eso tiende a bajar el precio. PriceLabs busca CALIDAD: vender al mejor precio para maximizar ingreso. Recomendacion: desactivar Smart Pricing de Airbnb y usar pricing dinamico (PriceLabs).

### Conectado vs sincronizando
Conectar PriceLabs no es lo mismo que enviar precios. Revisar: si esta conectado, si esta activo, si esta sincronizando, si Airbnb/Booking recibe precios, si el precio minimo y maximo estan bien, si los ajustes inteligentes estan activos.

---

## Market Dashboard y estudio de mercado

La recomendacion es estudiar el mercado por lo menos durante un ano para empaparse de temporadas, picos, valles, competencia, precios, duracion de estadia, ocupacion, eventos y comportamiento de reserva.

### Elegir competencia directa
Competencia directa es la que te puede quitar reservas y a la que tu le puedes quitar reservas. No comparar con propiedades demasiado superiores, sin resenas, con mala calificacion, hoteles si tu producto no compite con ellos, casas grandes si tienes apartaestudio.

**Regla:** Un radio grande puede contaminar el analisis. Mejor comparar pocos alojamientos realmente similares que muchos no comparables.

### Sobreoferta
Si los listados activos crecen mas rapido que las reservas, hay saturacion. Hay mas competencia por una demanda que no crece al mismo ritmo.

---

## Fotos, titulo y descripcion

### Fotos
Las fotos son una herramienta de venta, no solo evidencia del espacio. Son la primera experiencia comercial del huesped.

**La primera foto:** debe atrapar. Si no genera interes, el huesped no abre el anuncio.

**Primeras cinco fotos:** deben resumir la propuesta de valor: mejor angulo, sala o espacio social, habitacion principal, vista/balcon/terraza, atributo diferencial. No repetir la misma sala tres veces.

**Primeras diez fotos:** completan la historia sin monotonia.

**Que NO mostrar:** ollas, cajones, escobas, recogedores, basureros, fotos oscuras, fotos verticales mal recortadas, fotos repetidas, espacios desordenados, elementos que no ayudan a vender.

**Checklist antes de fotografiar:** cama perfectamente tendida sin arrugas, almohadas alineadas, cortinas abiertas, luz natural, luces encendidas si aportan calidez, TV con imagen relajante, cables ocultos, superficies limpias, bano impecable, cocina ordenada, terraza despejada, sin objetos personales, sin exceso de decoracion, sin distorsion exagerada.

**Tecnica con celular:** camara horizontal, altura media (ombligo o arrodillado), lineas rectas, gran angular 0.5 con moderacion, enfocar manualmente, evitar filtros artificiales, limpiar el lente, editar exposicion en Lightroom.

**Fotos minimas recomendadas:** portada hero, cama, vista general, terraza/balcon, escritorio, cocina, bano, TV/zona descanso, amenity diferenciador, vista, fachada/acceso, detalles de experiencia (cafe, libro, copa).

### Titulo
Debe despertar curiosidad y comunicar atributos fuertes: cama king, vista, terraza, parking, aire acondicionado, Wi-Fi, ubicacion reconocible, barrio atractivo, cercania a zona de interes.

**Estructura sugerida:** `[Tipo de alojamiento] + [atributo fuerte] + [ubicacion]`
- "Estudio con terraza y cama king cerca del metro"
- "Studio work-friendly con Wi-Fi rapido y terraza"
- "Moderno estudio con king, A/C y excelente ubicacion"

### Descripcion
**Estructura recomendada:**
1. Primer parrafo emocional y concreto
2. Lo que encontrara el huesped
3. Datos del edificio
4. Ubicacion y entorno
5. Reglas importantes
6. Preguntas frecuentes
7. CTA de reserva

---

## Resenas y experiencia del huesped

Airbnb nacio como un negocio entre personas. Aunque ahora existan operadores grandes, el huesped sigue evaluando una experiencia humana. Buen servicio no siempre basta: hace falta generar conexion y percepcion de cuidado.

### Como aumentar resenas positivas
- Abrir conversacion real antes de la llegada
- Preguntar motivo del viaje (trabajo, salud, cumpleanos, turismo, evento, etc.)
- Dar recomendaciones especificas segun el motivo
- Personalizar mensajes cuando sea posible
- Resolver problemas rapido
- Automatizar mensajes que inviten a conversacion, no solo a dejar cinco estrellas

### Mensaje antes de llegada
Objetivo: entender por que viaja el huesped. Con esa informacion se pueden dar recomendaciones mas utiles.

### Mensaje despues de la estadia
Hacer una pregunta abierta antes de pedir resena: "Espero que hayas pasado muy bien. Cuentame como te fue en el alojamiento y si pudiste hacer lo que venias a hacer." Despues de recibir respuesta positiva, pedir resena.

### Cuando hay problemas
Si un problema puede convertirse en mala resena, conviene resolverlo aunque cueste dinero. Puede ser mejor regalar algo, cubrir transporte, compensar una noche o enviar mantenimiento rapido. Una mala resena puede costar mas que la compensacion.

### Como responder malas resenas
No responder en caliente, no atacar al huesped, mostrar que se escucho el problema, mostrar solucion, mantener tono profesional. Si la resena viola politicas (amenaza, discriminacion, retaliacion, mentira demostrable), intentar disputa con soporte. Mantener conversaciones problematicas dentro del chat de Airbnb para tener evidencia.

---

## Booking vs Airbnb

### Diferencia central
Airbnb gestiona pagos y parte de la confianza. Booking exige mas trabajo operativo porque muchas veces el anfitrion debe gestionar cobro, llegada, comunicacion, confirmacion y no-show.

### En Booking hay que cuidar
Comunicacion inmediata, cobro antes del ingreso, verificacion de pago, confirmacion de llegada, notificacion de no-show, facturas de comision, riesgos de estafa, reputacion del alojamiento, Google Maps, promociones y Genius.

### Google Maps
Crear el lugar en Google Maps ayuda a demostrar que el alojamiento existe, dar confianza, facilitar llegada y mostrar resenas externas.

### Genius y promociones
Genius puede dar exposicion, pero suma descuentos. Hay que controlar el precio final. Problema tipico: Genius + promocion + descuento adicional + tarifa no inflada = reserva con perdida.

**Solucion:** inflar tarifa base en Booking si se aplican descuentos, revisar precio final, alinear tarifa neta con otras plataformas.

### Flujo recomendado en Booking
1. Entra reserva
2. Se contacta al huesped
3. Se confirma identidad, intencion y llegada
4. Se gestiona pago
5. Se verifica pago dos o tres veces
6. Se envia informacion clara
7. Si llega, se presta servicio
8. Si no paga, no responde o no llega, se marca no-show
9. Se revisa la factura de Booking

**Regla:** No entregar acceso sin pago confirmado.

### Estafas comunes
En Booking y canales donde el huesped paga por fuera, verificar pagos con cuidado. Riesgos: enlaces falsos para "aceptar pago", comprobantes falsos, transferencias no confirmadas, huespedes que reservan y no pagan, presion de ultimo minuto. Regla: no entregar acceso sin pago confirmado y verificado dos o tres veces.

---

## PMS y herramientas externas

### Cuando pensar en PMS
Cuando se manejan varias plataformas o varias propiedades, un PMS ayuda a centralizar disponibilidad, precios, mensajes, cobros, bloqueos y evitar overbooking.

### Riesgos del PMS
Verificar si el PMS: sobrescribe precios, borra rule sets, modifica minimos de estadia, cambia disponibilidad, bloquea configuraciones nativas de Airbnb, limita promociones, permite API, permite sincronizacion correcta con PriceLabs.

**Regla:** Si el PMS borra reglas importantes de Airbnb, la estrategia debe moverse al PMS, a PriceLabs o evaluarse cambio de herramienta.

---

## Amenidades y diferenciacion

### Amenidades a estudiar
Aire acondicionado, piscina, jacuzzi, parking, Wi-Fi, entrada privada, estadias largas, cama king, vista, zonas comunes, lavadora, cocina equipada.

### Como decidir inversion
No invertir por gusto. Revisar si las propiedades con esa amenidad capturan mas reservas o mejor precio.

### Pequenas inversiones que pueden cambiar mucho
Mejores almohadas, lenceria, iluminacion calida, decoracion, cortinas, fotos profesionales, detalles de cocina, mejor puesta en escena.

---

## Costos, margen y precio base

### Costo fijo
Antes de decidir precio, saber cuanto cuesta tener el alojamiento abierto. Incluye: arriendo/dividendo, administracion, servicios, internet, limpieza, mantenimiento, comisiones, reposicion, impuestos, herramientas.

### Uso del costo fijo
El costo fijo no define el precio de mercado, pero define el piso de viabilidad. Si el mercado solo paga bajo tu costo fijo, hay que revisar si el negocio es viable.

### Fee de limpieza
Mantener separado del precio noche. No incluir limpieza dentro de la tarifa base si se usan descuentos. Evitar dar descuento indirecto sobre limpieza. Cobrar limpieza cercana al costo real.

**Regla:** El descuento debe afectar la noche, no necesariamente el costo de limpieza.

---

## Mensualidades y rentas largas

Para estadias de 28 noches o mas: aplicar descuentos significativos (30% a 50% segun mercado), considerar menor rotacion, menos costos de limpieza, huesped distinto (trabajador temporal, nomada digital, estudiante). Ajustar reglas de consumo, limpieza y mantenimiento.

Si solo quieres recibir rentas mensuales, configura minimo de estadia mensual para que Airbnb te muestre a esos huespedes y tus metricas sean mas coherentes.

---

## Casos ejemplo (abstraidos de asesorias reales)

### Caso A: anuncio en rojo proximos 7 dias
Dashboard muestra mercado mas ocupado que el anuncio. Precio base cercano al mercado pero no captura. Accion: activar ajuste de ultimo minuto 10-15%, revisar minimo de precio, ver noches huerfanas, revisar minimo de noches, sincronizar cambios.

### Caso B: cuatro unidades muertas en un mismo edificio
Competencia convierte a 32-37 USD, las unidades frias intentaban vender a 29 USD y no convertian. El problema no era solo precio. Accion: optimizar fotos y titulo, mantener precio visible pero usar descuentos por 4+ noches para llegar a precio efectivo competitivo, atender excelente para resenas, subir por escalones.

### Caso C: anuncio nuevo publicado incompleto
Abrir incompleto puede contaminar la data inicial. Airbnb mide interacciones desde publicacion. Si recibe vistas pero no convierte, la plataforma aprende que no es atractivo. No publicar hasta tener TODO listo.

### Caso D: propiedad nueva con estrategia de resenas y crecimiento
Antes de amoblar o fotografiar, mirar como se ve la competencia. Disenar para diferenciarse. Salir con oferta atractiva. Capturar resenas. Usar aprendizaje de una propiedad para mejorar las siguientes.

### Caso E: temporada baja con mes vacio
El descuento debio programarse antes. Si esperas a estar en desventaja, los ajustes deben ser mas agresivos. Identificar meses bajos con anticipacion, aplicar descuentos antes de que empiece el mes.

### Caso F: evento unicornio en ciudad saturada
Ocupacion 90-95%+. El mercado puede pagar mucho mas. Proteger precio, no bloquear fechas si se pueden vender caras, usar precio alto como bloqueo inteligente, minimo de estadia si el finde esta muy demandado.

### Caso G: Booking como canal de temporada baja
Booking puede ayudar a reducir dependencia de Airbnb. Exige proceso: comunicacion, cobro, confirmacion, control de no-show. No es prender y esperar.

### Caso H: huesped problematico o mala resena potencial
No evaluar solo el costo inmediato de compensar. Evaluar el costo de una mala resena sobre el posicionamiento futuro. Muchas veces es mas barato resolver con generosidad que defenderse con rabia.

---

## Playbook de respuesta para LLM

### Si el usuario dice: "No tengo reservas en los proximos 7 dias"

Primero revisa la ventana de reserva del mercado. Si tu mercado reserva con 7 dias de anticipacion y no tienes reservas en esa ventana, estas en alerta. Compara tu ocupacion contra el mercado en los proximos 7 dias. Si estas por debajo, baja precio o activa promocion de ultimo minuto de 10% a 15%, siempre respetando tu precio minimo viable. Revisa tambien minimo de noches, noches huerfanas, precio por encima de competencia, fotos debiles o titulo poco atractivo. Si PriceLabs esta activo, verifica que este sincronizando y que el minimo no bloquee la bajada.

### Si el usuario dice: "Tengo visitas, pero no reservas"

El problema probablemente es conversion. Revisa precio final, fotos, primeras cinco imagenes, titulo, resenas, tarifa de limpieza y restricciones. Si la primera foto no compite, cambiala. Si las primeras cinco fotos repiten el mismo espacio, reordena. Si el precio final queda mas alto que la competencia por limpieza o persona adicional, ajusta.

### Si el usuario dice: "Mi anuncio se enfrio"

Revisa si perdio posicionamiento. Mira resenas recientes, calendario, precio contra competencia, configuracion y fotos. Si lleva poco tiempo mal, optimiza y espera 10 a 15 dias. Si lleva muchos meses sin traccion y la data esta muy contaminada, considera relanzar el anuncio desde cero con fotos, precio, descripcion y reglas listas.

### Si el usuario dice: "Estoy en temporada baja"

En temporada baja debes buscar ser de los primeros en reservar. Programa descuentos antes de llegar al mes critico. Usa la duracion promedio de estadia para decidir donde descontar. Si el mercado reserva 3 o 4 noches, descuenta ahi. No esperes a estar vacio.

### Si el usuario dice: "Estoy en temporada alta"

En temporada alta protege precio. Revisa ocupacion futura y eventos. Si la ciudad se acerca a 90% o mas de ocupacion, puedes cobrar mas que tu precio normal. No vendas demasiado temprano si la demanda puede pagar mas. Baja progresivamente si se acerca la fecha y no conviertes.

### Si el usuario dice: "Hay un evento en mi ciudad"

Verifica si es evento unicornio revisando ocupacion futura, historico y competencia. Si la ocupacion supera 90% o 95%, protege fechas, sube precio y considera minimo de estadia. No dejes que una reserva de una noche dane todo un fin de semana de alta demanda.

### Si el usuario dice: "Estoy usando PriceLabs y no funciona"

PriceLabs no reemplaza diagnostico. Verifica conexion, sincronizacion, minimos, maximos, ultimo minuto, noches huerfanas y ocupacion contra mercado. Luego revisa lo que PriceLabs no ve: fotos, resenas, calidad, titulo, mala experiencia reciente o posicionamiento.

### Si el usuario dice: "Quiero publicar en Booking"

Booking no se opera igual que Airbnb. Debes gestionar cobro, comunicacion, llegada, no-show y facturas. Crea Google Maps para dar confianza. Verifica pagos antes de entregar acceso. Controla promociones como Genius porque pueden acumularse y dejarte una tarifa final demasiado baja.

### Si el usuario dice: "Tengo una mala resena"

Primero intenta resolver y documentar. Si la resena viola politica, disputa con soporte y usa evidencia del chat. Si no se puede borrar, responde profesionalmente, sin atacar, mostrando solucion. Para evitar futuras malas resenas, personaliza comunicacion y resuelve problemas antes de que escalen.

---

## Checklist maestro de diagnostico

Usar este checklist antes de recomendar cualquier accion:

- ¿Cual es la ventana de reserva del mercado?
- ¿Cual es la ocupacion propia a 7, 30 y 60 dias?
- ¿Cual es la ocupacion del mercado en esos mismos periodos?
- ¿El precio propio esta arriba o abajo de la competencia?
- ¿Cual es el precio final del huesped?
- ¿Cual es el neto recibido?
- ¿Hay descuentos acumulados?
- ¿Hay minimo de noches?
- ¿Hay reserva inmediata?
- ¿El calendario esta abierto hacia el futuro?
- ¿Hay bloqueos por otras plataformas?
- ¿La propiedad tiene malas resenas recientes?
- ¿La primera foto vende?
- ¿Las primeras cinco fotos resumen la oferta?
- ¿El titulo comunica atributos fuertes?
- ¿La descripcion protege y persuade?
- ¿La tarifa de limpieza esta dentro del mercado?
- ¿El cobro por persona adicional saca el anuncio de competencia?
- ¿La temporada es alta, baja o normal?
- ¿Hay evento cercano?
- ¿PriceLabs esta sincronizando?
- ¿Booking, Airbnb o PMS son la fuente real del precio?

---

## Errores frecuentes

1. Bajar precio sin mirar mercado
2. Esperar a estar vacio para actuar
3. Aplicar descuentos en duraciones que el mercado no reserva
4. Mantener fotos oscuras o repetidas
5. Abrir un anuncio incompleto
6. Tratar Booking como Airbnb
7. Confiar 100% en PriceLabs
8. No revisar precio final del huesped
9. Acumular promociones sin control
10. Ignorar malas resenas
11. No tener evidencia en reclamos
12. Bloquear demasiado calendario
13. Usar minimo de noches alto en un mercado flexible
14. Querer rentabilidad maxima antes de tener resenas
15. Compararse con propiedades que no son competencia directa

---

## Crisis playbook

### Principio general
Primero se calma la emocion. Luego se resuelve el problema. El huesped necesita: sentirse escuchado, saber que alguien esta actuando, tener un plazo, recibir una solucion concreta.

### Script universal
```
Hola, [NOMBRE]. Entiendo la molestia y lamento el inconveniente.
Ya estoy revisando esto para resolverlo. Te actualizare en [TIEMPO_ESTIMADO].
Gracias por avisarnos. Queremos que tu experiencia siga siendo lo mas comoda posible.
```

### Scripts por tipo de problema

Limpieza:
```
Hola, [NOMBRE]. Lamento mucho lo que comentas. La limpieza es prioritaria para nosotros. Ya estoy coordinando una revision/solucion y te confirmare en [TIEMPO]. Gracias por avisarnos de inmediato.
```

Ruido:
```
Hola, [NOMBRE]. Entiendo la molestia. Ya estoy revisando la situacion y, si corresponde, lo escalaremos con administracion/conserjeria. Te mantengo informado/a.
```

Falla de Wi-Fi:
```
Hola, [NOMBRE]. Gracias por avisar. Vamos a revisar la conexion. Por favor confirma si el problema ocurre en todos tus dispositivos o solo en uno. Mientras tanto verificaremos el servicio y te actualizaremos en [TIEMPO].
```

Falta de item:
```
Hola, [NOMBRE]. Gracias por avisar. Ya estamos revisando la disponibilidad de [ITEM] para ayudarte. Te confirmo en [TIEMPO] como lo resolveremos.
```

Solicitud de reembolso:
```
Hola, [NOMBRE]. Entiendo tu punto. Vamos a revisar lo ocurrido, la evidencia disponible y la politica de la reserva para darte una respuesta justa. Te actualizo en [TIEMPO].
```

### Criterios de escalamiento a humano
Escalar cuando: hay solicitud de reembolso, dano material, huesped agresivo, posible actividad ilegal, entrega de codigos de acceso sin verificacion, falla grave de agua/luz/cerradura/seguridad, accidente, reclamo formal, conflicto con vecinos, incumplimiento grave de reglas, overbooking, error de precio significativo, amenaza de mala resena.

---

## Reglas de la casa

### Reglas minimas
- No fumar dentro del alojamiento
- No fiestas ni eventos
- No ruido despues del horario definido
- No exceder numero de huespedes declarados
- No mascotas, si aplica
- No turismo sexual ni actividades ilegales
- Respetar check-in y check-out
- Cuidar mobiliario, ropa de cama y artefactos
- Reportar danos o incidentes
- Cumplir normas del edificio

### Regla sobre fumar
```
Esta prohibido fumar dentro del alojamiento. Si se detecta olor a cigarro, cenizas, colillas o evidencia de humo, se podra aplicar un cargo adicional de limpieza/desodorizacion segun el costo real del servicio.
```

### Regla sobre fuestes
```
No se permiten fiestas, eventos ni reuniones que alteren la tranquilidad del edificio o de los vecinos.
```

### Regla sobre huespedes adicionales
```
Solo pueden ingresar las personas declaradas en la reserva. Cualquier huesped adicional debe ser informado y aprobado previamente.
```

---

## Evidencia y reclamaciones

Para reclamar danos o incumplimiento de reglas, guardar evidencia: fotos con fecha/hora/ubicacion, video si corresponde, descripcion del dano, presupuesto o boleta del servicio, regla incumplida, comunicacion con huesped, registro del equipo de limpieza.

**Proceso:**
1. Equipo detecta incidente
2. Toma evidencia
3. Reporta al administrador
4. Se contacta al huesped de forma profesional
5. Se genera solicitud en la plataforma
6. Si el huesped rechaza, se escala con intermediacion
7. Se guarda todo en carpeta de la reserva

---

## Limpieza y operacion

### Post check-out
Cambiar sabanas, fundas y toallas; revisar manchas; aspirar; trapear; limpiar bano; revisar ducha; reponer papel higienico y jabon; limpiar cocina; revisar refrigerador, microondas y vajilla; retirar basura; ventilar; revisar olores; tomar fotos finales.

### Pre-check-in
Cama impecable, toallas visibles, bano y cocina limpios, iluminacion funcionando, Wi-Fi funcionando, TV funcionando, A/C funcionando, cerradura funcionando, aroma neutro, mensaje de bienvenida enviado, guia disponible, codigo de acceso validado.

### Mantenimiento periodico
**Cada 15 dias:** luces, enchufes, A/C, TV, controles, fugas, presion de agua, cerraduras, ventanas, muebles, manchas/humedad.
**Cada 3 meses:** pintura, sellos, artefactos, inventario, calidad de ropa blanca, fotos del anuncio, descripcion y reglas.

---

## Metricas e interpretacion

### Metricas a monitorear
Ocupacion, ADR, RevPAR, ingreso bruto/neto, comisiones, costos fijos, costo de limpieza, ticket promedio, numero de reservas, duracion promedio de estadia, ventana de reserva, tasa de conversion, vistas, clics, reservas, resenas, calificacion promedio, incidentes, reclamos, reembolsos.

### Alta ocupacion + baja ganancia
**Diagnostico:** precio demasiado bajo, costos altos, fee de limpieza mal configurado, descuentos excesivos. **Accion:** revisar precio base, descuentos y costos.

### Baja ocupacion + buena ganancia por reserva
**Diagnostico:** precio alto, baja visibilidad, restricciones, fotos debiles. **Accion:** mejorar portada, revisar precio, reducir restricciones.

### Muchas vistas + pocas reservas
**Diagnostico:** precio no convence, fotos generan interes pero texto no cierra, reglas generan friccion. **Accion:** optimizar descripcion, revisar precio final, mejorar primeras 5 fotos.

### Pocas vistas
**Diagnostico:** mala portada, titulo debil, baja visibilidad por restricciones, precio fuera de mercado. **Accion:** cambiar portada, reescribir titulo, ampliar disponibilidad, revisar minimo de noches.

---

## Branding

Elementos minimos: nombre del alojamiento, paleta de colores, tipografias, logo simple, estilo fotografico, tono de comunicacion, plantillas de mensajes, guia visual, manual breve de identidad.

El estilo visual del anuncio debe coincidir con el espacio real y con el tono de los mensajes.

### Estilos posibles

| Estilo | Sensacion | Ideal para |
|---|---|---|
| Natural y acogedor | Calma, refugio | Cabanas, naturaleza |
| Moderno y minimalista | Orden, limpieza | Estudios, lofts urbanos |
| Vibrante | Energia | Playa, hostels, grupos |
| Clasico elegante | Sofisticacion | Suites, lujo |

---

## Psicologia del huesped

El huesped decide emocionalmente y justifica racionalmente. Tres necesidades psicologicas:
1. **Seguridad:** quiero confiar
2. **Confort emocional:** siento que me cuidan
3. **Pertenencia:** soy bienvenido

La confianza aumenta cuando: fotos coinciden con el alojamiento, mensajes coinciden con el tono de marca, reglas son claras, el check-in es simple, el huesped sabe que esperar.

La confianza disminuye cuando: fotos parecen artificiales, el texto promete demasiado, las reglas aparecen tarde, el huesped descubre limitaciones al llegar, la comunicacion es fria o lenta.

---

## Jornada emocional del huesped

### Fase 1: busqueda → captar atencion
Foto portada fuerte, titulo concreto, precio competitivo, resenas visibles.

### Fase 2: primer contacto → generar confianza
Responder rapido, usar nombre del huesped, confirmar fechas, aclarar dudas.

### Fase 3: check-in → reducir ansiedad
Instrucciones claras, confirmar horario, explicar acceso, entregar contacto de soporte, mensaje simple.

### Fase 4: estadia → anticipar problemas
Mensaje de seguimiento, respuesta rapida, solucion con plazos, registro de incidentes.

### Fase 5: check-out → cerrar bien y pedir resena
Recordar horario, agradecer, pedir evaluacion de forma suave, revisar danos, guardar evidencia.

---

## Mensajeria (templates)

### Variables estandar
`[NOMBRE] [FECHA_CHECKIN] [HORA_CHECKIN] [FECHA_CHECKOUT] [HORA_CHECKOUT] [DIRECCION] [UNIDAD] [LINK_GUIA] [CODIGO_ACCESO] [WIFI] [CONTACTO_SOPORTE] [REGLAS] [IDIOMA]`

### Primer contacto
```
Hola, [NOMBRE]. Gracias por escribirnos.
Para ayudarte mejor, ¿me confirmas las fechas exactas de tu viaje y cuantas personas se hospedarian?
Con eso reviso disponibilidad y te oriento con la mejor opcion.
```

### Confirmacion de interes
```
Si, el alojamiento esta preparado para una estadia comoda y practica.
Encontraras un espacio limpio, bien ubicado y equipado para descansar o trabajar. Las fotos muestran el alojamiento real, sin edicion exagerada.
Quedo atento si quieres avanzar con la reserva.
```

### Mensaje de cierre
```
Para esas fechas suele haber buena demanda, por lo que recomiendo reservar cuando tengas claridad del viaje.
Asi aseguras disponibilidad y dejamos todo preparado para tu llegada.
```

### Seguimiento durante la estadia
```
Hola, [NOMBRE]. Espero que todo vaya bien con tu estadia.
Te escribo solo para confirmar que hayas encontrado todo en orden. Si necesitas algo, avisanos por este canal.
```

### Check-in
```
Hola, [NOMBRE].
Tu check-in esta disponible desde las [HORA_CHECKIN] del [FECHA_CHECKIN].
Direccion: [DIRECCION]
Unidad: [UNIDAD]
Instrucciones de acceso: [INSTRUCCIONES]
Contacto de soporte: [CONTACTO_SOPORTE]
Cualquier duda durante tu llegada, escribenos por este mismo canal.
```

### Bienvenida
```
Hola, [NOMBRE]. Bienvenido/a a [NOMBRE_ALOJAMIENTO].
El espacio fue preparado para que tengas una estadia comoda y tranquila.
Te dejamos la guia del alojamiento aqui: [LINK_GUIA]
Cualquier cosa que necesites, puedes escribirnos.
```

### Recordatorio de check-out
```
Hola, [NOMBRE]. Te recuerdo que el check-out es hasta las [HORA_CHECKOUT] del [FECHA_CHECKOUT].
Antes de salir, por favor revisa que no olvides pertenencias personales y deja la puerta correctamente cerrada.
Gracias por hospedarte con nosotros.
```

### Solicitud de resena
```
Hola, [NOMBRE]. Gracias por elegirnos para tu estadia. Esperamos que hayas tenido una buena experiencia.
Si puedes dejarnos una evaluacion en la plataforma, nos ayudas mucho a seguir mejorando.
Sera un gusto recibirte nuevamente.
```

---

## Prompts para agentes

### Agente de optimizacion de anuncio
```
Actua como experto en renta corta, marketing de alojamientos, revenue management y experiencia del huesped.
Analiza este anuncio usando los siguientes criterios:
1. Portada y primeras 5 fotos.
2. Titulo.
3. Primeras 2 lineas de descripcion.
4. Claridad de amenities.
5. Reglas de la casa.
6. Ubicacion.
7. Publico objetivo.
8. Precio y restricciones.
9. Coherencia entre promesa y realidad.
10. Riesgos de baja conversion.
Devuelve: diagnostico, prioridades urgentes, nuevo titulo, nueva descripcion, reglas sugeridas, checklist de fotos, riesgos operativos, acciones para proximos 7 dias.
```

### Agente de pricing
```
Actua como revenue manager de renta corta.
Analiza la estrategia de precios considerando: ocupacion actual y futura, ADR, RevPAR, competencia, temporada, eventos, ventana de reserva, minimo de noches, descuentos, fee de limpieza, politica de cancelacion, resenas, calidad del anuncio.
No recomiendes subir precios solo por eventos. Primero valida senales del mercado.
Devuelve: diagnostico, riesgos, precio base/minimo recomendado, estrategia entre semana/fin de semana/temporada alta/temporada baja, acciones inmediatas.
```

### Agente de soporte al huesped
```
Actua como agente de soporte de un alojamiento de renta corta.
Reglas: tono amable, claro y directo; no entregues claves, codigos ni datos sensibles sin reserva verificada; no prometas reembolsos; no inventes informacion; si falta un dato, indica que debe validarse; si hay un problema, primero reconoce la molestia y luego entrega proximos pasos.
Mensaje del huesped: [MENSAJE]
Contexto de la reserva: [CONTEXTO]
Devuelve una respuesta lista para enviar.
```

### Agente de crisis
```
Actua como agente de crisis para renta corta.
Objetivo: calmar al huesped, reconocer la molestia, mostrar control, dar plazo, evitar culpar al huesped, evitar prometer compensaciones sin autorizacion.
Problema: [PROBLEMA]
Contexto: [CONTEXTO]
Devuelve: 1) respuesta inmediata para el huesped, 2) accion operativa interna, 3) evidencia que debe recopilarse, 4) cuando escalar a humano.
```

---

## Prioridades de implementacion

### Urgente
Mejorar fotos, reescribir titulos, endurecer reglas criticas, revisar configuracion de PMS, revisar minimo de noches, separar fee de limpieza, validar precio base.

### Alta
Crear rule sets, ampliar ventana de disponibilidad, crear mensajes automaticos, configurar evidencias de checkout, crear guia del huesped.

### Media
Revisar politica de cancelacion, crear branding, crear plantillas para redes, revisar performance semanal.

### Baja
Mejorar diseno de manuales, crear kit de bienvenida, automatizar reportes, comparar propiedades.

---

## Inversion y seleccion de proyectos

Al evaluar proyectos, ordenar por balance entre menor precio y mayor calidad. No mirar solo precio. Revisar: ubicacion, atractivos cercanos, amenidades, mantenimiento, administracion, seguridad, zonas comunes, posibilidad de operar Airbnb, reglas del proyecto, forma de pago, facilidad de reserva/bloqueo, potencial de diferenciacion.

Un proyecto con restaurante, bar, farmacia, minimarket, piscina, areas infantiles, recepcion o control de acceso puede mejorar experiencia y venta. Pero el mantenimiento importa: una buena inversion pierde atractivo si piscinas, areas verdes o zonas comunes se ven deterioradas.

---

## Operar como negocio, no solo como anfitrion

Ver el alojamiento como activo de negocio: revisar numeros, proyectar crecimiento, captar propiedades con criterio, gestionar marca, tener procesos, controlar canales, medir resultados, profesionalizar pricing, cuidar reputacion.

Roles que pueden intervenir: revenue management, logistica, finanzas, account management, servicio al cliente, limpieza, mantenimiento. En operaciones pequenas una persona asume varios roles; en operaciones grandes conviene separarlos.

---

## Conclusion operativa

La metodologia completa se resume asi:

1. Estudia el mercado.
2. Identifica como reserva el huesped.
3. Define precio base, minimo y estrategia por temporada.
4. Ajusta descuentos por duracion real de estadia.
5. Protege fechas de alta demanda.
6. Ataca rapido ventanas rojas como los proximos 7 dias sin reservas.
7. Optimiza fotos, titulo y descripcion.
8. Cuida experiencia y resenas.
9. Opera cada plataforma segun su logica.
10. Mide y calibra por escalones.

La mejor sugerencia no es "baja el precio". La mejor sugerencia es: diagnostica si el problema es mercado, visibilidad, conversion, precio, configuracion, calidad o plataforma. Luego toca la variable correcta con un cambio medible.

---

## Reglas finales

- El mercado manda.
- Las fotos venden primero.
- El titulo debe decir por que reservar.
- La descripcion debe cerrar confianza.
- Las reglas deben proteger la operacion.
- Menos restricciones suele significar mas visibilidad.
- El precio debe ser dinamico.
- La limpieza es el KPI operativo mas importante.
- La respuesta rapida reduce ansiedad.
- La coherencia evita malas resenas.
- La evidencia protege al anfitrion.
- La experiencia completa empieza antes del check-in y termina despues del check-out.
