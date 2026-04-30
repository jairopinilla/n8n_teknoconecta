# Seguimiento del Repositorio

## Cómo usar este archivo

Este documento es la bitácora viva del repositorio. Toda modificación sustantiva debe dejar aquí, como mínimo:

- qué se hizo,
- cuál es el estado actual resultante,
- cuál es el siguiente paso recomendado.

## Última actualización

- Fecha: `2026-04-30`
- Motivo: normalización documental multi-agente y saneamiento de documentación sensible.

## Qué se hizo en esta iteración

- Se creó `AGENTS.md` como fuente canónica y neutral para cualquier asistente de código.
- Se añadió `README.md` como puerta de entrada del repositorio.
- Se añadieron `CLAUDE.md` y `OPENCODE.md` como puntos de entrada compatibles, sin reglas divergentes.
- Se reemplazó el contenido de `.github/copilot-instructions.md` por una versión alineada con la nueva fuente canónica.
- Se creó `documentacion/guia-repositorio.md` con inventario del repo, convenciones y limitaciones conocidas.
- Se sanitizó `documentacion/tecnologias.md` para eliminar un token versionado y se reforzó la política de secretos.
- Se amplió `documentacion/tecnologias.md` para reflejar que el repo usa OpenAI, Google Gemini y Tavily en workflows específicos.

## Estado actual

- El repositorio tiene 12 workflows exportados en `workflows/`.
- De esas exportaciones, 10 aparecen activas y 2 inactivas en los JSON actuales.
- La instrucción canónica ya no depende de un archivo específico de Copilot.
- Existe una ruta documental clara: `README.md` -> `AGENTS.md` -> `documentacion/guia-repositorio.md` -> `documentacion/tecnologias.md` -> `documentacion/APIStaysDoc.md`.
- Los secretos operativos siguen estando previstos solo para archivos locales ignorados por git.

## Próximos pasos recomendados

1. Rotar la credencial de Directus que estuvo expuesta históricamente en documentación versionada.
2. Decidir si `sync_workflows.sh` debe exportar también workflows inactivos o si se mantendrá la limitación actual de forma explícita y permanente.
3. Ampliar la documentación por workflow con entradas, salidas, tablas afectadas y dependencias de credenciales para reducir más el contexto implícito.

## Riesgos y observaciones

- Aunque el token expuesto fue retirado del árbol de trabajo actual, el historial remoto puede seguir conteniéndolo. Esto requiere tratamiento operativo fuera de este commit.
- El script de sincronización y el contenido actual del repositorio no cubren exactamente el mismo universo de workflows, porque el repo contiene archivos inactivos y el script descarga solo activos.

## Historial resumido

| Fecha | Cambio | Estado |
|-------|--------|--------|
| 2026-04-30 | Se normalizó la documentación para asistentes multi-agente y se creó una bitácora viva del repositorio | Completado |