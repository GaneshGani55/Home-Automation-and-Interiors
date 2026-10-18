"""
One-page carpenter sheet for the staircase touch screen frame
(Waveshare 14inch 2K bare panel, clamped in a walnut frame).

Drawn in code (vector, to scale). Source of truth for the sizes:
electrical/WAVESHARE_INDOOR_PANEL.md v3.4.

  python3 pdfs/build_carpenter_sheet_14in.py
  -> pdfs/STAIRCASE_SCREEN_CARPENTER_SHEET.pdf
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT = Path(__file__).with_name("STAIRCASE_SCREEN_CARPENTER_SHEET.pdf")

# ---- sizes (real mm) -------------------------------------------------------
GLASS = (330.6, 232.0)      # screen glass outline (Waveshare drawing)
PICTURE = (296.4, 197.8)    # bright picture area
WINDOW = (300.0, 202.0)     # cut opening in the frame
POCKET = (333.0, 234.0)     # inside of the box = glass + ~1 mm each side
BOX_WALL = 12.0
BOX = (POCKET[0] + 2 * BOX_WALL, POCKET[1] + 2 * BOX_WALL)  # 357 x 258
HOLE = (370.0, 270.0)       # finished wall hole, 80 deep
FRAME = (410.0, 310.0)      # front frame outside (20 mm onto the wall)

INK = (0.09, 0.09, 0.09)
GREY = (0.42, 0.42, 0.42)
WALNUT = (0.69, 0.50, 0.34)
WALNUT_DARK = (0.48, 0.32, 0.20)
SCREEN = (0.14, 0.14, 0.15)
PLY = (0.93, 0.85, 0.68)
FOAM = (0.98, 0.62, 0.30)
FELT = (0.55, 0.20, 0.55)
STEEL = (0.35, 0.37, 0.40)
MAGNET = (0.62, 0.64, 0.68)
WALL = (0.93, 0.88, 0.77)
HATCH = (0.80, 0.72, 0.58)
CAVITY = (1.0, 0.99, 0.95)
RED = (0.78, 0.16, 0.16)
WHITE = (1, 1, 1)


def rgb(c, col, stroke=False):
    (c.setStrokeColorRGB if stroke else c.setFillColorRGB)(*col)


def text(c, x, y, s, size=8, bold=False, col=INK, anchor="left"):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    rgb(c, col)
    fn = {"left": c.drawString, "centre": c.drawCentredString,
          "right": c.drawRightString}[anchor]
    fn(x, y, s)


def arrow_head(c, x, y, dx, dy, size=1.6 * mm):
    import math
    ang = math.atan2(dy, dx)
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x - size * math.cos(ang - 0.35), y - size * math.sin(ang - 0.35))
    p.lineTo(x - size * math.cos(ang + 0.35), y - size * math.sin(ang + 0.35))
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def dim_line(c, x1, y1, x2, y2, label, size=9, offset=1.5 * mm):
    """Dimension line with arrows both ends and a label in the middle."""
    rgb(c, INK, stroke=True)
    rgb(c, INK)
    c.setLineWidth(0.5)
    c.setDash()
    c.line(x1, y1, x2, y2)
    arrow_head(c, x2, y2, x2 - x1, y2 - y1)
    arrow_head(c, x1, y1, x1 - x2, y1 - y2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if abs(y2 - y1) < 1e-6:  # horizontal
        w = c.stringWidth(label, "Helvetica-Bold", size) + 2 * mm
        rgb(c, WHITE)
        c.rect(mx - w / 2, my - 1.6 * mm, w, 3.4 * mm, fill=1, stroke=0)
        text(c, mx, my - 1.1 * mm, label, size, True, anchor="centre")
    else:  # vertical: label rotated
        c.saveState()
        c.translate(mx, my)
        c.rotate(90)
        w = c.stringWidth(label, "Helvetica-Bold", size) + 2 * mm
        rgb(c, WHITE)
        c.rect(-w / 2, -1.6 * mm, w, 3.4 * mm, fill=1, stroke=0)
        text(c, 0, -1.1 * mm, label, size, True, anchor="centre")
        c.restoreState()


def leader(c, lx, ly, px, py, label, size=7.5, anchor="left", bold=False):
    """Label at (lx, ly) with a thin line from the label's near end to the
    point (px, py), so the line never crosses its own text."""
    lines = label.split("\n")
    tx = lx + 1 * mm
    widths = [c.stringWidth(ln, "Helvetica-Bold" if bold and i == 0
                            else "Helvetica", size)
              for i, ln in enumerate(lines)]
    if px < lx:
        sx = lx
    else:
        sx = tx + max(widths) + 1 * mm
    rgb(c, GREY, stroke=True)
    c.setLineWidth(0.45)
    c.setDash()
    c.line(sx, ly, px, py)
    rgb(c, INK)
    c.circle(px, py, 0.55 * mm, fill=1, stroke=0)
    for i, ln in enumerate(lines):
        text(c, tx, ly - 1.2 * mm - i * (size + 1.2), ln, size,
             bold=bold and i == 0)


# ---- front view ------------------------------------------------------------
def front_view(c):
    s = 0.36 * mm          # page units per real mm
    cx, cy = 92 * mm, 112 * mm

    def rect(w, h, **kw):
        c.rect(cx - w / 2 * s, cy - h / 2 * s, w * s, h * s, **kw)

    text(c, 14 * mm, 180 * mm, "1.  FRONT VIEW  (what you see on the wall)",
         10, True)

    # frame
    rgb(c, WALNUT)
    rgb(c, WALNUT_DARK, stroke=True)
    c.setLineWidth(1)
    rect(*FRAME, fill=1, stroke=1)
    # finger notch, bottom centre
    rgb(c, WALNUT_DARK)
    c.wedge(cx - 12 * s, cy - FRAME[1] / 2 * s - 12 * s,
            cx + 12 * s, cy - FRAME[1] / 2 * s + 12 * s, 0, 180,
            fill=1, stroke=0)
    # window (the picture shows here)
    rgb(c, SCREEN)
    rect(*WINDOW, fill=1, stroke=0)
    # glass edge hidden behind wood: dotted
    c.setLineWidth(0.8)
    rgb(c, (0.20, 0.12, 0.06), stroke=True)
    c.setDash(1.2, 1.6)
    rect(*GLASS, fill=0, stroke=1)
    # wall hole behind: dashed
    c.setDash(4, 2.5)
    c.setLineWidth(0.9)
    rgb(c, INK, stroke=True)
    rect(*HOLE, fill=0, stroke=1)
    c.setDash()
    # magnets in the 20 mm overlap band, back of frame
    rgb(c, MAGNET)
    rgb(c, INK, stroke=True)
    c.setLineWidth(0.4)
    mx, my = (HOLE[0] + FRAME[0]) / 4, (HOLE[1] + FRAME[1]) / 4
    for sx in (-1, 1):
        for sy in (-1, 1):
            c.rect(cx + (sx * mx - 5) * s, cy + (sy * my - 5) * s,
                   10 * s, 10 * s, fill=1, stroke=1)
    # vent slots over the air gap (between box wall and hole)
    gap_mid_y = (BOX[1] / 2 + HOLE[1] / 2) / 2
    rgb(c, INK)
    for sy in (-1, 1):
        for vx in (-120, -60, 0, 60, 120):
            c.rect(cx + (vx - 15) * s, cy + (sy * gap_mid_y - 1.5) * s,
                   30 * s, 3 * s, fill=1, stroke=0)

    # labels inside the window
    text(c, cx, cy + 4 * mm, "WINDOW  (cut-out)", 10, True, WHITE, "centre")
    text(c, cx, cy - 1 * mm, "300 × 202", 13, True, WHITE, "centre")
    text(c, cx, cy - 6.5 * mm,
         "centre it on the bright picture — black border ≈ 17 each side",
         7, False, (0.85, 0.85, 0.85), "centre")
    text(c, cx, cy - 10.5 * mm,
         "wood covers ≈ 15 of the black glass border all round",
         7, False, (0.85, 0.85, 0.85), "centre")

    # dimensions
    top = cy + FRAME[1] / 2 * s
    left = cx - FRAME[0] / 2 * s
    dim_line(c, left, top + 5 * mm, left + FRAME[0] * s, top + 5 * mm,
             "FRAME OUTSIDE  410")
    c.setLineWidth(0.3)
    rgb(c, GREY, stroke=True)
    c.line(left, top + 1 * mm, left, top + 6.5 * mm)
    c.line(left + FRAME[0] * s, top + 1 * mm, left + FRAME[0] * s,
           top + 6.5 * mm)
    bot = cy - FRAME[1] / 2 * s
    dim_line(c, left - 5 * mm, bot, left - 5 * mm, top, "310")
    c.line(left - 6.5 * mm, bot, left - 1 * mm, bot)
    c.line(left - 6.5 * mm, top, left - 1 * mm, top)

    # legend
    y = 49 * mm
    x = 16 * mm
    c.setLineWidth(0.9)
    rgb(c, INK, stroke=True)
    c.setDash(4, 2.5)
    c.line(x, y + 1 * mm, x + 9 * mm, y + 1 * mm)
    c.setDash()
    text(c, x + 11 * mm, y, "Dashed = hole in the wall behind the frame:  "
         "370 × 270, 80 deep  (measure the real hole)", 8)
    y -= 5 * mm
    rgb(c, (0.20, 0.12, 0.06), stroke=True)
    c.setDash(1.2, 1.6)
    c.line(x, y + 1 * mm, x + 9 * mm, y + 1 * mm)
    c.setDash()
    text(c, x + 11 * mm, y, "Dotted = edge of the screen glass:  330.6 × 232  "
         "(hidden behind the wood)", 8)
    y -= 5 * mm
    rgb(c, MAGNET)
    rgb(c, INK, stroke=True)
    c.setLineWidth(0.4)
    c.rect(x + 3 * mm, y - 0.2 * mm, 2.6 * mm, 2.6 * mm, fill=1, stroke=1)
    rgb(c, INK)
    c.rect(x + 12 * mm - 11 * mm + 50 * mm, y + 0.4 * mm, 6 * mm, 1.2 * mm,
           fill=1, stroke=0)
    text(c, x + 11 * mm, y, "Magnets (back of frame)", 8)
    text(c, x + 59 * mm, y, "Air slots 30 × 3, top + bottom, over the gap "
         "round the box", 8)


# ---- side cut (enlarged) ---------------------------------------------------
def side_cut(c):
    k = 1.35 * mm                      # page units per real mm
    z0, v0 = -32.0, -48.0              # real-coordinate origin of the box
    X0, Y0 = 182 * mm, 84 * mm

    def P(z, v):
        return X0 + (z - z0) * k, Y0 + (v - v0) * k

    def box(z1, v1, z2, v2, fill, stroke=None, lw=0.5):
        (x1, y1), (x2, y2) = P(z1, v1), P(z2, v2)
        rgb(c, fill)
        if stroke:
            rgb(c, stroke, stroke=True)
            c.setLineWidth(lw)
        c.rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1),
               fill=1, stroke=1 if stroke else 0)

    text(c, 182 * mm, 186 * mm, "2.  SIDE CUT through the top edge  "
         "(drawn bigger)", 10, True)

    # cavity (open hole) + room
    box(0, -48, 44, 0, CAVITY)
    # wall above the hole, hatched
    box(0, 0, 44, 24, WALL)
    c.saveState()
    p = c.beginPath()
    x1, y1 = P(0, 0)
    x2, y2 = P(44, 24)
    p.rect(x1, y1, x2 - x1, y2 - y1)
    c.clipPath(p, stroke=0, fill=0)
    rgb(c, HATCH, stroke=True)
    c.setLineWidth(0.4)
    for i in range(-30, 80, 3):
        a, b = P(i, 0), P(i + 24, 24)
        c.line(a[0], a[1], b[0], b[1])
    c.restoreState()
    rgb(c, INK, stroke=True)
    c.setLineWidth(0.8)
    a, b = P(0, 0), P(0, 24)
    c.line(*a, *b)                      # wall face
    a, b = P(0, 0), P(44, 0)
    c.line(*a, *b)                      # top of hole
    # break lines
    rgb(c, GREY, stroke=True)
    c.setDash(2, 1.5)
    c.setLineWidth(0.4)
    a, b = P(-10, -48), P(44, -48)
    c.line(*a, *b)
    c.setDash()

    # frame (flange + lip) and its vent slot over the air gap
    box(-10, -34, 0, 20, WALNUT, WALNUT_DARK)
    box(-10, -5, 0, -2, CAVITY)
    # box wall
    box(0, -18, 30, -6, WALNUT_DARK, WALNUT_DARK)
    # magnet + steel plate
    box(-4, 6, 0, 14, MAGNET, INK, 0.4)
    box(0, 6, 1.5, 14, STEEL, INK, 0.4)
    # felt, screen, foam, backboard, turn-button
    box(0, -34, 1, -19, FELT)
    box(1, -48, 9, -19, SCREEN)
    box(9, -42, 12, -26, FOAM)
    box(12, -48, 18, -18, PLY, (0.55, 0.45, 0.28), 0.4)
    box(18, -27, 22, -18, (0.30, 0.30, 0.30))

    # labels on the room side (left)
    lx = 182 * mm + 1 * mm
    leader(c, lx, P(0, 20)[1] + 2 * mm, *P(-6, 18),
           "FRAME  10 thick", bold=True)
    leader(c, lx, P(0, 11)[1], *P(-2, 10), "MAGNET in frame\n+ steel plate in wall")
    leader(c, lx, P(0, -1)[1] - 1 * mm, *P(-5, -3.5),
           "AIR SLOT over\n~6 gap round the box")
    leader(c, lx, P(0, -22)[1], *P(-6, -26),
           "LIP covers 15 of\nthe glass border", bold=True)
    leader(c, lx, P(0, -36)[1] - 2 * mm, *P(-10, -34),
           "WINDOW EDGE")
    text(c, lx, P(0, -47)[1], "ROOM / STAIRS  ←", 7.5, True, GREY)

    # labels on the wall side (right)
    rx = P(31, 0)[0]
    leader(c, rx, P(0, -10)[1] + 1.2 * mm, *P(26, -12), "BOX WALL 12", bold=True)
    leader(c, rx, P(0, -23)[1], *P(20, -22.5), "TURN-BUTTON")
    leader(c, rx, P(0, -30)[1], *P(10.5, -33), "FOAM 3")
    leader(c, rx, P(0, -35.5)[1], *P(0.5, -30), "FELT 1")
    leader(c, rx, P(0, -40.5)[1], *P(15, -44), "BACKBOARD 6")
    leader(c, rx, P(0, -45.5)[1], *P(5, -46), "SCREEN ≈ 8–10")
    text(c, P(2, 0)[0], P(0, 17)[1], "WALL", 8, True, (0.45, 0.35, 0.22))
    text(c, P(43, 0)[0], P(0, -3.5)[1], "HOLE, 80 deep →", 7, True, GREY,
         "right")


# ---- steps + don'ts ----------------------------------------------------------
STEPS = [
    "Measure the REAL screen glass (≈ 330.6 × 232) and the REAL wall hole",
    "    after the mason (≈ 370 × 270, 80 deep). Your measurements win.",
    "Front frame 410 × 310, ~10 thick. Window 300 × 202 on the picture.",
    "Box glued behind the window: 12 walls, inside 333 × 234, ~30 deep.",
    "1 mm felt on the lip. Screen in, glass first (red film still on).",
    "3 mm foam strips on the silver back, then the 6 mm ply backboard",
    "    with a cut-out for the blue board + plugs (+50 on the plug side).",
    "4 turn-buttons hold the backboard. The box bottom rests in the hole",
    "    (it carries the weight, ~2.5 kg); 4 magnets only hold it closed.",
]


def steps(c):
    text(c, 182 * mm, 77 * mm, "3.  HOW TO BUILD IT", 10, True)
    y = 72 * mm
    n = 0
    for line in STEPS:
        if line.startswith("    "):
            text(c, 186 * mm, y, line.strip(), 7.6)
        else:
            n += 1
            text(c, 182 * mm, y, f"{n}.", 7.6, True)
            text(c, 186 * mm, y, line, 7.6)
        y -= 3.9 * mm


DONTS = [
    ("NO SCREWS, NAILS OR GLUE", "into the screen. It is only clamped,",
     "so it can come out for repair."),
    ("DON'T PRESS THE BACK", "Keep foam and wood off the blue board and",
     "the black taped strip (ribbon cable under it)."),
    ("LEAVE ROOM FOR CABLES", "Cables come up from the bottom of the hole.",
     "Leave 200 of loop so the frame pops forward."),
]


def donts(c):
    w, h, gap = 88 * mm, 22 * mm, 4.5 * mm
    x = 14 * mm
    for title, l1, l2 in DONTS:
        rgb(c, (1, 0.95, 0.95))
        rgb(c, RED, stroke=True)
        c.setLineWidth(1.1)
        c.roundRect(x, 12 * mm, w, h, 2 * mm, fill=1, stroke=1)
        text(c, x + 4 * mm, 12 * mm + h - 6.5 * mm, "✕  " + title, 9.5, True,
             RED)
        text(c, x + 4 * mm, 12 * mm + h - 12.5 * mm, l1, 8.2)
        text(c, x + 4 * mm, 12 * mm + h - 17 * mm, l2, 8.2)
        x += w + gap


def main():
    W, H = landscape(A4)
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Staircase screen — carpenter sheet")
    # title band
    rgb(c, WALNUT_DARK)
    c.rect(0, H - 17 * mm, W, 17 * mm, fill=1, stroke=0)
    text(c, 14 * mm, H - 9.5 * mm, "STAIRCASE TOUCH SCREEN — WOODEN FRAME",
         15, True, WHITE)
    text(c, 14 * mm, H - 14.3 * mm,
         "Carpenter sheet  ·  Waveshare 14-inch screen (bare panel, no screw "
         "holes)  ·  all sizes in mm  ·  build it with the real screen on "
         "your bench", 8.5, False, (0.95, 0.90, 0.84))
    front_view(c)
    side_cut(c)
    steps(c)
    donts(c)
    text(c, W - 14 * mm, 6 * mm,
         "Staircase panel · spec v3.4 · 18 Oct 2026 · source: "
         "electrical/WAVESHARE_INDOOR_PANEL.md", 6.5, False, GREY, "right")
    c.showPage()
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
