> ⚠️ **LEGACY — Fuente primaria: `playbook_renta_corta.md`.** Consolidado el 2026-05-25.

# Playbook para Agentes de Renta Corta
## Optimización, operación y mejores prácticas

> Documento diseñado como base de conocimiento para agentes de IA, asistentes de WhatsApp, flujos de n8n, equipos de soporte, revenue management y operación de alojamientos de renta corta.

---

## 1. Propósito del playbook

Este documento resume las mejores prácticas para operar alojamientos de renta corta en plataformas como Airbnb, Booking y canales directos.

El objetivo es que un agente pueda:

-  Optimizar anuncios para aumentar conversión.
-  Responder preguntas de huéspedes con claridad y consistencia.
-  Apoyar decisiones de pricing.
-  Reducir errores operativos.
-  Mejorar reseñas.
-  Mantener coherencia entre anuncio, precio, fotos, reglas y experiencia real.

---

## 2. Principios centrales

### 2.1. El mercado manda, no el evento

No basta con subir precios porque existe un concierto, feria, feriado o evento.  
La decisión debe basarse en señales reales del mercado:

-  Competidores comparables ya reservados.
-  Disminución de disponibilidad en el sector.
-  Aumento de ocupación futura.
-  Cambios en precios promedio.
-  Comportamiento histórico de la zona.
-  Picos detectados por herramientas como PriceLabs.

**Regla para agentes:**  
Nunca recomendar subir precios solo porque existe un evento. Primero revisar demanda, ocupación, disponibilidad y competencia.

---

### 2.2. La conversión depende de cuatro pilares

Toda estrategia debe analizarse desde estos cuatro factores:

1. **Ocupación:** entender cómo se está comportando el mercado.
2. **Precio:** definir tarifa según valor real del alojamiento y competencia.
3. **Visibilidad:** reducir restricciones y crear ofertas atractivas.
4. **Conversión:** mejorar fotos, título, descripción, reglas y experiencia.

Si un alojamiento no reserva, el agente debe diagnosticar cuál de estos cuatro pilares está fallando.

---

### 2.3. Coherencia entre expectativa y realidad

La experiencia debe coincidir con lo prometido.

No se debe:

-  Editar fotos de forma exagerada.
-  Prometer lujo si el espacio es funcional.
-  Ocultar restricciones importantes.
-  Exagerar distancias.
-  Usar textos genéricos que no describan el alojamiento real.

Sí se debe:

-  Mostrar fotos reales y bien cuidadas.
-  Describir atributos concretos.
-  Explicar reglas con claridad.
-  Ser transparente sobre limitaciones.
-  Resaltar beneficios verificables.

---

## 3. Agente principal: reglas de comportamiento

El agente debe actuar como asesor operativo de renta corta.

### 3.1. Tono

-  Claro.
-  Profesional.
-  Directo.
-  Humano.
-  Sin exagerar.
-  Sin prometer algo que no está confirmado.

### 3.2. Prohibiciones

El agente no debe:

-  Inventar amenities.
-  Inventar disponibilidad.
-  Inventar distancias.
-  Inventar políticas.
-  Recomendar cancelar reservas sin advertir consecuencias.
-  Prometer reembolsos sin validación humana.
-  Entregar claves, códigos de acceso o datos sensibles sin verificación de reserva.
-  Ocultar reglas importantes para lograr una reserva.

### 3.3. Criterio general

Ante duda, el agente debe responder con una de estas fórmulas:

```text
No tengo ese dato confirmado. Puedo ayudarte con la información disponible y dejar este punto como pendiente de validación.
```

```text
Para evitar entregarte información incorrecta, este dato debe validarse con administración antes de confirmarlo.
```

---

## 4. Revenue management

Revenue management es la gestión estratégica de precios, disponibilidad y restricciones para maximizar ingresos.

### 4.1. Variables que debe revisar el agente

Para sugerir precios, el agente debe considerar:

-  Ocupación futura.
-  Ocupación histórica.
-  ADR: tarifa diaria promedio.
-  RevPAR: ingreso por noche disponible.
-  Competencia directa.
-  Temporada alta, media o baja.
-  Anticipación de reserva.
-  Huecos entre reservas.
-  Cantidad de reseñas.
-  Calidad del anuncio.
-  Restricciones activas.
-  Costos fijos.
-  Fee de limpieza.
-  Comisiones de plataforma.

---

## 5. Estrategia de precios por temporada

### 5.1. Temporada alta

Objetivo: ser de los últimos en reservarse.

Estrategia:

-  Proteger fechas con precios más altos.
-  No bajar demasiado temprano.
-  Ajustar progresivamente al acercarse la fecha.
-  Observar si la competencia se reserva antes.
-  Reducir precio solo si la ocupación esperada no se materializa.

Regla para agente:

```text
En temporada alta no se debe competir por precio desde el inicio. Primero se protege margen; luego se ajusta según ocupación y cercanía de la fecha.
```

