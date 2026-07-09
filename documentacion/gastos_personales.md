# Gastos Personales — Documentacion Completa

> Fuente unica de verdad del proyecto Gestor de Gastos. Leer al iniciar contexto.
> Ultima actualizacion: 2026-07-06

---

## 1. VISION GENERAL

**Proyecto**: Sistema automatizado de gestion de finanzas personales que procesa correos bancarios, extrae movimientos con IA, y los clasifica en una base de datos estructurada.

**Stack**:

| Capa | Tecnologia | Detalle |
|------|-----------|---------|
| BD | PostgreSQL (VPS chitara) | DB `personal_contador`, fuente NocoDB `bq8ixhqm9ecwwrz` |
| BD legado | Neon PostgreSQL | Proyecto `old-lab-07457522`, schema `gestiongastos` (YA NO SE USA) |
| Automatizacion | n8n (VPS chitara) | 3 workflows: WF1, WF2, WF3 |
| Extraccion IA | GPT-4o via n8n | Prompt engineered con datasets catalogos |
| Frontend | Angular 20 + Ionic 8 | App "Saldito" en `saldito.chitaraagenteia.com` |
| Auth | Clerk | `charmed-lionfish-65`, email magic link + Google OAuth |
| Admin DB | NocoDB | Base `pakjusah66zi8ol`, fuente `personal_contador` |

**Arquitectura de datos**: NocoDB → PostgreSQL (source `bq8ixhqm9ecwwrz`, tipo `pg`, titulo `personal_contador`)

---

## 2. ESQUEMA DE BASE DE DATOS

### 2.1 Tablas de catalogo (lookups)

| Tabla | PK | Display | Unique |
|-------|-----|---------|--------|
| `usuario` | `usuarioid` | `usuariocorreo` | `usuariocorreo` |
| `banco` | `bancoid` | `banconombre` | `banconombre` |
| `divisa` | `divisaid` | `divisacodigo` | `divisacodigo`, `divisanombre` |
| `categoriaegreso` | `categoriaegresoid` | `categoriaegresonombre` | `categoriaegresonombre` |
| `categoriaingreso` | `categoriaingresoid` | `categoriaingresonombre` | `categoriaingresonombre` |
| `subcategoriaegreso` | `subcategoriaegresoid` | `subcategoriaegresonombre` | `subcategoriaegresonombre` |
| `controlabilidad` | `controlabilidadid` | `controlabilidadnombre` | `controlabilidadnombre` |
| `recurrencia` | `recurrenciaid` | `recurrencianombre` | `recurrencianombre` |
| `canal` | `canalid` | `canalnombre` | `canalnombre` |
| `direcciontransferencia` | `direcciontransferenciaid` | `direcciontransferencianombre` | `direcciontransferencianombre` |
| `contraparteconocida` | `contraparteconocidaid` | — | — |
| `estadobandejacorreo` | `estadobandejacorreoid` | `estadobandejacorreonombre` | — |
| `estadobandejaia` | `estadobandejaiaid` | `estadobandejaianombre` | — |
| `pais` | `paisid` | — | — |

### 2.2 Tablas transaccionales

#### bandejacorreo

| Campo | Tipo | Notas |
|-------|------|-------|
| `bandejacorreoid` | Number | PK |
| `bandejacorreofechaingesta` | DateTime | default now() |
| `bandejacorreofecharecepcionorigen` | DateTime | |
| `bandejacorreofuenteorigen` | Text | ej: 'gmail' |
| `bandejacorreoemailorigen` | Text | remitente |
| `bandejacorreoemaildestinatario` | Text | |
| `bandejacorreoidmensajegmail` | Text | UNIQUE |
| `bandejacorreopayloadcrudo` | JSON | |
| `bandejacorreotextoinformacion` | LongText | asunto + remitente + cuerpo |
| `bandejacorreointentos` | Number | default 0, max 3 |
| `bandejacorreologproceso` | LongText | |
| `bandejacorreofechaactualizacion` | DateTime | |
| `estadobandejacorreoid` | FK → estadobandejacorreo | Pendiente, EnProceso, Procesado, Error, Descartado |

