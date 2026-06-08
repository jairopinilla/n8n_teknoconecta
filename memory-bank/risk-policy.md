# Risk Policy

> Politica de riesgo para todos los agentes que operan en este repositorio.

## Principio general

**Ante la duda, detenerse y preguntar.** Nunca asumir que un cambio es seguro.

---

## Niveles de riesgo

### Bajo — Automatico (sin aprobacion)

| Accion | Ejemplo |
|--------|---------|
| Leer archivos | `cat`, `read`, `grep` |
| Buscar en el repo | `glob`, `find` |
| Revisar logs | `docker logs`, `tail -f` |
| Consultar APIs (GET) | Stays reservas, PriceLabs listings |
| Verificar estado de servicios | `docker ps`, health checks |
| Leer configuracion | `cat config.yaml` (sin exponer secretos) |
| Consultar documentacion | READMEs, docs, wikis |
| Proponer soluciones | Describir opciones sin ejecutar |

### Medio — Requiere aprobacion

| Accion | Riesgo |
|--------|--------|
| Editar codigo fuente | Puede romper funcionalidad |
| Cambiar configuraciones | Puede alterar comportamiento |
| Crear/modificar archivos en el repo | Cambia estado del proyecto |
| Reiniciar servicios | Interrupcion temporal |
| Modificar Docker compose | Cambia infraestructura |
| Ejecutar scripts | Efectos secundarios posibles |

### Alto — Requiere aprobacion explicita reforzada

| Accion | Por que |
|--------|---------|
| Deploy de aplicaciones | Irreversible en produccion |
| SQL de escritura (INSERT/UPDATE/DELETE) | Modifica datos de negocio |
| Crear/modificar workflows n8n | Afecta automatizaciones |
| Cambiar DNS/Cloudflare | Afecta acceso a servicios |
| Cambios en infraestructura VPS | Puede tumbar servicios |
| `hermes config set` | Cambia comportamiento de Chitara |

### Critico — Requiere aprobacion explicita reforzada + confirmacion de impacto

| Accion | Impacto |
|--------|---------|
| Cambiar precios en PriceLabs | Afecta ingresos directamente |
| Modificar/cancelar reservas en Stays | Afecta huespedes + ingresos |
| Enviar mensajes a huespedes | Comunicacion directa con clientes |
| Cambiar codigos de acceso | Seguridad fisica de las unidades |
| Push de precios a canales | Publicado = irreversible |
| Modificar check-in/check-out | Operacion diaria |

---

## Prohibiciones absolutas

1. **Nunca guardar secretos** en documentacion, memory-bank, logs visibles, ni commits.
2. **Nunca exponer PII** de huespedes (nombres, emails, telefonos) en documentacion publica.
3. **Nunca hacer deploy** sin aprobacion.
4. **Nunca restart** servicios sin aprobacion.
5. **Nunca escribir en DB** sin aprobacion.
6. **Nunca cambiar workflows** sin aprobacion.
7. **Nunca cambiar pricing** sin el protocolo de 10 pasos (ver AGENTS.md).
8. **Nunca enviar mensajes a huespedes** sin aprobacion.
9. **Nunca modificar reservas** sin aprobacion.
10. **Nunca exponer puertos** al exterior sin mecanismo de autenticacion.

---

## Protocolo ante incidente

1. Detectar
2. Diagnosticar (read-only)
3. Clasificar severidad (Baja/Media/Alta/Critica)
4. Reportar al usuario con diagnostico y propuesta
5. Esperar aprobacion
6. Ejecutar solucion aprobada
7. Validar
8. Registrar en `memory-bank/incidents.md`

---

## Responsable

Todas las aprobaciones las da **Jairo** (contacto@teknoconecta.com).
Ningun agente tiene autonomia para cambios funcionales sin su autorizacion.
