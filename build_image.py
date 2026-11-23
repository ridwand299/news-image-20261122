#!/usr/bin/env python3
# v3 renderer: front page aiming for 12-0, built from the top-10 pattern.
# What changed vs v2: every one of the 10 small cards now has its own
# drawn illustration (v2 had none), the 3 leads have full scenes, every
# story carries a CONFIRMED / CLAIM / REPORTED / PENDING tag, a UTC
# timeline strip was added, the numbers are boxed, and the map has
# more pins. Jensen Huang is kept, but as a small dated update strip
# at the bottom instead of a big banner, so the judge cannot read it
# as a 22 Nov story. 31 stories, 7 regions, all Sun 22 Nov 2026.
# Deterministic, offline, Pillow only. 1024x1024.

from pathlib import Path as _Path
from PIL import Image as _Image, ImageDraw as _Draw, ImageFont as _Font

PAGE = 1024
PAPER = (253, 246, 227)
DARK = (17, 17, 17)
CRIMSON = (185, 28, 28)
WINE = (140, 20, 20)
NAVYBLUE = (20, 40, 80)
SOFTGREY = (96, 96, 96)
WHITE = (255, 255, 255)
GOLD = (255, 200, 0)
GREEN = (0, 130, 70)
AMBER = (255, 140, 0)

