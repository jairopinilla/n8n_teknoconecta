# System Patterns — TeknoConecta

## Arquitectura de servicios

```
Internet
  ↓
Cloudflare (DNS + Access + Tunnel)
  ↓
Nginx (VPS host, puertos 80/443, SSL)
  ↓
Docker containers (redes internas, 127.0.0.1 bind)
  ↓
Servicios (n8n, Directus, Supabase, Saldito, PostgreSQL, etc.)
```

## Patron MCP

Los MCPs chitara conectan via SSH al VPS:
```
OpenCode → MCP server (Python local) → SSH → VPS → Docker container
```

Ejemplo: `supabase-chitara` → SSH → `docker exec postgres psql`

Los MCPs cloud (n8n-mcp, directus, supabase) son legacy y apuntan a servicios ya migrados.

## Patron de seguridad

1. **127.0.0.1 bind**: servicios Docker solo accesibles localmente
2. **Cloudflare Tunnel**: expone `*.chitaraagenteia.com` via Cloudflare edge
3. **Cloudflare Access**: Google SSO en 16 apps
4. **iptables**: bloquea acceso directo a puertos Docker desde internet
5. **Nginx**: reverse proxy con SSL (Let's Encrypt)

## Patron de encriptacion

```
Archivos planos (gitignored) ← openssl AES-256-CBC → Archivos .enc (commiteados)
                                                        Clave maestra definida en decrypt.sh
```

`bash decrypt.sh` al iniciar. `cat file | openssl enc ... > file.enc` para re-encriptar.

## Patron Stays ↔ Directus

- `_idlisting` (Stays, MongoDB ObjectId) ↔ `AlojamientoStayslistingIdLargo` (Directus)
- `AlojamientoStayslistingId` (corto) ↔ `AlojamientoStaysId` (Stays)
- Solo endpoints GET funcionales (reservas, search-listings)

## Patron Saldito (gestion_gastos)

```
Usuario → Clerk sign-in → JWT token → Frontend interceptor
  → POST /api/usuarios/ensure → Backend verifyToken → SELECT/INSERT Usuario
  → Dashboard carga datos (resumen, gastos, ingresos)
```

Auto-provisioning: nuevo Clerk user → `ensureUsuario` crea/actualiza registro en BD por email.