---

### 5.2. Temporada baja

Objetivo: ser de los primeros en reservarse.

Estrategia:

-  Activar precios competitivos con anticipación.
-  Usar descuentos por duración.
-  Reducir restricciones.
-  Aumentar atractivo visual del anuncio.
-  Crear promociones controladas.
-  Monitorear conversión semanalmente.

Regla para agente:

```text
En temporada baja, la prioridad es asegurar ocupación temprana. Un calendario vacío cerca de la fecha requiere acción agresiva.
```

---

### 5.3. Entre semana

Estrategia:

-  Ser más agresivo en precio.
-  Usar descuentos de última hora.
-  Incentivar reservas de trabajo.
-  Destacar escritorio, Wi-Fi y ubicación.

---

### 5.4. Fines de semana

Estrategia:

-  Ser menos agresivo.
-  Proteger tarifa.
-  Evaluar mínimos de estadía solo si no perjudican visibilidad.
-  Usar narrativa de escapada, descanso o ubicación.

---

## 6. PriceLabs

PriceLabs puede apoyar la estrategia mediante:

-  Dynamic Pricing: precios dinámicos.
-  Market Dashboard: análisis de mercado.
-  Portfolio Analytics: análisis de portafolio.
-  Insights Dashboard: tendencias de ocupación, ADR y demanda.
-  Revenue Estimator: estimación de ingresos potenciales.

### 6.1. Precio base

El precio base no es el precio mínimo.

Debe representar el valor normal del alojamiento en condiciones promedio de mercado.

El agente debe evitar recomendar un precio base sin revisar:

-  Tipo de propiedad.
-  Calidad del alojamiento.
-  Ubicación.
-  Capacidad.
-  Amenities.
-  Franja de precios de competidores.
-  Nivel de ocupación.
-  Reseñas.
-  Estacionalidad.

---

### 6.2. Precio mínimo

El precio mínimo debe cubrir:

-  Costos operativos.
-  Limpieza.
-  Comisiones.
-  Desgaste.
-  Margen mínimo aceptable.

Regla:

```text
Nunca bajar bajo el costo operativo real salvo estrategia puntual, medida y justificada.
```

---

### 6.3. Precio máximo

No siempre es necesario definir un precio máximo.

Si se usa, debe ser realista y estar alineado con el mercado.

Regla:

```text
El precio máximo no debe ser fantasioso. Debe representar un precio alto, pero vendible en condiciones excepcionales.
```

---

### 6.4. Market Dashboard

Para crear o interpretar un dashboard de mercado:

-  Elegir dirección exacta.
-  Definir radio competitivo real.
-  Evitar radios demasiado grandes que mezclen barrios distintos.
-  Comparar solo propiedades similares.
-  Revisar ocupación futura.
-  Revisar tarifas promedio.
-  Revisar disponibilidad.
-  Revisar tendencias año contra año.

Regla:

```text
Un radio grande puede contaminar el análisis. Mejor comparar pocos alojamientos realmente similares que muchos alojamientos no comparables.
```

---

## 7. Lectura de datos de ocupación

### 7.1. Señales relevantes

El agente debe observar:

-  Ocupación actual del sector.
-  Ocupación del año pasado a la misma fecha.
-  Cómo terminó realmente el año pasado.
-  Diferencia entre reservas actuales y comportamiento histórico.
-  Picos de demanda.
-  Valles de demanda.
-  Entrada de nueva competencia.

### 7.2. Interpretación

Si la ocupación actual se comporta parecido al año pasado, se puede usar el cierre del año anterior como referencia.

Si la ocupación actual se comporta diferente, no se debe asumir que el resultado final será igual al año anterior.

---

## 8. Restricciones y visibilidad

### 8.1. Regla general

Mientras más restricciones tenga un anuncio, menor puede ser su visibilidad.

Restricciones típicas:

-  Mínimo de noches.
-  Política de cancelación estricta.
-  Cobros adicionales poco competitivos.
-  Reglas poco claras.
-  Ventana de disponibilidad corta.
-  Falta de disponibilidad futura.
-  Requisitos excesivos para reservar.

---

### 8.2. Mínimo de noches

En vez de bloquear reservas de una noche, se recomienda aceptar una noche con precio más alto y aplicar descuentos por duración.

Ejemplo de rule set:

| Duración | Descuento sugerido |
|---|---:|
| 1 noche | 0% |
| 2 noches | 20% |
| 3 noches | 25% |
| 4+ noches | 30% |

Regla:

```text
No bloquear una noche si se puede resolver con precio. La restricción reduce visibilidad; el precio controla rentabilidad.
```

---

### 8.3. Huecos entre reservas

No todas las noches vacías tienen la misma probabilidad de reservarse.

Entre dos reservas:

-  La noche inmediatamente posterior al checkout tiene menor visibilidad.
-  Las noches intermedias tienen mayor visibilidad.
-  La noche antes del próximo check-in tiene menor visibilidad.

