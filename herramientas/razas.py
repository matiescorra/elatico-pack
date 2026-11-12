# Genera el marco de las ilustraciones del Libro de las Razas y la fuente elatico:razas
import json, math
from PIL import Image, ImageDraw
W, H = 64, 48
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = im.load()
OSC = (59, 38, 22, 255); ORO = (176, 128, 52, 255); ORO2 = (214, 170, 84, 255)
for y in range(H):
    for x in range(W):
        # rectángulo con esquinas recortadas
        cx, cy = min(x, W - 1 - x), min(y, H - 1 - y)
        if cx + cy < 3: continue
        borde = cx == 0 or cy == 0 or cx + cy == 3
        if borde: px[x, y] = OSC; continue
        if cx == 2 or cy == 2 or cx + cy == 5: px[x, y] = ORO; continue
        if cx == 1 or cy == 1 or cx + cy == 4: px[x, y] = OSC; continue
        # fondo: pergamino un poco más oscuro, con viñeta radial
        d = math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2))
        t = max(0.0, min(1.0, d))
        base = (232, 214, 172); fin = (196, 166, 112)
        c = tuple(int(base[i] * (1 - t) + fin[i] * t) for i in range(3))
        px[x, y] = c + (255,)
# adornos dorados en las esquinas interiores
for (x, y) in ((5, 5), (W - 6, 5), (5, H - 6), (W - 6, H - 6)):
    for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)): px[x + dx, y + dy] = ORO2
im.save('fuente/assets/elatico/textures/font/razas/marco.png')
EMBLEMAS = {  # orden = campo "emblema" de cada raza en la config de AticoCore
    'humano': 'iron_sword', 'enano': 'iron_pickaxe', 'elfo': 'bow', 'paladin': 'totem_of_undying', 'orco': 'iron_axe',
    'triton': 'trident', 'gnomo': 'clock_00', 'draconido': 'fire_charge', 'faerie': 'pink_petals', 'sombrio': 'ender_pearl',
    'licantropo': 'bone', 'titan': 'mace', 'olimpico': 'golden_apple'}
prov = [{'type': 'space', 'advances': {'': 25, '': -49}},
        {'type': 'bitmap', 'file': 'elatico:font/razas/marco.png', 'height': 48, 'ascent': 7, 'chars': ['']},
        {'type': 'bitmap', 'file': 'minecraft:item/written_book.png', 'height': 32, 'ascent': -1, 'chars': ['']}]
for i, (raza, tex) in enumerate(EMBLEMAS.items()):
    prov.append({'type': 'bitmap', 'file': f'minecraft:item/{tex}.png', 'height': 32, 'ascent': -1, 'chars': [chr(0xE210 + i)]})
json.dump({'providers': prov}, open('fuente/assets/elatico/font/razas.json', 'w'), indent=2, ensure_ascii=True)
print({r: i for i, r in enumerate(EMBLEMAS)})
