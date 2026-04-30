import json

with open(r'c:\Users\jairo\OneDrive\Documents\GitHub\n8n_teknoconecta\workflows\N8n_Update_Reservas_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Change workflow name
data['name'] = 'N8n_Update_Reservas_v2'

updated_nodes = []
for node in data.get('nodes', []):
    if node.get('name') == 'InsertarReservaNoExistente':
        q = node['parameters']['query']
        if '"Reserva_status"' not in q:
            q = q.replace(
                '  "Reserva_payload",\n  "HuespedId"',
                '  "Reserva_payload",\n  "Reserva_status",\n  "HuespedId"'
            )
            q = q.replace(
                's."payload",\n  NULL, -- HuespedId',
                "s.\"payload\",\n  s.\"payload\"->>'status',  -- Reserva_status\n  NULL, -- HuespedId"
            )
            node['parameters']['query'] = q
            updated_nodes.append(node['id'])

# Add the new "Update Reserva Estado y Fechas" node
new_node = {
    "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE public.\"Reserva\" r\nSET\n  \"Reserva_checkInDate\"  = (s.\"checkInDate\")::date,\n  \"Reserva_checkOutDate\" = (s.\"checkOutDate\")::date,\n  \"Reserva_checkInTime\"  = (s.\"checkInTime\")::time,\n  \"Reserva_checkOutTime\" = (s.\"checkOutTime\")::time,\n  \"Reserva_status\"       = s.\"payload\"->>'status',\n  \"UpdatedAt\"            = now() AT TIME ZONE 'America/Santiago'\nFROM public.\"ReservaStage\" s\nWHERE r.\"Reserva__id\" = s.\"_id\"\n  AND s.\"_id\" IS NOT NULL;",
        "options": {}
    },
    "type": "n8n-nodes-base.postgres",
    "typeVersion": 2.6,
    "position": [-336, -256],
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Update Reserva Estado y Fechas",
    "credentials": {
        "postgres": {
            "id": "zvx0J3DPht42SAUp",
            "name": "Postgres account"
        }
    }
}
data['nodes'].append(new_node)

# Update connections:
# InsertarReservaNoExistente -> Update Reserva Estado y Fechas -> ObtenerReservaSinAloHues
# (replacing direct InsertarReservaNoExistente -> ObtenerReservaSinAloHues)
conns = data.get('connections', {})

# Remove existing connection from InsertarReservaNoExistente to ObtenerReservaSinAloHues
if 'InsertarReservaNoExistente' in conns:
    main_out = conns['InsertarReservaNoExistente'].get('main', [[]])
    if main_out:
        main_out[0] = [c for c in main_out[0] if c.get('node') != 'ObtenerReservaSinAloHues']
        conns['InsertarReservaNoExistente']['main'] = main_out

# Add connection InsertarReservaNoExistente -> Update Reserva Estado y Fechas
if 'InsertarReservaNoExistente' in conns:
    conns['InsertarReservaNoExistente']['main'][0].append({
        "node": "Update Reserva Estado y Fechas",
        "type": "main",
        "index": 0
    })
else:
    conns['InsertarReservaNoExistente'] = {
        "main": [[{"node": "Update Reserva Estado y Fechas", "type": "main", "index": 0}]]
    }

# Add connection Update Reserva Estado y Fechas -> ObtenerReservaSinAloHues
conns['Update Reserva Estado y Fechas'] = {
    "main": [[{"node": "ObtenerReservaSinAloHues", "type": "main", "index": 0}]]
}

data['connections'] = conns

print(f'Updated nodes: {updated_nodes}')
print(f'New node added: {new_node["name"]}')

with open(r'c:\Users\jairo\OneDrive\Documents\GitHub\n8n_teknoconecta\workflows\N8n_Update_Reservas_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Done - file written')