Estrategias:

-  Ofrecer early check-in pagado.
-  Ofrecer late checkout pagado.
-  Vender noche intermedia con descuento.
-  Ajustar precio según probabilidad real de conversión.

---

## 9. Estrategia para anuncios nuevos

Las plataformas necesitan datos para entender un anuncio.

Durante los primeros meses, el objetivo principal debe ser:

-  Conseguir reservas.
-  Conseguir reseñas positivas.
-  Mejorar conversión.
-  Validar fotos, título y descripción.
-  Construir reputación.

Regla:

```text
En un anuncio nuevo, no maximizar precio demasiado temprano. Primero generar data, reseñas y señales positivas para el algoritmo.
```

---

## 10. Cuándo subir precios

Subir precios cuando:

-  Hay reseñas positivas consistentes.
-  La ocupación es saludable.
-  La conversión se mantiene.
-  El mercado muestra mayor demanda.
-  La competencia comparable ya está reservada.
-  El anuncio tiene fotos y descripción optimizadas.
-  Hay temporada alta próxima.

No subir precios si:

-  El anuncio aún no convierte.
-  Hay pocas reseñas.
-  Las fotos son débiles.
-  La descripción es genérica.
-  Hay exceso de disponibilidad en el mercado.
-  La ocupación futura está baja.

---

## 11. Revivir anuncios muertos

Un anuncio muerto es aquel que dejó de recibir reservas o perdió visibilidad.

### 11.1. Diagnóstico

Revisar:

-  Fotos.
-  Título.
-  Precio.
-  Descripción.
-  Reglas.
-  Reseñas recientes.
-  Restricciones.
-  Calendario.
-  Disponibilidad futura.
-  Competencia nueva.
-  Posición relativa en precio.

### 11.2. Estrategia de choque

Durante 30 días:

-  Mejorar fotos.
-  Reescribir título.
-  Reestructurar descripción.
-  Ajustar precio agresivamente.
-  Reducir restricciones.
-  Activar descuentos por duración.
-  Monitorear vistas, clics y reservas.
-  Buscar nuevas reseñas positivas.

Regla:

```text
Un anuncio con mala data necesita señales nuevas: mejor oferta, mejor portada, mejor descripción y actividad reciente.
```

---

## 12. Reservas largas y estrategia post-reserva

Cuando termina una reserva larga, el calendario puede quedar débil.

Estrategia:

-  Bajar precios agresivamente en noches próximas.
-  Incentivar reservas cortas para recuperar ocupación.
-  Evitar calendario vacío prolongado.
-  Volver gradualmente al precio normal cuando entren reservas.

Regla:

```text
Después de una reserva larga, la prioridad es reactivar ocupación. La ocupación genera más ocupación.
```

---

## 13. Alquileres mensuales

Para estadías de 28 noches o más:

-  Aplicar descuentos significativos.
-  Considerar menor rotación.
-  Considerar menos costos de limpieza.
-  Considerar huésped distinto: trabajador temporal, nómada digital, estudiante, relocalización.
-  Ajustar reglas de consumo, limpieza y mantenimiento.

Descuento orientativo:

-  28+ noches: 30% a 50%, según mercado y margen.

---

## 14. Booking.com

Booking debe tratarse distinto a Airbnb.

### 14.1. Elementos relevantes

-  Planes tarifarios flexibles, moderados o estrictos.
-  Tarifa reembolsable.
-  Tarifa no reembolsable.
-  Genius.
-  Descuentos móviles.
-  Promociones por país.
-  Ofertas relámpago.
-  Early bird.
-  Last minute.

### 14.2. Regla para agentes

```text
No aplicar descuentos acumulados sin revisar margen. En Booking, varias promociones pueden combinarse y erosionar rentabilidad.
```

---

## 15. PMS y automatización

PMS significa Property Management System.

Sirve para centralizar:

-  Calendario.
-  Tarifas.
-  Reservas.
-  Canales.
-  Mensajería.
-  Automatizaciones.
-  API.
-  Reportes.

### 15.1. Riesgos del PMS

El agente debe verificar si el PMS:

-  Sobrescribe precios.
-  Borra rule sets.
-  Modifica mínimos de estadía.
-  Cambia disponibilidad.
-  Bloquea configuraciones nativas de Airbnb.
-  Limita promociones.
-  Permite API.
-  Permite sincronización correcta con PriceLabs.

Regla:

```text
Si el PMS borra reglas importantes de Airbnb, la estrategia debe moverse al PMS, a PriceLabs o evaluarse cambio de herramienta.
```

---

## 16. Fee de limpieza

Recomendación general:

-  Mantener fee de limpieza separado del precio noche.
-  No incluir limpieza dentro de la tarifa base si se usan descuentos.
-  Evitar dar descuento indirecto sobre limpieza.
-  Cobrar limpieza cercana al costo real.

Regla:

