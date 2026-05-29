"""
WATER_AUTOMATION_SCHEMATIC.pdf
Path B — pure Python technical schematics for the water automation system.
No AI images; everything drawn with FPDF primitives so labels are precise.

Pages:
  1. Cover
  2. System block diagram (network topology)
  3. Floor plan with all 7 conduits color-coded
  4. Starter wiring schematic (Magnum Pradhaan + Sonoff parallel tap)
  5. Float failsafe topology (how Sintex high + sump low floats interrupt coils)

Run: python3 build_water_automation_schematic_pdf.py
"""
from fpdf import FPDF
from pathlib import Path
import math

OUT = Path(__file__).parent / "WATER_AUTOMATION_SCHEMATIC.pdf"

# Palette
INK         = ( 28,  28,  30)
INK_SOFT    = ( 90,  90,  95)
INK_FAINT   = (140, 140, 145)
RULE        = (220, 215, 205)
PAPER_TINT  = (252, 248, 240)
ROW_TINT    = (250, 246, 238)

GOLD        = (172, 130,  50)
GOLD_DARK   = (130,  95,  30)
GOLD_BAR    = (190, 150,  70)
GOLD_PALE   = (245, 234, 210)

INFO        = ( 50, 100, 160)   # data Cat6
INFO_PALE   = (228, 238, 250)
DANGER      = (180,  60,  50)   # mains / float / 220V
DANGER_PALE = (250, 230, 225)
COPPER      = (175, 110,  60)   # motor power
WARN        = (180, 130,  40)
WARN_PALE   = (252, 240, 215)
GOOD        = ( 70, 125,  70)
GOOD_PALE   = (228, 244, 230)
WATER       = ( 60, 130, 175)
WATER_PALE  = (220, 235, 245)


class SchematicPDF(FPDF):
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
        self.cell(0, 4, self._section.upper() if self._section else "WATER AUTOMATION SCHEMATIC", align="L")
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
        self.cell(0, 4, "Water Automation - SCHEMATIC  -  v1.0  -  2026-05-29  -  Pure-Python (no AI)", align="C")

    def page_title(self, num, title, sub=None):
        self.set_y(14)
        # Number chip
        self.set_fill_color(*GOLD_BAR)
        self.rect(self.MX, 14, 14, 5, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(self.MX, 14)
        self.cell(14, 5, f"  {num:02d}", align="L")
        # Title
        self.set_xy(self.MX, 22)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*INK)
        self.cell(0, 9, title)
        if sub:
            self.set_xy(self.MX, 32)
            self.set_font("Helvetica", "I", 10.5)
            self.set_text_color(*INK_SOFT)
            self.cell(0, 6, sub)
        # underline
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.5)
        y = 40 if sub else 34
        self.line(self.MX, y, self.MX + 22, y)
        self.set_y(y + 4)

    def callout(self, label, text, bar_color=INFO, label_color=INFO):
        self.ln(1)
        x0 = self.MX
        body_x = x0 + 5
        body_w = 210 - 2 * self.MX - 5
        y_start = self.get_y()
        self.set_xy(body_x, y_start)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*label_color)
        self.cell(0, 4.5, label.upper(), ln=1)
        self.set_x(body_x)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*INK)
        self.multi_cell(body_w, 5, text)
        y_end = self.get_y()
        self.set_fill_color(*bar_color)
        self.rect(x0, y_start + 0.5, 1.4, y_end - y_start - 0.5, "F")
        self.ln(1.5)

    # ---------- shared draw helpers ----------
    def arrow(self, x1, y1, x2, y2, color=INK, lw=0.5, dashed=False, head=True, ah=2.0):
        self.set_draw_color(*color)
        self.set_line_width(lw)
        if dashed:
            length = math.hypot(x2 - x1, y2 - y1)
            if length == 0:
                return
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            seg, gap = 1.8, 1.4
            t = 0
            while t < length:
                t2 = min(t + seg, length)
                self.line(x1 + ux * t, y1 + uy * t, x1 + ux * t2, y1 + uy * t2)
                t = t2 + gap
        else:
            self.line(x1, y1, x2, y2)
        if head:
            ang = math.atan2(y2 - y1, x2 - x1)
            self.line(x2, y2, x2 - ah * math.cos(ang - math.pi / 6), y2 - ah * math.sin(ang - math.pi / 6))
            self.line(x2, y2, x2 - ah * math.cos(ang + math.pi / 6), y2 - ah * math.sin(ang + math.pi / 6))

    def box(self, x, y, w, h, title, sub=None, fill=PAPER_TINT, border=INK, ts=9, ss=7):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "FD")
        # title at top
        self.set_font("Helvetica", "B", ts)
        self.set_text_color(*border)
        self.set_xy(x + 1, y + 1.5)
        self.multi_cell(w - 2, ts * 0.4, title, align="C")
        if sub:
            self.set_font("Helvetica", "", ss)
            self.set_text_color(*INK_SOFT)
            lines = sub.count("\n") + 1
            self.set_xy(x + 1, y + h - lines * ss * 0.45 - 0.5)
            self.multi_cell(w - 2, ss * 0.42, sub, align="C")


# ============================================================
#                        PAGE 1 — COVER
# ============================================================

