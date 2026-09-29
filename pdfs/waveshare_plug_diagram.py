"""
Draw install step 3 of the Waveshare staircase guide in code (no AI):
which plug goes in which socket on the back of the (G) screen, and why all
3 plugs must be L-shaped. Gemini kept drawing straight HDMI/USB plugs here,
and the L-shaped plugs are the whole point of this step.

Used by build_waveshare_install_guide_pdf.py (step 3). Standalone:
  python3 waveshare_plug_diagram.py [out.png]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 896  # same 4:3 size as the Gemini pictures
S = 2             # draw at 2x, then downsample for smooth lines

INK = (23, 23, 23)
GREY = (105, 105, 105)
WHITE = (255, 255, 255)
WALL = (238, 224, 196)
HATCH = (214, 194, 158)
CAVITY = (255, 252, 244)
WALNUT = (126, 80, 46)
WALNUT_DARK = (96, 58, 33)
CASE = (40, 42, 46)
BAY = (74, 78, 84)
PORT = (206, 210, 214)
PORT_HOLE = (52, 52, 52)
PLUG = (32, 32, 32)
CONDUIT = (198, 202, 206)
PANEL = (251, 246, 236)
PANEL_EDGE = (201, 178, 138)
HEAD = (80, 50, 20)
RED = (198, 40, 40)
GREEN = (46, 125, 50)

_FONTS: dict = {}


def _font(size: float, bold: bool = False):
    key = (size, bold)
    if key not in _FONTS:
        px = round(size * S)
        candidates = [
            ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0),
            ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
             else "/System/Library/Fonts/Supplemental/Arial.ttf", 0),
            ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", 0),
        ]
        for path, index in candidates:
            try:
                _FONTS[key] = ImageFont.truetype(path, px, index=index)
                break
            except OSError:
                continue
        else:
            _FONTS[key] = ImageFont.load_default(px)
    return _FONTS[key]


class Pen:
    """ImageDraw wrapper that takes coordinates in 1x units."""

    def __init__(self, img: Image.Image):
        self.img = img
        self.d = ImageDraw.Draw(img)

    @staticmethod
    def _pts(pts):
        return [(x * S, y * S) for x, y in pts]

    def rect(self, box, fill=None, outline=INK, width=2.5, radius=0):
        xy = [v * S for v in box]
        w = round(width * S) if outline else 0
        if radius:
            self.d.rounded_rectangle(xy, radius * S, fill=fill,
                                     outline=outline, width=w)
        else:
            self.d.rectangle(xy, fill=fill, outline=outline, width=w)

    def line(self, pts, fill=INK, width=1.5):
        self.d.line(self._pts(pts), fill=fill, width=round(width * S),
                    joint="curve")

    def poly(self, pts, fill=None, outline=INK, width=2.0):
        self.d.polygon(self._pts(pts), fill=fill)
        if outline:
            self.line(list(pts) + [pts[0]], outline, width)

    def circle(self, cx, cy, r, fill=None, outline=INK, width=2.0):
        box = [(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S]
        self.d.ellipse(box, fill=fill, outline=outline,
                       width=round(width * S) if outline else 0)

    def cable(self, pts, fill=PLUG, width=7.0):
        """Thick polyline with round ends."""
        self.line(pts, fill, width)
        for x, y in (pts[0], pts[-1]):
            self.circle(x, y, width / 2, fill=fill, outline=None)

    def text(self, xy, s, size=20, bold=False, fill=INK, anchor="la"):
        self.d.text((xy[0] * S, xy[1] * S), s, font=_font(size, bold),
                    fill=fill, anchor=anchor)

    def width_of(self, s, size, bold=False):
        return _font(size, bold).getlength(s) / S

    def wrap(self, s, size, bold, max_w):
        lines, cur = [], ""
        for word in s.split():
            trial = f"{cur} {word}".strip()
            if cur and self.width_of(trial, size, bold) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        return lines + [cur] if cur else lines

    def callout(self, x, y, w, head, body, target, color=INK, size=19):
        """White label box with a leader line to `target`; head is bold."""
        pad, lh = 9, size * 1.28
        lines = []
        if head:
            lines += [(t, True) for t in self.wrap(head, size, True,
                                                   w - 2 * pad)]
        lines += [(t, False) for t in self.wrap(body, size, False,
                                                w - 2 * pad)]
        h = 2 * pad + lh * len(lines)
        tx, ty = target
        self.line([(x, y + h / 2), (tx, ty)], INK, 1.6)
        self.circle(tx, ty, 4, fill=INK, outline=WHITE, width=1.5)
        self.rect((x, y, x + w, y + h), fill=WHITE, outline=INK, width=1.6,
                  radius=7)
        for i, (t, bold) in enumerate(lines):
            self.text((x + pad, y + pad + i * lh), t, size, bold,
                      color if bold else INK)

    def mark(self, cx, cy, r, kind):
        """Round badge: a number, or 'x' (red cross) / 'ok' (green tick)."""
        if kind == "x":
            self.circle(cx, cy, r, fill=RED, outline=None)
            k = r * 0.45
            self.line([(cx - k, cy - k), (cx + k, cy + k)], WHITE, r * 0.28)
            self.line([(cx - k, cy + k), (cx + k, cy - k)], WHITE, r * 0.28)
        elif kind == "ok":
            self.circle(cx, cy, r, fill=GREEN, outline=None)
            self.line([(cx - r * 0.48, cy + r * 0.02),
                       (cx - r * 0.12, cy + r * 0.38),
                       (cx + r * 0.5, cy - r * 0.36)], WHITE, r * 0.26)
        else:
            self.circle(cx, cy, r, fill=HEAD, outline=None)
            self.text((cx, cy + 1), kind, r * 1.15, True, WHITE, "mm")


# --------------------------------------------------------------------------- #
# Left panel - back of the screen, which plug goes where
# --------------------------------------------------------------------------- #
SOCKETS = [  # (centre x, marker, name, what it is)
    (180, "1", "HDMI", "the picture, from the server"),
    (258, "2", "Touch USB (micro-USB)",
     "touch only - it does NOT power the screen"),
    (330, "3", "12V power in",
     "12V 2A, from the PoE splitter or the 12V supply"),
    (404, "x", "5V 3A - leave empty",
     "it gives power OUT; it is not the power input"),
]


def _left_panel(p: Pen) -> None:
    p.rect((24, 24, 560, 872), fill=PANEL, outline=PANEL_EDGE, width=2,
           radius=18)
    p.text((48, 44), "BACK OF THE SCREEN", 30, True, HEAD)
    p.text((48, 84), "which plug goes where - match the names", 21, False,
           GREY)

    # walnut frame, black screen case, VESA 75 holes
    p.rect((62, 124, 522, 462), fill=WALNUT, width=3, radius=6)
    for y in (133, 141, 447, 454):
        p.line([(78, y), (506, y)], WALNUT_DARK, 1.2)
    for x in (72, 80, 504, 512):
        p.line([(x, 150), (x, 436)], WALNUT_DARK, 1.2)
    p.rect((94, 156, 490, 430), fill=CASE, width=2.5, radius=8)
    for cx, cy in ((242, 198), (342, 198), (242, 298), (342, 298)):
        p.circle(cx, cy, 6, fill=(96, 100, 106), width=1.5)

    # recessed port bay with the 4 sockets
    p.rect((132, 340, 452, 410), fill=BAY, width=2.5, radius=6)
    p.line([(140, 346), (444, 346)], (52, 55, 60), 3)
    p.poly([(152, 372), (208, 372), (201, 392), (159, 392)], PORT)
    p.poly([(161, 378), (199, 378), (195, 386), (165, 386)], PORT_HOLE,
           None)
    p.poly([(240, 376), (276, 376), (271, 389), (245, 389)], PORT)
    p.poly([(247, 380), (269, 380), (266, 385), (250, 385)], PORT_HOLE,
           None)
    p.circle(330, 382, 11, fill=PORT)
    p.circle(330, 382, 5.5, fill=PORT_HOLE, outline=None)
    p.circle(330, 382, 2, fill=PORT, outline=None)
    p.rect((380, 372, 428, 392), fill=PORT, width=2)
    p.rect((385, 377, 423, 383), fill=PORT_HOLE, outline=None)
    for cx, tag in ((180, "HDMI"), (258, "USB"), (330, "12V"),
                    (404, "5V 3A")):
        p.text((cx, 358), tag, 12, True, (222, 224, 228), "mm")

    # numbered markers under each socket
    for cx, kind, _, _ in SOCKETS:
        p.line([(cx, 396), (cx, 472)], INK, 1.6)
        p.circle(cx, 396, 4, fill=INK, outline=WHITE, width=1.5)
        p.mark(cx, 490, 17, kind)

    # legend
    y = 534
    for _, kind, name, what in SOCKETS:
        p.mark(66, y + 12, 15, kind)
        p.text((94, y), name, 21, True, RED if kind == "x" else INK)
        body = p.wrap(what, 19, False, 440)
        for i, t in enumerate(body):
            p.text((94, y + 29 + i * 24), t, 19, False, GREY)
        y += 29 + 24 * len(body) + 12
    for i, t in enumerate(p.wrap("All 3 plugs must be L-shaped - see right",
                                 21, True, 480)):
        p.text((48, y + 8 + i * 27), t, 21, True, HEAD)


# --------------------------------------------------------------------------- #
# Right panel - side view through the cavity: straight vs L-shaped plug
# --------------------------------------------------------------------------- #
def _section(p: Pen, top: float, straight: bool) -> None:
    color = RED if straight else GREEN
    p.mark(624, top + 22, 19, "x" if straight else "ok")
    p.text((654, top + 10),
           "STRAIGHT PLUG - WILL NOT FIT" if straight
           else "L-SHAPED PLUG - FITS", 24, True, color)

    ox, oy = 640, top + 62      # wall face, top of the drawn slice
    ys = oy + 150               # bottom edge of the screen
    yf = ys + 18                # cavity floor (6-8 mm below the screen)
    yb = oy + 250               # bottom of the drawn wall
    xc = ox + 208               # cavity back wall (80 mm deep)
    xr = 900                    # right edge of the drawn wall
    kx = ox + 55                # plug centre line

    # wall cut in section (hatched), with the cavity taken out
    x0, y0, x1, y1 = ox * S, oy * S, xr * S, yb * S
    hatch = Image.new("RGB", (x1 - x0, y1 - y0), WALL)
    hd = ImageDraw.Draw(hatch)
    for i in range(-(y1 - y0), x1 - x0, 13 * S):
        hd.line([(i, y1 - y0), (i + (y1 - y0), 0)], fill=HATCH, width=S)
    mask = Image.new("L", hatch.size, 255)
    ImageDraw.Draw(mask).rectangle((0, 0, (xc - ox) * S, (yf - oy) * S),
                                   fill=0)
    p.img.paste(hatch, (x0, y0), mask)
    p.rect((ox, oy, xc, yf), fill=CAVITY, outline=None)
    p.line([(xc, oy), (xc, yf), (ox, yf), (ox, yb)], INK, 2.5)
    p.text(((ox + xc) / 2 + 30, oy + 22), "cavity", 18, False, GREY, "mm")

    # conduit down to the server, near the back of the cavity
    p.rect((xc - 44, yf, xc - 20, yb), fill=CONDUIT, outline=None)
    p.line([(xc - 44, yf), (xc - 44, yb)], INK, 2)
    p.line([(xc - 20, yf), (xc - 20, yb)], INK, 2)

    # walnut bezel on the wall face
    p.rect((ox - 12, ys - 34, ox, yf + 56), fill=WALNUT, width=2.5)

    # screen (seen edge-on) with the recessed port bay on its back
    sx0, sx1 = ox + 4, ox + 65
    p.rect((sx0, oy, sx1, ys), fill=CASE, outline=None)
    p.rect((ox + 45, ys - 50, sx1, ys - 8), fill=BAY, outline=None)
    p.line([(sx0, oy), (sx0, ys), (sx1, ys), (sx1, ys - 8),
            (ox + 45, ys - 8), (ox + 45, ys - 50), (sx1, ys - 50),
            (sx1, oy)], INK, 2.5)
    p.rect((ox + 47, ys - 50, ox + 63, ys - 44), fill=PORT, width=1.5)

    if straight:
        body = [(kx - 8, ys - 44), (kx + 8, ys - 44), (kx + 8, ys + 26),
                (kx - 8, ys + 26)]
        p.poly(body, PLUG)
        p.poly([(kx - 8, ys + 26), (kx + 8, ys + 26), (kx + 4, ys + 38),
                (kx - 4, ys + 38)], PLUG)
        p.cable([(kx, ys + 38), (kx, ys + 60)])
        # the part that would have to go into the floor
        p.poly([(kx - 8, yf), (kx + 8, yf), (kx + 8, ys + 26),
                (kx + 4, ys + 38), (kx - 4, ys + 38), (kx - 8, ys + 26)],
               (214, 72, 72), RED, 2.5)
        p.line([(kx - 5, ys + 38), (kx - 5, ys + 60), (kx + 5, ys + 60),
                (kx + 5, ys + 38)], RED, 2.5)
        star = []
        for i in range(16):
            r = 22 if i % 2 == 0 else 10
            a = i * 3.14159 / 8
            star.append((kx + r * math.cos(a),
                         yf + r * math.sin(a)))
        p.poly(star, None, RED, 2.5)
        p.callout(915, oy - 4, 245, "", "Screen", (ox + 34, oy + 40))
        p.callout(915, oy + 48, 245, "",
                  "Only 6-8 mm spare around the screen", (ox + 24, ys + 9))
        p.callout(915, oy + 128, 245, "Straight plug:",
                  "sticks out past the screen edge and hits the cavity wall",
                  (kx + 12, yf + 4), RED)
    else:
        p.poly([(kx - 8, ys - 44), (kx + 8, ys - 44), (kx + 8, ys - 40),
                (ox + 92, ys - 40), (ox + 92, ys - 20), (kx - 8, ys - 20)],
               PLUG)
        p.poly([(ox + 92, ys - 38), (ox + 104, ys - 34), (ox + 104, ys - 26),
                (ox + 92, ys - 22)], PLUG)
        r, cy = 22, ys - 30
        cx = xc - 32
        arc = [(cx - r + r * math.sin(a / 10 * 1.5708),
                cy + r - r * math.cos(a / 10 * 1.5708))
               for a in range(11)]
        p.cable([(ox + 104, cy), (cx - r, cy)] + arc + [(cx, yb - 4)])
        p.callout(915, oy + 38, 245, "L-shaped plug:",
                  "the cable turns straight back into the cavity - it fits",
                  (ox + 98, ys - 30), GREEN)
        p.callout(915, oy + 160, 245, "",
                  "Cable runs to the conduit and down to the server",
                  (cx - 12, yf + 44))


def _right_panel(p: Pen) -> None:
    p.rect((580, 24, 1176, 872), fill=PANEL, outline=PANEL_EDGE, width=2,
           radius=18)
    p.text((604, 44), "WHY L-SHAPED PLUGS", 30, True, HEAD)
    p.text((604, 84), "side view through the wall cavity", 21, False, GREY)
    _section(p, 128, straight=True)
    p.line([(604, 486), (1152, 486)], PANEL_EDGE, 1.5)
    _section(p, 500, straight=False)


def draw(out_path: Path) -> None:
    img = Image.new("RGB", (W * S, H * S), WHITE)
    p = Pen(img)
    _left_panel(p)
    _right_panel(p)
    img.resize((W, H), Image.LANCZOS).save(out_path)


if __name__ == "__main__":
    draw(Path(sys.argv[1] if len(sys.argv) > 1 else "install-step-3.png"))
