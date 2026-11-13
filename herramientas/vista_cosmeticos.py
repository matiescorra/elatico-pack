"""Vista previa de los cosméticos sobre un jugador (rasterizador simple con z-buffer)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cosmeticos import C, PALETA

def hexa(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))+(255,)
JUG=[((-4,-24,-2,4,-12,2),hexa('#3b4f8a')),((-4,-12,-2,4,0,2),hexa('#2f8f9d')),((-8,-12,-2,-4,0,2),hexa('#c99070')),
     ((4,-12,-2,8,0,2),hexa('#c99070')),((-4,0,-4,4,8,4),hexa('#d9a37a')),((-3,3,-4.02,-1,4,-4.01),(255,255,255,255)),
     ((1,3,-4.02,3,4,-4.01),(255,255,255,255)),((-2,3,-4.03,-1,4,-4.02),(60,60,160,255)),((2,3,-4.03,3,4,-4.02),(60,60,160,255)),
     ((-4,6,-4.02,4,8,4.02),hexa('#4a2e1a'))]
SOMBRA={'up':1.0,'down':0.5,'north':0.8,'south':0.8,'east':0.6,'west':0.6}

def render(cajas, yaw, pitch=20, W=260, H=380, esc=7.0):
    img=np.full((H,W,3),245,float); zb=np.full((H,W),1e9)
    cy,sy=math.cos(math.radians(yaw)),math.sin(math.radians(yaw)); cp,sp=math.cos(math.radians(pitch)),math.sin(math.radians(pitch))
    def proy(p):
        x,y,z=p; x2=x*cy-z*sy; z2=x*sy+z*cy  # giro en y
        y3=y*cp-z2*sp; z3=y*sp+z2*cp       # inclinación
        return W/2+x2*esc, H*0.40-y3*esc, z3
    yy,xx=np.mgrid[0:H,0:W]
    for (x0,y0,z0,x1,y1,z1),col in cajas:
        V=lambda a,b,c:(a,b,c)
        caras={'north':[V(x0,y0,z0),V(x1,y0,z0),V(x1,y1,z0),V(x0,y1,z0)],'south':[V(x0,y0,z1),V(x0,y1,z1),V(x1,y1,z1),V(x1,y0,z1)],
               'west':[V(x0,y0,z0),V(x0,y1,z0),V(x0,y1,z1),V(x0,y0,z1)],'east':[V(x1,y0,z0),V(x1,y0,z1),V(x1,y1,z1),V(x1,y1,z0)],
               'down':[V(x0,y0,z0),V(x0,y0,z1),V(x1,y0,z1),V(x1,y0,z0)],'up':[V(x0,y1,z0),V(x1,y1,z0),V(x1,y1,z1),V(x0,y1,z1)]}
        a=col[3]/255
        for nombre,q in caras.items():
            P=[proy(p) for p in q]
            for tri in ((P[0],P[1],P[2]),(P[0],P[2],P[3])):
                (ax,ay,az),(bx,by,bz),(cx,cy_,cz)=tri
                d=(by-cy_)*(ax-cx)+(cx-bx)*(ay-cy_)
                if abs(d)<1e-9: continue
                x0b,x1b=int(max(0,min(ax,bx,cx))),int(min(W-1,max(ax,bx,cx))+1); y0b,y1b=int(max(0,min(ay,by,cy_))),int(min(H-1,max(ay,by,cy_))+1)
                if x0b>=x1b or y0b>=y1b: continue
                X=xx[y0b:y1b,x0b:x1b]+0.5; Y=yy[y0b:y1b,x0b:x1b]+0.5
                l1=((by-cy_)*(X-cx)+(cx-bx)*(Y-cy_))/d; l2=((cy_-ay)*(X-cx)+(ax-cx)*(Y-cy_))/d; l3=1-l1-l2
                m=(l1>=-1e-6)&(l2>=-1e-6)&(l3>=-1e-6)
                Z=l1*az+l2*bz+l3*cz
                zsub=zb[y0b:y1b,x0b:x1b]; m&=Z<zsub
                c=np.array(col[:3],float)*SOMBRA[nombre]
                sub=img[y0b:y1b,x0b:x1b]
                if a>=0.99:
                    sub[m]=c; zsub[m]=Z[m]
                else:
                    sub[m]=sub[m]*(1-a)+c*a
    return Image.fromarray(img.clip(0,255).astype(np.uint8))

def ordenar(cajas):  # translúcidos al final
    return sorted(cajas,key=lambda c:c[1][3]<255)

razas=['enano','elfo','paladin','orco','triton','gnomo','draconido','faerie','sombrio','licantropo','titan','olimpico','vampiro']
NOM={'paladin':'Paladín','triton':'Tritón','draconido':'Dracónido','sombrio':'Sombrío','licantropo':'Licántropo','titan':'Titán','olimpico':'Olímpico'}
tiles=[]
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
except Exception: f=None
for r in razas:
    cos=[(c[:6],PALETA[c[6]]) for p in ('cabeza','cuerpo') for c in C.get(f'{r}_{p}',[])]
    todas=ordenar(JUG+cos)
    a=render(todas,-35+180); b=render(todas,145+180)  # frente 3/4 y espalda 3/4
    t=Image.new('RGB',(520,410),(245,245,245)); t.paste(a,(0,30)); t.paste(b,(260,30))
    ImageDraw.Draw(t).text((10,6),NOM.get(r,r.capitalize()),fill=(40,40,40),font=f); tiles.append(t)
cols=4; filas=(len(tiles)+cols-1)//cols
hoja=Image.new('RGB',(520*cols,410*filas),(245,245,245))
for i,t in enumerate(tiles): hoja.paste(t,((i%cols)*520,(i//cols)*410))
hoja.save(sys.argv[1]); print('ok')
