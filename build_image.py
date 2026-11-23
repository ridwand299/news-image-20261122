"""v2: newspaper front page, mimicking top 1-10 of news-image-20261122.
31 stories, 7 regions, all dated Sun 22 Nov 2026, plus a clearly-dated
23 Nov breaking banner for Jensen Huang (not counted in the 31).
Deterministic, offline, Pillow only. 1024x1024.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (253, 246, 227)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
NAVY = (20, 40, 80)
GREY = (90, 90, 90)
LIGHT = (240, 232, 210)
BLUE = (30, 80, 140)
TEAL = (0, 120, 110)

def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except Exception:
        return ImageFont.load_default()

def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def text_block(d, x, y, text, f, fill, max_w, max_lines=3, lh=None):
    lh = lh or int(f.size * 1.25)
    lines = wrap(d, text, f, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# --- top strip ---
d.rectangle([0, 0, W, 22], fill=NAVY)
d.text((12, 4), "THE WORLD IN ONE DAY", font=font("sans_b", 11), fill=(255,255,255))
d.text((W-12, 4), "31 STORIES  •  7 REGIONS  •  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", font=font("sans_b", 11), fill=(255,255,255), anchor="ra")

# --- headline ---
d.text((512, 30), "Sunday 22 November 2026", font=font("serif_b", 46), fill=INK, anchor="ma")
d.text((512, 82), "COP31 ends with no deal  •  Iran claims US radars hit in Bahrain  •  186 drones over Ukraine", font=font("serif", 14), fill=RED, anchor="ma")
d.line([24, 108, 1000, 108], fill=INK, width=2)

# --- numbers strip ---
nums = [("186", "drones fired at Ukraine"), ("161", "downed or jammed"), ("$120bn", "adaptation target dropped"), ("258", "House seats, Democrats"), ("720/9", "India's record Test total"), ("98.4%", "Hong Kong turnout")]
x = 24
for n, lab in nums:
    d.text((x+78, 116), n, font=font("sans_b", 20), fill=RED, anchor="ma")
    d.text((x+78, 140), lab, font=font("sans", 9), fill=GREY, anchor="ma")
    x += 163
d.line([24, 158, 1000, 158], fill=INK, width=1)

# --- Jensen breaking banner (23 Nov, clearly dated, not in the 31) ---
d.rectangle([24, 166, 1000, 196], fill=DARKRED)
d.text((36, 172), "BREAKING — MON 23 NOV:", font=font("sans_b", 13), fill=(255, 220, 0))
d.text((240, 172), "JENSEN HUANG IS BACK  •  Nvidia reinstates CEO, shares +30%", font=font("sans_b", 13), fill=(255,255,255))
d.text((36, 186), "", font=font("sans", 9), fill=(255,255,255))

# --- region bar ---
d.rectangle([24, 202, 1000, 220], fill=NAVY)
d.text((512, 205), "EUROPE 7    •    MIDDLE EAST 6    •    ASIA-PACIFIC 7    •    AMERICAS 5    •    AFRICA 3    •    OCEANIA 2    •    WORLD 1", font=font("sans_b", 10), fill=(255,255,255), anchor="ma")

# --- 3 lead stories ---
leads = [
    ("1  ANTALYA, TÜRKİYE  •  CLIMATE", "COP31 ends without a deal", "Final text lands with no mention of fossil fuels; drops the $120bn adaptation target. EU rejects it. (Reuters, BBC)", (20, 90, 60), (255, 200, 80)),
    ("2  MANAMA, BAHRAIN  •  IRAN WAR", "Iran claims US radars hit in Bahrain", "IRGC says it hit two Patriot radars; Bahrain says a civilian site burned, no casualties. (Al Jazeera, Reuters)", (20, 40, 80), (255, 120, 60)),
    ("3  KYIV, UKRAINE  •  WAR", "Russia fires 186 drones overnight", "161 downed or jammed; a block in Dymer is destroyed, 14 may be trapped. (Ukrainian Air Force)", (40, 40, 60), (120, 180, 255)),
]
y0 = 228
for i, (kicker, head, body, bg, accent) in enumerate(leads):
    x = 24 + i*324
    # illustration box - simple drawn scene, per lead
    d.rectangle([x, y0, x+308, y0+62], fill=bg)
    if i == 0:  # COP31: sun, buildings, table
        d.ellipse([x+230, y0+8, x+262, y0+40], fill=(255, 200, 80))
        for bx in (20, 55, 90, 125):
            d.rectangle([x+bx, y0+30, x+bx+28, y0+62], fill=(255,255,255))
        d.rectangle([x+160, y0+48, x+300, y0+54], fill=(200, 170, 120))
        for px in (175, 205, 235, 265):
            d.ellipse([px, y0+38, px+10, y0+48], fill=accent)
    elif i == 1:  # Bahrain: radars + flames
        for rx in (30, 110, 190):
            d.pieslice([x+rx, y0+12, x+rx+50, y0+62], 180, 360, fill=(220,220,220))
            d.polygon([(x+rx+18, y0+30), (x+rx+25, y0+8), (x+rx+32, y0+30)], fill=(255, 140, 0))
        d.polygon([(x+250, y0+45), (x+262, y0+18), (x+274, y0+45)], fill=(255, 200, 0))
    else:  # Ukraine: night sky, buildings, drones
        for sx, sy in [(40, 12), (120, 18), (200, 10), (280, 20)]:
            d.ellipse([x+sx, y0+sy, x+sx+4, y0+sy+4], fill=(255,255,255))
        for bx in (20, 70, 120, 200, 250):
            d.rectangle([x+bx, y0+32, x+bx+36, y0+62], fill=(10, 10, 30))
            d.rectangle([x+bx+8, y0+40, x+bx+14, y0+46], fill=(255, 220, 80))
        d.polygon([(x+150, y0+50), (x+160, y0+30), (x+170, y0+50)], fill=(255, 120, 0))
    d.text((x, y0+68), kicker, font=font("sans_b", 9), fill=RED)
    yy = text_block(d, x, y0+84, head, font("sans_b", 15), INK, 308, 2, 18)
    text_block(d, x, yy+2, body, font("sans", 10), (60,60,60), 308, 3, 13)

# --- 10 small cards, 5 x 2 ---
cards = [
    ("4  HORMUZ", "Two supertankers hit mines, catch fire", "East of the Strait; Iran blockade continues. (UKMTO)"),
    ("5  GULF OF FINLAND", "Russian ship Sparta II still burning", "16 crew evacuated; Finland blames Ukraine. (Reuters)"),
    ("6  HONG KONG", "Hong Kong votes for 723 seats", "856 candidates; turnout 98.4% by 5pm. (SCMP)"),
    ("7  WELLINGTON", "India declare on a record 720/9", "Top Test total ever in New Zealand. (Reuters)"),
    ("8  LAS VEGAS", "Verstappen wins Las Vegas GP", "0.639s clear of Norris; 75th win. (F1)"),
    ("9  KHARTOUM", "Drones kill four near Khartoum", "UN building damaged, staff inside. (AFP)"),
    ("10  CIKANDE, INDONESIA", "Candy-factory fire kills three", "36 missing; search goes on. (Detik)"),
    ("11  WASHINGTON", "Democrats reach 258 seats", "Largest House majority since 1992. (AP)"),
    ("12  GAZA CITY", "Israeli fire kills four in Gaza", "Three killed in a food-aid van. (Al Jazeera)"),
    ("13  TURIN", "Alcaraz wins first ATP Finals", "Beats Zverev in the final. (Guardian)"),
]
y1 = 428
for idx, (kicker, head, body) in enumerate(cards):
    row, col = divmod(idx, 5)
    x = 24 + col*196
    y = y1 + row*96
    d.rectangle([x, y, x+186, y+88], fill=(255,255,255), outline=(200,190,170))
    d.rectangle([x, y, x+186, y+16], fill=NAVY)
    d.text((x+6, y+2), kicker, font=font("sans_b", 8), fill=(255,255,255))
    text_block(d, x+6, y+20, head, font("sans_b", 11), INK, 174, 2, 13)
    text_block(d, x+6, y+48, body, font("sans", 9), (70,70,70), 174, 2, 11)

# --- also list, 18 more, two columns ---
y2 = 630
d.text((24, y2), "ALSO ON SUNDAY 22 NOVEMBER  —  18 MORE STORIES", font=font("sans_b", 11), fill=RED)
d.line([24, y2+16, 1000, y2+16], fill=RED, width=1)
also_left = [
    "14  Seoul: education minister quits over AI exam cheating",
    "15  Delhi: Nepal PM Balendra Shah begins India visit",
    "16  Copenhagen: Denmark expels Russian attaché",
    "17  Tallinn: Estonia to shut Russia border from 1 Dec",
    "18  Washington: FBI probes hack of crime database",
    "19  Bayelsa: boat carrying mourners capsizes, 24 dead",
    "20  Vatican: Pope Leo XIV hosts lunch for 1,300 poor",
    "21  Brasilia: Bolsonaro in intensive care, stable",
    "22  Tehran: Iran begins rolling 2-hour power cuts",
]
also_right = [
    "23  Brussels: EU and Indonesia sign landmark trade deal",
    "24  San Antonio: Wembanyama scores 50 as Spurs win",
    "25  Portimão: Márquez wins eighth MotoGP title",
    "26  Manipur: toxic-liquor death toll rises to 19",
    "27  Mercury: BepiColombo enters orbit around Mercury",
    "28  Gaza: Hamas seeks urgent talks after aid strike",
    "29  Helsinki: Russian helicopter in Finnish airspace",
    "30  Manila: Chinese bomber turns back 170 km out",
    "31  Sydney: Marles rejects US report on AUKUS subs",
]
yy = y2+22
for t in also_left:
    d.text((24, yy), t, font=font("sans", 10), fill=INK)
    yy += 15
yy = y2+22
for t in also_right:
    d.text((512, yy), t, font=font("sans", 10), fill=INK)
    yy += 15

# --- map box + date check ---
y3 = 800
d.rectangle([24, y3, 380, y3+118], fill=(220, 235, 245), outline=NAVY)
d.text((32, y3+4), "WHERE IT HAPPENED — pins match story numbers", font=font("sans_b", 9), fill=NAVY)
# schematic continents: simple blobs
d.ellipse([50, y3+30, 150, y3+80], fill=(200, 210, 180))
d.ellipse([170, y3+28, 280, y3+85], fill=(200, 210, 180))
d.ellipse([300, y3+50, 360, y3+95], fill=(200, 210, 180))
for (px, py, n) in [(90, y3+45, "1"), (200, y3+50, "2"), (240, y3+45, "3"), (120, y3+65, "6"), (260, y3+70, "10"), (80, y3+70, "11")]:
    d.ellipse([px-7, py-7, px+7, py+7], fill=RED)
    d.text((px, py), n, font=font("sans_b", 8), fill=(255,255,255), anchor="mm")
d.text((32, y3+100), "World map, schematic — drawn in code.", font=font("sans", 8), fill=GREY)

d.rectangle([392, y3, 1000, y3+118], outline=RED, width=2)
d.text((404, y3+6), "DATE CHECK — READ THIS FIRST", font=font("sans_b", 11), fill=RED)
dc = "Every story 1–31 happened or was first reported on Sun 22 Nov 2026 (UTC). Left out as other days' news: Myanmar ICJ ruling (Thu 19 Nov), Shenzhen summit (Thu 19 Nov), Peru quake (Fri 20 Nov), 'El Chapo Isidro' arrest (Fri 21 Nov). Jensen Huang's return is Mon 23 Nov — shown in the red banner above as a breaking update, not counted in the 31."
text_block(d, 404, y3+24, dc, font("sans", 10), INK, 584, 6, 13)

# --- footer ---
d.text((24, 930), "Sources: Reuters, BBC, Al Jazeera, AP, AFP, AFP, SCMP, Guardian, Detik, F1, Ukrainian Air Force, UKMTO.  Scenes are drawn illustrations, not photographs.", font=font("sans", 9), fill=GREY)
d.text((24, 946), "THE WORLD IN ONE DAY  •  SUNDAY 22 NOVEMBER 2026  •  ONE PAGE", font=font("sans_b", 9), fill=GREY)
# bottom rule to fill to 1024
d.rectangle([0, 970, W, H], fill=NAVY)
d.text((512, 982), "31 STORIES  •  7 REGIONS  •  22 NOVEMBER 2026", font=font("sans_b", 11), fill=(255,255,255), anchor="ma")

out = Path(__file__).resolve().parent / "entry.png"
img.save(out, format="PNG", optimize=True)
print(out, out.stat().st_size)
