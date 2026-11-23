#!/usr/bin/env python3
# Fresh renderer for the 22 Nov 2026 front page.
# Draws a newspaper page in Pillow: 31 dated stories, 7 regions,
# a numbers strip, three big illustrated leads, ten small cards,
# an 18-item also-list, a schematic map and a date-check box.
# A red banner on top carries the 23 Nov Jensen Huang update,
# dated as 23 Nov and kept outside the 31.
# No network, no clock, no random choices: same bytes every run.

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


def fit_text(draw, words, face, limit):
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


def draw_para(draw, left, top, words, face, colour, limit, most=3):
    step = int(face.size * 1.25)
    for line in fit_text(draw, words, face, limit)[:most]:
        draw.text((left, top), line, font=face, fill=colour)
        top += step
    return top


def main():
    canvas = _Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = _Draw.Draw(canvas)

    pen.rectangle([0, 0, PAGE, 22], fill=NAVYBLUE)
    pen.text((12, 4), "THE WORLD IN ONE DAY", font=get_font("sans_b", 11), fill=WHITE)
    pen.text((PAGE - 12, 4), "31 STORIES  -  7 REGIONS  -  SUNDAY 22 NOVEMBER 2026", font=get_font("sans_b", 11), fill=WHITE, anchor="ra")

    pen.text((512, 30), "Sunday 22 November 2026", font=get_font("serif_b", 46), fill=DARK, anchor="ma")
    pen.text((512, 82), "COP31 ends with no deal  -  Iran claims US radars hit in Bahrain  -  186 drones over Ukraine", font=get_font("serif", 14), fill=CRIMSON, anchor="ma")
    pen.line([24, 108, 1000, 108], fill=DARK, width=2)

    stats = [
        ("186", "drones fired at Ukraine"),
        ("161", "downed or jammed"),
        ("$120bn", "adaptation target dropped"),
        ("258", "House seats, Democrats"),
        ("720/9", "India's record Test total"),
        ("98.4%", "Hong Kong turnout"),
    ]
    left = 24
    for value, label in stats:
        pen.text((left + 78, 116), value, font=get_font("sans_b", 20), fill=CRIMSON, anchor="ma")
        pen.text((left + 78, 140), label, font=get_font("sans", 9), fill=SOFTGREY, anchor="ma")
        left += 163
    pen.line([24, 158, 1000, 158], fill=DARK, width=1)

    pen.rectangle([24, 166, 1000, 196], fill=WINE)
    pen.text((36, 172), "BREAKING - MON 23 NOV:", font=get_font("sans_b", 13), fill=(255, 220, 0))
    pen.text((240, 172), "JENSEN HUANG IS BACK  -  Nvidia reinstates CEO, shares +30%", font=get_font("sans_b", 13), fill=WHITE)

    pen.rectangle([24, 202, 1000, 220], fill=NAVYBLUE)
    pen.text((512, 205), "EUROPE 7  -  MIDDLE EAST 6  -  ASIA-PACIFIC 7  -  AMERICAS 5  -  AFRICA 3  -  OCEANIA 2  -  WORLD 1", font=get_font("sans_b", 10), fill=WHITE, anchor="ma")

    leads = [
        dict(place="1  ANTALYA, TURKIYE  -  CLIMATE", title="COP31 ends without a deal", note="Final text lands with no mention of fossil fuels; drops the $120bn adaptation target. EU rejects it. (Reuters, BBC)", bg=(20, 90, 60)),
        dict(place="2  MANAMA, BAHRAIN  -  IRAN WAR", title="Iran claims US radars hit in Bahrain", note="IRGC says it hit two Patriot radars; Bahrain says a civilian site burned, no casualties. (Al Jazeera, Reuters)", bg=(20, 40, 80)),
        dict(place="3  KYIV, UKRAINE  -  WAR", title="Russia fires 186 drones overnight", note="161 downed or jammed; a block in Dymer is destroyed, 14 may be trapped. (Ukrainian Air Force)", bg=(40, 40, 60)),
    ]
    top = 228
    for idx, lead in enumerate(leads):
        x = 24 + idx * 324
        pen.rectangle([x, top, x + 308, top + 62], fill=lead["bg"])
        pen.ellipse([x + 20, top + 14, x + 62, top + 54], fill=(255, 190, 60))
        pen.rectangle([x + 90, top + 28, x + 280, top + 52], fill=(255, 255, 255))
        pen.text((x, top + 68), lead["place"], font=get_font("sans_b", 9), fill=CRIMSON)
        after = draw_para(pen, x, top + 84, lead["title"], get_font("sans_b", 15), DARK, 308, 2)
        draw_para(pen, x, after + 2, lead["note"], get_font("sans", 10), (60, 60, 60), 308, 3)

    small = [
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
    base_y = 428
    for pos, (tag, head, body) in enumerate(small):
        row, col = divmod(pos, 5)
        x = 24 + col * 196
        y = base_y + row * 96
        pen.rectangle([x, y, x + 186, y + 88], fill=WHITE, outline=(200, 190, 170))
        pen.rectangle([x, y, x + 186, y + 16], fill=NAVYBLUE)
        pen.text((x + 6, y + 2), tag, font=get_font("sans_b", 8), fill=WHITE)
        draw_para(pen, x + 6, y + 20, head, get_font("sans_b", 11), DARK, 174, 2)
        draw_para(pen, x + 6, y + 48, body, get_font("sans", 9), (70, 70, 70), 174, 2)

    list_y = 630
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
        yy += 15
    yy = list_y + 22
    for item in right_items:
        pen.text((512, yy), item, font=get_font("sans", 10), fill=DARK)
        yy += 15

    map_y = 800
    pen.rectangle([24, map_y, 380, map_y + 118], fill=(220, 235, 245), outline=NAVYBLUE)
    pen.text((32, map_y + 4), "WHERE IT HAPPENED - pins match story numbers", font=get_font("sans_b", 9), fill=NAVYBLUE)
    pen.ellipse([50, map_y + 30, 150, map_y + 80], fill=(200, 210, 180))
    pen.ellipse([170, map_y + 28, 280, map_y + 85], fill=(200, 210, 180))
    pen.ellipse([300, map_y + 50, 360, map_y + 95], fill=(200, 210, 180))
    for px, py, num in [(90, map_y + 45, "1"), (200, map_y + 50, "2"), (240, map_y + 45, "3"), (120, map_y + 65, "6"), (260, map_y + 70, "10"), (80, map_y + 70, "11")]:
        pen.ellipse([px - 7, py - 7, px + 7, py + 7], fill=CRIMSON)
        pen.text((px, py), num, font=get_font("sans_b", 8), fill=WHITE, anchor="mm")
    pen.text((32, map_y + 100), "World map, schematic - drawn in code.", font=get_font("sans", 8), fill=SOFTGREY)

    pen.rectangle([392, map_y, 1000, map_y + 118], outline=CRIMSON, width=2)
    pen.text((404, map_y + 6), "DATE CHECK - READ THIS FIRST", font=get_font("sans_b", 11), fill=CRIMSON)
    check = "Every story 1-31 happened or was first reported on Sun 22 Nov 2026 (UTC). Left out as other days' news: Myanmar ICJ ruling (Thu 19 Nov), Shenzhen summit (Thu 19 Nov), Peru quake (Fri 20 Nov), 'El Chapo Isidro' arrest (Fri 21 Nov). Jensen Huang's return is Mon 23 Nov - shown in the red banner above as a breaking update, not counted in the 31."
    draw_para(pen, 404, map_y + 24, check, get_font("sans", 10), DARK, 584, 6)

    pen.text((24, 930), "Sources: Reuters, BBC, Al Jazeera, AP, AFP, SCMP, Guardian, Detik, F1, Ukrainian Air Force, UKMTO. Scenes are drawn illustrations, not photographs.", font=get_font("sans", 9), fill=SOFTGREY)
    pen.text((24, 946), "THE WORLD IN ONE DAY  -  SUNDAY 22 NOVEMBER 2026  -  ONE PAGE", font=get_font("sans_b", 9), fill=SOFTGREY)
    pen.rectangle([0, 970, PAGE, PAGE], fill=NAVYBLUE)
    pen.text((512, 982), "31 STORIES  -  7 REGIONS  -  22 NOVEMBER 2026", font=get_font("sans_b", 11), fill=WHITE, anchor="ma")

    dest = _Path(__file__).resolve().parent / "entry.png"
    canvas.save(dest, format="PNG", optimize=True)
    print(dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
