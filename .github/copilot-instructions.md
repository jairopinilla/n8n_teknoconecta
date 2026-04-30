# GitHub Copilot Instructions

La fuente canónica de instrucciones para este repositorio es `AGENTS.md`. Este archivo existe para que GitHub Copilot cargue el contexto correcto, pero no debe convertirse en una fuente paralela ni divergente.

## Leer primero

1. `AGENTS.md`
2. `README.md`
3. `documentacion/guia-repositorio.md`
4. `documentacion/seguimiento.md`
5. `documentacion/APIStaysDoc.md` si el trabajo toca Stays.net

## Reglas clave

- Usar siempre el `.vscode/mcp.json` local del workspace como referencia de MCP; no usar configuraciones globales del usuario para este repo.
- La zona horaria operativa es `America/Santiago` y las fechas deben salir de PostgreSQL cuando corresponda.
- Stays.net no tiene MCP propio en este proyecto; su referencia obligatoria es `documentacion/APIStaysDoc.md`.
- Airbnb no tiene API pública en esta arquitectura; los flujos relacionados dependen de correo y parsing con LLM.
- No versionar secretos. Si aparece un token o API key en un archivo tracked, retirarlo antes de commit.
- Toda modificación sustantiva debe actualizar `documentacion/seguimiento.md` con lo realizado y el siguiente paso.

Si hay una nueva convención que deba permanecer en el repo, se agrega primero a `AGENTS.md` y luego, si corresponde, este archivo sigue apuntando a ella.
