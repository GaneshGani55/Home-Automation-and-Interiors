"""
Build WATER_AUTOMATION_VISUAL.pdf — a compact, image-led handoff PDF for the
electrician. One image per page with a short text annotation below.

Three AI-generated images (Gemini Nano Banana 2):
  - water-automation-system-overview-v1.png
  - water-automation-sump-jb-mount-v1.png
  - water-automation-jb-internals-v1.png

Plus one summary page with the 7-conduit schedule (drawn in Python).

Run: python3 build_water_automation_visual_pdf.py
"""
from fpdf import FPDF
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMG_DIR = ROOT / "interior-design" / "generated-images"
OUT = Path(__file__).parent / "WATER_AUTOMATION_VISUAL.pdf"

INK         = ( 28,  28,  30)
INK_SOFT    = ( 90,  90,  95)
INK_FAINT   = (140, 140, 145)
RULE        = (220, 215, 205)
PAPER_TINT  = (252, 248, 240)

GOLD        = (172, 130,  50)
GOLD_DARK   = (130,  95,  30)
GOLD_BAR    = (190, 150,  70)

INFO        = ( 50, 100, 160)
DANGER      = (180,  60,  50)
COPPER      = (175, 110,  60)


class VisualPDF(FPDF):
    MX = 16
    MY_TOP = 16
    MY_BOT = 14

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=self.MY_BOT)
        self.set_margins(self.MX, self.MY_TOP, self.MX)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_FAINT)
        self.cell(0, 4, "Water Automation - Visual Handoff  -  v1.0  -  2026-05-29", align="C")

    def page_title(self, num, title, subtitle=None):
        # Page number chip
        self.set_xy(self.MX, 8)
        self.set_fill_color(*GOLD_BAR)
        self.rect(self.MX, 8, 14, 5, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(self.MX, 8)
        self.cell(14, 5, f" {num:02d}", align="L")
        # Title
        self.set_xy(self.MX, 16)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*INK)
        self.cell(0, 10, title)
        if subtitle:
            self.set_xy(self.MX, 27)
            self.set_font("Helvetica", "I", 11)
            self.set_text_color(*INK_SOFT)
            self.cell(0, 6, subtitle)
        # Underline
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.5)
        y = 36 if subtitle else 30
        self.line(self.MX, y, self.MX + 24, y)

    def caption_block(self, label, text, bar_color=INFO, label_color=INFO):
        self.ln(2)
        x0 = self.MX
        body_x = x0 + 5
        body_w = 210 - 2 * self.MX - 5
        y_start = self.get_y()
        self.set_xy(body_x, y_start)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*label_color)
        self.cell(0, 5, label.upper(), ln=1)
        self.set_x(body_x)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(body_w, 5.2, text)
        y_end = self.get_y()
        self.set_fill_color(*bar_color)
        self.rect(x0, y_start + 0.5, 1.4, y_end - y_start - 0.5, "F")


def add_image_page(pdf, num, title, subtitle, image_path, label, caption):
    pdf.add_page()
    pdf.page_title(num, title, subtitle)
    # Image
    img_y = 44
    img_w = 210 - 2 * pdf.MX
    # Position image with auto-height (FPDF preserves aspect ratio when only width given)
    pdf.image(str(image_path), x=pdf.MX, y=img_y, w=img_w)
    # Move cursor below image - estimate height from aspect ratio
    # We assume 16:9 for image 1 and 4:3 for images 2,3
    # FPDF doesn't expose image height directly; use known ratios
    # Caller passes the ratio via label arg as last char? Simpler: assume after image add, get_y is set
    # Actually after pdf.image(), get_y is NOT updated. We need to set it manually.
    # Use aspect ratio from image dimensions:
    from PIL import Image
    im = Image.open(image_path)
    iw, ih = im.size
    img_h = img_w * ih / iw
    pdf.set_xy(pdf.MX, img_y + img_h + 4)
    pdf.caption_block(label, caption)


