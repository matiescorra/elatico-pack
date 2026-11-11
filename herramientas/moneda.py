from PIL import Image, ImageDraw, ImageFont
import math
P={'o':(74,44,10),'G':(255,236,140),'g':(246,190,40),'d':(196,128,18),'R':(122,22,18),'r':(222,52,40),
   'y':(255,222,120),'k':(28,20,16),'w':(255,255,255),'p':(240,120,110),'b':(150,40,30)}
def moneda():
    im=Image.new('RGBA',(16,16),(0,0,0,0)); c=7.5
    for y in range(16):
        for x in range(16):
            d=math.hypot(x-c,y-c)
            if d>7.6: continue
            if d>6.6: col=P['o']
            elif d>5.5:
                # borde: brillo arriba-izquierda, sombra abajo-derecha
                ang=math.atan2(y-c,x-c); col=P['G'] if (x+y)<13 else (P['d'] if (x+y)>17 else P['g'])
            else: col=P['g']
            im.putpixel((x,y),col+(255,))
    casa=["....bR....",
          "...RrrR...",
          "..RrrrrR..",
          ".RrrrrrrR.",
          "RrrrrrrrrR",
          ".oyyyyyyo.",
          ".oykyykyo.",
          ".opyyyypo.",
          ".okwwwwko.",
          ".oooooooo."]
    for j,row in enumerate(casa):
        for i,ch in enumerate(row):
            if ch!='.': im.putpixel((3+i,3+j),P[ch]+(255,))
    return im
m=moneda(); m.save('moneda16.png')
# vista previa: ícono grande + cómo se ve en el texto
prev=Image.new('RGBA',(620,250),(46,46,54,255)); d=ImageDraw.Draw(prev)
prev.alpha_composite(m.resize((192,192),Image.NEAREST),(20,30))
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
t=m.resize((24,24),Image.NEAREST)
for i,(txt,y) in enumerate([("Dinero de Mati: ",60),("[Tienda] 16× Diamante ",110),("Encargo cumplido +",160)]):
    d.text((240,y),txt,font=f,fill=(240,240,240)); w=d.textlength(txt,font=f)
    prev.alpha_composite(t,(240+int(w),y+2)); d.text((240+w+28,y),["250","40","35"][i],font=f,fill=(255,200,60))
d.text((240,205),"(así en el chat, carteles y tablón)",font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16),fill=(170,170,180))
prev.save('/mnt/user-data/outputs/moneda-atipeso.png')
