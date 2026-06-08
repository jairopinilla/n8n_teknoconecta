# Diagnostic First Protocol

## Objetivo

Garantizar que ningun agente ejecute cambios sin antes entender el problema, diagnosticar en modo read-only, proponer alternativas, y recibir aprobacion explicita del usuario (Jairo).

Este protocolo aplica a todos los agentes que operen en este repositorio: OpenCode, Chitara (Hermes), Claude, y cualquier otro asistente IA.

---

## Modos de trabajo

### 1. Modo entendimiento

Antes de actuar, el agente debe entender:
- Que se esta pidiendo
- Cual es el contexto actual (leer `memory-bank/activeContext.md`)
- Que sistemas estan involucrados
- Cual es el estado previo

**Permitido sin aprobacion**: Leer archivos, buscar en el repo, revisar documentacion.

### 2. Modo diagnostico

Investigar el problema en modo solo lectura:
- Revisar logs (`docker logs`, `gateway.log`, `agent.log`)
- Consultar bases de datos (SELECT, no INSERT/UPDATE/DELETE)
- Revisar configuraciones actuales
- Verificar estado de servicios
- Consultar APIs en modo lectura

**Permitido sin aprobacion**: Cualquier operacion read-only.

### 3. Modo solucion

Proponer una o mas soluciones al usuario:
- Describir que se hara
- Explicar pros/contras de cada alternativa
- Indicar riesgos
- Estimar impacto

**NO ejecutar nada. Solo proponer.**

### 4. Gate de aprobacion

El agente se detiene y presenta la propuesta al usuario. Solo continua cuando el usuario dice explicitamente que aprueba. Frases validas de aprobacion:
- "procede"
- "dale"
- "hazlo"
- "aprobado"
- "ejecuta"

Frases que NO son aprobacion:
- "que opinas?"
- "interesante"
- "podria ser"

### 5. Plan por pasos

Toda solucion aprobada se divide en pasos medianos:
- Cada paso es verificable independientemente
- Cada paso tiene un rollback claro
- Los pasos se presentan al usuario antes de ejecutar
- El usuario puede aprobar todos, algunos, o ninguno

### 6. Modo ejecucion

Ejecutar SOLO los pasos aprobados:
- Un paso a la vez (salvo que el usuario diga "ejecuta N-M de corrido")
- Despues de cada paso: verificar que funciono
- Si falla: detenerse, reportar, esperar instrucciones

### 7. Validacion

Despues de cada paso ejecutado:
- Verificar que el cambio se aplico correctamente
- Mostrar evidencia (logs, queries, curl, etc.)
- Indicar si el paso fue exitoso o fallo
- Indicar cual es el siguiente paso recomendado

### 8. Registro en Memory Bank

Registrar en `memory-bank/` cuando:
- Se diagnostica un problema relevante
- Se toma una decision
- Se ejecuta un cambio funcional
- Ocurre un incidente
- Se establece una nueva regla operacional

---

## Acciones permitidas sin aprobacion

| Accion | Ejemplo |
|--------|---------|
| Leer archivos del repo | `cat`, `grep`, `read` |
| Buscar en el repo | `glob`, `grep`, busqueda de contenido |
| Revisar logs | `docker logs`, `cat *.log` |
| Consultar APIs en modo lectura | `GET` requests, `SELECT` queries |
| Verificar estado de servicios | `docker ps`, `curl health`, `systemctl status` |
| Leer configuraciones | `cat config.yaml`, `cat .env` (sin exponer secretos) |
| Consultar documentacion | Leer docs, READMEs, wikis |
| Proponer soluciones | Describir alternativas sin ejecutar |

---

## Acciones que requieren aprobacion

| Accion | Nivel de riesgo |
|--------|----------------|
| Editar codigo fuente | Medio |
| Cambiar configuraciones | Medio |
| Modificar Docker compose | Medio-Alto |
| Reiniciar servicios | Medio |
| Ejecutar SQL de escritura (INSERT/UPDATE/DELETE) | Alto |
| Crear/modificar workflows n8n | Alto |
| Cambiar DNS/Cloudflare | Alto |
| Deploy de aplicaciones | Alto |
| Cambios en infraestructura VPS | Alto |
| `hermes config set` (cualquier parametro) | Alto |

---

## Acciones de negocio de arriendo de alto riesgo

Estas acciones requieren **aprobacion explicita reforzada** (el usuario debe confirmar que entiende el impacto):

| Accion | Por que es alto riesgo |
|--------|----------------------|
| Cambiar precios en PriceLabs | Afecta ingresos directamente |
| Modificar reservas en Stays | Afecta huespedes |
| Enviar mensajes a huespedes | Comunicacion directa con clientes |
| Cambiar codigos de acceso/cerraduras | Seguridad fisica |
| Modificar check-in/check-out | Operacion diaria |
| Cambiar asignacion de aseos | Coordinacion con Valentina |
| Push de precios a canales | Irreversible una vez publicado |
| Cancelar o modificar reservas | Impacto financiero + reputacional |

---

## Formato de respuesta esperado

Cuando el agente diagnostica y propone:

```
## Diagnostico
[que encontre, evidencia]

## Problema identificado
[resumen claro]

## Propuesta(s)
### Opcion A: [nombre]
- Que hace: ...
- Pros: ...
- Contras: ...
- Riesgo: Bajo/Medio/Alto

### Opcion B: [nombre]
...

## Pasos (si se aprueba Opcion X)
1. [paso 1 - verificable]
2. [paso 2 - verificable]
3. [paso 3 - verificable]

## Espero tu aprobacion.
```

---

## Ejemplo de flujo correcto

**Usuario**: "Chitara dice que no puede acceder a Stays API"

**Agente** (modo diagnostico):
1. Lee logs: `docker exec hermes tail -50 /opt/data/logs/agent.log`
2. Encuentra: "Error: 401 Unauthorized"
3. Verifica config: `grep STAYS /opt/homelab/hermes/docker-compose.yml`
4. Detecta: el header de autenticacion esta mal

**Agente** (propone):
> Diagnostico: Chitara usa `api-key` como header pero Stays espera `Authorization: Basic`.
> Propuesta: Cambiar el header en `mcp-servers/hermes-chitara/server.py` linea 88.
> Riesgo: Bajo (solo afecta lectura de API, no escritura).
> Espero tu aprobacion.

**Usuario**: "procede"

**Agente** (ejecuta):
1. Edita el archivo
2. Pushea a GitHub
3. Pull en VPS
4. Reinicia Hermes
5. Verifica con curl
6. Reporta resultado

---

## Reglas finales

1. **Nunca saltar directo a editar o ejecutar.** Siempre diagnosticar primero.
2. **Nunca asumir que el usuario quiere un cambio.** Siempre preguntar.
3. **Nunca guardar secretos** en documentacion, memory-bank, ni logs visibles.
4. **Nunca exponer datos sensibles** de huespedes (PII) sin autorizacion.
5. **Si hay duda sobre el nivel de riesgo, detenerse y preguntar.**
6. **El protocolo no se puede saltar** ni con urgencia ni con "sentido comun".
7. **Cada sesion comienza leyendo** `memory-bank/activeContext.md`.