def page_cover(pdf):
    pdf.add_page()
    # full-bleed cream tint
    pdf.set_fill_color(*PAPER_TINT)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 0, 210, 2.5, "F")
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 294.5, 210, 2.5, "F")
    # Title
    pdf.set_xy(pdf.MX, 50)
    pdf.set_font("Helvetica", "", 32)
    pdf.set_text_color(*INK)
    pdf.cell(0, 12, "Water Automation")
    pdf.set_xy(pdf.MX, 65)
    pdf.cell(0, 12, "Visual Handoff")
    pdf.set_xy(pdf.MX, 84)
    pdf.set_font("Helvetica", "I", 13)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 6, "Three pictures + one floor plan. That is it.")
    pdf.set_draw_color(*GOLD_BAR)
    pdf.set_line_width(0.8)
    pdf.line(pdf.MX, 99, pdf.MX + 60, 99)
    # Hero image
    hero = IMG_DIR / "water-automation-system-overview-v1.png"
    if hero.exists():
        from PIL import Image
        im = Image.open(hero)
        iw, ih = im.size
        img_w = 210 - 2 * pdf.MX
        img_h = img_w * ih / iw
        pdf.image(str(hero), x=pdf.MX, y=110, w=img_w)
        caption_y = 110 + img_h + 4
    else:
        caption_y = 130
    # Caption under hero
    pdf.set_xy(pdf.MX, caption_y)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 5, "AT A GLANCE", ln=1)
    pdf.set_xy(pdf.MX, caption_y + 6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.2,
                   "Sintex tank on the terrace. Sump in the porch. Server in the staircase. "
                   "Starters + Sonoff inside the foyer cupboard. Sensor data flows over Cat6 / PoE. "
                   "Float wires are the hardware failsafe. Motor power runs from the cupboard out.")
    # Hand-to
    pdf.set_xy(pdf.MX, 250)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 5, "HAND THIS TO")
    pdf.set_xy(pdf.MX, 256)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, "Electrician (pre-plaster)  /  Plumber  /  Owner (reference)")


def page_sump_jb(pdf):
    img = IMG_DIR / "water-automation-sump-jb-mount-v1.png"
    if not img.exists():
        return
    add_image_page(
        pdf, 2,
        "Where the Sump JB goes",
        "Porch West wall, 300 mm above floor, beside the manhole",
        img,
        "What this picture shows",
        "Junction box (grey) mounted at knee-height on the porch west wall, BESIDE the manhole "
        "(not directly above). The manhole cover, when lifted open, hinges on its west edge and "
        "lies flat against this same wall - so the JB must sit to one side. Window sill above "
        "keeps the box well clear of the glass. Conduit drops down the wall surface to the sump.",
    )


def page_jb_inside(pdf):
    img = IMG_DIR / "water-automation-jb-internals-v1.png"
    if not img.exists():
        return
    add_image_page(
        pdf, 3,
        "What goes inside the JB",
        "ESP32 + PoE splitter + terminal block + 4 cable glands",
        img,
        "What this picture shows",
        "Box lid lifted. Inside: small ESP32 board (top-left) reads the sensor and talks to the "
        "server. PoE splitter (top-right) takes 48 V off the Cat6 cable and converts to 5 V to "
        "power the board. Terminal block (bottom) is where wires land. 4 cable glands at the "
        "bottom face - the cables always enter from below so water sheds away.",
    )