#### bandejaia

| Campo | Tipo | Notas |
|-------|------|-------|
| `bandejaiaid` | Number | PK |
| `bandejacorreoid` | FK → bandejacorreo | |
| `bandejaiatipomovimiento` | Text | 'egreso', 'ingreso', 'transferencia' |
| `bandejaiarazon` | Text | por que se asigno ese tipo |
| `bandejaialogproceso` | LongText | |
| `estadobandejaiaid` | FK → estadobandejaia | Pendiente, EnProceso, Procesado, Error |

#### egreso

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `egresoid` | Number | **PK** |
| `usuarioid` | FK → usuario | **NOT NULL** |
| `categoriaegresoid` | FK → categoriaegreso | **NOT NULL** |
| `subcategoriaegresoid` | FK → subcategoriaegreso | nullable |
| `controlabilidadid` | FK → controlabilidad | nullable |
| `recurrenciaid` | FK → recurrencia | nullable |
| `canalid` | FK → canal | nullable |
| `bancoid` | FK → banco | nullable |
| `divisaid` | FK → divisa | **NOT NULL** |
| `bandejacorreoid` | FK → bandejacorreo | nullable |
| `contraparteconocidaid` | FK → contraparteconocida | nullable |
| `egresocontraparte` | LongText | **NOT NULL** |
| `egresoesinformadoporbanco` | Boolean | **NOT NULL**, default false |
| `egresocuenta` | Text | nullable |
| `egresotarjeta` | Text | nullable |
| `egresotarjetaproveedor` | Text | nullable |
| `egresomontooriginal` | Decimal | **NOT NULL** |
| `egresomonto` | Number | calculado (app) |
| `egresofechamovimiento` | DateTime | **NOT NULL** |
| `egresodescripcion` | LongText | nullable |
| `egresoescuotas` | Boolean | **NOT NULL**, default false |
| `egresonumerocuotaactual` | Number | nullable |
| `egresototalcuotas` | Number | nullable |
| `egresoescargoautomatico` | Boolean | **NOT NULL**, default false |
| `egresomovimientohash` | Text | **UNIQUE + NOT NULL** |
| `egresofechacreacion` | DateTime | default now() |
| `egresofechaactualizacion` | DateTime | |
| + campos calculados: `egresoanio`, `egresomesnumero`, `egresomesnombre`, `egresodiasemananumero`, `egresodiasemananombre`, `egresodiames`, `egresofranjahoraria` | | manejados por triggers/app |

**Constraints NOT NULL (13)**: usuarioid, categoriaegresoid, egresocontraparte, egresoesinformadoporbanco, egresomontooriginal, divisaid, egresofechamovimiento, egresoescuotas, egresoescargoautomatico, egresomovimientohash, egresofechacreacion

**Constraints UNIQUE (1)**: `egresomovimientohash`

**Check constraints (2)**:
- `CK_Egreso_Cuotas`: si `escuotas=true` → `numerocuotaactual` y `totalcuotas` deben ser NOT NULL
- `CK_Egreso_BancoConsistencia`: si `esinformadoporbanco=true` → `bancoid` NOT NULL; si `false` → `bancoid` NULL

#### ingreso

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `ingresoid` | Number | **PK** |
| `usuarioid` | FK → usuario | **NOT NULL** |
| `categoriaingresoid` | FK → categoriaingreso | nullable |
| `bancoid` | FK → banco | nullable |
| `divisaid` | FK → divisa | nullable |
| `bandejacorreoid` | FK → bandejacorreo | nullable |
| `contraparteconocidaid` | FK → contraparteconocida | nullable |
| `ingresocontraparte` | LongText | |
| `ingresoesinformadoporbanco` | Boolean | default false |
| `ingresocuenta` | Text | nullable |
| `ingresotarjeta` | Text | nullable |
| `ingresotarjetaproveedor` | Text | nullable |
| `ingresomontooriginal` | Decimal | |
| `ingresomonto` | Number | calculado |
| `ingresofechamovimiento` | DateTime | |
| `ingresodescripcion` | LongText | nullable |
| `ingresomovimientohash` | Text | **UNIQUE + NOT NULL** |
| `ingresofechacreacion` | DateTime | default now() |
| `ingresofechaactualizacion` | DateTime | |
| + campos calculados (anio, mes, dia, etc.) | | |

