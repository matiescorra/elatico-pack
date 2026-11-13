"""Genera los cosméticos de raza (modelos 3D de cubos) para el pack de El Ático.

Unidades: "píxeles de jugador". La cabeza ocupa x -4..4, y 0..8 (y=0 es el cuello), z -4..4,
con la cara mirando a -z (norte). El torso ocupa x -4..4, y -12..0, z -2..2 (espalda en z=+2).
El plugin AticoCore escala 1 unidad = 1 píxel del jugador y pone el cuello en su lugar.
"""
import json, os, sys
from PIL import Image

RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'fuente')

PALETA = {  # nombre: (r,g,b,a)
 'barba': (138, 75, 42, 255), 'barba2': (96, 52, 28, 255), 'oro': (232, 185, 49, 255), 'oro2': (176, 128, 22, 255),
 'hueso': (239, 230, 207, 255), 'piedra': (138, 138, 138, 255), 'piedra2': (90, 90, 96, 255), 'rojo': (192, 48, 40, 255),
 'aqua': (63, 182, 168, 255), 'aqua2': (36, 120, 118, 255), 'cuerno': (58, 46, 46, 255), 'ala': (190, 240, 255, 130),
 'capucha': (30, 30, 38, 255), 'pelo': (109, 98, 88, 255), 'verde': (92, 150, 60, 255), 'sangre': (120, 14, 26, 255),
 'piel': (233, 198, 165, 255), 'blanco': (240, 240, 240, 255), 'escama': (200, 80, 30, 255), 'membrana': (150, 30, 30, 200),
 'plata': (200, 210, 220, 255), 'esmeralda': (40, 200, 110, 255), 'rosa': (220, 150, 150, 255), 'negro': (22, 20, 24, 255),
}
NOMBRES = list(PALETA)
LADO = 6  # celdas por fila (6x6 = 36 colores máx.), cada celda de 4x4 en una textura de 24x24
assert len(NOMBRES) <= LADO * LADO