```text
El descuento debe afectar la noche, no necesariamente el costo de limpieza.
```

---

## 17. Política de cancelación

Políticas más flexibles pueden mejorar visibilidad y conversión.

El agente debe equilibrar:

-  Riesgo de cancelación.
-  Temporada.
-  Demanda.
-  Margen.
-  Nivel de ocupación.
-  Posicionamiento del anuncio.

Regla:

```text
Mientras más estricta la política, menor atractivo puede tener el anuncio. Usar flexibilidad cuando se necesita visibilidad.
```

---

## 18. Optimización del anuncio

### 18.1. Título

El título debe incluir:

-  Ubicación o microzona.
-  Atributo fuerte.
-  Beneficio principal.
-  Diferenciador competitivo.

Ejemplos de atributos:

-  Cama king.
-  Terraza.
-  Wi-Fi rápido.
-  Escritorio.
-  Aire acondicionado.
-  Cerca del metro.
-  Vista.
-  Piscina.
-  Estacionamiento, si aplica.
-  Ideal trabajo.
-  Ideal pareja.

Estructura sugerida:

```text
[Tipo de alojamiento] + [atributo fuerte] + [ubicación]
```

Ejemplos:

```text
Estudio con terraza y cama king cerca del metro
```

```text
Studio work-friendly con Wi-Fi rápido y terraza
```

```text
Moderno estudio con king, A/C y excelente ubicación
```

---

### 18.2. Descripción

Estructura recomendada:

1. Primer párrafo emocional y concreto.
2. Lo que encontrará el huésped.
3. Datos del edificio.
4. Ubicación y entorno.
5. Reglas importantes.
6. Preguntas frecuentes.
7. CTA de reserva.

Plantilla:

```text
Disfruta una estadía cómoda en [CIUDAD/ZONA], en un [TIPO DE ALOJAMIENTO] pensado para [TIPO DE HUÉSPED]. El espacio cuenta con [ATRIBUTOS PRINCIPALES] y está ubicado cerca de [REFERENCIAS REALES].

Lo que encontrarás:
-  [Amenity 1]
-  [Amenity 2]
-  [Amenity 3]
-  [Amenity 4]
-  [Amenity 5]

Ideal para:
-  Viajes de trabajo.
-  Parejas.
-  Estadías cortas.
-  Visitas por trámites.
-  Turismo urbano.

Importante:
-  [Regla 1]
-  [Regla 2]
-  [Regla 3]

Reserva con confianza. El alojamiento es tal como se muestra en las fotos.
```

---

## 19. Fotos que convierten

### 19.1. Regla principal

Las primeras fotos deciden si el huésped sigue mirando o abandona el anuncio.

Prioridad:

1. Foto portada.
2. Primeras 5 fotos.
3. Primeras 10 fotos.

La portada debe vender la promesa principal.

---

### 19.2. Checklist antes de fotografiar

-  Cama perfectamente tendida.
-  Sin arrugas visibles.
-  Almohadas alineadas.
-  Cortinas abiertas.
-  Luz natural.
-  Luces encendidas si aportan calidez.
-  Televisor con imagen relajante si aparece.
-  Cables ocultos.
-  Superficies limpias.
-  Baño impecable.
-  Cocina ordenada.
-  Terraza despejada.
-  Sin objetos personales.
-  Sin exceso de decoración.
-  Sin distorsión exagerada.

---

### 19.3. Técnica con celular

Si no hay fotógrafo profesional:

-  Usar cámara horizontal.
-  Tomar fotos a altura media.
-  Mantener líneas rectas.
-  Usar gran angular con moderación.
-  Evitar deformar muebles o paredes.
-  Enfocar manualmente tocando el punto principal.
-  Revisar que la foto esté nítida.
-  Evitar filtros artificiales.

---

### 19.4. Fotos mínimas recomendadas

-  Portada hero.
-  Cama.
-  Vista general del espacio.
-  Terraza o balcón.
-  Escritorio o zona de trabajo.
-  Cocina.
-  Baño.
-  TV / zona de descanso.
-  Amenity diferenciador.
-  Vista.
-  Fachada o acceso.
-  Espacios comunes, si aplican.
-  Experiencia: café, desayuno, libro, copa o detalle sutil.

---

### 19.5. Errores que reducen conversión

-  Fotos oscuras.
-  Cama arrugada.
-  Ángulos torcidos.
-  Baño mal iluminado.
-  Exceso de objetos.
-  Fotos con filtros intensos.
-  Fotos que prometen más de lo real.
-  No mostrar baño.
-  No mostrar cocina.
-  No mostrar acceso o edificio si aporta confianza.
-  Usar la peor foto como portada.

---

## 20. Branding del alojamiento

Una marca de hospedaje transmite confianza.

### 20.1. Elementos mínimos

-  Nombre del alojamiento.
-  Paleta de colores.
-  Tipografías.
-  Logo simple.
-  Estilo fotográfico.
-  Tono de comunicación.
-  Plantillas de mensajes.
-  Guía visual para publicaciones.
-  Manual breve de identidad.