**Constraints NOT NULL (9)**: usuarioid, ingresocontraparte, ingresoesinformadoporbanco, ingresomontooriginal, divisaid, ingresofechamovimiento, ingresomovimientohash, ingresofechacreacion

**Constraints UNIQUE (1)**: `ingresomovimientohash`

#### transferencia

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `transferenciaid` | Number | **PK** |
| `usuarioid` | FK → usuario | |
| `direcciontransferenciaid` | FK → direcciontransferencia | |
| `bancoid` | FK → banco | |
| `divisaid` | FK → divisa | |
| `bandejacorreoid` | FK → bandejacorreo | |
| `contraparteconocidaid` | FK → contraparteconocida | nullable |
| `transferenciacontraparte` | LongText | |
| `transferenciacuentaorigen` | Text | default 'No informada' |
| `transferenciacuentadestino` | Text | default 'No informada' |
| `transferenciamontooriginal` | Decimal | |
| `transferenciamonto` | Number | calculado |
| `transferenciafechamovimiento` | DateTime | |
| `transferenciadescripcion` | LongText | nullable |
| `transferenciareferencia` | Text | nullable |
| `transferenciamovimientohash` | Text | **UNIQUE + NOT NULL** |
| `transferenciafechacreacion` | DateTime | default now() |
| `transferenciafechaactualizacion` | DateTime | |
| + campos calculados | | |

**Constraints NOT NULL (10)**: usuarioid, direcciontransferenciaid, bancoid, transferenciacontraparte, transferenciacuentaorigen, transferenciacuentadestino, transferenciamontooriginal, divisaid, transferenciafechamovimiento, transferenciamovimientohash, transferenciafechacreacion

**Constraints UNIQUE (1)**: `transferenciamovimientohash`

---

## 3. WORKFLOWS n8n

Archivos en `n8n/workflows/`:

| Archivo | Nombre | Funcion |
|---------|--------|---------|
| `Gastos_WF1_Webhook_Email.json` | 01 Webhook Email a BandejaCorreo | Recibe emails via POST y los inserta en `bandejacorreo` |
| `Gastos_WF2_Triage_Correos.json` | 02 Triage Correos a BandejaIA | Cada 5 min: clasifica correos pendientes con IA → `bandejaia` |
| `Gastos_WF3_Distribuir_Movimientos.json` | 03 Extraer y Distribuir Movimientos | Recibe de WF2: extrae JSON con GPT-4o y hace INSERT en la tabla correspondiente |

### WF1 — Webhook Email a BandejaCorreo

```
[POST /gastos-email] → [Parsear Email] → [INSERT bandejacorreo] → [Responder OK]
```

- Recibe email como JSON
- Extrae: fecha, fuente, email_origen, email_dest, msg_id, payload crudo, texto_info
- Inserta en `bandejacorreo` con `estadobandejacorreoid = 1` (Pendiente)
- Retorna el `bandejacorreoid` generado

Campos usados del input: `asunto`, `emailOrigen`, `emailDestinatario`, `idMensajeGmail`, `fechaRecepcion`, `fuenteOrigen`, `texto`/`body_plain`/`body_text`

### WF2 — Triage Correos a BandejaIA

```
[Trigger 5min] → [Obtener Pendientes] → [Loop correos] → [Marcar EnProceso] → [Clasificar con IA (tipoMovimiento)] → [INSERT/UPDATE bandejaia]
```

- Trigger: cada 5 minutos
- Obtiene hasta 10 correos con estado 'Pendiente' y < 3 intentos
- Por cada correo:
  1. Marca como 'EnProceso'
  2. Usa IA para clasificar tipo de movimiento (egreso/ingreso/transferencia)
  3. Inserta en `bandejaia` con `ON CONFLICT (bandejacorreoid) DO UPDATE`
