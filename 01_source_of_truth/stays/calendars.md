# Calendarios — Stays.net

El calendario de disponibilidad se gestiona desde Stays.net.
Los workflows sincronizan reservas hacia PostgreSQL para analisis y mensajeria.

## Flujo de sincronizacion

1. Workflow `N8n_Update_Reservas` consulta `/external/v1/booking/reservations`
2. Persiste en PostgreSQL (tabla `Reserva`)
3. Workflows de mensajeria leen desde PostgreSQL

## Exportaciones

Archivos historicos en `07_data_exports/stays_exports/`.

## Reglas

- Zona horaria: `America/Santiago`
- Fechas operativas deben salir de PostgreSQL con `now() AT TIME ZONE 'America/Santiago'`
