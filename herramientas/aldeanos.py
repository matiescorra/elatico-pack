# Aldeanos más humanos: sin la nariz gigante, cara con cejas separadas, pelo y (opcional) barba
import sys
from PIL import Image, ImageDraw, ImageFont
BASE = '/tmp/ma/package/minecraft-assets/data/26.1/entity/villager/villager.png'
PIEL = [(190, 136, 108), (183, 130, 114), (179, 123, 98)]

def hacer(barba, pelo=((74, 49, 33), (92, 61, 40), (61, 40, 27)), ojos=(59, 89, 140)):
    im = Image.open(BASE).convert('RGBA'); p = im.load()
    P = lambda x, y: pelo[(x * 7 + y * 3) % 3]
    S = lambda x, y: PIEL[(x * 5 + y * 11) % 3] if (x * 5 + y * 11) % 7 else PIEL[0]
    for x in range(24, 32):           # nariz invisible
        for y in range(0, 6): p[x, y] = (0, 0, 0, 0)
    for x in range(8, 16):            # coronilla
        for y in range(0, 8): p[x, y] = P(x, y) + (255,)
    for x in range(24, 32):           # nuca
        for y in range(8, 16): p[x, y] = P(x, y) + (255,)
    for x0 in (0, 16):                # costados (patillas)
        for x in range(x0, x0 + 8):
            for y in range(8, 18):
                lim = 12 if (x0 == 0 and x < 4) or (x0 == 16 and x > 19) else 11
                if y <= lim: p[x, y] = P(x, y) + (255,)
                else: p[x, y] = S(x, y) + (255,)
            p[x0 + (5 if x0 == 0 else 2), 13] = (160, 104, 84, 255)   # oreja
    # cara
    for x in range(8, 16):
        for y in range(8, 18): p[x, y] = S(x, y) + (255,)
    for x in range(8, 16): p[x, 8] = P(x, 8) + (255,)
    for x in (8, 9, 14, 15): p[x, 9] = P(x, 9) + (255,)
    for x in (8, 15):
        for y in (10, 11): p[x, y] = P(x, y) + (255,)
    for x in (9, 10, 13, 14): p[x, 12] = pelo[2] + (255,)            # cejas separadas
    p[9, 13] = (245, 240, 232, 255); p[10, 13] = ojos + (255,)       # ojos
    p[13, 13] = ojos + (255,); p[14, 13] = (245, 240, 232, 255)
    p[11, 14] = (170, 112, 92, 255); p[12, 14] = (160, 104, 84, 255)  # sombra de nariz chica
    p[10, 15] = (200, 128, 112, 255); p[13, 15] = (200, 128, 112, 255)  # cachetes
    for x in (11, 12): p[x, 16] = (128, 66, 56, 255)                 # boca
    if barba:
        for x in range(8, 16):
            for y in (15, 16, 17):
                if y == 16 and x in (11, 12): continue
                if y == 15 and x in (10, 11, 12, 13): p[x, y] = pelo[0] + (255,) if x in (10, 13) else p[x, y]
                else: p[x, y] = P(x, y) + (255,)
        for x in range(24, 32): p[x, 17] = P(x, 17) + (255,)
        for x0 in (0, 16):
            for x in range(x0, x0 + 8):
                for y in (15, 16, 17):
                    if (x0 == 0 and x >= 5) or (x0 == 16 and x <= 18): p[x, y] = P(x, y) + (255,)
        for x in range(16, 24):        # barba vista desde abajo
            for y in range(0, 8): p[x, y] = P(x, y) + (255,)
    return im

def cara(im, escala=22):
    return im.crop((8, 8, 16, 18)).resize((8 * escala, 10 * escala), Image.NEAREST)

if __name__ == '__main__':
    van = Image.open(BASE).convert('RGBA')
    a = hacer(False); b = hacer(True)
    a.save('opciones/aldeano_A.png'); b.save('opciones/aldeano_B.png')
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
    lienzo = Image.new('RGBA', (3 * 220 + 80, 330), (40, 42, 50, 255)); d = ImageDraw.Draw(lienzo)
    for i, (t, im) in enumerate((('Actual (vanilla)', van), ('Opción A: sin nariz', a), ('Opción B: con barba', b))):
        x = 20 + i * 240
        lienzo.alpha_composite(cara(im), (x, 70))
        d.text((x, 20), t, fill=(240, 230, 200), font=F)
    lienzo.save('opciones/aldeanos_caras.png')