- Si error: marca como 'Error' e incrementa intentos

### WF3 — Extraer y Distribuir Movimientos

Nodos (14):

```
01 - Webhook WF2          ← Recibe {bandejacorreoid, bandejacorreotextoinformacion, bandejacorreoemaildestinatario, tipoMovimiento, razon}
02 - Cargar Datasets      → Carga catalogos en un solo query (categorias, subcategorias, bancos, divisas, etc.)
03 - Armar Prompt         → Code node que construye system prompt + user prompt con datasets embebidos
04 - IA Extraer           → GPT-4o extrae JSON del correo segun tipoMovimiento
05 - Validar JSON         → Valida campos obligatorios: tipo, contraparte, monto, divisa, fechaMovimiento, categoria
06 - Valido?              → IF: valid=true → construir INSERT, valid=false → marcar error
07 - Construir INSERT     → ⚠️ Code node con el script de INSERT (ver seccion 5)
08 - Insertar Movimiento  → Ejecuta el INSERT en tabla egreso/ingreso/transferencia
09 - Marcar Procesado     → UPDATE bandejacorreo → estado 'Procesado'
10 - BandejaIA Procesado  → UPDATE bandejaia → estado 'Procesado'
11 - Responder OK         → 200 {status:'ok'}
12 - BandejaIA Error      → UPDATE bandejaia → estado 'Error' (rama false del IF)
13 - Marcar Error Correo  → UPDATE bandejacorreo → estado 'Error'
14 - Responder Error      → 200 {status:'error'}
```

---

## 4. FLUJO DE DATOS COMPLETO

```
Email bancario (Gmail)
  ↓ (reenvio automatico o API)
POST /gastos-email (WF1)
  ↓
bandejacorreo [Pendiente]
  ↓ (WF2 cada 5min)
bandejacorreo [EnProceso] + bandejaia [tipoMovimiento clasificado]
  ↓ (WF2 → webhook WF3)
GPT-4o extrae JSON del correo (WF3)
  ↓
Validacion de campos (WF3 nodo 05)
  ↓
INSERT en: egreso / ingreso / transferencia (WF3 nodos 07-08)
  ↓
bandejacorreo [Procesado] + bandejaia [Procesado] (WF3 nodos 09-10)
```

---

## 5. SCRIPT DE INSERCION (nodo 07 de WF3)

### Version actual en produccion (WF3)

**⚠️ TIENE BUGS CONOCIDOS:**
1. **Falta `usuarioid`** — es NOT NULL pero no se inserta
2. **Falta `egresomovimientohash`** — es UNIQUE + NOT NULL pero no se calcula
3. **Typo**: `egresoescargas` debe ser `egresoescuotas`

### Script adaptado (version corregida para usar en el nodo 07)

Reemplazar el contenido del Code node `07 - Construir INSERT` con:

