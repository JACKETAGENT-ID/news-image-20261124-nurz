#!/usr/bin/env python3
"""THE WORLD TODAY — a broadsheet front page for Tuesday 24 November 2026.

Draws entry.png (1024x1024) from scratch with Pillow: cream newsprint,
a serif masthead, one lead story with a cracked-globe drawing, five
story cards and a markets ticker. System fonts only, no network, no
randomness — every run writes byte-identical output.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (22, 20, 18)
RED = (164, 32, 26)
GREY = (96, 90, 80)
CARD = (252, 249, 242)
RULE = (22, 20, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, fill, max_w, leading):
    for ln in wrap(draw, text, font, max_w):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def centered(draw, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)


def globe(draw, cx, cy, r):
    """A line-drawn globe with a jagged crack down its middle."""
    box = [cx - r, cy - r, cx + r, cy + r]
    draw.ellipse(box, outline=INK, width=4)
    for f in (0.35, 0.7):
        w = r * f
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    for f in (-0.5, 0.5):
        yy = cy + r * f
        half = int(r * (1 - f * f) ** 0.5)
        draw.line([cx - half, yy, cx + half, yy], fill=INK, width=2)
    crack = [(cx - 6, cy - r + 6), (cx + 14, cy - r // 2), (cx - 10, cy - 8),
             (cx + 16, cy + r // 3), (cx - 4, cy + 2 * r // 3),
             (cx + 8, cy + r - 8)]
    draw.line(crack, fill=RED, width=6, joint="curve")


def card(draw, x, y, w, h, kicker, headline, body, hsize=25, bsize=17):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=INK)
    draw.text((x + 10, y + 6), kicker, font=F(SANS_B, 16), fill=PAPER)
    yy = text_block(draw, x + 12, y + 42, headline, F(SERIF_B, hsize), INK,
                    w - 24, int(hsize * 1.22))
    text_block(draw, x + 12, yy + 4, body, F(SANS, bsize), GREY, w - 24,
               int(bsize * 1.3))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- dateline bar -------------------------------------------------
    d.rectangle([0, 0, W, 40], fill=INK)
    d.text((24, 11), "TUESDAY · 24 NOVEMBER 2026", font=F(SANS_B, 17),
           fill=PAPER)
    right = "ONE PAGE · THE WHOLE DAY"
    d.text((W - 24 - d.textlength(right, font=F(SANS_B, 17)), 11), right,
           font=F(SANS_B, 17), fill=PAPER)

    # --- masthead ------------------------------------------------------
    centered(d, 58, "THE WORLD TODAY", F(SERIF_B, 84), INK)
    d.line([24, 160, W - 24, 160], fill=RULE, width=5)
    d.line([24, 168, W - 24, 168], fill=RULE, width=2)
    centered(d, 178, "The day's world news, summed up on a single page",
             F(SERIF, 19), GREY)

    # --- lead story ----------------------------------------------------
    d.text((24, 216), "ANTALYA · CLIMATE SUMMIT", font=F(SANS_B, 20),
           fill=RED)
    d.text((24, 244), "CLIMATE TALKS", font=F(SERIF_B, 62), fill=INK)
    d.text((24, 318), "COLLAPSE OVER", font=F(SERIF_B, 62), fill=INK)
    d.text((24, 392), "FOSSIL FUELS", font=F(SERIF_B, 62), fill=RED)
    text_block(d, 24, 472,
               "COP31 runs nearly 50 hours into overtime — then more "
               "than 90 nations reject a final text that never once "
               "names fossil fuels. Diplomats call it climate "
               "diplomacy's darkest moment.",
               F(SERIF, 21), INK, 600, 28)
    globe(d, 828, 352, 128)
    d.line([24, 596, W - 24, 596], fill=RULE, width=3)

    # --- three story cards ---------------------------------------------
    cw, ch, gap, y0 = 317, 218, 12, 612
    card(d, 24, y0, cw, ch, "LIBYA · WAR AT SEA",
         "Sea Drones Sink Russian Corvette",
         "Kyiv says seven naval drones sank the Merkury at Benghazi, "
         "carrying the Black Sea fight into the Mediterranean. The UN "
         "seeks a probe.")
    card(d, 24 + (cw + gap), y0, cw, ch, "THE HAGUE · JUSTICE",
         "14 Nations Back Rohingya Ruling",
         "Fourteen countries affirm the ICJ finding of genocide "
         "against Myanmar over the Rohingya; Britain adds new "
         "sanctions on junta figures.")
    card(d, 24 + 2 * (cw + gap), y0, cw, ch, "UNITED NATIONS · AI",
         "UN Chief Sets AI Deadline",
         "Guterres gives member states one year to build a global "
         "framework limiting the risks of artificial intelligence.")

    # --- two wide cards --------------------------------------------------
    y1 = y0 + ch + gap
    card(d, 24, y1, 488, 118, "UKRAINE · OVERNIGHT",
         "Zaporizhzhia Strike Kills 2, Hurts 22",
         "Two children are among the wounded in the overnight "
         "Russian attack, regional officials say.",
         hsize=22, bsize=16)
    card(d, 524, y1, 476, 118, "DHAKA · THE RETURN",
         "Hasina Flies Home 16 December",
         "Bangladesh's ousted prime minister plans to end two years "
         "of exile in India, her spokesperson says.",
         hsize=22, bsize=16)

    # --- ticker ----------------------------------------------------------
    ty = y1 + 118 + 8
    d.rectangle([0, ty, W, H], fill=INK)
    ticker = ("S&P 500 +4.7% · NASDAQ +6.5% · GOLD $3,620 · BRENT $86.70 · "
              "TIANGONG STATION TAKES ITS FIRST FOREIGN ASTRONAUT · "
              "M5.6 QUAKE SHAKES NEPAL")
    text_block(d, 24, ty + 8, ticker, F(MONO, 16), PAPER, W - 48, 22)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
