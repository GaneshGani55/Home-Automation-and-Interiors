"""
WATER_AUTOMATION_VISUAL_v2.pdf
Replaces the failed v1 (which had a zoomed-out hero shot nobody could parse).

v2 approach: each page has ONE focused AI image of a single component, with
PRECISE Python-rendered labels and callout arrows on top of it. The AI handles
the realistic 3D visualization, Python handles the technical accuracy.

Pages:
  1. Cover
  2. Sintex tank + sensor riser modification (close-up)
  3. Sintex JB on parapet wall
  4. Sump cross-section (probe + float inside the pit)
  5. Sump JB on porch wall (manhole cover open against wall)
  6. JB internals (exploded view)

Each image is annotated with callout lines pointing to features.

Run: python3 build_water_automation_visual_v2_pdf.py
"""
from fpdf import FPDF
from pathlib import Path
from PIL import Image
import math

ROOT = Path(__file__).parent.parent
IMG_DIR = ROOT / "interior-design" / "generated-images"
OUT = Path(__file__).parent / "WATER_AUTOMATION_VISUAL_v2.pdf"

INK         = ( 28,  28,  30)
INK_SOFT    = ( 90,  90,  95)
INK_FAINT   = (140, 140, 145)
RULE        = (220, 215, 205)
PAPER_TINT  = (252, 248, 240)

GOLD        = (172, 130,  50)
GOLD_DARK   = (130,  95,  30)
GOLD_BAR    = (190, 150,  70)
GOLD_PALE   = (245, 234, 210)

INFO        = ( 50, 100, 160)
INFO_PALE   = (228, 238, 250)
DANGER      = (180,  60,  50)
DANGER_PALE = (250, 230, 225)
GOOD        = ( 70, 125,  70)
GOOD_PALE   = (228, 244, 230)
COPPER      = (175, 110,  60)
WARN        = (180, 130,  40)


class VisualPDF(FPDF):
    MX = 14
    MY_TOP = 14
    MY_BOT = 12

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=self.MY_BOT)
        self.set_margins(self.MX, self.MY_TOP, self.MX)
        self._section = ""

    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(6)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*INK_FAINT)
        self.cell(0, 4, self._section.upper() if self._section else "WATER AUTOMATION VISUAL", align="L")
        self.set_x(-self.MX - 10)
        self.cell(10, 4, f"{self.page_no():02d}", align="R")
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.2)
        self.line(self.MX, 12, 210 - self.MX, 12)
        self.set_y(self.MY_TOP)

    def footer(self):
        self.set_y(-9)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_FAINT)
        self.cell(0, 4, "Water Automation - VISUAL v2  -  Annotated AI images  -  2026-05-29", align="C")

    def page_title(self, num, title, sub=None):
        self.set_y(14)
        self.set_fill_color(*GOLD_BAR)
        self.rect(self.MX, 14, 14, 5, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(self.MX, 14)
        self.cell(14, 5, f"  {num:02d}", align="L")
        self.set_xy(self.MX, 22)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*INK)
        self.cell(0, 9, title)
        if sub:
            self.set_xy(self.MX, 32)
            self.set_font("Helvetica", "I", 10.5)
            self.set_text_color(*INK_SOFT)
            self.cell(0, 6, sub)
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.5)
        y = 40 if sub else 34
        self.line(self.MX, y, self.MX + 22, y)
        self.set_y(y + 4)

    def callout_arrow(self, target_x, target_y, label_x, label_y, label, color=INK, side="R"):
        """Draw a callout line from target (feature on image) to label position.
        side: which side of the label the line should connect to.
              'R' means label is on the right of target -> line connects to label's LEFT edge
              'L' means label is on the left of target  -> line connects to label's RIGHT edge
              'T'/'B' means label is above/below       -> line connects to label's BOTTOM/TOP centre
        """
        self.set_draw_color(*color)
        self.set_line_width(0.4)
        # Anchor at target with small filled dot
        self.set_fill_color(*color)
        self.ellipse(target_x - 0.8, target_y - 0.8, 1.6, 1.6, "F")
        # Label text first (so we can compute its right edge)
        self.set_font("Helvetica", "B", 8)
        lbl_w = self.get_string_width(label)
        # Decide line endpoint based on side
        if side == "R":
            line_end_x = label_x - 1.5
            line_end_y = label_y
        elif side == "L":
            line_end_x = label_x + lbl_w + 1.5
            line_end_y = label_y
        elif side == "T":
            line_end_x = label_x + lbl_w / 2
            line_end_y = label_y + 2.5   # below the label baseline approx
        else:  # B
            line_end_x = label_x + lbl_w / 2
            line_end_y = label_y - 1
        self.line(target_x, target_y, line_end_x, line_end_y)
        # Label text
        self.set_text_color(*color)
        self.text(label_x, label_y + 1, label)

    def callouts(self, image_box, callouts_data, page_left=14, page_right=196):
        """Draw a set of callouts. Image is centered; labels go in left/right zones.
        image_box: (x, y, w, h) of where the image is on the page
        page_left, page_right: leftmost/rightmost x coordinates for label text
        """
        ix, iy, iw, ih = image_box
        self.set_font("Helvetica", "B", 8)
        for c in callouts_data:
            tx = ix + c["rel_x"] * iw
            ty = iy + c["rel_y"] * ih
            side = c.get("side", "R")
            offset = c.get("offset", 8)
            color = c.get("color", INK)
            lbl = c["label"]
            lbl_w = self.get_string_width(lbl)
            if side == "R":
                lx = ix + iw + offset
                # Clamp so label fits within page_right
                if lx + lbl_w > page_right:
                    lx = page_right - lbl_w
                ly = ty
            elif side == "L":
                lx = ix - offset - lbl_w - 2
                # Clamp so label doesn't go off page_left
                if lx < page_left:
                    lx = page_left
                ly = ty
            elif side == "T":
                lx = tx - lbl_w / 2
                if lx < page_left:
                    lx = page_left
                if lx + lbl_w > page_right:
                    lx = page_right - lbl_w
                ly = iy - 3   # close to image top, below title underline
            else:  # B
                lx = tx - lbl_w / 2
                if lx < page_left:
                    lx = page_left
                if lx + lbl_w > page_right:
                    lx = page_right - lbl_w
                ly = iy + ih + 4
            self.callout_arrow(tx, ty, lx, ly, lbl, color, side=side)