```javascript
const mov = $('05 - Validar JSON').item.json;
const bandejaCorreoId = $input.first().json.bandejacorreoid;
const emailDestinatario = $input.first().json.bandejacorreoemaildestinatario.replace(/'/g, "''");

const esc = s => (s || '').replace(/'/g, "''");

let query = '';

if (mov.tipo === 'egreso') {
  query = `
    INSERT INTO egreso (
      usuarioid,
      categoriaegresoid,
      subcategoriaegresoid,
      controlabilidadid,
      recurrenciaid,
      canalid,
      egresocontraparte,
      bancoid,
      egresoesinformadoporbanco,
      egresocuenta,
      egresotarjeta,
      egresotarjetaproveedor,
      egresomontooriginal,
      divisaid,
      egresofechamovimiento,
      egresodescripcion,
      bandejacorreoid,
      contraparteconocidaid,
      egresoescuotas,
      egresonumerocuotaactual,
      egresototalcuotas,
      egresoescargoautomatico,
      egresomovimientohash
    )
    SELECT
      u.usuarioid,
      ce.categoriaegresoid,
      se.subcategoriaegresoid,
      co.controlabilidadid,
      re.recurrenciaid,
      ca.canalid,
      '${esc(mov.contraparte)}',
      ba.bancoid,
      ${mov.esInformadoPorBanco || false},
      ${mov.cuenta ? "'" + esc(mov.cuenta) + "'" : 'NULL'},
      ${mov.tarjeta ? "'" + esc(mov.tarjeta) + "'" : 'NULL'},
      ${mov.tarjetaProveedor ? "'" + esc(mov.tarjetaProveedor) + "'" : 'NULL'},
      ${mov.monto},
      di.divisaid,
      '${esc(mov.fechaMovimiento)}'::TIMESTAMP,
      ${mov.descripcion ? "'" + esc(mov.descripcion) + "'" : 'NULL'},
      ${bandejaCorreoId},
      ${mov.contraparteConocidaId || 'NULL'},
      ${mov.esCuotas || false},
      ${mov.numeroCuotaActual || 'NULL'},
      ${mov.totalCuotas || 'NULL'},
      ${mov.esCargoAutomatico || false},
      digest(
        ${bandejaCorreoId}::text || '|' || 'egreso' || '|' ||
        '${esc(mov.contraparte)}' || '|' || ${mov.monto}::text || '|' ||
        '${esc(mov.divisa)}' || '|' || '${esc(mov.fechaMovimiento)}',
        'sha256'
      )
    FROM
      (SELECT usuarioid FROM usuario WHERE usuariocorreo = '${emailDestinatario}' LIMIT 1) u
    CROSS JOIN (SELECT categoriaegresoid FROM categoriaegreso WHERE categoriaegresonombre = '${esc(mov.categoriaEgreso)}') ce
    CROSS JOIN (SELECT divisaid FROM divisa WHERE divisacodigo = '${esc(mov.divisa)}') di
    LEFT JOIN subcategoriaegreso se
      ON se.subcategoriaegresonombre = ${mov.subcategoriaEgreso ? "'" + esc(mov.subcategoriaEgreso) + "'" : "''"}
      AND se.categoriaegresoid = ce.categoriaegresoid
    LEFT JOIN controlabilidad co
      ON co.controlabilidadnombre = ${mov.controlabilidad ? "'" + esc(mov.controlabilidad) + "'" : "''"}
    LEFT JOIN recurrencia re
      ON re.recurrencianombre = ${mov.recurrencia ? "'" + esc(mov.recurrencia) + "'" : "''"}
    LEFT JOIN canal ca
      ON ca.canalnombre = ${mov.canal ? "'" + esc(mov.canal) + "'" : "''"}
    LEFT JOIN banco ba
      ON ba.banconombre = ${mov.banco ? "'" + esc(mov.banco) + "'" : "''"}
    RETURNING egresoid AS movimientoid;
  `;

} else if (mov.tipo === 'ingreso') {
  query = `
    INSERT INTO ingreso (
      usuarioid,
      categoriaingresoid,
      ingresocontraparte,
      bancoid,
      ingresoesinformadoporbanco,
      ingresocuenta,
      ingresotarjeta,
      ingresotarjetaproveedor,
      ingresomontooriginal,
      divisaid,
      ingresofechamovimiento,
      ingresodescripcion,
      bandejacorreoid,
      contraparteconocidaid,
      ingresomovimientohash
    )
    SELECT
      u.usuarioid,
      ci.categoriaingresoid,
      '${esc(mov.contraparte)}',
      ba.bancoid,
      ${mov.esInformadoPorBanco || false},
      ${mov.cuenta ? "'" + esc(mov.cuenta) + "'" : 'NULL'},
      ${mov.tarjeta ? "'" + esc(mov.tarjeta) + "'" : 'NULL'},
      ${mov.tarjetaProveedor ? "'" + esc(mov.tarjetaProveedor) + "'" : 'NULL'},
      ${mov.monto},
      di.divisaid,
      '${esc(mov.fechaMovimiento)}'::TIMESTAMP,
      ${mov.descripcion ? "'" + esc(mov.descripcion) + "'" : 'NULL'},
      ${bandejaCorreoId},
      ${mov.contraparteConocidaId || 'NULL'},
      digest(
        ${bandejaCorreoId}::text || '|' || 'ingreso' || '|' ||
        '${esc(mov.contraparte)}' || '|' || ${mov.monto}::text || '|' ||
        '${esc(mov.divisa)}' || '|' || '${esc(mov.fechaMovimiento)}',
        'sha256'
      )
    FROM
      (SELECT usuarioid FROM usuario WHERE usuariocorreo = '${emailDestinatario}' LIMIT 1) u
    CROSS JOIN (SELECT categoriaingresoid FROM categoriaingreso WHERE categoriaingresonombre = '${esc(mov.categoriaIngreso)}') ci
    CROSS JOIN (SELECT divisaid FROM divisa WHERE divisacodigo = '${esc(mov.divisa)}') di
    LEFT JOIN banco ba
      ON ba.banconombre = ${mov.banco ? "'" + esc(mov.banco) + "'" : "''"}
    RETURNING ingresoid AS movimientoid;
  `;

} else if (mov.tipo === 'transferencia') {
  query = `
    INSERT INTO transferencia (
      usuarioid,
      direcciontransferenciaid,
      transferenciacontraparte,
      bancoid,
      transferenciacuentaorigen,
      transferenciacuentadestino,
      transferenciamontooriginal,
      divisaid,
      transferenciafechamovimiento,
      transferenciadescripcion,
      transferenciareferencia,
      bandejacorreoid,
      contraparteconocidaid,
      transferenciamovimientohash
    )
    SELECT
      u.usuarioid,
      dt.direcciontransferenciaid,
      '${esc(mov.contraparte)}',
      ba.bancoid,
      '${esc(mov.cuentaOrigen || 'No informada')}',
      '${esc(mov.cuentaDestino || 'No informada')}',
      ${mov.monto},
      di.divisaid,
      '${esc(mov.fechaMovimiento)}'::TIMESTAMP,
      ${mov.descripcion ? "'" + esc(mov.descripcion) + "'" : 'NULL'},
      ${mov.referencia ? "'" + esc(mov.referencia) + "'" : 'NULL'},
      ${bandejaCorreoId},
      ${mov.contraparteConocidaId || 'NULL'},
      digest(
        ${bandejaCorreoId}::text || '|' || 'transferencia' || '|' ||
        '${esc(mov.contraparte)}' || '|' || ${mov.monto}::text || '|' ||
        '${esc(mov.divisa)}' || '|' || '${esc(mov.fechaMovimiento)}',
        'sha256'
      )
    FROM
      (SELECT usuarioid FROM usuario WHERE usuariocorreo = '${emailDestinatario}' LIMIT 1) u
    CROSS JOIN (SELECT direcciontransferenciaid FROM direcciontransferencia WHERE direcciontransferencianombre = '${esc(mov.direccionTransferencia)}') dt
    CROSS JOIN (SELECT divisaid FROM divisa WHERE divisacodigo = '${esc(mov.divisa)}') di
    CROSS JOIN (SELECT bancoid FROM banco WHERE banconombre = '${esc(mov.banco || '')}') ba
    RETURNING transferenciaid AS movimientoid;
  `;
}

query = query.replace(/\$(\d+)/g, (_, digits) => "' || chr(36) || '" + digits);

return [{ json: { query, tipo: mov.tipo } }];
```