---

### 20.2. Estilos posibles

| Estilo | Sensación | Ideal para |
|---|---|---|
| Natural y acogedor | Calma, refugio | Cabañas, naturaleza |
| Moderno y minimalista | Orden, limpieza | Estudios, lofts urbanos |
| Vibrante | Energía | Playa, hostels, grupos |
| Clásico elegante | Sofisticación | Suites, lujo |

---

### 20.3. Regla de coherencia

```text
El estilo visual del anuncio debe coincidir con el espacio real y con el tono de los mensajes.
```

---

## 21. Psicología del huésped

El huésped decide emocionalmente y justifica racionalmente.

### 21.1. Tres necesidades psicológicas

1. **Seguridad:** quiero confiar.
2. **Confort emocional:** siento que me cuidan.
3. **Pertenencia:** soy bienvenido.

---

### 21.2. Primera impresión

El huésped juzga en segundos.

Activadores positivos:

-  Foto clara.
-  Título concreto.
-  Respuesta rápida.
-  Limpieza visible.
-  Aroma agradable.
-  Mensaje amable.
-  Reglas simples.
-  Coherencia entre fotos y realidad.

---

### 21.3. Coherencia

La confianza aumenta cuando:

-  Fotos coinciden con el alojamiento.
-  Mensajes coinciden con el tono de marca.
-  Reglas son claras.
-  El check-in es simple.
-  El huésped sabe qué esperar.

La confianza disminuye cuando:

-  Fotos parecen artificiales.
-  El texto promete demasiado.
-  Las reglas aparecen tarde.
-  El huésped descubre limitaciones al llegar.
-  La comunicación es fría o lenta.

---

## 22. Jornada emocional del huésped

### 22.1. Fase 1: búsqueda

Objetivo: captar atención.

Acciones:

-  Foto portada fuerte.
-  Título concreto.
-  Precio competitivo.
-  Reseñas visibles.
-  Descripción clara.

---

### 22.2. Fase 2: primer contacto

Objetivo: generar confianza.

Acciones:

-  Responder rápido.
-  Usar nombre del huésped.
-  Confirmar fechas.
-  Aclarar dudas.
-  Mantener tono amable y directo.

---

### 22.3. Fase 3: check-in

Objetivo: reducir ansiedad.

Acciones:

-  Enviar instrucciones claras.
-  Confirmar horario.
-  Explicar acceso.
-  Entregar contacto de soporte.
-  Mantener mensaje simple.

---

### 22.4. Fase 4: estadía

Objetivo: anticipar problemas.

Acciones:

-  Mensaje de seguimiento.
-  Respuesta rápida.
-  Solución con plazos.
-  Registro de incidentes.
-  Escalamiento si corresponde.

---

### 22.5. Fase 5: check-out

Objetivo: cerrar bien y pedir reseña.

Acciones:

-  Recordar horario.
-  Agradecer.
-  Pedir evaluación de forma suave.
-  Revisar daños.
-  Guardar evidencia fotográfica.

---

## 23. Mensajería para agentes

### 23.1. Variables estándar

Usar estas variables en automatizaciones:

```text
[NOMBRE]
[FECHA_CHECKIN]
[HORA_CHECKIN]
[FECHA_CHECKOUT]
[HORA_CHECKOUT]
[DIRECCION]
[UNIDAD]
[LINK_GUIA]
[CODIGO_ACCESO]
[WIFI]
[CONTACTO_SOPORTE]
[REGLAS]
[IDIOMA]
```

---

### 23.2. Primer contacto

```text
Hola, [NOMBRE]. Gracias por escribirnos.

Para ayudarte mejor, ¿me confirmas las fechas exactas de tu viaje y cuántas personas se hospedarían?

Con eso reviso disponibilidad y te oriento con la mejor opción.
```

---

### 23.3. Confirmación de interés

```text
Sí, el alojamiento está preparado para una estadía cómoda y práctica.

Encontrarás un espacio limpio, bien ubicado y equipado con lo necesario para descansar o trabajar. Las fotos muestran el alojamiento real, sin edición exagerada.

Quedo atento si quieres avanzar con la reserva.
```

---

### 23.4. Mensaje de cierre

```text
Para esas fechas suele haber buena demanda, por lo que recomiendo reservar cuando tengas claridad del viaje.

Así aseguras disponibilidad y dejamos todo preparado para tu llegada.
```

---

### 23.5. Check-in

```text
Hola, [NOMBRE].

Tu check-in está disponible desde las [HORA_CHECKIN] del [FECHA_CHECKIN].

Dirección:
[DIRECCION]

Unidad:
[UNIDAD]

Instrucciones de acceso:
[INSTRUCCIONES]

Contacto de soporte:
[CONTACTO_SOPORTE]

Cualquier duda durante tu llegada, escríbenos por este mismo canal.
```

---