def uv(color):
    i = NOMBRES.index(color)
    c, f = (i % LADO) * 4, (i // LADO) * 4
    k = 16 / (LADO * 4)  # las UV van de 0 a 16 sobre toda la textura
    return [round((c + 1) * k, 3), round((f + 1) * k, 3), round((c + 3) * k, 3), round((f + 3) * k, 3)]

def caja(x0, y0, z0, x1, y1, z1, color, luz=0):
    """Una caja en píxeles de jugador → elemento del modelo (x,z se corren +8 para centrar)."""
    a = [min(x0, x1) + 8, min(y0, y1), min(z0, z1) + 8]
    b = [max(x0, x1) + 8, max(y0, y1), max(z0, z1) + 8]
    for v in a + b:
        assert -16 <= v <= 32, (x0, y0, z0, x1, y1, z1)
    e = {'from': [round(v, 3) for v in a], 'to': [round(v, 3) for v in b],
         'faces': {f: {'uv': uv(color), 'texture': '#p'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}
    if luz: e['light_emission'] = luz
    return e

def espejo(cajas):
    """Duplica cajas del lado izquierdo (x<0) al derecho."""
    out = []
    for c in cajas:
        out.append(c)
        x0, y0, z0, x1, y1, z1, *resto = c
        out.append((-x1, y0, z0, -x0, y1, z1, *resto))
    return out

def anillo(y0, y1, afuera, grosor, color, luz=0, sin_frente=False):
    a, b = afuera, afuera - grosor
    r = [(-a, y0, b, -b, y1, -b, color, luz), (b, y0, -b, a, y1, b, color, luz),  # izq/der (x)
         (-a, y0, b, a, y1, a, color, luz)]                                        # atrás
    if sin_frente:
        r += [(-a, y0, -a, -1.5, y1, -b, color, luz), (1.5, y0, -a, a, y1, -b, color, luz)]
    else:
        r += [(-a, y0, -a, a, y1, -b, color, luz)]
    # corregir: izq/der van de -b a b en z
    r[0] = (-a, y0, -b, -b, y1, b, color, luz); r[1] = (b, y0, -b, a, y1, b, color, luz)
    return r

C = {}

C['enano_cabeza'] = [
    (-4, -2, -4.8, 4, 3, -4, 'barba'),            # barba sobre la cara de abajo
    (-3, -4, -4.8, 3, -2, -4.1, 'barba'),
    (-2, -6, -4.6, 2, -4, -4.2, 'barba'),
    (-3.2, 3, -5.0, 3.2, 3.8, -4.6, 'barba2'),    # bigote
    *espejo([(-4.6, 1, -4.2, -4, 5, -1, 'barba'),  # patillas
             (-2.6, -8, -4.5, -1.6, -6, -4.0, 'barba2'), (-2.8, -8.8, -4.7, -1.4, -7.6, -3.8, 'oro')]),  # trenzas con cuentas
]
C['elfo_cabeza'] = [
    *espejo([(-5.2, 2.5, -1.2, -4, 6, 1.2, 'piel'), (-6, 5, -0.2, -4.6, 8.5, 1.8, 'piel'), (-6.8, 7.5, 0.8, -5.6, 10.5, 2.6, 'piel'),
             (-7.2, 10, 1.6, -6.4, 11.5, 2.8, 'piel'), (-5.25, 3, -1.25, -4.9, 5.5, 0.6, 'rosa')]),
    *anillo(5.5, 6.2, 4.3, 0.3, 'plata'),          # diadema
    (-0.7, 5.2, -4.6, 0.7, 6.6, -4.25, 'esmeralda', 8),
]
C['paladin_cabeza'] = anillo(10, 10.8, 5, 1.2, 'oro', 15)  # aureola que brilla
C['orco_cabeza'] = espejo([(-3.4, 0, -5.3, -2, 3.5, -4, 'hueso'), (-3.2, 3.5, -5.1, -2.3, 5.2, -4.3, 'hueso'), (-3.1, 5.2, -4.9, -2.6, 5.9, -4.5, 'hueso')])
C['triton_cabeza'] = [
    *espejo([(-6, 3, 0.5, -4, 7, 1.3, 'aqua'), (-8, 4, 0.7, -6, 8, 1.1, 'aqua2'), (-4.4, 2, -3, -4, 4, 0, 'aqua2')]),
    (-0.4, 8, -2, 0.4, 10, 4, 'aqua'), (-0.35, 10, 0, 0.35, 11.5, 4.2, 'aqua2'), (-0.3, 11.5, 2, 0.3, 12.5, 4.5, 'aqua2'),
]
C['gnomo_cabeza'] = [
    (-5, 7, -5, 5, 8, 5, 'rojo'), (-4.3, 8, -4.3, 4.3, 10, 4.3, 'rojo'), (-3.5, 10, -3.2, 3.5, 12, 3.8, 'rojo'),
    (-2.6, 12, -2.1, 2.6, 14, 3.1, 'rojo'), (-1.8, 14, -0.8, 1.8, 16, 2.8, 'rojo'), (-1, 16, 0.6, 1, 18, 2.6, 'rojo'),
    (-0.8, 17.5, 2.4, 0.8, 19, 4.4, 'blanco'),       # pompón caído
    (-3, -1, -4.6, 3, 3, -4, 'blanco'), (-2, -3, -4.5, 2, -1, -4.1, 'blanco'),  # barbita blanca
]
C['draconido_cabeza'] = espejo([
    (-3.5, 7, 0, -1.5, 9, 2, 'cuerno'), (-3.4, 8.5, 2, -1.9, 10.5, 4, 'cuerno'), (-3.2, 9.5, 4, -2.2, 11, 6, 'cuerno'),
    (-3, 10.3, 6, -2.4, 11.2, 7.5, 'hueso'), (-4.45, 2, -3, -4, 4, 0, 'escama'), (-4.45, 4.5, -2, -4, 5.5, 1, 'escama')])
C['draconido_cuerpo'] = [
    *espejo([(-9, -3, 2.1, -1, -2, 2.9, 'cuerno'), (-3, -8, 2.3, -1, -3, 2.6, 'membrana'), (-6, -7, 2.3, -3, -3, 2.6, 'membrana'),
             (-9, -5, 2.3, -6, -3, 2.6, 'membrana')]),
    (-1.2, -12, 2, 1.2, -10, 4, 'escama'), (-1, -13, 4, 1, -11.5, 7, 'escama'), (-0.8, -14, 7, 0.8, -12.8, 10, 'escama'),
    (-0.5, -14.3, 10, 0.5, -13.3, 12, 'hueso'),
]
C['faerie_cuerpo'] = espejo([
    (-3, -7, 2.2, -1, 0, 2.5, 'ala', 6), (-6, -6, 2.2, -3, 2, 2.5, 'ala', 6), (-9, -4, 2.2, -6, 3, 2.5, 'ala', 6),
    (-11, -2, 2.2, -9, 3, 2.5, 'ala', 6), (-3, -11, 2.2, -1, -7, 2.5, 'ala', 6), (-6, -12, 2.2, -3, -8, 2.5, 'ala', 6)])
C['sombrio_cabeza'] = [
    (-4.6, 8, -4.6, 4.6, 8.7, 4.6, 'capucha'), (-4.6, -1, 4, 4.6, 8, 4.6, 'capucha'),
    (-4.6, -1, -4.6, -4, 8, 4, 'capucha'), (4, -1, -4.6, 4.6, 8, 4, 'capucha'),
    (-4.6, 7.3, -5.3, 4.6, 8.7, -4.6, 'capucha'), (-4.3, 0, -4.5, 4.3, 2.6, -4, 'negro'),
]
C['licantropo_cabeza'] = espejo([(-4, 8, -0.5, -1.5, 10, 1, 'pelo'), (-3.6, 10, -0.4, -2, 11.5, 0.9, 'pelo'),
                                 (-3.2, 11.5, -0.3, -2.6, 12.3, 0.7, 'pelo'), (-3.5, 8.2, -0.6, -2, 10.5, -0.5, 'rosa')])
C['licantropo_cuerpo'] = [(-1.5, -12, 2, 1.5, -9, 4, 'pelo'), (-1.8, -14, 4, 1.8, -10, 7, 'pelo'),
                          (-1.5, -16, 7, 1.5, -12, 9.5, 'pelo'), (-1, -16, 9.5, 1, -13.5, 11, 'blanco')]
C['titan_cabeza'] = [*anillo(7, 9, 4.6, 0.7, 'piedra'),
                     *[(x - 0.6, 9, z - 0.6, x + 0.6, 11.5 if (x and z) else 10.5, z + 0.6, 'piedra2')
                       for x in (-4, 0, 4) for z in (-4, 0, 4) if (x, z) != (0, 0)]]
C['olimpico_cabeza'] = [*anillo(5.5, 6.3, 4.4, 0.4, 'oro2', sin_frente=True),
                        *espejo([(-4.9, 6, z, -4.4, 7.2, z + 1, 'oro') for z in (-3.5, -1.5, 0.5, 2.5)]),
                        *[(x, 6, 4.4, x + 1, 7.2, 4.9, 'oro') for x in (-3, -0.5, 2)],
                        *espejo([(-3.6, 6, -4.9, -2.6, 7.2, -4.4, 'oro')])]
C['vampiro_cuerpo'] = [(-5, -16, 2.2, 5, 0, 2.7, 'negro'), (-4.8, -15.5, 2.0, 4.8, -0.5, 2.2, 'sangre'),
                       (-4.9, 0, 4.3, 4.9, 4.5, 4.9, 'negro'), (-4.9, 0, -1, -4.3, 4, 4.3, 'negro'), (4.3, 0, -1, 4.9, 4, 4.3, 'negro'),
                       (-4.3, 0, 4.1, 4.3, 4.2, 4.3, 'sangre')]

def generar():
    tex = Image.new('RGBA', (LADO * 4, LADO * 4), (0, 0, 0, 0))
    for i, n in enumerate(NOMBRES):
        c, f = (i % LADO) * 4, (i // LADO) * 4
        for x in range(4):
            for y in range(4):
                tex.putpixel((c + x, f + y), PALETA[n])
    dtex = os.path.join(RAIZ, 'assets/elatico/textures/item'); os.makedirs(dtex, exist_ok=True)
    tex.save(os.path.join(dtex, 'cosmeticos.png'))
    dmod = os.path.join(RAIZ, 'assets/elatico/models/item/cosmetico'); os.makedirs(dmod, exist_ok=True)
    dit = os.path.join(RAIZ, 'assets/elatico/items/cosmetico'); os.makedirs(dit, exist_ok=True)
    for nombre, cajas in C.items():
        modelo = {'textures': {'p': 'elatico:item/cosmeticos', 'particle': 'elatico:item/cosmeticos'},
                  'ambientocclusion': False, 'elements': [caja(*c) for c in cajas]}
        json.dump(modelo, open(os.path.join(dmod, nombre + '.json'), 'w'), indent=1)
        json.dump({'model': {'type': 'minecraft:model', 'model': 'elatico:item/cosmetico/' + nombre}},
                  open(os.path.join(dit, nombre + '.json'), 'w'), indent=1)
    print(len(C), 'cosméticos generados')

if __name__ == '__main__':
    generar()