### Calculo del hash

El hash se calcula automaticamente via **trigger BEFORE INSERT** en las 3 tablas transaccionales.
Usa `digest()` de `pgcrypto` (SHA-256).

**Campos que componen el hash:**

| # | Egreso | Ingreso | Transferencia |
|---|--------|---------|---------------|
| 1 | `usuarioid` | `usuarioid` | `usuarioid` |
| 2 | `'egreso'` (literal) | `'ingreso'` (literal) | `'transferencia'` (literal) |
| 3 | `egresocontraparte` | `ingresocontraparte` | `transferenciacontraparte` |
| 4 | `egresomontooriginal` | `ingresomontooriginal` | `transferenciamontooriginal` |
| 5 | `divisacodigo` (resuelto via FK) | `divisacodigo` | `divisacodigo` |
| 6 | `egresofechamovimiento` | `ingresofechamovimiento` | `transferenciafechamovimiento` |
| 7 | `egresocuenta` | `ingresocuenta` | `transferenciacuentaorigen` |
| 8 | `egresotarjeta` | `ingresotarjeta` | `transferenciacuentadestino` |
| 9 | `egresotarjetaproveedor` | `ingresotarjetaproveedor` | — |

Todos los campos nullable usan `COALESCE(campo, '')` para mantener determinismo.

