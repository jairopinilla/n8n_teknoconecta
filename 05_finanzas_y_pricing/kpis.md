# KPIs

## Metricas a tracking

| Metrica | Definicion | Formula |
|---------|-----------|---------|
| Ocupacion | % noches ocupadas sobre disponibles | (noches ocupadas / noches disponibles) * 100 |
| ADR | Tarifa promedio por noche | Revenue bruto / noches ocupadas |
| RevPAR | Revenue por noche disponible | Revenue bruto / noches disponibles |
| Margen neto | Rentabilidad despues de costos | (Revenue neto / Revenue bruto) * 100 |
| Cancelaciones | % de reservas canceladas | (cancelaciones / reservas totales) * 100 |
| Lead time | Antelacion promedio de reserva | Promedio (fecha de reserva - fecha arrival) |
| Longitud estadia | Promedio de noches por reserva | Promedio (noches por reserva) |

## Pipeline de datos

raw → cleaned → curated → reporting

- Raw: exportaciones directas de Stays / PriceLabs
- Cleaned: datos normalizados con fecha de corte
- Curated: metricas calculadas por unidad y periodo
- Reporting: dashboards y alertas

## Costos operativos

- Limpieza: por reserva
- Comisiones OTA: segun plataforma
- Costos fijos: electricidad, agua, internet, conserjeria
- Costos variables: mantenimiento, reposiciones