def page_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*PAPER_TINT)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 0, 210, 2.5, "F")
    pdf.rect(0, 294.5, 210, 2.5, "F")

    pdf.set_xy(pdf.MX, 60)
    pdf.set_font("Helvetica", "", 32)
    pdf.set_text_color(*INK)
    pdf.cell(0, 12, "Water Automation")
    pdf.set_xy(pdf.MX, 75)
    pdf.cell(0, 12, "Schematic Drawings")

    pdf.set_xy(pdf.MX, 94)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 6, "4 clean technical diagrams. Pure Python. No AI.")

    pdf.set_draw_color(*GOLD_BAR)
    pdf.set_line_width(0.8)
    pdf.line(pdf.MX, 108, pdf.MX + 60, 108)

    pdf.set_xy(pdf.MX, 122)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 6, "WHAT'S INSIDE")

    items = [
        ("02", "System block diagram", "Who talks to whom: server, JBs, sensors, motors"),
        ("03", "Floor plan + 7 conduits", "Top-down house, every cable run color-coded"),
        ("04", "Starter wiring", "How Sonoff parallel-taps Magnum Pradhaan control circuit"),
        ("05", "Float failsafe topology", "Mechanical safety wiring: Sintex high + sump low"),
    ]
    for i, (n, t, d) in enumerate(items):
        y = 134 + i * 14
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

    pdf.set_xy(pdf.MX, 220)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 5, "COMPANION DOCS")
    pdf.set_xy(pdf.MX, 226)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5,
                   "WATER_AUTOMATION.pdf  -  full long-form spec (11 pages)\n"
                   "WATER_AUTOMATION_VISUAL.pdf  -  AI-rendered scene visualisations")

    pdf.set_xy(pdf.MX, 254)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*INK_FAINT)
    pdf.cell(0, 4, "v1.0  -  2026-05-29  -  Pure-Python schematic deck")


# ============================================================
#                  PAGE 2 — BLOCK DIAGRAM
# ============================================================