**Triggers:**

```sql
CREATE OR REPLACE FUNCTION calcular_hash_movimiento()
RETURNS TRIGGER AS $$
DECLARE
  v_divisa_codigo text;
BEGIN
  SELECT divisacodigo INTO v_divisa_codigo FROM divisa WHERE divisaid = NEW.divisaid;
  -- (logica especifica por tabla)
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hash_egreso BEFORE INSERT ON egreso FOR EACH ROW EXECUTE FUNCTION calcular_hash_movimiento();
CREATE TRIGGER trg_hash_ingreso BEFORE INSERT ON ingreso FOR EACH ROW EXECUTE FUNCTION calcular_hash_movimiento();
CREATE TRIGGER trg_hash_transferencia BEFORE INSERT ON transferencia FOR EACH ROW EXECUTE FUNCTION calcular_hash_movimiento();
```

El WF3 puede enviar `egresomovimientohash` en el INSERT (el trigger lo sobrescribe) o dejar de enviarlo.

---

## 6. PROMPT DE EXTRACCION IA

Archivo: `documentacion/prompt_wf3_extraccion.txt`

La IA (GPT-4o) recibe:
- **System prompt**: instrucciones completas + reglas + formato de respuesta
- **User prompt**: el correo a procesar + datasets de catalogos embebidos

Los datasets se cargan en el nodo `02 - Cargar Datasets` con un solo query que devuelve JSON con:
`categorias_ingreso`, `categorias_egreso`, `subcategorias_egreso`, `controlabilidad`, `recurrencia`, `canal`, `direccion_transferencia`, `contrapartes`, `bancos`, `divisas`

Formato de cada dataset:
- Catalogos simples: `id:nombre:descripcion`
- Subcategorias: `id:categoriaId:categoria:subcategoria`
- Contrapartes: `id:giro:nombre:patron`
- Divisas: `id:codigo:nombre:decimales`
- Bancos: `id:nombre:nombreCorto:esDigital`

Parametros GPT-4o: temperature=0.2, topP=0.1, maxTokens=2000, 3 reintentos con 5s entre intentos.

---

## 7. MIGRACION DEL ESQUEMA (gestiongastos → personal_contador)

### Que cambio

| Aspecto | Antes (Neon gestiongastos) | Ahora (VPS personal_contador) |
|---------|---------------------------|-------------------------------|
| Host DB | Neon cloud `old-lab-07457522` | PostgreSQL VPS chitara |
| Schema | `gestiongastos` | `public` (default) |
| Tabla usuario lookup | `Email.EmailDireccion` | `usuario.usuariocorreo` |
| Naming | PascalCase (`UsuarioId`) | lowercase (`usuarioid`) |
| Tablas | `"Egreso"`, `"Banco"` | `egreso`, `banco` |
| Columna contraparte | `EgresoContraparte` | `egresocontraparte` |
| Columna cuotas | `EgresoEsCuotas` | `egresoescuotas` |
| Columna cargo auto | `EgresoEsCargoAutomatico` | `egresoescargoautomatico` |

### Campos nuevos (no existian en gestiongastos)