def annotated_image_page(pdf, num, title, sub, image_path, callouts_data, caption_label, caption_text):
    """Render an image with annotation overlays + caption."""
    pdf._section = f"{num:02d} {title}"
    pdf.add_page()
    pdf.page_title(num, title, sub)

    if not image_path.exists():
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*DANGER)
        pdf.cell(0, 10, f"MISSING IMAGE: {image_path.name}")
        return

    # Calculate image placement - centered, with label zones BOTH sides
    page_w = 210 - 2 * pdf.MX
    label_zone_w = 34   # each side
    img_avail_w = page_w - 2 * label_zone_w   # ~114 mm
    img_top = pdf.get_y() + 4
    # Get image natural aspect
    im = Image.open(image_path)
    iw_px, ih_px = im.size
    img_h = img_avail_w * ih_px / iw_px
    # Cap image height
    max_img_h = 150
    if img_h > max_img_h:
        img_h = max_img_h
        img_w_adj = img_h * iw_px / ih_px
    else:
        img_w_adj = img_avail_w
    # Centre image horizontally on the page
    ix = (210 - img_w_adj) / 2
    iy = img_top
    pdf.image(str(image_path), x=ix, y=iy, w=img_w_adj, h=img_h)

    # Draw callouts - constrain to page margins
    pdf.callouts((ix, iy, img_w_adj, img_h), callouts_data,
                 page_left=pdf.MX, page_right=210 - pdf.MX)

    # Caption
    pdf.set_y(iy + img_h + 6)
    if pdf.get_y() > 250:
        pdf.set_y(250)
    # bar callout
    x0 = pdf.MX
    body_x = x0 + 5
    body_w = 210 - 2 * pdf.MX - 5
    y_start = pdf.get_y()
    pdf.set_xy(body_x, y_start)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*INFO)
    pdf.cell(0, 4.5, caption_label.upper(), ln=1)
    pdf.set_x(body_x)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(body_w, 5, caption_text)
    y_end = pdf.get_y()
    pdf.set_fill_color(*INFO)
    pdf.rect(x0, y_start + 0.5, 1.4, y_end - y_start - 0.5, "F")