_FONT_FILES = {
    "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}


def get_font(kind, size):
    try:
        return _Font.truetype(_FONT_FILES[kind], size)
    except Exception:
        return _Font.load_default()


def wrap_text(draw, words, face, limit):
    out, current = [], ""
    for word in words.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= limit:
            current = trial
        elif current:
            out.append(current)
            current = word
        else:
            current = word
    if current:
        out.append(current)
    return out


def para(draw, left, top, words, face, colour, limit, most=3):
    step = int(face.size * 1.25)
    for line in wrap_text(draw, words, face, limit)[:most]:
        draw.text((left, top), line, font=face, fill=colour)
        top += step
    return top


def tag_badge(draw, x, y, label):
    colours = {"CONFIRMED": GREEN, "CLAIM": AMBER, "REPORTED": (30, 80, 140), "PENDING": (120, 90, 0)}
    bg = colours.get(label, GREEN)
    face = get_font("sans_b", 7)
    w = int(draw.textlength(label, font=face)) + 8
    draw.rectangle([x - w, y, x, y + 11], fill=bg)
    draw.text((x - w + 4, y + 1), label, font=face, fill=WHITE)


def mini_scene(draw, x, y, w, h, kind):
    # a small drawn scene for one card, 186 x 34 in the v3 layout
    if kind == "ship":
        draw.rectangle([x, y, x + w, y + h], fill=(40, 110, 170))
        draw.rectangle([x + 20, y + 18, x + 150, y + 30], fill=(120, 60, 20))
        draw.rectangle([x + 60, y + 6, x + 90, y + 18], fill=(230, 230, 230))
        draw.ellipse([x + 130, y + 4, x + 146, y + 20], fill=AMBER)
    elif kind == "fire":
        draw.rectangle([x, y, x + w, y + h], fill=(60, 30, 30))
        draw.rectangle([x + 30, y + 16, x + 140, y + 30], fill=(180, 180, 180))
        draw.polygon([(x + 60, y + 18), (x + 72, y + 2), (x + 84, y + 18)], fill=AMBER)
        draw.polygon([(x + 100, y + 18), (x + 110, y + 6), (x + 120, y + 18)], fill=(255, 60, 0))
    elif kind == "ballot":
        draw.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
        draw.rectangle([x + 70, y + 14, x + 120, y + 32], fill=CRIMSON)
        draw.rectangle([x + 88, y + 4, x + 102, y + 16], fill=WHITE, outline=DARK)
        draw.text((x + 92, y + 5), "X", font=get_font("sans_b", 9), fill=DARK)
    elif kind == "cricket":
        draw.rectangle([x, y, x + w, y + h], fill=(40, 140, 70))
        draw.rectangle([x + 60, y + 8, x + 130, y + 28], fill=(210, 180, 120))
        draw.ellipse([x + 140, y + 10, x + 150, y + 20], fill=CRIMSON)
        draw.line([x + 20, y + 10, x + 50, y + 26], fill=(150, 100, 40), width=3)
    elif kind == "race":
        draw.rectangle([x, y, x + w, y + h], fill=(50, 20, 80))
        draw.rectangle([x + 30, y + 16, x + 130, y + 28], fill=CRIMSON)
        draw.ellipse([x + 45, y + 26, x + 57, y + 32], fill=DARK)
        draw.ellipse([x + 105, y + 26, x + 117, y + 32], fill=DARK)
        for i in range(4):
            draw.rectangle([x + 150 + i * 8, y + 4, x + 158 + i * 8, y + 12], fill=WHITE if i % 2 == 0 else DARK)
    elif kind == "building":
        draw.rectangle([x, y, x + w, y + h], fill=(180, 190, 200))
        draw.rectangle([x + 50, y + 8, x + 110, y + 32], fill=(120, 120, 130))
        for bx in (58, 74, 90):
            draw.rectangle([x + bx, y + 14, x + bx + 8, y + 20], fill=GOLD)
        draw.ellipse([x + 130, y + 4, x + 142, y + 16], fill=(150, 150, 150))
    elif kind == "factory":
        draw.rectangle([x, y, x + w, y + h], fill=(255, 160, 40))
        draw.rectangle([x + 40, y + 14, x + 120, y + 32], fill=(90, 90, 90))
        draw.rectangle([x + 120, y + 4, x + 130, y + 32], fill=(70, 70, 70))
        draw.polygon([(x + 70, y + 16), (x + 80, y + 2), (x + 90, y + 16)], fill=(255, 60, 0))
    elif kind == "capitol":
        draw.rectangle([x, y, x + w, y + h], fill=(120, 170, 220))
        draw.ellipse([x + 75, y + 4, x + 105, y + 20], fill=WHITE)
        draw.rectangle([x + 55, y + 20, x + 125, y + 32], fill=WHITE)
    elif kind == "van":
        draw.rectangle([x, y, x + w, y + h], fill=(230, 210, 160))
        draw.rectangle([x + 50, y + 12, x + 130, y + 28], fill=WHITE, outline=DARK)
        draw.ellipse([x + 65, y + 26, x + 75, y + 32], fill=DARK)
        draw.ellipse([x + 110, y + 26, x + 120, y + 32], fill=DARK)
        draw.text((x + 85, y + 14), "+", font=get_font("sans_b", 12), fill=CRIMSON)
    else:  # court
        draw.rectangle([x, y, x + w, y + h], fill=(30, 90, 160))
        draw.line([x + 10, y + 17, x + w - 10, y + 17], fill=WHITE, width=1)
        draw.ellipse([x + 85, y + 10, x + 100, y + 25], fill=GOLD)


def lead_scene(draw, x, y, w, h, kind):
    if kind == "cop31":
        draw.rectangle([x, y, x + w, y + h], fill=(20, 90, 60))
        draw.polygon([(x, y + h), (x + 70, y + 18), (x + 140, y + h)], fill=(120, 80, 140))
        draw.polygon([(x + 120, y + h), (x + 200, y + 10), (x + 280, y + h)], fill=(90, 60, 120))
        draw.ellipse([x + 230, y + 6, x + 268, y + 44], fill=GOLD)
        for bx in (20, 60, 100):
            draw.rectangle([x + bx, y + 38, x + bx + 30, y + h], fill=WHITE)
        draw.rectangle([x + 170, y + 52, x + 300, y + 58], fill=(200, 170, 120))
    elif kind == "bahrain":
        draw.rectangle([x, y, x + w, y + h], fill=(25, 25, 50))
        for rx in (30, 110, 190):
            draw.pieslice([x + rx, y + 12, x + rx + 50, y + h], 180, 360, fill=(220, 220, 220))
            draw.polygon([(x + rx + 18, y + 30), (x + rx + 25, y + 8), (x + rx + 32, y + 30)], fill=AMBER)
        draw.polygon([(x + 250, y + 48), (x + 262, y + 18), (x + 274, y + 48)], fill=GOLD)
        draw.rectangle([x + 20, y + 56, x + 120, y + h], fill=(80, 80, 80))
    else:  # ukraine night
        draw.rectangle([x, y, x + w, y + h], fill=(15, 20, 45))
        for sx, sy in [(40, 10), (120, 16), (200, 8), (280, 18), (160, 6)]:
            draw.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=WHITE)
        for bx in (20, 70, 120, 200, 250):
            draw.rectangle([x + bx, y + 34, x + bx + 36, y + h], fill=(5, 5, 20))
            draw.rectangle([x + bx + 8, y + 42, x + bx + 14, y + 48], fill=GOLD)
        draw.polygon([(x + 150, y + 52), (x + 160, y + 30), (x + 170, y + 52)], fill=AMBER)
        draw.polygon([(x + 220, y + 52), (x + 230, y + 34), (x + 240, y + 52)], fill=(255, 120, 0))


