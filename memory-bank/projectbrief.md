# Project Brief — TeknoConecta

## Overview

Plataforma de automatización integral para la operación de renta corta (short-term rental). Orquesta reservas, comunicación con huéspedes, limpieza, conserjería y pagos mediante workflows de n8n, PostgreSQL, Directus y múltiples integraciones externas como Stays.net, Airbnb (vía correo), WhatsApp/Twilio y LLMs.

## Core Requirements

- Sincronizar reservas desde Stays.net y Airbnb hacia PostgreSQL con mínima intervención humana.
- Enviar correos y mensajes WhatsApp programados a huéspedes según el ciclo de vida de la reserva.
- Procesar formularios externos (Tally.so) y correos de conserjería con extracción estructurada vía LLM.
- Operar un chatbot conversacional para huéspedes usando RAG y LLMs.
- Mantener integridad de datos entre Stays.net, Directus y PostgreSQL.
- Automatizar asignaciones de aseo y generar reportes.

## Goals

- Reducir intervención manual al mínimo posible.
- Centralizar el conocimiento operativo en documentación versionada y consultable.
- Mantener el sistema funcionando 24/7 con monitoreo y alertas.
- Escalar a múltiples propiedades sin aumentar la carga operativa.

## Scope

### In Scope

- Automatización de reservas, comunicación y aseo.
- Integración con Stays.net, Twilio, Gmail, Tally.so, MercadoPago.
- Procesamiento de lenguaje natural para correos y chatbot.
- Documentación viva del sistema.

### Out of Scope

- Gestión directa de precios dinámicos (lo maneja Stays.net).
- Aplicación móvil para huéspedes.
- Integración con OTAs más allá de Airbnb y Stays.net.
