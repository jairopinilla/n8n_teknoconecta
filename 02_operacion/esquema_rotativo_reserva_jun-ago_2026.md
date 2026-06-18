# Esquema Rotativo — Reserva Lunes-Viernes (Jun-Ago 2026)

> **Cliente**: Estadia recurrente, solo lunes a viernes, bloque semanal con aseo incluido.  
> **Periodo**: 22 de junio al 28 de agosto de 2026 (10 semanas)  
> **Estrategia**: Rotacion entre 4 departamentos para mantener visibilidad en Airbnb.

---

## Distribucion semanal

| Sem | Lunes | Viernes | Depto | Noches | Arriendo | Aseo | Total semana |
|-----|-------|---------|-------|--------|----------|------|-------------|
| 1 | 22 Jun | 26 Jun | **702** | 4 | $72,000 | $30,000 | **$102,000** |
| 2 | 29 Jun | 3 Jul | **709** | 4 | $105,684 | $30,000 | **$135,684** |
| 3 | 6 Jul | 10 Jul | **901** | 4 | $123,679 | $30,000 | **$153,679** |
| 4 | 13 Jul | 17 Jul | **709** | 4 | $108,479 | $30,000 | **$138,479** |
| 5 | 20 Jul | 24 Jul | **901** | 4 | $137,633 | $30,000 | **$167,633** |
| 6 | 27 Jul | 31 Jul | **702** | 4 | $101,099 | $30,000 | **$131,099** |
| 7 | 3 Ago | 7 Ago | **902** | 4 | $127,152 | $30,000 | **$157,152** |
| 8 | 10 Ago | 14 Ago | **709** | 4 | $99,968 | $30,000 | **$129,968** |
| 9 | 17 Ago | 21 Ago | **902** | 4 | $119,838 | $30,000 | **$149,838** |
| 10 | 24 Ago | 28 Ago | **702** | 4 | $109,721 | $30,000 | **$139,721** |

---

## Carga por departamento

| Depto | Semanas este huesped | Otras reservas (ya existentes) | Semanas libres | Visibilidad Airbnb |
|-------|---------------------|-------------------------------|----------------|-------------------|
| **901** | 2 (semanas 3, 5) | 6 semanas ya reservadas | 4/10 | Muy sano |
| **902** | 2 (semanas 7, 9) | 6 semanas ya reservadas | 4/10 | Muy sano |
| **709** | 3 (semanas 2, 4, 8) | 0 | 7/10 | Necesita mas bookings |
| **702** | 3 (semanas 1, 6, 10) | 0 | 7/10 | Igual que 709 |

---

## Totales

| Concepto | Monto |
|----------|-------|
| Arriendo (40 noches) | $1,105,253 |
| Aseos (10 × $30,000) | $300,000 |
| **Gran Total** | **$1,405,253** |
| Promedio por noche | $27,631 |
| Promedio por semana | $140,525 |

---

## Calendario resumen por departamento

### 901
- Sem 1-2: Ocupado (otro huesped)
- **Sem 3**: CHECK-IN Lunes 6 Jul → CHECK-OUT Viernes 10 Jul
- Sem 4: Libre (Airbnb)
- **Sem 5**: CHECK-IN Lunes 20 Jul → CHECK-OUT Viernes 24 Jul
- Sem 6-9: Ocupado (otro huesped)
- Sem 10: Libre (Airbnb)

### 902
- Sem 1-6: Ocupado (otro huesped)
- **Sem 7**: CHECK-IN Lunes 3 Ago → CHECK-OUT Viernes 7 Ago
- Sem 8: Libre (Airbnb)
- **Sem 9**: CHECK-IN Lunes 17 Ago → CHECK-OUT Viernes 21 Ago
- Sem 10: Libre (Airbnb)

### 709
- Sem 1: Libre (Airbnb)
- **Sem 2**: CHECK-IN Lunes 29 Jun → CHECK-OUT Viernes 3 Jul
- Sem 3: Libre (Airbnb)
- **Sem 4**: CHECK-IN Lunes 13 Jul → CHECK-OUT Viernes 17 Jul
- Sem 5-7: Libre (Airbnb)
- **Sem 8**: CHECK-IN Lunes 10 Ago → CHECK-OUT Viernes 14 Ago
- Sem 9-10: Libre (Airbnb)

### 702
- **Sem 1**: CHECK-IN Lunes 22 Jun → CHECK-OUT Viernes 26 Jun
- Sem 2-5: Libre (Airbnb)
- **Sem 6**: CHECK-IN Lunes 27 Jul → CHECK-OUT Viernes 31 Jul
- Sem 7-9: Libre (Airbnb)
- **Sem 10**: CHECK-IN Lunes 24 Ago → CHECK-OUT Viernes 28 Ago

---

## Parametros

- **Precios**: Datos desde PriceLabs API (fetch del 18 Jun 2026)
- **Aseo**: $30,000 CLP por limpieza (confirmado en reservas anteriores)
- **Check-in**: Lunes 15:00
- **Check-out**: Viernes 11:00
- **Noches por semana**: 4 (lun, mar, mie, jue)
- **PMS**: Stays.net → sync automatico a Airbnb, Booking.com

## Notas operativas

1. **Bloqueo en Stays**: Al crear la reserva manual en Stays, automaticamente se sincroniza con Airbnb y Booking.com
2. **Aseo**: Programar 1 aseo semanal (viernes check-out o lunes pre check-in) para cada depto
3. **Coordinacion**: Si el huesped necesita early check-in o late check-out, solo si la unidad esta libre el dia anterior/posterior
4. **Misma tarifa para el huesped**: Aunque los costos internos varian por depto, se puede cotizar un precio fijo semanal al huesped