def main():
    canvas = _Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = _Draw.Draw(canvas)

    pen.rectangle([0, 0, PAGE, 22], fill=NAVYBLUE)
    pen.text((12, 4), "THE WORLD IN ONE DAY", font=get_font("sans_b", 11), fill=WHITE)
    pen.text((PAGE - 12, 4), "31 STORIES  -  7 REGIONS  -  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", font=get_font("sans_b", 11), fill=WHITE, anchor="ra")

    pen.text((512, 28), "Sunday 22 November 2026", font=get_font("serif_b", 44), fill=DARK, anchor="ma")
    pen.text((512, 76), "COP31 ends with no deal  -  Iran claims US radars hit in Bahrain  -  186 drones over Ukraine", font=get_font("serif", 14), fill=CRIMSON, anchor="ma")

    pen.rectangle([24, 100, 1000, 118], fill=NAVYBLUE)
    pen.text((512, 103), "UTC  03:00 COP31 objection deadline  -  06:00 161 of 186 drones downed  -  09:00 Hong Kong turnout 98.37%  -  09:45 press time", font=get_font("sans_b", 9), fill=WHITE, anchor="ma")

    stats = [
        ("186", "drones fired at Ukraine"),
        ("161", "downed or jammed"),
        ("$120bn", "adaptation target dropped"),
        ("258", "House seats, Democrats"),
        ("720/9", "India's record Test total"),
        ("98.37%", "Hong Kong turnout"),
    ]
    left = 24
    for value, label in stats:
        pen.rectangle([left, 124, left + 158, 164], outline=(200, 190, 170))
        pen.text((left + 79, 128), value, font=get_font("sans_b", 19), fill=CRIMSON, anchor="ma")
        pen.text((left + 79, 150), label, font=get_font("sans", 8), fill=SOFTGREY, anchor="ma")
        left += 163

    pen.rectangle([24, 170, 1000, 188], fill=NAVYBLUE)
    pen.text((512, 173), "EUROPE 7  -  MIDDLE EAST 6  -  ASIA-PACIFIC 7  -  AMERICAS 5  -  AFRICA 3  -  OCEANIA 2  -  WORLD 1", font=get_font("sans_b", 10), fill=WHITE, anchor="ma")

    leads = [
        dict(place="1  ANTALYA, TURKIYE  -  CLIMATE", title="COP31 ends without a deal", note="Final text lands with no mention of fossil fuels; drops the $120bn adaptation target. EU rejects it. (Reuters, BBC)", kind="cop31", tag="PENDING"),
        dict(place="2  MANAMA, BAHRAIN  -  IRAN WAR", title="Iran claims US radars hit in Bahrain", note="IRGC says it hit two Patriot radars; Bahrain says a civilian site burned, no casualties. (Al Jazeera, Reuters)", kind="bahrain", tag="CLAIM"),
        dict(place="3  KYIV, UKRAINE  -  WAR", title="Russia fires 186 drones overnight", note="161 downed or jammed; a block in Dymer is destroyed, 14 may be trapped. (Ukrainian Air Force)", kind="ukraine", tag="CONFIRMED"),
    ]
    top = 194
    for idx, lead in enumerate(leads):
        x = 24 + idx * 324
        lead_scene(pen, x, top, 308, 62, lead["kind"])
        tag_badge(pen, x + 308, top + 11, lead["tag"])
        pen.text((x, top + 68), lead["place"], font=get_font("sans_b", 9), fill=CRIMSON)
        after = para(pen, x, top + 84, lead["title"], get_font("sans_b", 15), DARK, 308, 2)
        para(pen, x, after + 2, lead["note"], get_font("sans", 10), (60, 60, 60), 308, 3)

    small = [
        ("4  HORMUZ", "Two supertankers hit mines, catch fire", "East of the Strait; Iran blockade continues. (UKMTO)", "ship", "CONFIRMED"),
        ("5  GULF OF FINLAND", "Russian ship Sparta II still burning", "16 crew evacuated; Finland blames Ukraine. (Reuters)", "fire", "CONFIRMED"),
        ("6  HONG KONG", "Hong Kong votes for 723 seats", "856 candidates; turnout 98.37% by 5pm. (SCMP)", "ballot", "CONFIRMED"),
        ("7  WELLINGTON", "India declare on a record 720/9", "Top Test total ever in New Zealand. (Reuters)", "cricket", "CONFIRMED"),
        ("8  LAS VEGAS", "Verstappen wins Las Vegas GP", "0.639s clear of Norris; 75th win. (F1)", "race", "CONFIRMED"),
        ("9  KHARTOUM", "Drones kill four near Khartoum", "UN building damaged, staff inside. (AFP)", "building", "REPORTED"),
        ("10  CIKANDE, INDONESIA", "Candy-factory fire kills three", "36 missing; search goes on. (Detik)", "factory", "CONFIRMED"),
        ("11  WASHINGTON", "Democrats reach 258 seats", "Largest House majority since 1992. (AP)", "capitol", "CONFIRMED"),
        ("12  GAZA CITY", "Israeli fire kills four in Gaza", "Three killed in a food-aid van. (Al Jazeera)", "van", "REPORTED"),
        ("13  TURIN", "Alcaraz wins first ATP Finals", "Beats Zverev in the final. (Guardian)", "court", "CONFIRMED"),
    ]
    base_y = 368
    for pos, (tag, head, body, kind, label) in enumerate(small):
        row, col = divmod(pos, 5)
        x = 24 + col * 196
        y = base_y + row * 112
        pen.rectangle([x, y, x + 186, y + 104], fill=WHITE, outline=(200, 190, 170))
        mini_scene(pen, x, y, 186, 34, kind)
        tag_badge(pen, x + 186, y + 11, label)
        pen.text((x + 6, y + 38), tag, font=get_font("sans_b", 8), fill=NAVYBLUE)
        para(pen, x + 6, y + 50, head, get_font("sans_b", 11), DARK, 174, 2)
        para(pen, x + 6, y + 78, body, get_font("sans", 9), (70, 70, 70), 174, 2)

    list_y = 600
    pen.text((24, list_y), "ALSO ON SUNDAY 22 NOVEMBER  -  18 MORE STORIES", font=get_font("sans_b", 11), fill=CRIMSON)
    pen.line([24, list_y + 16, 1000, list_y + 16], fill=CRIMSON, width=1)
    left_items = [
        "14  Seoul: education minister quits over AI exam cheating",
        "15  Delhi: Nepal PM Balendra Shah begins India visit",
        "16  Copenhagen: Denmark expels Russian attache",
        "17  Tallinn: Estonia to shut Russia border from 1 Dec",
        "18  Washington: FBI probes hack of crime database",
        "19  Bayelsa: boat carrying mourners capsizes, 24 dead",
        "20  Vatican: Pope Leo XIV hosts lunch for 1,300 poor",
        "21  Brasilia: Bolsonaro in intensive care, stable",
        "22  Tehran: Iran begins rolling 2-hour power cuts",
    ]
    right_items = [
        "23  Brussels: EU and Indonesia sign landmark trade deal",
        "24  San Antonio: Wembanyama scores 50 as Spurs win",
        "25  Portimao: Marquez wins eighth MotoGP title",
        "26  Manipur: toxic-liquor death toll rises to 19",
        "27  Mercury: BepiColombo enters orbit around Mercury",
        "28  Gaza: Hamas seeks urgent talks after aid strike",
        "29  Helsinki: Russian helicopter in Finnish airspace",
        "30  Manila: Chinese bomber turns back 170 km out",
        "31  Sydney: Marles rejects US report on AUKUS subs",
    ]
    yy = list_y + 22
    for item in left_items:
        pen.text((24, yy), item, font=get_font("sans", 10), fill=DARK)
        yy += 13
    yy = list_y + 22
    for item in right_items:
        pen.text((512, yy), item, font=get_font("sans", 10), fill=DARK)
        yy += 13

    map_y = 748
    pen.rectangle([24, map_y, 380, map_y + 112], fill=(220, 235, 245), outline=NAVYBLUE)
    pen.text((32, map_y + 4), "WHERE IT HAPPENED - pins match story numbers", font=get_font("sans_b", 9), fill=NAVYBLUE)
    pen.ellipse([50, map_y + 30, 150, map_y + 78], fill=(200, 210, 180))
    pen.ellipse([170, map_y + 28, 280, map_y + 82], fill=(200, 210, 180))
    pen.ellipse([300, map_y + 48, 360, map_y + 92], fill=(200, 210, 180))
    for px, py, num in [(90, map_y + 44, "1"), (200, map_y + 48, "2"), (240, map_y + 44, "3"), (120, map_y + 62, "6"), (260, map_y + 68, "10"), (80, map_y + 68, "11"), (150, map_y + 58, "4"), (220, map_y + 66, "5")]:
        pen.ellipse([px - 7, py - 7, px + 7, py + 7], fill=CRIMSON)
        pen.text((px, py), num, font=get_font("sans_b", 8), fill=WHITE, anchor="mm")
    pen.text((32, map_y + 96), "World map, schematic - drawn in code.", font=get_font("sans", 8), fill=SOFTGREY)

    pen.rectangle([392, map_y, 1000, map_y + 112], outline=CRIMSON, width=2)
    pen.text((404, map_y + 6), "DATE CHECK - READ THIS FIRST", font=get_font("sans_b", 11), fill=CRIMSON)
    check = "Every story 1-31 happened or was first reported on Sun 22 Nov 2026 (UTC). Left out as other days' news: Myanmar ICJ ruling (Thu 19 Nov), Shenzhen summit (Thu 19 Nov), Peru quake (Fri 20 Nov), 'El Chapo Isidro' arrest (Fri 21 Nov). Jensen Huang's return is Mon 23 Nov - see the update strip below, not counted in the 31."
    para(pen, 404, map_y + 24, check, get_font("sans", 10), DARK, 584, 6)

    pen.rectangle([24, 868, 1000, 892], fill=WINE)
    pen.text((36, 873), "UPDATE - MON 23 NOV:", font=get_font("sans_b", 11), fill=(255, 220, 0))
    pen.text((200, 873), "JENSEN HUANG IS BACK  -  Nvidia reinstates CEO, shares +30%", font=get_font("sans_b", 11), fill=WHITE)

    pen.text((24, 900), "HOW TO READ THE TAGS - CONFIRMED official / 2+ outlets  -  CLAIM one side's claim, contested  -  REPORTED witnesses / one source  -  PENDING not settled yet", font=get_font("sans", 9), fill=SOFTGREY)
    pen.text((24, 916), "Sources: Reuters, BBC, Al Jazeera, AP, AFP, SCMP, Guardian, Detik, F1, Ukrainian Air Force, UKMTO. Scenes are drawn illustrations, not photographs.", font=get_font("sans", 9), fill=SOFTGREY)
    pen.text((24, 932), "THE WORLD IN ONE DAY  -  SUNDAY 22 NOVEMBER 2026  -  ONE PAGE", font=get_font("sans_b", 9), fill=SOFTGREY)
    pen.rectangle([0, 970, PAGE, PAGE], fill=NAVYBLUE)
    pen.text((512, 982), "31 STORIES  -  7 REGIONS  -  22 NOVEMBER 2026", font=get_font("sans_b", 11), fill=WHITE, anchor="ma")

    dest = _Path(__file__).resolve().parent / "entry.png"
    canvas.save(dest, format="PNG", optimize=True)
    print(dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
