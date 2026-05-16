# Secretos

Este directorio documenta que secretos existen y donde deben vivir.
**Ningun valor secreto real debe estar en este repositorio.**

## Inventario de secretos

| Secreto | Ubicacion real | Tipo |
|---------|---------------|------|
| n8n JWT Bearer | `.vscode/mcp.json` | Token de acceso |
| Stays API Key | `.vscode/mcp.json` | API credential |
| Supabase keys | `.vscode/mcp.json` | API credential |
| OpenAI API Key | `.vscode/mcp.json` | API credential |
| PriceLabs API Key | `.vscode/mcp.json` | API credential |
| Twilio credentials | `secrets.json` | API credential |
| Gmail credentials | n8n credential store | OAuth |
| Numeros de telefono | n8n credential store | Operational |
| Codigos de acceso | Fuera del repo | Access codes |

## Secretos detectados en archivos versionados (CRITICAL)

| Archivo | Secreto | Accion requerida |
|---------|---------|------------------|
| `exportadata/exportar_supabase.ipynb` | Supabase anon key + PII huespedes + direccion personal host | REMOVER de git history |
| `exportadata/export_20260504_104837.xlsx` | Datos de reservas con PII | REMOVER de git + agregar a .gitignore |
| `workflows/N8n_Update_Reservas.json` | Numeros de telefono hardcodeados | Mover a credential nodes |
| `workflows/N8n_Update_Reservas_v2.json` | Numeros de telefono + emails hardcodeados | Mover a credential nodes |
| `documentacion/tecnologias.md` | Numeros de telefono operativos | Redactar |

## Politica

- Los valores reales deben estar en variables de entorno, gestor de secretos o configuracion privada fuera del repo
- `.vscode/mcp.json` y `secrets.json` estan en `.gitignore`
- Ningun secreto real debe aparecer en archivos versionados
- Si se detecta un secreto en un archivo versionado, marcarlo como CRITICAL y removerlo
