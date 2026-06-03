Evalúa este plan de migración de arquitectura para Gestor de Gastos.
NO ejecutes cambios. Solo analiza, cuestiona y ajusta, luego presenta el plan refinado.

---

## Contexto actual

| Capa | Tecnologia | Host |
|------|-----------|------|
| Backend API | Node.js ESM, @clerk/backend, @neondatabase/serverless | VPS Docker (chitara) |
| DB | Neon PostgreSQL (pooled), proyecto old-lab-07457522, 0.25 CU, schema gestiongastos | Neon cloud |
| Workers | Python 3, Vercel serverless (clasificador de correos, 12 steps) | Vercel Hobby |
| Frontend | Angular 20 + Ionic 8 (SPA, PWA) | VPS Docker (nginx) |
| Auth | Clerk (instancia development, email magic link + Google OAuth) | Clerk cloud |

### Estructura del backend actual
- `backend/src/server.mjs`: HTTP server, CORS, rutas
- `backend/src/auth.mjs`: verifyToken() de @clerk/backend
- `backend/src/db.mjs`: ensureUsuario(), executeReadOnlyWithClaims(), health check
- `backend/src/routes.mjs`: 9 endpoints (health, usuarios, ingresos, egresos, transferencias, movimientos, resumen-mensual, gasto-por-categoria, top-contrapartes, ultimos-movimientos, correo/*)
- DB usa RLS con set_config('request.jwt.claims')

---

## Puntos a evaluar

### 1. Neon PostgreSQL
- **Situacion**: BD gestionada por Neon. No tenemos acceso al servidor fisico. 
- **Riesgo**: No podemos auditar ejecuciones SQL, no hay pgAudit.
- **Costo**: 0.25 CU (minimo), ~$0/mes en plan gratuito.
- **Alternativa**: Migrar al PostgreSQL local del VPS (ya existe: puerto 5432, container postgres).
- **Preguntas**:
  - ¿Conviene perder la gestion serverless de Neon por ganar auditoria?
  - ¿Que impacto tiene en cold starts y latencia?
  - ¿El VPS tiene recursos para manejar la BD + todos los servicios existentes?

### 2. Python serverless en Vercel
- **Situacion**: workers/python/ con 12 steps en Vercel serverless functions.
- **Problema**: Proyecto fragmentado, dificil de mantener.
- **Objetivo**: Consolidar en un solo proyecto Python con framework ligero.
- **Frameworks a evaluar**:
  - FastAPI (maduro, async, pero pesado para Vercel)
  - Flask (ligero, pero sincrono)
  - Hono.py (nuevo, muy ligero, Vercel-optimizado)
  - Solo funciones individuales sin framework
- **Criterio**: Menor cold start, menor costo en Vercel, mantenible.
- **Auth**: ¿Como manejar Clerk JWT validation desde Python?

### 3. Migracion Node → Python (del backend)
- **Impacto**: 9 endpoints REST (~300 lineas de codigo)
- **Frontend**: Cambiar todas las llamadas HTTP de `environment.api.baseUrl`
- **Riesgo**: Regresion, tiempo de desarrollo, testing.
- **Alternativa**: Mantener Node.js para el backend API y solo consolidar workers en Python.

### 4. Trazabilidad
- **Objetivo**: Documentar cada funcionalidad con diagrama de flujo.
- **Ejemplo**: Login → Clerk sign-in → token JWT → frontend interceptor → POST /api/usuarios/ensure → backend verifyToken → ensureUsuario (SELECT/INSERT/UPDATE Usuario) → dashboard carga datos.
- **Formato**: Mermaid o textual, un archivo por funcionalidad en docs/trazabilidad/.

---

## Decisiones sugeridas (para debate)

1. **BD**: Mantener Neon. Es barato, serverless, sin carga de mantenimiento. Para auditoria podemos agregar una tabla de logs (`AuditoriaQuery`) y un middleware que registre cada consulta.
2. **Backend API**: Mantener Node.js. Funciona, es minimo, no hay razon de peso para migrar.
3. **Workers Python**: Consolidar en un solo proyecto Vercel con Hono.py o FastAPI ligero. Mover auth a middleware compartido.
4. **Auditoria**: Crear tabla `gestiongastos."AuditoriaQuery"` con campos: query, usuario, timestamp, duracion. Agregar middleware en el backend.
5. **Trazabilidad**: Generar docs/mermaid para cada endpoint.

---

## Entrega esperada
1. Analisis critico punto por punto (pros/contras de cada decision)
2. Matriz de decision: costo vs complejidad vs mantenibilidad
3. Plan de implementacion priorizado (que hacer primero)
4. Diagramas de trazabilidad si se aprueba la migracion
5. Estimacion de tiempo para cada fase
