# Configuración de servidores MCP para OpenCode

Esta guía detalla cómo configurar OpenCode para que lea servidores MCP desde un repositorio.

## Archivos necesarios

Se requieren 3 archivos en la raíz del repositorio:

```
tu-repo/
├── .vscode/
│   ├── mcp.json          ← servidores MCP (con credenciales)
│   └── settings.json     ← deshabilita discovery de otros clientes
├── .gitignore            ← incluye .vscode/mcp.json
├── AGENTS.md             ← documenta el setup (opcional pero recomendado)
└── OPENCODE.md           ← punto de entrada compatible (opcional)
```

---

## Paso 1: `.vscode/settings.json`

Este archivo deshabilita la búsqueda automática de configuraciones MCP de otros clientes (Claude Desktop, Windsurf, Cursor) para que OpenCode **solo** lea el `mcp.json` del workspace.

```json
{
  "chat.mcp.discovery.enabled": {
    "claude-desktop": false,
    "windsurf": false,
    "cursor-global": false,
    "cursor-workspace": false
  }
}
```

---

## Paso 2: `.vscode/mcp.json`

Define los servidores MCP. Soporta dos tipos: `http` (API remota) y `stdio` (proceso local vía npx).

### Estructura base

```json
{
  "servers": {
    "nombre-del-servidor": {
      "type": "http",
      "url": "https://url-del-mcp.com",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```

### Tipo `http` — servidor remoto

Para APIs que exponen un endpoint MCP sobre HTTP. La autenticación va en `headers`.

```json
{
  "type": "http",
  "url": "https://mcp.ejemplo.com",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

**Ejemplos reales:**

```json
{
  "supabase": {
    "type": "http",
    "url": "https://mcp.supabase.com/mcp?project_ref=TU_PROJECT_REF",
    "headers": {
      "Authorization": "Bearer TU_SUPABASE_TOKEN"
    }
  },
  "directus": {
    "type": "http",
    "url": "https://TU_INSTANCIA.directus.app/mcp",
    "headers": {
      "Authorization": "Bearer TU_DIRECTUS_TOKEN"
    }
  },
  "vercel": {
    "type": "http",
    "url": "https://mcp.vercel.com",
    "headers": {
      "Authorization": "Bearer TU_VERCEL_TOKEN"
    }
  },
  "jina": {
    "type": "http",
    "url": "https://mcp.jina.ai/v1",
    "headers": {
      "Authorization": "Bearer TU_JINA_API_KEY"
    }
  },
  "google-maps": {
    "type": "http",
    "url": "https://mapstools.googleapis.com/mcp",
    "headers": {
      "X-Goog-Api-Key": "TU_GOOGLE_API_KEY"
    }
  },
  "mercadopago": {
    "type": "http",
    "url": "https://mcp.mercadopago.com/mcp",
    "headers": {
      "Authorization": "Bearer TU_MERCADOPAGO_TOKEN"
    }
  },
  "airroi": {
    "type": "http",
    "url": "https://mcp.airroi.com",
    "headers": {
      "X-API-KEY": "TU_AIRROI_API_KEY"
    }
  },
  "clerk": {
    "type": "http",
    "url": "https://mcp.clerk.com/mcp",
    "headers": {
      "Authorization": "Bearer TU_CLERK_SECRET_KEY"
    }
  }
}
```

### Tipo `stdio` — proceso local

Ejecuta un paquete npm que actúa como MCP server. El comando y sus argumentos se definen en `command` y `args`. Las variables de entorno (API keys) van en `env`.

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "<paquete-npm>", "<arg1>", "<arg2>"],
  "env": {
    "API_KEY": "<valor>"
  }
}
```

**Ejemplos reales:**

```json
{
  "neon": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@neondatabase/mcp-server-neon", "start", "TU_NEON_API_KEY"]
  },
  "openai": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@mzxrai/mcp-openai@latest"],
    "env": {
      "OPENAI_API_KEY": "TU_OPENAI_API_KEY"
    }
  },
  "perplexity": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "perplexity-mcp"],
    "env": {
      "PERPLEXITY_API_KEY": "TU_PERPLEXITY_API_KEY"
    }
  }
}
```

### Caso especial: n8n con supergateway

n8n expone MCP sobre HTTP pero requiere `supergateway` como proxy stdio:

```json
{
  "n8n-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "supergateway",
      "--streamableHttp",
      "https://TU_INSTANCIA_N8N/mcp-server/http",
      "--header",
      "authorization:Bearer TU_N8N_TOKEN"
    ]
  }
}
```

---

## Paso 3: `.gitignore`

Añadir al `.gitignore` del repositorio para no versionar credenciales:

```gitignore
# MCP local con secretos
.vscode/mcp.json
```

Si el `.gitignore` no existe, crearlo en la raíz del repo.

---

## Paso 4: Documentar en las instrucciones del repositorio

En el `AGENTS.md` (o equivalente) del repositorio, añadir una línea que indique la existencia y propósito del archivo:

```markdown
- `.vscode/mcp.json`: configuración local de MCP del workspace. Es local, está ignorada por git y debe preferirse sobre configuraciones globales del usuario.
```

Si el repo usa `OPENCODE.md` como punto de entrada, ese archivo debe ser delgado y redirigir a `AGENTS.md`:

```markdown
# OPENCODE.md

Ver [AGENTS.md](./AGENTS.md) para las instrucciones completas del repositorio.
```

---

## Verificación

Para confirmar que OpenCode leyó los servidores correctamente:

1. Cerrar y reabrir el workspace
2. Los servidores definidos en `.vscode/mcp.json` deben aparecer como herramientas disponibles
3. Si un servidor no aparece, revisar que las credenciales sean válidas y que `npx` esté instalado

---

## Notas importantes

- **Nunca** versionar `.vscode/mcp.json` — contiene secretos en texto plano
- **Siempre** usar este archivo local en vez de configuraciones globales del usuario
- El archivo es específico del workspace; cada repositorio puede tener sus propios servidores
- Para servidores `stdio`, se requiere Node.js y `npx` instalados en el sistema
- Si el workspace está en WSL, asegurarse de que `npx` esté accesible desde la terminal de WSL