def page_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*PAPER_TINT)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 0, 210, 2.5, "F")
    pdf.rect(0, 294.5, 210, 2.5, "F")

    pdf.set_xy(pdf.MX, 50)
    pdf.set_font("Helvetica", "", 30)
    pdf.set_text_color(*INK)
    pdf.cell(0, 12, "Water Automation")
    pdf.set_xy(pdf.MX, 64)
    pdf.cell(0, 12, "Visual Handoff  v2")

    pdf.set_xy(pdf.MX, 84)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 6, "Close-up renders. Every part labelled. No guess-work.")

    pdf.set_draw_color(*GOLD_BAR)
    pdf.set_line_width(0.8)
    pdf.line(pdf.MX, 98, pdf.MX + 60, 98)

    pdf.set_xy(pdf.MX, 116)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 6, "WHAT'S INSIDE")

    items = [
        ("02", "Sintex tank + sensor riser",  "How the cap is modified, where the sensor sits, where the float hangs"),
        ("03", "Sintex JB on parapet wall",   "Where the box mounts on terrace, where the conduit drops to"),
        ("04", "Sump cross-section",          "What's inside the pit: probe, float, water levels"),
        ("05", "Sump JB on porch W wall",     "Why the box sits beside the manhole, not above it"),
        ("06", "Inside the JB",               "ESP32, PoE splitter, terminal block, 4 cable glands"),
    ]
    for i, (n, t, d) in enumerate(items):
        y = 130 + i * 14
        pdf.set_fill_color(*GOLD_PALE)
        pdf.rect(pdf.MX, y, 8, 8, "F")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*GOLD_DARK)
        pdf.set_xy(pdf.MX, y + 1.5)
        pdf.cell(8, 5, n, align="C")
        pdf.set_xy(pdf.MX + 12, y)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*INK)
        pdf.cell(0, 5, t)
        pdf.set_xy(pdf.MX + 12, y + 5)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*INK_SOFT)
        pdf.cell(0, 4, d)

    pdf.set_xy(pdf.MX, 232)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 5, "USE WITH")
    pdf.set_xy(pdf.MX, 238)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5,
                   "WATER_AUTOMATION_SCHEMATIC.pdf  -  the wiring schematics (floor plan + circuit)\n"
                   "WATER_AUTOMATION.pdf  -  the long-form spec with full BOM and sign-off checklist")

    pdf.set_xy(pdf.MX, 264)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*INK_FAINT)
    pdf.cell(0, 4, "v2.0  -  2026-05-29  -  AI renders annotated with Python overlay")


