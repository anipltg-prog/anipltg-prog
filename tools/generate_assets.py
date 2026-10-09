"""Alpha Numeric software-profile artwork. Requires Python 3 and Pillow.

The code and interfaces are branded concept art, not a product screenshot,
an executable example, or live operating data. Original logos are retained.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
BG = (6, 10, 20)
PANEL = (10, 18, 33)
BLUE = (42, 151, 255)
CYAN = (109, 221, 255)
YELLOW = (255, 226, 0)
WHITE = (242, 247, 255)
MUTED = (149, 167, 191)
LINE = (33, 50, 75)


def font(size, bold=False, mono=False):
    if mono:
        paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "DejaVuSansMono.ttf", "Consolas.ttf"]
    else:
        weight = "Bold" if bold else "Regular"
        paths = [f"/usr/share/fonts/opentype/urw-base35/NimbusSans-{weight}.otf",
                 f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
                 f"DejaVuSans{'-Bold' if bold else ''}.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for path in paths:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    return ImageFont.load_default(size=size)


def text(d, xy, value, size=20, fill=WHITE, bold=False, mono=False):
    d.text(xy, value, font=font(size, bold, mono), fill=fill, anchor="lt")


def fit(d, xy, value, size, width, fill=WHITE, bold=False, mono=False):
    while size > 8 and d.textlength(value, font=font(size, bold, mono)) > width: size -= 1
    text(d, xy, value, size, fill, bold, mono)


def base(w, h, glow=True):
    image = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(image)
    if glow:
        layer = Image.new("RGB", (w // 4, h // 4), BG)
        pixels = layer.load()
        for y in range(layer.height):
            for x in range(layer.width):
                p = math.exp(-(((x - layer.width * .81) / (layer.width * .47)) ** 2 +
                               ((y - layer.height * .27) / (layer.height * .81)) ** 2) * 2.4)
                pixels[x, y] = (round(6 + p * 6), round(10 + p * 16), round(20 + p * 35))
        image = layer.resize((w, h), Image.Resampling.BICUBIC)
        d = ImageDraw.Draw(image)
    for x in range(22, w, 32):
        for y in range(20, h, 32):
            d.ellipse((x, y, x + 1, y + 1), fill=(22, 35, 53))
    d.rectangle((0, 0, w - 1, h - 1), outline=LINE)
    return image


def logo(image, filename, xy, width):
    im = Image.open(ASSETS / filename).convert("RGBA")
    im = im.crop(im.getbbox())
    im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    image.paste(im, xy, im)


def rounded(d, box, fill=PANEL, outline=LINE, radius=14, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def glow_point(image, xy, color, radius=3):
    layer = Image.new("RGBA", image.size)
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse((x - radius * 3, y - radius * 3, x + radius * 3, y + radius * 3), fill=(*color, 90))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 2))
    result = Image.alpha_composite(image.convert("RGBA"), layer)
    d = ImageDraw.Draw(result)
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, 255))
    return result.convert("RGB")


def chevron(d, x, y, color=BLUE, scale=1):
    d.line([(x, y), (x + 14 * scale, y + 8 * scale), (x, y + 16 * scale)], fill=color, width=max(1, round(3 * scale)))


def draw_icon(d, name, x, y, color=BLUE, scale=1):
    def p(a, b): return (x + a * scale, y + b * scale)
    def line(points, width=2): d.line([p(*a) for a in points], fill=color, width=max(1, round(width * scale)), joint="curve")
    def rect(box, r=0):
        points=[p(box[0],box[1]),p(box[2],box[3])]
        if r: d.rounded_rectangle(points, radius=r*scale, outline=color, width=max(1, round(2*scale)))
        else:d.rectangle(points, outline=color, width=max(1, round(2*scale)))
    if name == "interface":
        rect((0, 2, 34, 28), 3);line([(0, 10), (34, 10)])
        rect((4, 14, 13, 24));line([(18, 15), (29, 15)]);line([(18, 21), (26, 21)])
    elif name == "device":
        rect((8, 4, 27, 28), 3);rect((12, 8, 23, 16))
        line([(15, 23), (20, 23)])
        line([(3, 9), (0, 13), (0, 20), (3, 24)])
        line([(32, 9), (35, 13), (35, 20), (32, 24)])
    elif name == "code":
        line([(10, 5), (0, 16), (10, 27)])
        line([(25, 5), (35, 16), (25, 27)])
        line([(21, 2), (14, 30)])
    elif name == "automation":
        for a, v in [(4, 9), (17, 24), (30, 14)]:
            line([(a, 0), (a, 32)])
            d.rectangle([p(a-4, v-3), p(a+4, v+3)],fill=PANEL,outline=color,width=max(1,round(2*scale)))
    elif name == "data":
        line([(1, 1), (1, 30), (35, 30)])
        line([(5, 23), (13, 15), (20, 19), (31, 5)])
        for a,b in [(5,23),(13,15),(20,19),(31,5)]:
            d.ellipse([p(a-2,b-2),p(a+2,b+2)],fill=color)
    elif name == "chip":
        rect((7, 7, 28, 28), 4)
        for v in (11,18,25):
            line([(v,0),(v,7)]);line([(v,28),(v,35)])
            line([(0,v),(7,v)]);line([(28,v),(35,v)])
    elif name == "lighting":
        d.ellipse([p(7,0),p(28,22)],outline=color,width=max(1,round(2*scale)))
        line([(12,21),(12,28),(23,28),(23,21)]);line([(14,32),(21,32)])
    elif name == "sensor":
        d.ellipse([p(12,13),p(23,24)],outline=color,width=max(1,round(2*scale)))
        d.arc([p(5,6),p(30,31)],180,0,fill=color,width=max(1,round(2*scale)))
        d.arc([p(0,1),p(35,36)],180,0,fill=color,width=max(1,round(2*scale)))


def path_point(path, u):
    lengths=[math.dist(a,b) for a,b in zip(path,path[1:])]
    remain=u*sum(lengths)
    for (a,b), length in zip(zip(path,path[1:]),lengths):
        if remain <= length:
            t=remain/length
            return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
        remain-=length
    return path[-1]


def export_animation(name, frames, duration):
    frames[0].save(ASSETS / f"{name}.png", optimize=True)
    # A shared palette keeps the static background stable while GIF stores frame differences.
    samples=Image.new("RGB",(frames[0].width,frames[0].height*4))
    for i,n in enumerate([0,len(frames)//4,len(frames)//2,3*len(frames)//4]):
        samples.paste(frames[n],(0,i*frames[0].height))
    palette=samples.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(ASSETS/f"{name}.gif",save_all=True,append_images=indexed[1:],
                    duration=duration,loop=0,disposal=1,optimize=True)


def software_hero():
    w,h=1200,660
    still=base(w,h)
    d=ImageDraw.Draw(still)
    logo(still,"logo-innovations.png",(56,35),285)
    rounded(d,(922,43,1144,77),fill=(11,22,40),outline=(35,78,127),radius=17)
    text(d,(943,55),"SOFTWARE × SYSTEMS",13,CYAN,mono=True)
    text(d,(59,145),"BUILDING CONNECTED INTELLIGENCE",13,MUTED,mono=True)
    text(d,(55,182),"Code.",92,WHITE,bold=True)
    text(d,(55,279),"Connect.",92,WHITE,bold=True)
    text(d,(55,376),"Create.",92,BLUE,bold=True)
    text(d,(59,491),"Digital experiences for a",24,MUTED)
    text(d,(59,522),"connected physical world.",24,MUTED)

    # A recognizable editor composition, with the original company identity outside it.
    shadow=Image.new("RGBA",still.size)
    sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((631,154,1156,584),radius=24,fill=(0,75,185,42))
    shadow=shadow.filter(ImageFilter.GaussianBlur(22))
    still=Image.alpha_composite(still.convert("RGBA"),shadow).convert("RGB")
    d=ImageDraw.Draw(still)
    rounded(d,(642,160,1144,574),fill=(8,16,30),outline=(53,88,135),radius=15)
    d.line((643,209,1143,209),fill=LINE,width=1)
    for x,c in [(665,(234,95,98)),(684,(238,188,72)),(703,(81,184,128))]:
        d.ellipse((x,179,x+8,187),fill=c)
    text(d,(727,177),"systems.connect",15,WHITE,mono=True)
    text(d,(1040,181),"CONCEPT",10,MUTED,mono=True)
    d.line((685,228,685,442),fill=(25,40,64),width=1)
    for i in range(8):text(d,(656,243+i*27),str(i+1).zfill(2),11,(74,94,122),mono=True)
    d.line((665,471,1121,471),fill=LINE,width=1)
    draw_icon(d,"device",666,492,CYAN,.8)
    draw_icon(d,"chip",813,492,BLUE,.8)
    draw_icon(d,"interface",981,492,YELLOW,.8)
    text(d,(703,499),"devices",13,MUTED,mono=True)
    text(d,(850,499),"integrate",13,MUTED,mono=True)
    text(d,(1018,499),"interface",13,MUTED,mono=True)
    d.line((777,504,803,504),fill=LINE,width=2)
    d.line((950,504,969,504),fill=LINE,width=2)
    text(d,(666,544),"ILLUSTRATIVE CODE",10,(107,129,155),mono=True)
    d.line((56,609,1144,609),fill=LINE,width=1)
    terms=["WEB INTERFACES","CONNECTED DEVICES","AUTOMATION","BMS + IoT"]
    for i,value in enumerate(terms):
        x=59+i*282
        d.ellipse((x,631,x+5,636),fill=BLUE if i%2==0 else YELLOW)
        text(d,(x+15,628),value,12,MUTED,mono=True)

    lines=[
        [("const ",CYAN),("platform",WHITE),(" = {",MUTED)],
        [("  energy",BLUE),(":     ",MUTED),("\"visible\",",YELLOW)],
        [("  lighting",BLUE),(":   ",MUTED),("\"intelligent\",",YELLOW)],
        [("  automation",BLUE),(": ",MUTED),("\"connected\",",YELLOW)],
        [("  experience",BLUE),(": ",MUTED),("\"human\"",YELLOW)],
        [("};",MUTED)],
        [("",MUTED)],
        [("connect",CYAN),("(platform);",WHITE)],
    ]
    length=sum(len(value) for row in lines for value,_ in row)
    frames=[]
    # Start with the complete composition, then cycle through three software themes.
    phrases=["design.interfaces()","connect.devices()","visualize.systems()"]
    for i in range(80):
        phase=i/80
        image=still.copy()
        d=ImageDraw.Draw(image)
        theme=min(2,int(phase*3))
        phrase=phrases[theme]
        text(d,(59,567),"> ",21,YELLOW,mono=True)
        text(d,(88,567),phrase,21,CYAN,mono=True)
        if i%10<5:
            xx=88+d.textlength(phrase,font=font(21,mono=True))+4
            d.rectangle((xx,565,xx+10,588),fill=YELLOW)
        # A readable hold, a brief erase, and a progressive code reveal.
        if i < 22:count=length
        elif i < 26:count=round(length*(26-i)/4)
        elif i < 59:count=round(length*(i-26)/33)
        else:count=length
        remaining=count
        cursor=None
        for row,segments in enumerate(lines):
            xx=700;y=240+row*27
            row_length=sum(len(value) for value,_ in segments)
            if 0<remaining<row_length:
                rounded(d,(694,y-4,1128,y+24),fill=(15,33,56),outline=None,radius=4)
            for value,color in segments:
                visible=value[:max(0,remaining)]
                text(d,(xx,y),visible,18,color,mono=True)
                xx+=d.textlength(visible,font=font(18,mono=True))
                remaining-=len(value)
                if remaining<=0 and cursor is None:cursor=(xx,y)
        if cursor and i%10<5 and count<length:
            d.rectangle((cursor[0]+2,cursor[1]-1,cursor[0]+4,cursor[1]+18),fill=CYAN)
        packet_path=[(655,160),(1130,160),(1144,174),(1144,560),(1130,574),(656,574)]
        image=glow_point(image,path_point(packet_path,phase),BLUE,3)
        for j,(a,b) in enumerate([(777,803),(950,969)]):
            image=glow_point(image,(a+(b-a)*((phase*3+j*.4)%1),504),YELLOW if j else CYAN,2)
        frames.append(image)
    export_animation("alphanumeric-hero",frames,100)
    frames[0].resize((1280,704),Image.Resampling.LANCZOS).crop((0,0,1280,640)).save(ASSETS/"github-social-preview.png",optimize=True)
    mobile=base(600,925)
    md=ImageDraw.Draw(mobile)
    logo(mobile,"logo-innovations.png",(36,29),270)
    text(md,(36,135),"BUILDING CONNECTED INTELLIGENCE",12,MUTED,mono=True)
    fit(md,(33,174),"Code. Connect.",69,533,WHITE,True)
    text(md,(34,251),"Create.",80,BLUE,bold=True)
    text(md,(37,349),"Digital experiences for a connected world.",21,MUTED)
    md.line((36,883,564,883),fill=LINE,width=1)
    text(md,(36,902),"INTERFACES / DEVICES / INTELLIGENCE",12,CYAN,mono=True)
    mobile_frames=[]
    for i,frame in enumerate(frames):
        image=mobile.copy()
        editor=frame.crop((642,159,1145,575)).resize((528,437),Image.Resampling.LANCZOS)
        image.paste(editor,(36,419))
        d=ImageDraw.Draw(image)
        phrase=phrases[min(2,int((i/80)*3))]
        text(d,(37,387),"> ",20,YELLOW,mono=True)
        text(d,(65,387),phrase,20,CYAN,mono=True)
        if i%10<5:
            xx=65+d.textlength(phrase,font=font(20,mono=True))+4
            d.rectangle((xx,385,xx+9,407),fill=YELLOW)
        mobile_frames.append(image)
    export_animation("alphanumeric-hero-mobile",mobile_frames,100)


def connection_animation():
    w,h=1200,420
    still=base(w,h)
    d=ImageDraw.Draw(still)
    text(d,(48,34),"FROM SIGNAL TO SOFTWARE",13,CYAN,mono=True)
    text(d,(46,65),"Sense. Connect. Visualize.",43,WHITE,bold=True)
    text(d,(936,40),"CONNECTION CONCEPT",11,MUTED,mono=True)
    devices=[("METERS","device"),("SENSORS","sensor"),("LIGHTING","lighting"),("CONTROLS","automation")]
    for j,(label,symbol) in enumerate(devices):
        yy=144+j*54
        rounded(d,(48,yy,310,yy+44),fill=(10,21,38),outline=LINE,radius=8)
        draw_icon(d,symbol,62,yy+9,BLUE if j%2==0 else CYAN,.72)
        text(d,(102,yy+16),label,13,WHITE,mono=True)

    center=(579,252)
    for radius,color in [(77,(28,62,97)),(64,(37,89,146))]:
        d.ellipse((center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius),outline=color,width=1)
    rounded(d,(535,208,623,296),fill=(12,30,55),outline=BLUE,radius=18,width=2)
    text(d,(556,228),"AN",37,WHITE,bold=True)
    text(d,(531,346),"INTEGRATE",12,CYAN,mono=True)
    paths=[]
    for j in range(4):
        yy=166+j*54
        path=[(310,yy),(388+j*13,yy),(439+j*13,252),(502,252)]
        paths.append(path);d.line(path,fill=(34,59,88),width=2,joint="curve")
    out_path=[(656,252),(741,252),(767,226)]
    d.line(out_path,fill=(45,75,104),width=2,joint="curve")

    rounded(d,(766,146,1150,328),fill=(9,18,33),outline=(46,74,112),radius=12)
    d.line((767,182,1149,182),fill=LINE,width=1)
    for x in [785,798,811]:d.ellipse((x,162,x+5,167),fill=(85,116,150))
    text(d,(835,159),"your interface",12,WHITE,mono=True)
    for j in range(3):
        xx=786+j*113
        rounded(d,(xx,197,xx+98,228),fill=(17,34,54),outline=None,radius=6)
        text(d,(xx+10,209),["EQUIPMENT","CONTROL","INSIGHT"][j],10,CYAN,mono=True)
    for yy in [246,268,290]:d.line((786,yy,1126,yy),fill=(26,41,62),width=1)
    # Unlabelled waveform is symbolic interface artwork, with no numerical values.
    wave=[(786+k*8,270+15*math.sin(k*.27)+9*math.cos(k*.61)) for k in range(43)]
    d.line(wave,fill=BLUE,width=2,joint="curve")
    text(d,(841,346),"MONITOR / UNDERSTAND / CONTROL",11,MUTED,mono=True)
    d.line((48,383,1150,383),fill=LINE,width=1)
    text(d,(48,400),"FIELD DEVICES",10,MUTED,mono=True)
    text(d,(475,400),"CONNECTED INTELLIGENCE",10,MUTED,mono=True)
    text(d,(914,400),"USER EXPERIENCE",10,MUTED,mono=True)
    frames=[]
    for i in range(60):
        phase=i/60
        image=still.copy()
        for j,path in enumerate(paths):
            u=(phase*1.4+j*.21)%1
            image=glow_point(image,path_point(path,u),BLUE if j%2==0 else CYAN,3)
        image=glow_point(image,path_point(out_path,(phase*2)%1),YELLOW,3)
        d=ImageDraw.Draw(image)
        angle=int(phase*360)
        d.arc((502,175,656,329),angle,angle+62,fill=CYAN,width=3)
        d.arc((502,175,656,329),angle+180,angle+202,fill=YELLOW,width=3)
        xx=786+340*phase
        d.line((xx,239,xx,303),fill=(45,108,155),width=1)
        image=glow_point(image,(xx,270+15*math.sin(phase*42*.27)+9*math.cos(phase*42*.61)),YELLOW,2)
        frames.append(image)
    export_animation("connected-software",frames,100)
    mobile=base(600,872)
    d=ImageDraw.Draw(mobile)
    text(d,(36,28),"FROM SIGNAL TO SOFTWARE",12,CYAN,mono=True)
    text(d,(34,61),"Sense. Connect.",43,WHITE,bold=True)
    text(d,(34,113),"Visualize.",43,WHITE,bold=True)
    mobile_paths=[]
    for j,(label,symbol) in enumerate(devices):
        xx=36+(j%2)*276;yy=200+(j//2)*64
        rounded(d,(xx,yy,xx+252,yy+46),fill=PANEL,outline=LINE,radius=8)
        draw_icon(d,symbol,xx+13,yy+10,BLUE if j%2==0 else CYAN,.72)
        text(d,(xx+53,yy+17),label,13,WHITE,mono=True)
        start=(xx+126,yy+46)
        if j<2:
            side=20 if j%2==0 else 580
            path=[start,(start[0],254),(side,254),(side,343),(245 if j%2==0 else 355,382)]
        else:
            path=[start,(start[0],328),(265 if j%2==0 else 335,367)]
        mobile_paths.append(path);d.line(path,fill=(37,69,101),width=2,joint="curve")
    d.ellipse((223,349,377,503),outline=(37,80,128),width=1)
    rounded(d,(256,382,344,470),fill=(12,30,55),outline=BLUE,radius=18,width=2)
    text(d,(277,402),"AN",37,WHITE,bold=True)
    text(d,(252,517),"INTEGRATE",12,CYAN,mono=True)
    out=[(300,541),(300,586)]
    d.line(out,fill=LINE,width=2)
    d.line((36,816,564,816),fill=LINE,width=1)
    text(d,(36,837),"CONNECTED DEVICES / DIGITAL EXPERIENCE",12,MUTED,mono=True)
    mobile_frames=[]
    for i,frame in enumerate(frames):
        phase=i/60
        image=mobile.copy()
        for j,path in enumerate(mobile_paths):
            image=glow_point(image,path_point(path,(phase*1.4+j*.21)%1),BLUE if j%2==0 else CYAN,3)
        image=glow_point(image,path_point(out,(phase*2)%1),YELLOW,3)
        d=ImageDraw.Draw(image)
        angle=int(phase*360)
        d.arc((223,349,377,503),angle,angle+62,fill=CYAN,width=3)
        d.arc((223,349,377,503),angle+180,angle+202,fill=YELLOW,width=3)
        interface=frame.crop((766,146,1151,329)).resize((528,251),Image.Resampling.LANCZOS)
        image.paste(interface,(36,565))
        mobile_frames.append(image)
    export_animation("connected-software-mobile",mobile_frames,100)


def capability_card(filename,index,title,subtitle,lines,symbol,color):
    image=base(560,260,False)
    d=ImageDraw.Draw(image)
    d.line((0,0,560,0),fill=color,width=3)
    draw_icon(d,symbol,34,32,color,1.1)
    text(d,(442,36),f"0{index} /",13,MUTED,mono=True)
    text(d,(34,99),title,34,WHITE,bold=True)
    text(d,(35,147),subtitle,12,color,mono=True)
    for j,value in enumerate(lines):fit(d,(35,184+j*25),value,18,488,MUTED)
    image.save(ASSETS/filename,optimize=True)


def brand_panel(source,destination,description):
    image=base(560,236,False)
    d=ImageDraw.Draw(image)
    logo(image,source,(43,32),474)
    d.line((43,182,517,182),fill=LINE,width=1)
    fit(d,(43,205),description,12,474,MUTED,mono=True)
    image.save(ASSETS/destination,optimize=True)


def capability_boards():
    names=["capability-interfaces.png","capability-integration.png","capability-automation.png","capability-intelligence.png"]
    desktop=base(1200,594,False)
    mobile=base(600,1122,False)
    for i,name in enumerate(names):
        card=Image.open(ASSETS/name)
        desktop.paste(card,(32+(i%2)*576,28+(i//2)*278))
        mobile.paste(card,(20,20+i*274))
    desktop.save(ASSETS/"software-capabilities.png",optimize=True)
    mobile.save(ASSETS/"software-capabilities-mobile.png",optimize=True)


def link(filename,label,width,color):
    image=Image.new("RGB",(width*2,72),BG)
    d=ImageDraw.Draw(image)
    rounded(d,(1,1,width*2-2,70),fill=(11,23,41),outline=(41,70,105),radius=11,width=2)
    d.rectangle((0,16,5,56),fill=color)
    text(d,(28,25),label,23,WHITE,bold=True)
    text(d,(width*2-43,23),"↗",26,color)
    image.save(ASSETS/filename,optimize=True)


def footer():
    image=base(1200,176)
    d=ImageDraw.Draw(image)
    text(d,(47,33),"Let's build what's next.",43,WHITE,bold=True)
    text(d,(49,100),"SOFTWARE / AUTOMATION / CONNECTED INTELLIGENCE",14,CYAN,mono=True)
    chevron(d,1058,54,BLUE,3.2);chevron(d,1110,54,YELLOW,3.2)
    image.save(ASSETS/"software-footer.png",optimize=True)


if __name__=="__main__":
    for filename in ["logo-innovations.png","logo-engineering-technology.png"]:
        if not (ASSETS/filename).is_file():raise SystemExit(f"Missing official logo: {filename}")
    software_hero()
    connection_animation()
    capability_card("capability-interfaces.png",1,"Interfaces that inform.","DASHBOARDS / EQUIPMENT / TRENDS",
                    ["Make connected systems readable.","Turn operational information into clear views."],"interface",BLUE)
    capability_card("capability-integration.png",2,"Devices that connect.","METERS / SENSORS / GATEWAYS",
                    ["Bring field signals into a digital layer.","Plan around the equipment already installed."],"device",CYAN)
    capability_card("capability-automation.png",3,"Controls that work.","LIGHTING / BUILDINGS / AUTOMATION",
                    ["Connect control with everyday operation.","Keep the experience practical and usable."],"automation",YELLOW)
    capability_card("capability-intelligence.png",4,"Information with context.","ALARMS / HISTORY / SITE VISIBILITY",
                    ["Organize events, equipment and trends.","Give operators a clearer view of their systems."],"data",BLUE)
    capability_boards()
    brand_panel("logo-innovations.png","brand-innovations.png","ENERGY / POWER / LIGHTING / AUTOMATION / R&D")
    brand_panel("logo-engineering-technology.png","brand-engineering-technology.png","LIGHTING / CONTROL / BMS / IoT")
    link("link-innovations.png","INNOVATIONS",150,BLUE)
    link("link-engineering-technology.png","ENGINEERING & TECHNOLOGY",247,YELLOW)
    link("link-contact.png","LET'S CONNECT",165,CYAN)
    footer()
    # Remove the superseded brochure visual. Other unrelated assets are preserved.
    (ASSETS/"connected-intelligence.png").unlink(missing_ok=True)
    for filename in sorted(ASSETS.iterdir()):print(f"{filename.name}: {filename.stat().st_size:,} bytes")