def page_block_diagram(pdf):
    pdf._section = "02 Block diagram"
    pdf.add_page()
    pdf.page_title(2, "System Block Diagram", "Who talks to whom")

    # Two columns: left = control plane (data), right = power plane
    x = pdf.MX
    y = pdf.get_y() + 2
    w = 210 - 2 * pdf.MX
    h = 200

    # Background panel
    pdf.set_fill_color(*PAPER_TINT)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, h, "FD")

    # Two zone labels at top
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INFO)
    pdf.set_xy(x + 5, y + 2)
    pdf.cell(w / 2 - 10, 4, "CONTROL PLANE  (data + signals)")
    pdf.set_text_color(*COPPER)
    pdf.set_xy(x + w / 2 + 5, y + 2)
    pdf.cell(w / 2 - 10, 4, "POWER PLANE  (motor mains)")

    # Vertical divider
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.2)
    pdf.line(x + w / 2, y + 10, x + w / 2, y + h - 4)

    # ===== CONTROL PLANE (left half) =====
    # Columns and divider
    col_w = w / 2 - 4  # each column inner width
    left_x = x + 2
    right_x = x + w / 2 + 2
    # Cell width inside each column
    cell_w = col_w - 8
    # Server centered in left column
    pdf.box(left_x + (col_w - cell_w) / 2, y + 12, cell_w, 16,
            "SERVER", "Home Assistant + PoE switch\n(staircase niche)",
            fill=GOOD_PALE, border=GOOD, ts=9, ss=6.8)
    # Two sensor JBs - stacked vertically below server, side by side
    sjb_w = (col_w - 14) / 2
    pdf.box(left_x + 4, y + 36, sjb_w, 20, "SINTEX JB",
            "WT32-ETH01\n+ PoE splitter\nterrace SW",
            fill=INFO_PALE, border=INFO, ts=8, ss=6.4)
    pdf.box(left_x + 4 + sjb_w + 6, y + 36, sjb_w, 20, "SUMP JB",
            "WT32-ETH01\n+ PoE splitter\nporch W wall",
            fill=INFO_PALE, border=INFO, ts=8, ss=6.4)
    # Sensors below
    pdf.box(left_x + 4, y + 62, sjb_w, 16, "Ultrasonic", "JSN-SR04T\non riser",
            fill=WARN_PALE, border=WARN, ts=8, ss=6.4)
    pdf.box(left_x + 4 + sjb_w + 6, y + 62, sjb_w, 16, "Pressure probe",
            "DFRobot SEN0257\nin sump",
            fill=WARN_PALE, border=WARN, ts=8, ss=6.4)
    # Floats below sensors
    pdf.box(left_x + 4, y + 84, sjb_w, 14, "Sintex float",
            "NC, ~95%",
            fill=DANGER_PALE, border=DANGER, ts=8, ss=6.4)
    pdf.box(left_x + 4 + sjb_w + 6, y + 84, sjb_w, 14, "Sump float",
            "NC, ~25 cm",
            fill=DANGER_PALE, border=DANGER, ts=8, ss=6.4)

    sintex_cx = left_x + 4 + sjb_w / 2
    sump_cx = left_x + 4 + sjb_w + 6 + sjb_w / 2

    # Arrows: Server -> JBs (Cat6)
    server_cx = left_x + col_w / 2
    pdf.arrow(server_cx - 8, y + 28, sintex_cx, y + 36, color=INFO, lw=0.5, head=True)
    pdf.arrow(server_cx + 8, y + 28, sump_cx, y + 36, color=INFO, lw=0.5, head=True)
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(*INFO)
    pdf.text(sintex_cx - 12, y + 34, "C-Sintex-1")
    pdf.text(sump_cx - 10, y + 34, "C-Sump-1")
    # JB -> sensor arrows (short)
    pdf.arrow(sintex_cx, y + 56, sintex_cx, y + 62, color=WARN, lw=0.4, head=True)
    pdf.arrow(sump_cx, y + 56, sump_cx, y + 62, color=WARN, lw=0.4, head=True)
    # JB -> float arrows
    pdf.arrow(sintex_cx, y + 78, sintex_cx, y + 84, color=DANGER, lw=0.4, dashed=True, head=False)
    pdf.arrow(sump_cx, y + 78, sump_cx, y + 84, color=DANGER, lw=0.4, dashed=True, head=False)

    # ===== POWER PLANE (right half) =====
    # DB cupboard at top spans right column
    pdf.box(right_x + 4, y + 12, col_w - 8, 16, "DB CUPBOARD",
            "foyer, E wall, behind door swing",
            fill=GOLD_PALE, border=GOLD_DARK, ts=9, ss=6.8)
    # Two starter boxes side-by-side
    st_w = (col_w - 14) / 2
    st_x1 = right_x + 4
    st_x2 = right_x + 4 + st_w + 6
    pdf.box(st_x1, y + 36, st_w, 22, "P1 STARTER",
            "Magnum PSP1H\nborewell 1.5HP\n(coil + contactor)",
            fill=PAPER_TINT, border=INK_SOFT, ts=8, ss=6.4)
    pdf.box(st_x2, y + 36, st_w, 22, "P2 STARTER",
            "Magnum PSP1\nbooster 1HP\n(coil + contactor)",
            fill=PAPER_TINT, border=INK_SOFT, ts=8, ss=6.4)
    # Sonoff below, full width
    pdf.box(right_x + 4, y + 64, col_w - 8, 12, "SONOFF DUALR3",
            "Ch1 -> P1 coil  /  Ch2 -> P2 coil  (WiFi)",
            fill=INFO_PALE, border=INFO, ts=8, ss=6.4)
    # Motors at bottom
    pdf.box(st_x1, y + 82, st_w, 16, "Borewell motor",
            "submersible, 1.5HP",
            fill=DANGER_PALE, border=DANGER, ts=8, ss=6.4)
    pdf.box(st_x2, y + 82, st_w, 16, "P2 pump",
            "in cage, on E wall",
            fill=WARN_PALE, border=WARN, ts=8, ss=6.4)

    p1_cx = st_x1 + st_w / 2
    p2_cx = st_x2 + st_w / 2

    # Power arrows: starter -> motor
    pdf.arrow(p1_cx, y + 76, p1_cx, y + 82, color=COPPER, lw=0.8, head=True)
    pdf.arrow(p2_cx, y + 76, p2_cx, y + 82, color=COPPER, lw=0.8, head=True)
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(*COPPER)
    pdf.text(p1_cx - 10, y + 80, "C-Motor-P1")
    pdf.text(p2_cx - 10, y + 80, "C-Motor-P2")

    # Sonoff -> starter (signal)
    pdf.arrow(p1_cx, y + 64, p1_cx, y + 58, color=INFO, lw=0.4, head=True)
    pdf.arrow(p2_cx, y + 64, p2_cx, y + 58, color=INFO, lw=0.4, head=True)

    # Float wires crossing the divider
    # Sintex float -> P1 AND P2 coils
    pdf.arrow(sintex_cx, y + 98, p1_cx, y + 58, color=DANGER, lw=0.5, dashed=True, head=True)
    pdf.arrow(sintex_cx, y + 98, p2_cx, y + 58, color=DANGER, lw=0.5, dashed=True, head=True)
    # Sump float -> P2 only
    pdf.arrow(sump_cx, y + 98, p2_cx, y + 58, color=DANGER, lw=0.5, dashed=True, head=True)

    # Float crossing labels at bottom of frame
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.set_text_color(*DANGER)
    pdf.text(left_x + 6, y + h - 14, "C-Sintex-2: Sintex float -> BOTH coils (in series with coil supply)")
    pdf.text(left_x + 6, y + h - 11, "C-Sump-2: Sump float -> P2 coil only (dry-run protection)")

    # Legend at bottom
    pdf.set_y(y + h + 4)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(pdf.MX, pdf.get_y() + 3, "LEGEND:")
    lx = pdf.MX + 14
    ly = pdf.get_y() + 3
    # data
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.6)
    pdf.line(lx, ly - 1, lx + 8, ly - 1)
    pdf.set_text_color(*INFO)
    pdf.text(lx + 10, ly, "data (Cat6 / PoE)")
    # float (dashed)
    pdf.set_draw_color(*DANGER)
    pdf.set_line_width(0.5)
    for t in range(0, 8, 2):
        pdf.line(lx + 55 + t, ly - 1, lx + 56 + t, ly - 1)
    pdf.set_text_color(*DANGER)
    pdf.text(lx + 65, ly, "float wire (220V, series w/ coil)")
    # motor power
    pdf.set_draw_color(*COPPER)
    pdf.set_line_width(0.8)
    pdf.line(lx + 125, ly - 1, lx + 133, ly - 1)
    pdf.set_text_color(*COPPER)
    pdf.text(lx + 135, ly, "motor power")


