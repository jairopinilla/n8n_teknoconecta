INSERT INTO egreso (
  usuarioid,
  categoriaegresoid,
  subcategoriaegresoid,
  controlabilidadid,
  recurrenciaid,
  canalid,
  bancoid,
  divisaid,
  bandejacorreoid,
  contraparteconocidaid,
  egresocontraparte,
  egresoesinformadoporbanco,
  egresocuenta,
  egresotarjeta,
  egresotarjetaproveedor,
  egresomontooriginal,
  egresofechamovimiento,
  egresodescripcion,
  egresoescuotas,
  egresonumerocuotaactual,
  egresototalcuotas,
  egresoescargoautomatico
)
SELECT
  u.usuarioid,
  ce.categoriaegresoid,
  se.subcategoriaegresoid,
  co.controlabilidadid,
  re.recurrenciaid,
  ca.canalid,
  ba.bancoid,
  di.divisaid,
  $1,   -- bandejaCorreoId
  $2,   -- contraparteConocidaId
  $3,   -- contraparte
  $4,   -- esInformadoPorBanco
  $5,   -- cuenta
  $6,   -- tarjeta
  $7,   -- tarjetaProveedor
  $8,   -- monto
  $9::TIMESTAMP,   -- fechaMovimiento
  $10,  -- descripcion
  $11,  -- esCuotas
  $12,  -- numeroCuotaActual
  $13,  -- totalCuotas
  $14,  -- esCargoAutomatico
  $15,  -- emailDestinatario
  $16,  -- categoriaEgreso
  $17,  -- divisa
  $18,  -- subcategoriaEgreso
  $19,  -- controlabilidad
  $20,  -- recurrencia
  $21,  -- canal
  $22   -- banco
FROM
  (SELECT usuarioid FROM usuario WHERE usuariocorreo = $15 LIMIT 1) u
CROSS JOIN
  (SELECT categoriaegresoid FROM categoriaegreso WHERE categoriaegresonombre = $16) ce
CROSS JOIN
  (SELECT divisaid FROM divisa WHERE divisacodigo = $17) di
LEFT JOIN subcategoriaegreso se
  ON se.subcategoriaegresonombre = $18
  AND se.categoriaegresoid = ce.categoriaegresoid
LEFT JOIN controlabilidad co
  ON co.controlabilidadnombre = $19
LEFT JOIN recurrencia re
  ON re.recurrencianombre = $20
LEFT JOIN canal ca
  ON ca.canalnombre = $21
LEFT JOIN banco ba
  ON ba.banconombre = $22
ON CONFLICT (egresomovimientohash) DO NOTHING
RETURNING egresoid, egresomovimientohash;
