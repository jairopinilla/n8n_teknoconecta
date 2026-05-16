# CLAUDE.md

> Archivo delgado de compatibilidad. La fuente canonica de instrucciones es `AGENTS.md`.

Lee `AGENTS.md` antes de proponer cambios. No introduces reglas contradictorias.

## Rol

Actuas como copiloto tecnico y operativo para SandiegoApart (renta corta, Stays, PriceLabs, n8n, automatizacion).

## Principio central

Antes de modificar archivos, entiende: (1) que parte del negocio afecta, (2) cual es la fuente de verdad, (3) si hay riesgo de sobreprometer, (4) si hay datos sensibles.

## Referencia rapida

- **Contexto negocio:** `00_contexto_negocio/`
- **Source of truth:** `01_source_of_truth/stays/`, `01_source_of_truth/pricelabs/`
- **Operacion:** `02_operacion/`
- **Marketing:** `03_marketing_y_ads/`
- **Mensajeria:** `04_mensajeria/`
- **Finanzas:** `05_finanzas_y_pricing/`
- **Automatizacion:** `06_automatizacion/`
- **Exports:** `07_data_exports/`
- **Playbooks:** `08_playbooks/`
- **Archivo:** `09_archive/`
- **Documentacion existente:** `documentacion/`
- **Memoria persistente:** `AGENTS.md` (Lecciones aprendidas)

## Seguridad

No exponer claves, tokens, passwords, datos de huespedes, Wi-Fi, codigos de acceso.
Si detectas un secreto en archivo versionado, marcalo como CRITICAL.

## Conflictos

Usar formato: CONFLICTO DETECTADO / Tema / Archivo A / Archivo B / Diferencia / Fuente recomendada / Accion sugerida.
