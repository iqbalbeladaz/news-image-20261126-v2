#!/usr/bin/env python3
"""Render the front page of 26 November 2026 as a broadsheet image.

Draws a 1024x1024 newspaper front page with Pillow only: a navy masthead,
a lead markets story, six regional story cards, a numbers panel and an
"also today" band. All text is wrapped to fit its box before drawing.
Run:  python3 generate.py            -> writes entry.png next to this file
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 20, 26)
NAVY = (18, 40, 75)
NAVY_SOFT = (28, 56, 102)
GOLD = (217, 164, 65)
RED = (178, 34, 34)
CARD = (255, 255, 255)
MUTED = (90, 92, 100)
RULE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def card(draw, x, y, w, h, kicker, head, body, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                           outline=RULE, width=1)
    draw.rectangle([x, y + 10, x + 5, y + h - 10], fill=accent)
    kx, ky = x + 18, y + 12
    draw.text((kx, ky), kicker, font=font(SANS_B, 14), fill=accent)
    hy = ky + 22
    hy = para(draw, kx, hy, head, font(SERIF_B, 20), INK, w - 36, 24)
    para(draw, kx, hy + 2, body, font(SANS, 15), MUTED, w - 36, 19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # page margin

    # ---- Masthead ----
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 132], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 16), title,
           font=tf, fill=(255, 255, 255))
    date = "THURSDAY, 26 NOVEMBER 2026"
    df = font(SANS_B, 22)
    d.text(((W - d.textlength(date, font=df)) / 2, 88), date,
           font=df, fill=GOLD)

    # ---- Lead story: markets ----
    ly, lh = 148, 164
    d.rounded_rectangle([mx, ly, W - mx, ly + lh], radius=8, fill=CARD,
                        outline=RULE, width=1)
    d.rectangle([mx, ly + 10, mx + 5, ly + lh - 10], fill=RED)
    d.text((mx + 20, ly + 12), "MARKETS  •  LEAD STORY",
           font=font(SANS_B, 14), fill=RED)
    head = "Nasdaq plunges 4% as AI sell-off deepens"
    hy = para(d, mx + 20, ly + 38, head, font(SERIF_B, 32), INK, 660, 38)
    para(d, mx + 20, hy + 6,
         "Tech rout deepens: Nvidia falls 8.6% as investors dump AI stocks. "
         "Trump unveils a new tariff plan covering 14 trading partners.",
         font(SANS, 18), MUTED, 660, 24)
    # Big number block on the right of the lead card
    bx = W - mx - 190
    d.line([bx - 16, ly + 34, bx - 16, ly + lh - 24], fill=RULE, width=1)
    d.text((bx, ly + 44), "-4.0%", font=font(SERIF_B, 52), fill=RED)
    d.text((bx, ly + 108), "NASDAQ, 26 NOV",
           font=font(SANS_B, 14), fill=MUTED)

    # ---- Story cards, two columns x three rows ----
    stories = [
        ("BANGLADESH", "Garment pay up 36% after protests",
         "Dhaka raises the minimum wage for garment workers by more than "
         "a third.", NAVY_SOFT),
        ("NORTH KOREA", "Pyongyang orders Swiss office shut",
         "North Korea tells Switzerland to close its cooperation office "
         "in the capital.", NAVY_SOFT),
        ("INDIA", "Constitution Day, 18 years after 26/11",
         "India marks Constitution Day and remembers the 2008 Mumbai "
         "attacks, 18 years on.", NAVY_SOFT),
        ("CRICKET", "Sooryavanshi, 15, smashes 204 off 53 balls",
         "Vaibhav Sooryavanshi hits the fastest List A double century "
         "ever.", NAVY_SOFT),
        ("SOUTH AFRICA", "Court backs Ramaphosa in Phala Phala case",
         "A South African court rules for President Cyril Ramaphosa in "
         "the Phala Phala case.", NAVY_SOFT),
        ("NEPAL & CHESS", "Quake shakes Koshi; Gukesh plays on",
         "A 5.6-magnitude quake hits Koshi, Nepal. In Geneva, Gukesh "
         "faces Sindarov.", NAVY_SOFT),
    ]
    cw = (W - 2 * mx - 20) // 2
    ch, gap = 130, 12
    y = 336
    for i, (kick, head, body, acc) in enumerate(stories):
        x = mx + (i % 2) * (cw + 20)
        card(d, x, y, cw, ch, kick, head, body, acc)
        if i % 2 == 1:
            y += ch + gap

    # ---- The day in numbers ----
    ny = y + 4
    nh = 132
    d.rounded_rectangle([mx, ny, W - mx, ny + nh], radius=8, fill=NAVY)
    d.text((mx + 18, ny + 10), "THE DAY IN NUMBERS",
           font=font(SANS_B, 15), fill=GOLD)
    stats = [
        ("-4.0%", "Nasdaq falls"),
        ("-8.6%", "Nvidia falls"),
        ("204 off 53", "Sooryavanshi balls"),
        ("1,220", "IPL sign-ups"),
        ("+36%", "Garment pay rise"),
        ("5.6", "Nepal quake magnitude"),
    ]
    cell_w = (W - 2 * mx - 36) // 3
    for i, (num, label) in enumerate(stats):
        cx = mx + 18 + (i % 3) * cell_w
        cy = ny + 36 + (i // 3) * 46
        d.text((cx, cy), num, font=font(SERIF_B, 24), fill=(255, 255, 255))
        d.text((cx, cy + 28), label, font=font(SANS, 13), fill=(190, 200, 220))

    # ---- Also today ----
    ay = ny + nh + 12
    d.text((mx, ay), "ALSO TODAY",
           font=font(SANS_B, 15), fill=RED)
    also = ("Hasina asks to return home on 16 December  •  Cost-of-living "
            "strike grips Greece  •  Pope speaks on the failure of COP31  •  "
            "Bulgaria rescues 35 migrants at sea  •  Flipkart CEO to step "
            "down in December  •  US consumer confidence at a near two-year high")
    para(d, mx, ay + 24, also, font(SANS, 16), INK, W - 2 * mx, 22)

    # ---- Footer ----
    d.line([mx, H - 34, W - mx, H - 34], fill=RULE, width=1)
    foot = "All events first reported on 26 November 2026  •  Compiled from wire reports"
    ff = font(SANS, 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, H - 26), foot,
           font=ff, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