def build():
    pdf = VisualPDF()
    page_cover(pdf)

    # Page 2: Sintex riser
    annotated_image_page(
        pdf, 2, "Sintex tank + sensor riser",
        "Where to drill the cap, what to mount on top",
        IMG_DIR / "water-automation-sintex-riser-v1.png",
        [
            {"rel_x": 0.5, "rel_y": 0.10, "side": "R", "label": "JSN-SR04T", "color": INFO},
            {"rel_x": 0.5, "rel_y": 0.22, "side": "R", "label": "30 cm PVC riser", "color": INFO},
            {"rel_x": 0.45, "rel_y": 0.42, "side": "R", "label": "screw cap (drilled)", "color": GOLD_DARK},
            {"rel_x": 0.55, "rel_y": 0.55, "side": "R", "label": "float switch (95%)", "color": DANGER},
            {"rel_x": 0.50, "rel_y": 0.80, "side": "R", "label": "1500 L Sintex", "color": INK},
            {"rel_x": 0.20, "rel_y": 0.90, "side": "L", "label": "terrace SW corner", "color": INK_SOFT},
        ],
        "What this shows",
        "Sintex tank cap modified: drill a 32 mm hole at the centre, install a 1\" threaded PVC fitting "
        "with rubber gasket, screw in a 30 cm vertical PVC pipe. JSN-SR04T sensor sits inside a small "
        "weatherproof cap at the top of the riser, cable exits sideways. The high-level float hangs "
        "inside the tank from a separate small hole in the screw cap.",
    )

    # Page 3: Sintex JB on parapet
    annotated_image_page(
        pdf, 3, "Sintex JB on parapet wall",
        "Terrace SW corner, shaded side of the parapet",
        IMG_DIR / "water-automation-sintex-jb-mount-v1.png",
        [
            {"rel_x": 0.50, "rel_y": 0.30, "side": "R", "label": "IP66 JB", "color": INFO},
            {"rel_x": 0.50, "rel_y": 0.55, "side": "R", "label": "4 cable glands", "color": INK},
            {"rel_x": 0.42, "rel_y": 0.70, "side": "L", "label": "conduit drops", "color": INFO},
            {"rel_x": 0.42, "rel_y": 0.90, "side": "L", "label": "terrace floor", "color": INK_SOFT},
            {"rel_x": 0.60, "rel_y": 0.15, "side": "T", "label": "parapet wall top", "color": INK_SOFT},
        ],
        "What this shows",
        "Junction box mounted on the inner face of the terrace parapet, shaded side. Conduit drops down "
        "the wall surface to the embedded C-Sintex-1 (Cat6) and C-Sintex-2 (float wire) conduits that "
        "run under the terrace screed back into the staircase shaft.",
    )

    # Page 4: Sump cross-section (if available)
    sump_x_img = IMG_DIR / "water-automation-sump-crosssection-v1.png"
    if sump_x_img.exists():
        annotated_image_page(
            pdf, 4, "Sump cross-section",
            "What's inside the pit",
            sump_x_img,
            [
                {"rel_x": 0.20, "rel_y": 0.85, "side": "L", "label": "pressure probe", "color": COPPER},
                {"rel_x": 0.75, "rel_y": 0.65, "side": "R", "label": "low-level float (25 cm)", "color": DANGER},
                {"rel_x": 0.50, "rel_y": 0.10, "side": "T", "label": "manhole cover", "color": INK},
                {"rel_x": 0.50, "rel_y": 0.50, "side": "R", "label": "water level", "color": INFO},
                {"rel_x": 0.10, "rel_y": 0.50, "side": "L", "label": "brick + waterproof", "color": INK_SOFT},
            ],
            "What this shows",
            "Inside the underground sump: pressure transducer probe hangs ~10 cm above the floor for "
            "level reading. Low-level pendulum float hangs at ~25 cm - when water drops below this, the "
            "float opens and kills the booster pump (dry-run protection, mechanical, no server needed).",
        )

    # Page 5: Sump JB on porch wall (existing image)
    annotated_image_page(
        pdf, 5, "Sump JB on porch wall",
        "Porch W wall, 300 mm above floor, BESIDE the manhole",
        IMG_DIR / "water-automation-sump-jb-mount-v1.png",
        [
            {"rel_x": 0.65, "rel_y": 0.40, "side": "R", "label": "IP66 JB", "color": INFO},
            {"rel_x": 0.65, "rel_y": 0.55, "side": "R", "label": "4 cable glands", "color": INK},
            {"rel_x": 0.30, "rel_y": 0.50, "side": "L", "label": "manhole cover (OPEN, against wall)", "color": DANGER},
            {"rel_x": 0.40, "rel_y": 0.80, "side": "L", "label": "sump pit below", "color": COPPER},
            {"rel_x": 0.50, "rel_y": 0.30, "side": "T", "label": "conduit up the wall", "color": INFO},
            {"rel_x": 0.85, "rel_y": 0.15, "side": "T", "label": "corner window sill above", "color": INK_SOFT},
        ],
        "What this shows",
        "JB mounted at knee-height on porch W wall, BESIDE the manhole - not directly above. The "
        "manhole cover hinges on the W side and lies flat against this wall when open, so the JB has "
        "to sit to one side. Below the window sill (3 ft AGL) and above the floor splash zone.",
    )

    # Page 6: JB internals (existing image)
    annotated_image_page(
        pdf, 6, "Inside the JB",
        "ESP32 + PoE splitter + terminal block + 4 glands",
        IMG_DIR / "water-automation-jb-internals-v1.png",
        [
            {"rel_x": 0.40, "rel_y": 0.40, "side": "L", "label": "ESP32 board", "color": INFO},
            {"rel_x": 0.65, "rel_y": 0.40, "side": "R", "label": "PoE splitter (48V -> 5V)", "color": GOOD},
            {"rel_x": 0.55, "rel_y": 0.62, "side": "R", "label": "terminal block", "color": GOLD_DARK},
            {"rel_x": 0.30, "rel_y": 0.78, "side": "L", "label": "cable glands (4)", "color": INK},
            {"rel_x": 0.55, "rel_y": 0.85, "side": "B", "label": "cables enter from below", "color": INK_SOFT},
            {"rel_x": 0.55, "rel_y": 0.15, "side": "T", "label": "hinged lid (lifted open)", "color": INK_SOFT},
        ],
        "What this shows",
        "Box lid lifted. PoE Cat6 enters via one of the bottom glands, lands at the splitter which "
        "drops 48 V to 5 V for the ESP32. Sensor wires from inside the tank/sump also enter via the "
        "bottom glands and land on the terminal block. All four glands face DOWN - water sheds away.",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