# ============================================================
#               PAGE 3 — FLOOR PLAN + CONDUITS
# ============================================================

def page_floor_plan(pdf):
    pdf._section = "03 Floor plan + conduits"
    pdf.add_page()
    pdf.page_title(3, "Floor plan + conduits", "Top-down, all 7 runs colour-coded")

    # Drawing area
    x = pdf.MX
    y = pdf.get_y() + 2
    w = 210 - 2 * pdf.MX
    h = 175

    pdf.set_fill_color(*PAPER_TINT)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, h, "FD")

    # Compass
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INK_FAINT)
    pdf.text(x + w - 12, y + 6, "N")
    pdf.set_draw_color(*INK_FAINT)
    pdf.set_line_width(0.4)
    pdf.line(x + w - 10, y + 8, x + w - 10, y + 14)
    pdf.line(x + w - 10, y + 8, x + w - 12, y + 11)
    pdf.line(x + w - 10, y + 8, x + w - 8, y + 11)

    # Layout coordinates inside drawing area
    # House outline (L-shape), roughly 32' x 18' aspect
    # Place house occupying central-lower area; terrace shown above house
    ix = x + 18
    iy = y + 35
    iw = w - 36
    ih = h - 55

    # === TERRACE strip at top of drawing ===
    ter_h = 30
    pdf.set_fill_color(*WATER_PALE)
    pdf.set_draw_color(*WATER)
    pdf.set_line_width(0.4)
    pdf.rect(ix, y + 4, iw, ter_h, "FD")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*WATER)
    pdf.text(ix + 3, y + 9, "TERRACE  (SW corner)")
    # Sintex circle in SW corner of terrace
    sintex_cx = ix + 12
    sintex_cy = y + 22
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*WATER)
    pdf.set_line_width(0.5)
    pdf.ellipse(sintex_cx - 7, sintex_cy - 7, 14, 14, "FD")
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*WATER)
    pdf.set_xy(sintex_cx - 8, sintex_cy - 1.5)
    pdf.cell(16, 3, "SINTEX", align="C")
    pdf.set_xy(sintex_cx - 8, sintex_cy + 1.5)
    pdf.set_font("Helvetica", "", 6)
    pdf.cell(16, 3, "1500 L", align="C")
    # Sintex JB nearby
    sjb_x = sintex_cx + 10
    sjb_y = sintex_cy - 4
    pdf.set_fill_color(*INFO_PALE)
    pdf.set_draw_color(*INFO)
    pdf.rect(sjb_x, sjb_y, 12, 7, "FD")
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.set_text_color(*INFO)
    pdf.set_xy(sjb_x, sjb_y + 1.5)
    pdf.cell(12, 3, "Sintex JB", align="C")

    # === House outline ===
    # Define wall coordinates
    # House: rectangle from ix,iy to ix+iw, iy+ih
    # L-shape: missing top-right corner (notch for foyer/entrance)
    # Actually simplest: rectangle for now
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.7)
    pdf.rect(ix, iy, iw, ih, "FD")

    # Wall labels
    pdf.set_font("Helvetica", "I", 6)
    pdf.set_text_color(*INK_FAINT)
    pdf.text(ix + iw / 2 - 5, iy - 1, "(N wall)")
    pdf.text(ix - 10, iy + ih / 2, "W wall")
    pdf.text(ix + iw + 2, iy + ih / 2, "E wall")
    pdf.text(ix + iw / 2 - 5, iy + ih + 4, "(S wall)")

    # Main door indicator on N wall (right portion - foyer in NE)
    door_x = ix + iw - 18
    pdf.set_draw_color(*GOLD_DARK)
    pdf.set_line_width(0.6)
    pdf.line(door_x, iy, door_x + 6, iy)
    pdf.set_font("Helvetica", "I", 5.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.text(door_x - 4, iy - 2, "main door")

    # === Porch with sump (north of main door) ===
    porch_x = door_x - 4
    porch_y = iy - 22
    porch_w = 22
    porch_h = 18
    pdf.set_fill_color(245, 240, 230)
    pdf.set_draw_color(*GOLD_DARK)
    pdf.set_line_width(0.4)
    pdf.rect(porch_x, porch_y, porch_w, porch_h, "FD")
    pdf.set_font("Helvetica", "I", 6.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.text(porch_x + 2, porch_y - 1, "PORCH")
    # Sump in porch (near W edge of porch)
    sump_x = porch_x + 2
    sump_y = porch_y + 4
    pdf.set_fill_color(*WATER_PALE)
    pdf.set_draw_color(*WATER)
    pdf.set_line_width(0.5)
    pdf.rect(sump_x, sump_y, 8, 8, "FD")
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_text_color(*WATER)
    pdf.set_xy(sump_x, sump_y + 2.5)
    pdf.cell(8, 3, "SUMP", align="C")
    # Sump JB on porch W wall (left edge of porch, beside the sump)
    smjb_x = porch_x - 1
    smjb_y = porch_y + 12
    pdf.set_fill_color(*INFO_PALE)
    pdf.set_draw_color(*INFO)
    pdf.rect(smjb_x, smjb_y, 9, 5, "FD")
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_text_color(*INFO)
    pdf.set_xy(smjb_x, smjb_y + 0.8)
    pdf.cell(9, 3, "Sump JB", align="C")

    # === Inside house: rooms simplified ===
    # Staircase niche on W side
    nicheX = ix + 2
    nicheY = iy + ih / 2 - 8
    pdf.set_fill_color(*GOOD_PALE)
    pdf.set_draw_color(*GOOD)
    pdf.set_line_width(0.5)
    pdf.rect(nicheX, nicheY, 18, 16, "FD")
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*GOOD)
    pdf.set_xy(nicheX, nicheY + 5)
    pdf.cell(18, 3, "SERVER", align="C")
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_xy(nicheX, nicheY + 9)
    pdf.cell(18, 3, "(stair niche)", align="C")
    # DB cupboard on E wall (NE corner)
    dbX = ix + iw - 22
    dbY = iy + 6
    pdf.set_fill_color(*GOLD_PALE)
    pdf.set_draw_color(*GOLD_DARK)
    pdf.set_line_width(0.5)
    pdf.rect(dbX, dbY, 20, 22, "FD")
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*GOLD_DARK)
    pdf.set_xy(dbX, dbY + 2)
    pdf.cell(20, 3, "DB", align="C")
    pdf.set_xy(dbX, dbY + 6)
    pdf.cell(20, 3, "CUPBOARD", align="C")
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_xy(dbX, dbY + 11)
    pdf.cell(20, 3, "P1 + P2 +", align="C")
    pdf.set_xy(dbX, dbY + 14)
    pdf.cell(20, 3, "Sonoff", align="C")

    # === Outside motor cage (E side, outside) ===
    cageX = ix + iw + 3
    cageY = iy + 8
    pdf.set_fill_color(*WARN_PALE)
    pdf.set_draw_color(*WARN)
    pdf.set_line_width(0.4)
    pdf.rect(cageX, cageY, 10, 12, "FD")
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_text_color(*WARN)
    pdf.set_xy(cageX, cageY + 2)
    pdf.cell(10, 3, "P2", align="C")
    pdf.set_xy(cageX, cageY + 5)
    pdf.cell(10, 3, "CAGE", align="C")
    # Borewell symbol (E side, further down)
    bwX = ix + iw + 3
    bwY = iy + ih - 18
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.5)
    pdf.rect(bwX, bwY, 10, 15, "FD")
    pdf.set_font("Helvetica", "B", 5.5)
    pdf.set_text_color(*INK)
    pdf.set_xy(bwX, bwY + 3)
    pdf.cell(10, 3, "BORE-", align="C")
    pdf.set_xy(bwX, bwY + 6)
    pdf.cell(10, 3, "WELL", align="C")
    pdf.set_xy(bwX, bwY + 10)
    pdf.set_font("Helvetica", "", 5)
    pdf.cell(10, 3, "(P1)", align="C")

    # ============== DRAW THE 7 CONDUITS ==============

    def draw_conduit(points, color, dashed=False, lw=0.7, label=None, label_xy=None):
        pdf.set_draw_color(*color)
        pdf.set_line_width(lw)
        for i in range(len(points) - 1):
            if dashed:
                length = math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
                if length == 0:
                    continue
                ux = (points[i + 1][0] - points[i][0]) / length
                uy = (points[i + 1][1] - points[i][1]) / length
                t = 0
                while t < length:
                    t2 = min(t + 1.5, length)
                    pdf.line(points[i][0] + ux * t, points[i][1] + uy * t,
                             points[i][0] + ux * t2, points[i][1] + uy * t2)
                    t = t2 + 1.2
            else:
                pdf.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
        if label and label_xy:
            pdf.set_font("Helvetica", "B", 6)
            pdf.set_text_color(*color)
            pdf.text(label_xy[0], label_xy[1], label)

    # C-Sintex-1: Server -> Sintex JB (Cat6)
    draw_conduit([
        (nicheX + 9, nicheY),
        (nicheX + 9, y + 30),
        (sjb_x + 6, y + 30),
        (sjb_x + 6, sjb_y + 7),
    ], INFO, lw=0.7, label="C-Sintex-1", label_xy=(nicheX + 12, y + 33))

    # C-Sintex-2: Sintex JB -> DB cupboard (mains float)
    draw_conduit([
        (sjb_x + 12, sjb_y + 3.5),
        (sjb_x + 18, sjb_y + 3.5),
        (sjb_x + 18, y + 32),
        (dbX + 10, y + 32),
        (dbX + 10, dbY),
    ], DANGER, dashed=True, lw=0.6, label="C-Sintex-2", label_xy=(sjb_x + 20, y + 30))

    # C-Sump-1: Server -> Sump JB (Cat6)
    draw_conduit([
        (nicheX + 9, nicheY),
        (nicheX + 9, iy - 2),
        (smjb_x - 2, iy - 2),
        (smjb_x - 2, smjb_y + 2.5),
        (smjb_x, smjb_y + 2.5),
    ], INFO, lw=0.7, label="C-Sump-1", label_xy=(nicheX + 22, iy - 4))

    # C-Sump-2: Sump JB -> DB cupboard (float)
    draw_conduit([
        (smjb_x + 9, smjb_y + 2.5),
        (smjb_x + 12, smjb_y + 2.5),
        (smjb_x + 12, iy - 3.5),
        (dbX + 16, iy - 3.5),
        (dbX + 16, dbY),
    ], DANGER, dashed=True, lw=0.6, label="C-Sump-2", label_xy=(smjb_x + 14, iy - 5))

    # C-DB-Backup: Server -> DB cupboard
    draw_conduit([
        (nicheX + 18, nicheY + 8),
        (dbX - 2, nicheY + 8),
        (dbX - 2, dbY + 11),
        (dbX, dbY + 11),
    ], GOLD_DARK, dashed=True, lw=0.5, label="C-DB-Backup", label_xy=(nicheX + 22, nicheY + 6))

    # C-Motor-P1: DB cupboard -> Borewell
    draw_conduit([
        (dbX + 20, dbY + 14),
        (ix + iw + 0.5, dbY + 14),
        (ix + iw + 0.5, bwY + 5),
        (bwX, bwY + 5),
    ], COPPER, lw=0.9, label="C-Motor-P1", label_xy=(dbX + 22, dbY + 18))

    # C-Motor-P2: DB cupboard -> P2 cage
    draw_conduit([
        (dbX + 20, dbY + 16),
        (cageX, dbY + 16),
    ], COPPER, lw=0.9, label="C-Motor-P2", label_xy=(dbX + 22, dbY + 22))

    # Legend at bottom of drawing
    pdf.set_y(y + h + 3)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(pdf.MX, pdf.get_y() + 3, "LEGEND:")
    lx = pdf.MX + 14
    ly = pdf.get_y() + 3
    pdf.set_draw_color(*INFO); pdf.set_line_width(0.7)
    pdf.line(lx, ly - 1, lx + 10, ly - 1)
    pdf.set_text_color(*INFO); pdf.text(lx + 12, ly, "Cat6 PoE (data)")
    pdf.set_draw_color(*DANGER); pdf.set_line_width(0.5)
    for t in range(0, 10, 2): pdf.line(lx + 55 + t, ly - 1, lx + 56 + t, ly - 1)
    pdf.set_text_color(*DANGER); pdf.text(lx + 67, ly, "float 220V")
    pdf.set_draw_color(*COPPER); pdf.set_line_width(0.9)
    pdf.line(lx + 95, ly - 1, lx + 105, ly - 1)
    pdf.set_text_color(*COPPER); pdf.text(lx + 107, ly, "motor power")
    pdf.set_draw_color(*GOLD_DARK); pdf.set_line_width(0.4)
    for t in range(0, 10, 2): pdf.line(lx + 137 + t, ly - 1, lx + 138 + t, ly - 1)
    pdf.set_text_color(*GOLD_DARK); pdf.text(lx + 149, ly, "empty (pull string)")