### 23.6. Bienvenida

```text
Hola, [NOMBRE].

Bienvenido/a a [NOMBRE_ALOJAMIENTO]. El espacio fue preparado para que tengas una estadía cómoda y tranquila.

Te dejamos la guía del alojamiento aquí:
[LINK_GUIA]

Cualquier cosa que necesites, puedes escribirnos.
```

---

### 23.7. Seguimiento durante la estadía

```text
Hola, [NOMBRE]. Espero que todo vaya bien con tu estadía.

Te escribo solo para confirmar que hayas encontrado todo en orden. Si necesitas algo, avísanos por este canal.
```

---

### 23.8. Recordatorio de check-out

```text
Hola, [NOMBRE].

Te recuerdo que el check-out es hasta las [HORA_CHECKOUT] del [FECHA_CHECKOUT].

Antes de salir, por favor revisa que no olvides pertenencias personales y deja la puerta correctamente cerrada.

Gracias por hospedarte con nosotros.
```

---

### 23.9. Solicitud de reseña

```text
Hola, [NOMBRE].

Gracias por elegirnos para tu estadía. Esperamos que hayas tenido una buena experiencia.

Si puedes dejarnos una evaluación en la plataforma, nos ayudas mucho a seguir mejorando y a que otros huéspedes reserven con confianza.

Será un gusto recibirte nuevamente.
```

---

## 24. Playbook de crisis

### 24.1. Principio general

Primero se calma la emoción. Luego se resuelve el problema.

El huésped necesita:

-  Sentirse escuchado.
-  Saber que alguien está actuando.
-  Tener un plazo.
-  Recibir una solución concreta.

---

### 24.2. Script universal

```text
Hola, [NOMBRE]. Entiendo la molestia y lamento el inconveniente.

Ya estoy revisando esto para resolverlo. Te actualizaré en [TIEMPO_ESTIMADO].

Gracias por avisarnos. Queremos que tu experiencia siga siendo lo más cómoda posible.
```

---

### 24.3. Problema de limpieza

```text
Hola, [NOMBRE]. Lamento mucho lo que comentas.

La limpieza es prioritaria para nosotros. Ya estoy coordinando una revisión/solución y te confirmaré en [TIEMPO].

Gracias por avisarnos de inmediato.
```

---

### 24.4. Problema de ruido

```text
Hola, [NOMBRE]. Entiendo la molestia.

Ya estoy revisando la situación y, si corresponde, lo escalaremos con administración/conserjería.

Te mantengo informado/a.
```

---

### 24.5. Falla de Wi-Fi

```text
Hola, [NOMBRE]. Gracias por avisar.

Vamos a revisar la conexión. Por favor confirma si el problema ocurre en todos tus dispositivos o solo en uno.

Mientras tanto, verificaremos el estado del servicio y te actualizaremos en [TIEMPO].
```

---

### 24.6. Falta de ítem

```text
Hola, [NOMBRE]. Gracias por avisar.

Ya estamos revisando la disponibilidad de [ITEM] para ayudarte. Te confirmo en [TIEMPO] cómo lo resolveremos.
```

---

### 24.7. Solicitud de reembolso

```text
Hola, [NOMBRE]. Entiendo tu punto.

Vamos a revisar lo ocurrido, la evidencia disponible y la política de la reserva para darte una respuesta justa.

Te actualizo en [TIEMPO].
```

---

## 25. Reglas de la casa

Las reglas deben estar explícitas en el anuncio, mensajes y guía del huésped.

### 25.1. Reglas mínimas

-  No fumar dentro del alojamiento.
-  No fiestas ni eventos.
-  No ruido después del horario definido.
-  No exceder número de huéspedes declarados.
-  No mascotas, si aplica.
-  No turismo sexual ni actividades ilegales.
-  Respetar check-in y check-out.
-  Cuidar mobiliario, ropa de cama y artefactos.
-  Reportar daños o incidentes.
-  Cumplir normas del edificio.

---

### 25.2. Regla sobre fumar

```text
Está prohibido fumar dentro del alojamiento. Si se detecta olor a cigarro, cenizas, colillas o evidencia de humo dentro del espacio, se podrá aplicar un cargo adicional de limpieza/desodorización según el costo real del servicio.
```

---

### 25.3. Regla sobre fiestas

```text
No se permiten fiestas, eventos ni reuniones que alteren la tranquilidad del edificio o de los vecinos.
```

---

### 25.4. Regla sobre huéspedes adicionales

```text
Solo pueden ingresar las personas declaradas en la reserva. Cualquier huésped adicional debe ser informado y aprobado previamente.
```

---

### 25.5. Regla sobre ruido

```text
Se debe mantener volumen moderado durante toda la estadía y respetar el horario de silencio definido por el edificio.
```

---

## 26. Evidencia y reclamaciones

Para reclamar daños o incumplimiento de reglas, el equipo debe guardar evidencia.

### 26.1. Evidencia mínima

