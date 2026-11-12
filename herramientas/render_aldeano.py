# Render 3D simple (ortográfico) del modelo de aldeano, para comparar texturas
import math, numpy as np
from PIL import Image, ImageDraw
def caja(u, v, x, y, z, w, h, d, infl=0.0, piv=(0, 0, 0), rotx=0.0):
    return dict(u=u, v=v, o=(x - infl, y - infl, z - infl), s=(w + 2 * infl, h + 2 * infl, d + 2 * infl), tw=w, th=h, td=d, piv=piv, rotx=rotx)
MODELO = [caja(0, 0, -4, -10, -4, 8, 10, 8), caja(32, 0, -4, -10, -4, 8, 10, 8, .5), caja(24, 0, -1, -3, -6, 2, 4, 2),
          caja(16, 20, -4, 0, -3, 8, 12, 6), caja(0, 38, -4, 0, -3, 8, 20, 6, .5),
          caja(44, 22, -8, -2, -2, 4, 8, 4, piv=(0, 3, -1), rotx=-.75), caja(44, 22, 4, -2, -2, 4, 8, 4, piv=(0, 3, -1), rotx=-.75),
          caja(40, 38, -4, 2, -2, 8, 4, 4, piv=(0, 3, -1), rotx=-.75),
          caja(0, 22, -2, 0, -2, 4, 12, 4, piv=(-2, 12, 0)), caja(0, 22, -2, 0, -2, 4, 12, 4, piv=(2, 12, 0))]
def caras(c):
    u, v = c['u'], c['v']; w, h, d = c['tw'], c['th'], c['td']
    # (normal, rect UV (u0,v0,ancho,alto), función que da el punto 3D para (s,t) en [0,1])
    (x0, y0, z0), (sw, sh, sd) = c['o'], c['s']; x1, y1, z1 = x0 + sw, y0 + sh, z0 + sd
    return [((0, 0, -1), (u + d, v + d, w, h), lambda s, t: (x1 - s * sw, y0 + t * sh, z0)),        # frente (-z)
            ((0, 0, 1), (u + 2 * d + w, v + d, w, h), lambda s, t: (x0 + s * sw, y0 + t * sh, z1)),  # atrás
            ((-1, 0, 0), (u + d + w, v + d, d, h), lambda s, t: (x0, y0 + t * sh, z0 + s * sd)),     # izquierda
            ((1, 0, 0), (u, v + d, d, h), lambda s, t: (x1, y0 + t * sh, z1 - s * sd)),              # derecha
            ((0, -1, 0), (u + d, v, w, d), lambda s, t: (x1 - s * sw, y0, z1 - t * sd)),             # arriba
            ((0, 1, 0), (u + d + w, v, w, d), lambda s, t: (x1 - s * sw, y1, z0 + t * sd))]          # abajo
def render(tex, capas=(), escala=14, yaw=-35, pitch=18):
    T = [np.asarray(t.convert('RGBA')) for t in (tex,) + tuple(capas)]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    def proj(p, c):
        x, y, z = p; px_, py_, pz_ = c['piv']
        if c['rotx']:
            ca, sa = math.cos(c['rotx']), math.sin(c['rotx']); y, z = y * ca - z * sa, y * sa + z * ca
        x, y, z = x + px_, y + py_, z + pz_
        x, z = x * cy - z * sy, x * sy + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z
    polys = []
    for c in MODELO:
        for n, (u0, v0, uw, vh), f in caras(c):
            for i in range(uw):
                for j in range(vh):
                    col = None
                    for t in T:
                        if 0 <= v0 + j < t.shape[0] and 0 <= u0 + i < t.shape[1] and t[v0 + j, u0 + i, 3] > 20: col = t[v0 + j, u0 + i]
                    if col is None: continue
                    pts = [proj(f(a / uw, b / vh), c) for a, b in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))]
                    zc = sum(p[2] for p in pts) / 4
                    luz = {(0, -1, 0): 1.0, (0, 0, -1): .92, (1, 0, 0): .78, (-1, 0, 0): .78, (0, 0, 1): .7, (0, 1, 0): .55}[n]
                    polys.append((zc, pts, tuple(int(min(255, k * luz)) for k in col[:3])))
    polys.sort(key=lambda q: -q[0])
    W = 40 * escala; im = Image.new('RGBA', (W, int(W * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _, pts, col in polys:
        d.polygon([(W / 2 + p[0] * escala, W * .45 + p[1] * escala) for p in pts], fill=col)
    return im