# ============================================================
#              PAGE 4 — STARTER WIRING SCHEMATIC
# ============================================================

def page_starter_wiring(pdf):
    pdf._section = "04 Starter wiring"
    pdf.add_page()
    pdf.page_title(4, "Starter wiring", "How the Sonoff parallel-taps the Magnum Pradhaan")

    x = pdf.MX
    y = pdf.get_y() + 2
    w = 210 - 2 * pdf.MX
    h = 90

    pdf.set_fill_color(*PAPER_TINT)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, h, "FD")

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*INK)
    pdf.set_xy(x + 4, y + 3)
    pdf.cell(0, 5, "MAGNUM PRADHAAN CONTROL CIRCUIT  +  SONOFF PARALLEL TAP")
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*INK_FAINT)
    pdf.set_xy(x + 4, y + 8)
    pdf.cell(0, 4, "Identical for both P1 (1.5HP) and P2 (1HP). Manual buttons remain functional.")

    # Schematic positions
    sx = x + 8
    sw = w - 16
    rail_y = y + 35
    x_L = sx + 6
    x_MCB = sx + 22
    x_OL = sx + 40
    x_RED = sx + 58
    x_PARL = sx + 74
    x_PARR = sx + 120
    x_FLOAT = sx + 136
    x_COIL = sx + 154
    x_N = sx + sw - 4

    # Base rail
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.6)
    pdf.line(x_L, rail_y, x_PARL, rail_y)
    pdf.line(x_PARR, rail_y, x_N, rail_y)

    # L terminal
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*DANGER)
    pdf.text(x_L - 7, rail_y - 3, "L 220V")
    pdf.set_fill_color(*DANGER)
    pdf.ellipse(x_L - 1.2, rail_y - 1.2, 2.4, 2.4, "F")
    pdf.set_text_color(*INK)
    pdf.text(x_N + 2, rail_y - 3, "N")
    pdf.set_fill_color(*INK)
    pdf.ellipse(x_N - 1.2, rail_y - 1.2, 2.4, 2.4, "F")

    def inline_comp(cx, cy, label, color=INK):
        cw, ch = 14, 8
        pdf.set_fill_color(*PAPER_TINT)
        pdf.set_draw_color(*color)
        pdf.set_line_width(0.5)
        pdf.rect(cx - cw / 2, cy - ch / 2, cw, ch, "FD")
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(*color)
        pdf.set_xy(cx - cw / 2, cy - 2)
        pdf.cell(cw, 4, label, align="C")

    inline_comp(x_MCB, rail_y, "MCB", INFO)
    inline_comp(x_OL, rail_y, "OL", GOLD_DARK)
    inline_comp(x_RED, rail_y, "RED", DANGER)
    inline_comp(x_FLOAT, rail_y, "FLOAT", DANGER)

    # Coil (with hatching)
    cw, ch = 14, 9
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.5)
    pdf.rect(x_COIL - cw / 2, rail_y - ch / 2, cw, ch, "FD")
    pdf.set_line_width(0.25)
    for t in range(-3, 14, 2):
        pdf.line(x_COIL - cw / 2 + t, rail_y - ch / 2,
                 x_COIL - cw / 2 + t + ch, rail_y + ch / 2)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*INFO)
    pdf.set_xy(x_COIL - cw / 2, rail_y + ch / 2 + 1)
    pdf.cell(cw, 3, "COIL", align="C")

    # Parallel branches
    offsets = [-14, 0, 14]
    labels = [
        ("GREEN", GOOD),
        ("AUX", INK_SOFT),
        ("SONOFF", INFO),
    ]
    top_y = rail_y + offsets[0]
    bot_y = rail_y + offsets[-1]
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.6)
    pdf.line(x_PARL, top_y, x_PARL, bot_y)
    pdf.line(x_PARR, top_y, x_PARR, bot_y)
    for off, (lbl, col) in zip(offsets, labels):
        by = rail_y + off
        pdf.line(x_PARL, by, x_PARR, by)
        inline_comp((x_PARL + x_PARR) / 2, by, lbl, col)

    # ADD annotation
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INFO)
    pdf.text(x_PARR + 3, rail_y + offsets[-1] + 1, "ADD")
    pdf.set_font("Helvetica", "I", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(x_PARR + 3, rail_y + offsets[-1] + 4, "this")

    # Legend
    leg_y = y + h - 18
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.2)
    pdf.line(sx, leg_y - 2, sx + sw, leg_y - 2)

    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(sx, leg_y + 2, "LEGEND:")

    def lentry(lx, ly, lbl, desc, col):
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(*col)
        pdf.text(lx, ly, lbl)
        lblw = pdf.get_string_width(lbl)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.set_text_color(*INK)
        pdf.text(lx + lblw + 1.5, ly, "= " + desc)
        return lblw + 1.5 + pdf.get_string_width("= " + desc) + 6

    lx = sx + 18
    ly = leg_y + 2
    for lbl, desc, col in [("MCB", "16A Type C", INFO),
                            ("OL", "thermal overload", GOLD_DARK),
                            ("RED", "manual stop (NC)", DANGER),
                            ("FLOAT", "Sintex high (NC)", DANGER),
                            ("COIL", "contactor coil", INFO)]:
        lx += lentry(lx, ly, lbl, desc, col)
    lx = sx + 18
    ly = leg_y + 6
    for lbl, desc, col in [("GREEN", "manual start (NO)", GOOD),
                            ("AUX", "latching (NO)", INK_SOFT),
                            ("SONOFF", "server start/stop (NO)", INFO)]:
        lx += lentry(lx, ly, lbl, desc, col)

    # Path note
    pdf.set_font("Helvetica", "I", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(sx, leg_y + 11, "Existing path: L -> MCB -> OL -> RED(NC) -> [GREEN latched by AUX] -> FLOAT(NC) -> COIL -> N")
    pdf.text(sx, leg_y + 14, "Sonoff is wired in PARALLEL with the GREEN button. Manual + server both can start the motor.")

    pdf.set_y(y + h + 4)
    pdf.callout(
        "What this buys us",
        "Server can start/stop the motor via Sonoff WiFi. Manual operation still works "
        "(green/red buttons unchanged). Thermal overload (OL) and Sintex high-float (FLOAT) "
        "remain in series with the coil - true hardware safety, independent of any server.",
        bar_color=GOOD, label_color=GOOD,
    )
    pdf.callout(
        "Wiring rule",
        "Sonoff's switched output goes in PARALLEL with the green button - NEVER in series, "
        "NEVER bypasses the float. Test manual operation BEFORE energising the Sonoff for the first time.",
        bar_color=DANGER, label_color=DANGER,
    )


# ============================================================
#         PAGE 5 — FLOAT FAILSAFE TOPOLOGY
# ============================================================

def page_float_topology(pdf):
    pdf._section = "05 Float failsafe"
    pdf.add_page()
    pdf.page_title(5, "Float failsafe topology",
                   "Mechanical safety: how floats interrupt the contactor coils")

    x = pdf.MX
    y = pdf.get_y() + 2
    w = 210 - 2 * pdf.MX
    h = 130

    pdf.set_fill_color(*PAPER_TINT)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, h, "FD")

    # Title inside frame
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*INK)
    pdf.set_xy(x + 4, y + 3)
    pdf.cell(0, 4, "FLOAT FAILSAFE WIRING - SERIES TOPOLOGY")
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*INK_FAINT)
    pdf.set_xy(x + 4, y + 8)
    pdf.cell(0, 4, "Both floats are NC (normally closed). When water triggers the float, the contact OPENS, breaking the coil supply.")

    # Top: Sintex float -> BOTH coils
    # Left side: Sintex high float
    sx_lhs = x + 12
    pdf.box(sx_lhs, y + 18, 40, 18, "SINTEX HIGH", "Camsco float\nNC, ~95% level",
            fill=WATER_PALE, border=WATER, ts=9, ss=7)
    # Right side: two coils (P1 and P2)
    coil_w = 30
    cx1 = x + w - 70
    cx2 = x + w - 30
    cy_top = y + 22
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.5)
    # P1 coil
    pdf.rect(cx1, cy_top, coil_w, 12, "FD")
    pdf.set_line_width(0.25)
    for t in range(-3, 18, 2):
        pdf.line(cx1 + t, cy_top, cx1 + t + 12, cy_top + 12)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INFO)
    pdf.set_xy(cx1, cy_top - 4)
    pdf.cell(coil_w, 4, "P1 COIL", align="C")
    pdf.set_font("Helvetica", "", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_xy(cx1, cy_top + 13)
    pdf.cell(coil_w, 3, "(borewell)", align="C")
    # P2 coil
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.5)
    pdf.rect(cx2, cy_top, coil_w, 12, "FD")
    pdf.set_line_width(0.25)
    for t in range(-3, 18, 2):
        pdf.line(cx2 + t, cy_top, cx2 + t + 12, cy_top + 12)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INFO)
    pdf.set_xy(cx2, cy_top - 4)
    pdf.cell(coil_w, 4, "P2 COIL", align="C")
    pdf.set_font("Helvetica", "", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_xy(cx2, cy_top + 13)
    pdf.cell(coil_w, 3, "(booster)", align="C")

    # Sintex float wire splits to both coils
    pdf.set_draw_color(*DANGER)
    pdf.set_line_width(0.7)
    # From Sintex float to a split point, then to both coils
    pdf.line(sx_lhs + 40, y + 27, cx1 - 8, y + 27)
    pdf.line(cx1 - 8, y + 27, cx1 - 8, cy_top + 6)
    pdf.line(cx1 - 8, cy_top + 6, cx1, cy_top + 6)
    # Split to P2
    pdf.line(cx1 - 8, y + 27, cx1 - 8, y + 22)  # already drawn above
    pdf.line(cx1 - 8, y + 22, cx2 - 8, y + 22)
    pdf.line(cx2 - 8, y + 22, cx2 - 8, cy_top + 6)
    pdf.line(cx2 - 8, cy_top + 6, cx2, cy_top + 6)

    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*DANGER)
    pdf.text(sx_lhs + 42, y + 25, "Sintex float opens -> BOTH coils drop")

    # Bottom half: Sump low float -> P2 coil only
    cy_bot = y + 80
    sx_bot = x + 12
    pdf.box(sx_bot, cy_bot - 6, 40, 18, "SUMP LOW", "Camsco CT-220\nNC, ~25cm above floor",
            fill=WATER_PALE, border=WATER, ts=9, ss=7)
    # P2 coil shown again for clarity (bottom)
    cx2b = x + w - 30
    cy_bot_coil = cy_bot - 6
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.5)
    pdf.rect(cx2b, cy_bot_coil + 4, coil_w, 12, "FD")
    pdf.set_line_width(0.25)
    for t in range(-3, 18, 2):
        pdf.line(cx2b + t, cy_bot_coil + 4, cx2b + t + 12, cy_bot_coil + 16)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*INFO)
    pdf.set_xy(cx2b, cy_bot_coil)
    pdf.cell(coil_w, 4, "P2 COIL", align="C")
    pdf.set_font("Helvetica", "", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_xy(cx2b, cy_bot_coil + 17)
    pdf.cell(coil_w, 3, "(P2 only - dry-run protection)", align="C")

    # Sump float wire to P2 coil only
    pdf.set_draw_color(*DANGER)
    pdf.set_line_width(0.7)
    pdf.line(sx_bot + 40, cy_bot + 3, cx2b - 4, cy_bot + 3)
    pdf.line(cx2b - 4, cy_bot + 3, cx2b - 4, cy_bot_coil + 10)
    pdf.line(cx2b - 4, cy_bot_coil + 10, cx2b, cy_bot_coil + 10)

    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*DANGER)
    pdf.text(sx_bot + 42, cy_bot + 1, "Sump float opens (low water) -> P2 coil drops")
    pdf.set_font("Helvetica", "I", 6.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(sx_bot + 42, cy_bot + 6, "Note: NOT wired to P1 - borewell doesn't draw from sump")

    # Center divider note
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.2)
    pdf.line(x + 4, y + 60, x + w - 4, y + 60)

    # Note at bottom of frame
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_xy(x + 4, y + h - 8)
    pdf.multi_cell(w - 8, 3.2,
                   "These wires are 220 V mains-class - 2-core 1.5 sqmm double-insulated, "
                   "in separate 16 mm conduits (C-Sintex-2 and C-Sump-2). NEVER share conduit with Cat6.")

    pdf.set_y(y + h + 4)
    pdf.callout(
        "Why both floats are mechanical, not server-controlled",
        "Mains-voltage NC contacts in series with the coil supply means the failsafe is "
        "physical and instant. No CPU, no firmware, no WiFi can fail it. If the entire smart "
        "system burns down, the floats still cut the motor when water reaches the trigger level.",
        bar_color=GOOD, label_color=GOOD,
    )


def build():
    pdf = SchematicPDF()
    page_cover(pdf)
    page_block_diagram(pdf)
    page_floor_plan(pdf)
    page_starter_wiring(pdf)
    page_float_topology(pdf)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
