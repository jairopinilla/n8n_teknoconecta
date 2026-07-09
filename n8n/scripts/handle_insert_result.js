// ============================================================
// n8n Code Node — Manejo de respuesta INSERT Egreso
// ============================================================
// Va DESPUES del nodo Postgres que ejecuta la query.
// Input:  resultado del nodo Postgres
// Output: { ok, egresoid?, hash?, duplicado?, error? }
// ============================================================

const resultado = $input.all();

// Caso 1: INSERT exitoso (Postgres devuelve la fila con RETURNING)
if (resultado.length > 0 && resultado[0].json && resultado[0].json.egresoid) {
  const { egresoid, egresomovimientohash } = resultado[0].json;
  return [{
    json: {
      ok: true,
      insertado: true,
      egresoid,
      hash: egresomovimientohash,
      duplicado: false,
      mensaje: `Egreso #${egresoid} insertado correctamente`
    }
  }];
}

// Caso 2: ON CONFLICT DO NOTHING — ya existe, ninguna fila retornada
if (resultado.length === 0 || (resultado[0].json && !resultado[0].json.egresoid)) {
  return [{
    json: {
      ok: true,
      insertado: false,
      egresoid: null,
      hash: null,
      duplicado: true,
      mensaje: 'Movimiento duplicado — ignorado (ON CONFLICT)'
    }
  }];
}

// Caso 3: Respuesta inesperada
return [{
  json: {
    ok: false,
    insertado: false,
    error: 'Respuesta inesperada del nodo Postgres',
    raw: resultado
  }
}];
