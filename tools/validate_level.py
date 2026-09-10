import json

with open(r'C:\Users\epe_m\Downloads\level.json') as f:
    level = json.load(f)

tilesets = {i: ts for i, ts in enumerate(level['tilesets'])}
layer = next(l for l in level['layers'] if l['name'] == 'Background')

seen_ids = []
for row in layer['data']:
    for cell in row:
        if isinstance(cell, dict):
            tid = cell['tilesetId']
            if tid not in seen_ids:
                seen_ids.append(tid)

id_to_ts_idx = {tid: i for i, tid in enumerate(seen_ids)}

errors = []
for ry, row in enumerate(layer['data']):
    for rx, cell in enumerate(row):
        if not isinstance(cell, dict):
            continue
        ts_idx = id_to_ts_idx[cell['tilesetId']]
        ts = tilesets[ts_idx]
        if cell['tileX'] >= ts['cols'] or cell['tileY'] >= ts['rows']:
            msg = "row %d col %d: tileX=%d tileY=%d -> %s (%dx%d) OUT OF BOUNDS" % (
                ry, rx, cell['tileX'], cell['tileY'], ts['name'], ts['cols'], ts['rows'])
            errors.append(msg)

if errors:
    print("%d out-of-bounds tiles:" % len(errors))
    for e in errors[:20]:
        print(" ", e)
else:
    print("All tile coordinates within bounds.")

print()
print("Tileset mapping used:")
for tid, idx in id_to_ts_idx.items():
    ts = tilesets[idx]
    print("  id %d -> [%d] %s (%dx%d)" % (tid, idx, ts['name'], ts['cols'], ts['rows']))
