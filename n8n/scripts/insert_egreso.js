// ============================================================
// n8n Code Node — Construir INSERT Egreso
// ============================================================
// Input:  mov (JSON del AI extraction) + bandejacorreo data
// Output: { query, params[] } → listo para nodo Postgres
//
// El hash se calcula automaticamente via trigger BEFORE INSERT.
// ON CONFLICT DO NOTHING evita duplicados segun el UNIQUE hash.
// ============================================================

const mov = $('05 - Validar JSON').item.json;
const bandejaCorreoId = $input.first().json.bandejacorreoid;
const emailDestinatario = $input.first().json.bandejacorreoemaildestinatario;

const esc = s => (s || '').replace(/'/g, "''");
const txt = v => (v === null || v === undefined || v === '') ? 'NULL' : `'${esc(String(v))}'`;
const num = v => (v === null || v === undefined || v === '') ? 'NULL' : String(v);
const bol = v => v ? 'TRUE' : 'FALSE';

// ── Query con LEFT JOINs para catalogos opcionales ──────────
const query = `
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
    ${num(bandejaCorreoId)},
    ${num(mov.contraparteConocidaId)},
    ${txt(mov.contraparte)},
    ${bol(mov.esInformadoPorBanco)},
    ${txt(mov.cuenta)},
    ${txt(mov.tarjeta)},
    ${txt(mov.tarjetaProveedor)},
    ${num(mov.monto)},
    ${txt(mov.fechaMovimiento)}::TIMESTAMP,
    ${txt(mov.descripcion)},
    ${bol(mov.esCuotas)},
    ${num(mov.numeroCuotaActual)},
    ${num(mov.totalCuotas)},
    ${bol(mov.esCargoAutomatico)}
  FROM
    (SELECT usuarioid FROM usuario WHERE usuariocorreo = ${txt(emailDestinatario)} LIMIT 1) u
  CROSS JOIN
    (SELECT categoriaegresoid FROM categoriaegreso WHERE categoriaegresonombre = ${txt(mov.categoriaEgreso)}) ce
  CROSS JOIN
    (SELECT divisaid FROM divisa WHERE divisacodigo = ${txt(mov.divisa)}) di
  LEFT JOIN subcategoriaegreso se
    ON se.subcategoriaegresonombre = ${txt(mov.subcategoriaEgreso)}
    AND se.categoriaegresoid = ce.categoriaegresoid
  LEFT JOIN controlabilidad co
    ON co.controlabilidadnombre = ${txt(mov.controlabilidad)}
  LEFT JOIN recurrencia re
    ON re.recurrencianombre = ${txt(mov.recurrencia)}
  LEFT JOIN canal ca
    ON ca.canalnombre = ${txt(mov.canal)}
  LEFT JOIN banco ba
    ON ba.banconombre = ${txt(mov.banco)}
  ON CONFLICT (egresomovimientohash) DO NOTHING
  RETURNING egresoid, egresomovimientohash
`;

return [{ json: { query, tipo: 'egreso', contraparte: mov.contraparte, monto: mov.monto } }];