-  Fotos con fecha.
-  Fotos con hora.
-  Fotos con ubicación.
-  Video si corresponde.
-  Descripción del daño.
-  Presupuesto o boleta del servicio.
-  Regla incumplida.
-  Comunicación con huésped.
-  Registro del equipo de limpieza.

### 26.2. Proceso

1. Equipo detecta incidente.
2. Toma evidencia.
3. Reporta al administrador.
4. Se contacta al huésped de forma profesional.
5. Se genera solicitud en la plataforma.
6. Si el huésped rechaza, se escala con intermediación.
7. Se guarda todo en carpeta de la reserva.

---

## 27. Limpieza y operación

### 27.1. Limpieza post check-out

Checklist:

-  Cambiar sábanas.
-  Cambiar fundas.
-  Cambiar toallas.
-  Revisar manchas.
-  Aspirar.
-  Trapear.
-  Limpiar baño.
-  Revisar ducha.
-  Reponer papel higiénico.
-  Reponer jabón.
-  Limpiar cocina.
-  Revisar refrigerador.
-  Revisar microondas.
-  Revisar vajilla.
-  Retirar basura.
-  Ventilar.
-  Revisar olores.
-  Tomar fotos finales.

---

### 27.2. Pre-check-in

Checklist:

-  Cama impecable.
-  Toallas visibles.
-  Baño limpio.
-  Cocina limpia.
-  Iluminación funcionando.
-  Wi-Fi funcionando.
-  TV funcionando.
-  A/C funcionando.
-  Cerradura funcionando.
-  Aroma neutro.
-  Mensaje de bienvenida enviado.
-  Guía disponible.
-  Código de acceso validado.

---

### 27.3. Mantenimiento periódico

Cada 15 días:

-  Revisar luces.
-  Revisar enchufes.
-  Revisar A/C.
-  Revisar TV.
-  Revisar controles.
-  Revisar fugas.
-  Revisar presión de agua.
-  Revisar cerraduras.
-  Revisar ventanas.
-  Revisar muebles.
-  Revisar manchas o humedad.

Cada 3 meses:

-  Revisar pintura.
-  Revisar sellos.
-  Revisar artefactos.
-  Revisar inventario.
-  Revisar calidad de ropa blanca.
-  Revisar fotos del anuncio.
-  Revisar descripción y reglas.

---

## 28. Métricas de gestión

El agente debe monitorear:

-  Ocupación.
-  ADR.
-  RevPAR.
-  Ingreso bruto.
-  Ingreso neto.
-  Comisiones.
-  Costos fijos.
-  Costo de limpieza.
-  Ticket promedio.
-  Número de reservas.
-  Duración promedio de estadía.
-  Ventana de reserva.
-  Tasa de conversión.
-  Vistas.
-  Clics.
-  Reservas.
-  Reseñas.
-  Calificación promedio.
-  Incidentes.
-  Reclamos.
-  Reembolsos.

---

## 29. Interpretación de métricas

### 29.1. Alta ocupación + baja ganancia

Diagnóstico probable:

-  Precio demasiado bajo.
-  Costos altos.
-  Fee de limpieza mal configurado.
-  Descuentos excesivos.

Acción:

-  Revisar precio base.
-  Revisar descuentos.
-  Revisar costos.
-  Subir tarifas en fechas fuertes.

---

### 29.2. Baja ocupación + buena ganancia por reserva

Diagnóstico probable:

-  Precio alto.
-  Baja visibilidad.
-  Restricciones.
-  Fotos débiles.
-  Mala descripción.

Acción:

-  Mejorar portada.
-  Revisar precio.
-  Reducir restricciones.
-  Activar promociones puntuales.

---

### 29.3. Muchas vistas + pocas reservas

Diagnóstico probable:

-  Precio no convence.
-  Fotos generan interés pero texto no cierra.
-  Reglas generan fricción.
-  Reseñas insuficientes.

Acción:

-  Optimizar descripción.
-  Revisar precio final con fees.
-  Mejorar primeras 5 fotos.
-  Revisar política de cancelación.

---

### 29.4. Pocas vistas

Diagnóstico probable:

-  Mala portada.
-  Título débil.
-  Baja visibilidad por restricciones.
-  Mala disponibilidad.
-  Precio fuera de mercado.

Acción:

-  Cambiar portada.
-  Reescribir título.
-  Ampliar disponibilidad.
-  Revisar mínimo de noches.
-  Revisar ranking de precio.

---

## 30. Prioridades de implementación

### Urgente

-  Mejorar fotos.
-  Reescribir títulos.
-  Endurecer reglas críticas.
-  Revisar configuración de PMS.
-  Revisar mínimo de noches.
-  Separar fee de limpieza.
-  Validar precio base.

### Alta

-  Crear rule sets.
-  Ampliar ventana de disponibilidad.
-  Crear mensajes automáticos.
-  Configurar evidencias de checkout.
-  Crear guía del huésped.

