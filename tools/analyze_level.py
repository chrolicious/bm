import json

with open(r'C:\Users\epe_m\Downloads\level.json') as f:
    level = json.load(f)

tilesets = level['tilesets']
layer = next(l for l in level['layers'] if l['name'] == 'Background')

# Find max tileX/tileY per numeric ID
id_bounds = {}
for row in layer['data']:
    for cell in row:
        if not isinstance(cell, dict):
            continue
        tid = cell['tilesetId']
        if tid not in id_bounds:
            id_bounds[tid] = [0, 0]
        id_bounds[tid][0] = max(id_bounds[tid][0], cell['tileX'])
        id_bounds[tid][1] = max(id_bounds[tid][1], cell['tileY'])

print("Required minimum tileset sizes per ID (sorted):")
for tid in sorted(id_bounds):
    mx, my = id_bounds[tid]
    print("  id %d: needs >= %d cols, >= %d rows" % (tid, mx+1, my+1))

print()
print("Available tilesets:")
for i, ts in enumerate(tilesets):
    print("  [%d] %-30s %dx%d" % (i, ts['name'], ts['cols'], ts['rows']))

# Greedy: sorted IDs -> first unassigned tileset (array order) that satisfies constraints
print()
print("Greedy mapping (sorted timestamp -> first valid tileset):")
assigned = set()
mapping = {}
for tid in sorted(id_bounds):
    mx, my = id_bounds[tid]
    for i, ts in enumerate(tilesets):
        if i not in assigned and ts['cols'] > mx and ts['rows'] > my:
            assigned.add(i)
            mapping[tid] = i
            print("  id %d -> [%d] %s" % (tid, i, ts['name']))
            break
    else:
        print("  id %d -> NO VALID TILESET FOUND" % tid)
