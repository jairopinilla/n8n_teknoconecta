# Product Context — TeknoConecta

## Problem Statement

Operar múltiples departamentos de renta corta manualmente no escala: cada reserva requiere coordinación de check-in/check-out, mensajes programados, asignación de aseo, procesamiento de pagos y resolución de incidencias. Airbnb no ofrece API pública, Stays.net tiene endpoints limitados, y la información está dispersa entre varios sistemas.

## Solution

Esta plataforma:

- Centraliza todas las reservas en PostgreSQL vía polling de Stays.net y parsing LLM de correos Airbnb.
- Automatiza la comunicación multi-canal (correo, WhatsApp) según el estado de cada reserva.
- Procesa formularios y correos entrantes con IA para extraer datos estructurados.
- Ofrece un chatbot RAG para consultas de huéspedes.
- Expone reportes y dashboards vía Directus.
- Usa n8n como orquestador central con patrones event-driven y schedule-driven.

## User Experience

- **Huéspedes**: reciben correos y WhatsApp automáticos con instrucciones de acceso, recordatorios y encuestas post-estadía.
- **Operadores (Jairo/Isaías)**: interactúan con el sistema vía Directus y n8n, reciben notificaciones de incidencias.
- **Personal de aseo**: recibe asignaciones vía WhatsApp con formularios Tally.so.
- **Conserjería**: correos interpretados automáticamente y persistidos como eventos estructurados.

## Success Criteria

- Toda reserva de Stays.net o Airbnb debe aparecer en PostgreSQL en <15 min desde su creación.
- Los correos programados deben enviarse en la fecha/hora exacta (zona Santiago).
- El chatbot debe responder consultas frecuentes con precisión >90%.
- Los formularios de aseo deben procesarse sin intervención manual.
- Cero pérdida de datos entre sistemas.