- `contraparteconocidaid` (FK a `contraparteconocida`)
- `egresomovimientohash` (UNIQUE, NOT NULL)
- `egresofechacreacion` (default now())
- `egresofechaactualizacion`
- Campos calculados: anio, mes, dia, franjahoraria (manejados por app/triggers)

---

## 8. CONEXION A LA BASE DE DATOS

### NocoDB (admin UI)
- Base ID: `pakjusah66zi8ol`
- Source: `bq8ixhqm9ecwwrz` (PG, `personal_contador`)
- Workspace: `wcdl33nz`

### n8n credential
- Nombre: `Postgres Gastos`
- Host: PostgreSQL del VPS chitara (127.0.0.1:5432 o via Docker network)
- DB: `personal_contador`
- Schema: `public`

### Acceso programatico
- La DB esta en el VPS (5.252.52.190), accesible via Docker network interna
- Los workflows n8n usan la credential `Postgres Gastos` para conectarse

---

## 9. ISSUES CONOCIDOS (2026-07-07)

| # | Issue | Severidad | Estado |
|---|-------|-----------|--------|
| 1 | Nodo 07 WF3 no inserta `usuarioid` (NOT NULL) | 🟢 RESUELTO | WF2 en vivo ya usa nodos Postgres separados con JOIN a `usuario` |
| 2 | Nodo 07 WF3 no calcula `egresomovimientohash` (UNIQUE + NOT NULL) | 🟢 RESUELTO | Hash calculado via trigger BEFORE INSERT en DB |
| 3 | Typo `egresoescargas` en vez de `egresoescuotas` | 🟢 RESUELTO | WF2 en vivo usa queries SQL directas con nombres correctos |
| 4 | Falta `ON CONFLICT` en inserts → error si mismo correo procesado 2+ veces | 🟢 RESUELTO | WF2 en vivo: los 3 nodos Postgres tienen `ON CONFLICT (movimientohash) DO NOTHING` |
| 5 | La IA devuelve `contraparte` como objeto `{ContraparteConocidaId, ...}` o string — el script actual solo maneja string | 🟡 | El script de seccion 5 usa `mov.contraparte` como string; si es objeto, fallara |
| 6 | La IA devuelve objetos con IDs para catalogos (ej: `{CategoriaEgresoId, CategoriaEgresoNombre}`) pero el script usa strings planos (`mov.categoriaEgreso`) | 🟡 | El validador (nodo 05) no hace flattening de objetos a strings |
| 7 | `mov.monto` se inserta en `egresomontooriginal` (que es lo correcto) pero tambien existe `egresomonto` como campo calculado | ✅ | OK, `egresomonto` lo maneja trigger/app |
| 8 | `pgcrypto` debe estar instalado en la DB del VPS | 🟢 RESUELTO | Verificado: v1.4 instalada |
| 9 | `ingresomovimientohash` y `transferenciamovimientohash` sin UNIQUE + NOT NULL | 🟢 RESUELTO | Constraints agregadas (2026-07-06) |
| 10 | `egresomovimientohash` documentado como UNIQUE + NOT NULL pero no aplicado en DB | 🟢 RESUELTO | Constraint aplicada (2026-07-06) |
| 11 | WF2 versionado en git (13 nodos) desactualizado vs produccion (26 nodos, arquitectura Switch + 3 Postgres separados) | 🟢 RESUELTO | Sincronizado 2026-07-07 |

---

## 10. ARCHIVOS RELACIONADOS

| Archivo | Contenido |
|---------|-----------|
| `n8n/workflows/Gastos_WF1_Webhook_Email.json` | WF1 — ingesta de emails |
| `n8n/workflows/Gastos_WF2_Triage_Correos.json` | WF2 — clasificacion por tipo |
| `n8n/workflows/Gastos_WF3_Distribuir_Movimientos.json` | WF3 — extraccion + INSERT |
| `documentacion/prompt_wf3_extraccion.txt` | Prompt de extraccion IA |
| `documentacion/plan_arquitectura_gastos.md` | Plan de migracion (historico) |
| `memory-bank/techContext.md` | Contexto tecnico general |