def page_conduit_summary(pdf):
    pdf.add_page()
    pdf.page_title(4, "The 7 conduits", "What to lay before plastering")
    pdf.set_y(44)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)

    # Render a clean colored table of the 7 conduits
    rows = [
        ("C-Sintex-1", "20 mm grey",  "Server  ->  Sintex JB (terrace)",      "Cat6 (data + PoE)",         INFO),
        ("C-Sintex-2", "16 mm",       "Sintex JB  ->  DB cupboard",           "Float wire (220 V)",        DANGER),
        ("C-Sump-1",   "20 mm grey",  "Server  ->  Sump JB (porch W wall)",   "Cat6 (data + PoE)",         INFO),
        ("C-Sump-2",   "16 mm",       "Sump JB  ->  DB cupboard",             "Float wire (220 V)",        DANGER),
        ("C-DB-Backup","20 mm grey",  "Server  ->  DB cupboard",              "Empty (pull string only)",  GOLD_DARK),
        ("C-Motor-P1", "25 mm blue",  "DB cupboard  ->  Borewell head",       "Motor power (4 sqmm arm.)", COPPER),
        ("C-Motor-P2", "25 mm blue",  "DB cupboard  ->  P2 cage (E wall)",    "Motor power (2.5 sqmm)",    COPPER),
    ]

    x0 = pdf.MX
    y = pdf.get_y() + 4
    row_h = 14
    col_w = [28, 26, 64, 48, 14]  # ID, size, route, carries, color swatch

    # Header
    pdf.set_fill_color(*INK)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    headers = ["Conduit ID", "Size", "From  ->  To", "Carries", ""]
    pdf.set_xy(x0, y)
    for h, w in zip(headers, col_w):
        pdf.cell(w, 8, "  " + h, fill=True)
    y += 8

    pdf.set_font("Helvetica", "", 9)
    fill = False
    for cid, size, route, carries, color in rows:
        pdf.set_xy(x0, y)
        if fill:
            pdf.set_fill_color(250, 246, 238)
            pdf.rect(x0, y, sum(col_w), row_h, "F")
        # ID
        pdf.set_xy(x0 + 2, y + 2)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*INK)
        pdf.cell(col_w[0] - 2, 4, cid)
        # Size
        pdf.set_xy(x0 + col_w[0] + 2, y + 2)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*INK_SOFT)
        pdf.cell(col_w[1] - 2, 4, size)
        # Route
        pdf.set_xy(x0 + col_w[0] + col_w[1] + 2, y + 2)
        pdf.set_text_color(*INK)
        pdf.cell(col_w[2] - 2, 4, route)
        # Carries
        pdf.set_xy(x0 + col_w[0] + col_w[1] + col_w[2] + 2, y + 2)
        pdf.set_text_color(*INK)
        pdf.cell(col_w[3] - 2, 4, carries)
        # Color swatch
        sx = x0 + col_w[0] + col_w[1] + col_w[2] + col_w[3] + 2
        pdf.set_fill_color(*color)
        pdf.rect(sx, y + 4, 10, 6, "F")
        # Bottom rule
        pdf.set_draw_color(*RULE)
        pdf.set_line_width(0.15)
        pdf.line(x0, y + row_h, x0 + sum(col_w), y + row_h)
        y += row_h
        fill = not fill

    pdf.set_y(y + 6)
    pdf.caption_block(
        "RULES THAT DON'T BEND",
        "(1) Data conduits and mains conduits NEVER share. Run them parallel, 50 mm apart. "
        "(2) Pull string in every conduit before plastering. "
        "(3) Both sensor JBs are IP66 polycarbonate, 250 x 200 x 120 mm preferred. "
        "(4) Cable glands always on the bottom face. "
        "(5) Sump JB: porch W wall, 300 mm above floor, beside the manhole.",
        bar_color=DANGER, label_color=DANGER,
    )

    pdf.ln(2)
    pdf.caption_block(
        "FULL DETAIL",
        "See WATER_AUTOMATION.pdf for the long version - same content as this with "
        "per-conduit routing, materials checklist, sequencing, and an electrician acceptance "
        "checklist. This 4-page Visual Handoff is the short-form companion.",
    )


def build():
    pdf = VisualPDF()
    page_cover(pdf)
    page_sump_jb(pdf)
    page_jb_inside(pdf)
    page_conduit_summary(pdf)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