### Media

-  Revisar política de cancelación.
-  Crear branding.
-  Crear plantillas para redes.
-  Revisar performance semanal.

### Baja

-  Mejorar diseño de manuales.
-  Crear kit de bienvenida.
-  Automatizar reportes.
-  Comparar propiedades.

---

## 31. Flujo recomendado para agente de optimización de anuncios

```text
1. Revisar tipo de alojamiento.
2. Revisar ubicación.
3. Revisar huéspedes objetivo.
4. Revisar fotos.
5. Revisar título.
6. Revisar descripción.
7. Revisar reglas.
8. Revisar amenities.
9. Revisar precio base.
10. Revisar mínimos de estadía.
11. Revisar política de cancelación.
12. Revisar competencia.
13. Proponer mejoras priorizadas.
14. Generar nuevo copy.
15. Generar checklist visual.
```

---

## 32. Prompt para agente de optimización de anuncio

```text
Actúa como experto en renta corta, marketing de alojamientos, revenue management y experiencia del huésped.

Analiza este anuncio usando los siguientes criterios:
1. Portada y primeras 5 fotos.
2. Título.
3. Primeras 2 líneas de descripción.
4. Claridad de amenities.
5. Reglas de la casa.
6. Ubicación.
7. Público objetivo.
8. Precio y restricciones.
9. Coherencia entre promesa y realidad.
10. Riesgos de baja conversión.

Devuelve:
- Diagnóstico.
- Prioridades urgentes.
- Nuevo título.
- Nueva descripción.
- Reglas sugeridas.
- Checklist de fotos.
- Riesgos operativos.
- Acciones para próximos 7 días.
```

---

## 33. Prompt para agente de pricing

```text
Actúa como revenue manager de renta corta.

Con la información disponible, analiza la estrategia de precios considerando:
- Ocupación actual.
- Ocupación futura.
- ADR.
- RevPAR.
- Competencia.
- Temporada.
- Eventos.
- Ventana de reserva.
- Mínimo de noches.
- Descuentos.
- Fee de limpieza.
- Política de cancelación.
- Reseñas.
- Calidad del anuncio.

No recomiendes subir precios solo por eventos. Primero valida señales del mercado.

Devuelve:
- Diagnóstico.
- Riesgos.
- Precio base recomendado.
- Precio mínimo recomendado.
- Estrategia entre semana.
- Estrategia fin de semana.
- Estrategia temporada alta.
- Estrategia temporada baja.
- Acciones inmediatas.
```

---

## 34. Prompt para agente de soporte al huésped

```text
Actúa como agente de soporte de un alojamiento de renta corta.

Reglas:
- Responde con tono amable, claro y directo.
- No entregues claves, códigos ni datos sensibles sin reserva verificada.
- No prometas reembolsos.
- No inventes información.
- Si falta un dato, indica que debe validarse.
- Si hay un problema, primero reconoce la molestia y luego entrega próximos pasos.

Mensaje del huésped:
[MENSAJE]

Contexto de la reserva:
[CONTEXTO]

Devuelve una respuesta lista para enviar.
```

---

## 35. Prompt para agente de crisis

```text
Actúa como agente de crisis para renta corta.

Objetivo:
- Calmar al huésped.
- Reconocer la molestia.
- Mostrar control.
- Dar plazo.
- Evitar culpar al huésped.
- Evitar prometer compensaciones sin autorización.

Problema:
[PROBLEMA]

Contexto:
[CONTEXTO]

Devuelve:
1. Respuesta inmediata para el huésped.
2. Acción operativa interna.
3. Evidencia que debe recopilarse.
4. Cuándo escalar a humano.
```

---

## 36. Criterios de escalamiento a humano

El agente debe escalar cuando:

-  Hay solicitud de reembolso.
-  Hay daño material.
-  Hay huésped agresivo.
-  Hay posible actividad ilegal.
-  Hay que entregar códigos de acceso sin verificación.
-  Hay falla grave de agua, luz, cerradura o seguridad.
-  Hay accidente.
-  Hay reclamo formal.
-  Hay conflicto con vecinos.
-  Hay incumplimiento grave de reglas.
-  Hay overbooking.
-  Hay error de precio significativo.
-  Hay amenaza de mala reseña.

---

## 37. Resumen ejecutivo para agentes

La renta corta funciona cuando precio, anuncio, experiencia y operación están alineados.

Reglas finales:

-  El mercado manda.
-  Las fotos venden primero.
-  El título debe decir por qué reservar.
-  La descripción debe cerrar confianza.
-  Las reglas deben proteger la operación.
-  Menos restricciones suele significar más visibilidad.
-  El precio debe ser dinámico.
-  La limpieza es el KPI operativo más importante.
-  La respuesta rápida reduce ansiedad.
-  La coherencia evita malas reseñas.
-  La evidencia protege al anfitrión.
-  La experiencia completa empieza antes del check-in y termina después del check-out.