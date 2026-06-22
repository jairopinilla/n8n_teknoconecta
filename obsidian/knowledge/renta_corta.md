# Renta Corta — Cheat-sheet de recomendaciones (Chitara)

> Resumen accionable para responder rapido. Fuente completa: `documentacion/playbook_renta_corta.md`.
> Asesorias procesadas: `documentacion/insights_airbnb_2026-06-22.md`.
> Si la consulta es compleja, lee el playbook completo antes de responder.

## Tesis central
La renta corta es un negocio vivo. La rentabilidad aparece cuando se alinean: mercado, precio, visibilidad, fotos, configuracion, resenas, experiencia y seguimiento. El error comun es resolver todo bajando precio. Bajar precio puede ser correcto, pero solo en el momento, duracion y contexto adecuados.

## Formato de respuesta
Diagnostico probable -> causa -> prioridad -> acciones inmediatas -> que NO hacer -> senal de que funciono.

## Los 4 pilares (si no reserva, diagnosticar cual falla)
1. Ocupacion (como se comporta el mercado)
2. Precio (segun valor real y competencia)
3. Visibilidad (menos restricciones, ofertas atractivas)
4. Conversion (fotos, titulo, descripcion, reglas, experiencia)

## Glosario minimo
- ADR: precio promedio diario que se intenta cobrar (intencion de precio).
- RevPAR: ingresos del mes / dias del mes. Comparar contra costo fijo diario.
- Ventana de reserva: anticipacion con que reserva el mercado. Si es 7 dias y no tienes reservas en ese rango -> alerta.
- Noches huerfanas: noches sueltas entre dos reservas; tratarlas con tarifa/descuento especifico.
- Evento unicornio: demanda extraordinaria que puede permitir cobrar multiplos del precio normal.

## Marco de diagnostico (antes de actuar)
Disponibilidad real -> visible -> recibe visitas -> recibe clics -> convierte -> precio vs competencia directa -> fotos competitivas -> resenas recientes -> restricciones -> temporada (alta/baja/evento) -> la ventana exige accion inmediata o permite esperar -> el problema es Airbnb/Booking/PriceLabs/PMS o configuracion propia.

## Casos clave
- **Sin reservas proximos 7 dias:** comparar ocupacion propia vs mercado. Si estas por debajo: promo de ultimo minuto 10-15% (respetando minimo viable), revisar minimo de noches, noches huerfanas, precio sobre competencia, fotos/titulo. Verificar que PriceLabs sincronice y el minimo no bloquee.
- **Sin reservas proximos 30 dias:** si el mercado tambien esta lento, es temporada baja; si el mercado se ocupa y tu no, es oferta/precio/visibilidad/calidad. Crear descuentos en la duracion que el mercado reserva (3-4 noches), no solo semanal.
- **Anuncio en rojo vs mercado:** 7 dias = urgente; 30 = estrategia con poca espera; 60 = prevenir antes de la urgencia.
- **Tengo visitas pero no reservas:** problema de conversion. Revisar precio final (con fees), primeras 5 fotos, titulo, resenas, restricciones.
- **Anuncio que se enfrio:** revisar posicionamiento, resenas, calendario, precio, fotos. Optimizar y esperar 10-15 dias. Si lleva meses con data intoxicada, considerar recrearlo.
- **Reservas de ultima hora:** posible ADR muy alto; identificar el precio donde si convierte y no esperar al ultimo dia.
- **Reservas pero poca rentabilidad:** mirar RevPAR vs costo fijo; subir precio por escalones; revisar descuentos acumulados.

## Pricing por temporada
- **Alta:** ser de los ultimos en reservarse. Proteger precio, no bajar temprano, ajustar al acercarse la fecha. Si el mercado supera 80-95% de ocupacion, cobrar muy por encima del promedio. La tarifa es montana, no linea plana (viernes/sabado mas altos).
- **Baja:** ser de los primeros en reservarse. Programar descuentos ANTES de entrar al mes bajo. No esperar a estar vacio.
- **Entre semana:** mas agresivo, descuentos de ultima hora, destacar escritorio/Wi-Fi/ubicacion.
- **Fin de semana:** menos agresivo, proteger tarifa.

## Noches huerfanas
Bajarlas fuerte esta bien (ej. de 100 a 60 USD); al cierre de mes suman. No bloquear una noche si se resuelve con precio.

## Subir precio sin matar conversion (escalones)
Encontrar precio que convierte -> conseguir reservas -> subir un escalon pequeno -> esperar -> si no convierte, volver al anterior. El precio se calibra con el mercado, no con orgullo.

## Fotos, titulo, descripcion
- **Fotos:** todas horizontales (Airbnb recorta las verticales). Tecnica: altura del ombligo, angulo 0.5, lineas rectas, luz, TV con imagen icononica, cama tendida. Primeras 5 fotos resumen la propuesta de valor; cada unidad con su ADN.
- **Titulo (max 50 car):** tipo + atributo fuerte + ubicacion. Ej: "Estudio con terraza y cama king en Santiago Centro".
- **Descripcion:** estructurar con emojis, solo en el idioma base (Airbnb traduce). Coherencia con la realidad.

## Resenas / huesped problematico
Con huespedes fastidiosos: proteger la resena dando beneficios (sabanas, aseo gratis) aunque cueste; suele ser mas barato que una mala resena. Llamar a soporte en modo informativo para dejar precedente. Anuncio con calificacion <=4.6: el algoritmo castiga; considerar recrearlo. Las resenas se pueden apelar.

## Que NO hacer
Bajar precio sin mirar mercado; esperar a estar vacio; descontar en duraciones que el mercado no reserva; fotos oscuras o repetidas; abrir anuncio incompleto; confiar 100% en PriceLabs; ignorar el precio final del huesped; acumular promociones sin control; subir precios solo por un evento sin validar demanda.

## Regla de oro
La mejor sugerencia no es "baja el precio". Primero diagnostica si el problema es mercado, visibilidad, conversion, precio, configuracion, calidad o plataforma; luego toca la variable correcta con un cambio medible.
