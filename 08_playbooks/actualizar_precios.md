# Playbook: Actualizar precios

## Flujo normal

1. PriceLabs actualiza precios diariamente (automatico)
2. Verificar que la sincronizacion Stays ← PriceLabs esta activa
3. Si hay cambios manuales: hacer en PriceLabs, NO en Stays (se sobrescribira)

## Cuando intervenir manualmente

- Eventos locales que PriceLabs no captura
- Periodos de alta demanda no reflejados
- Errores en la sincronizacion

## Reglas

- No modificar precios directamente en Stays si PriceLabs los controla
- Documentar cambios manuales en seguimiento
- Verificar despues de cada cambio que la sincronizacion funciona
