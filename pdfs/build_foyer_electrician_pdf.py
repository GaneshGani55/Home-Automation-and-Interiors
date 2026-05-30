"""
Build the FOYER ELECTRICIAN MASTER PLAN PDF.

A printable, on-site reference for the electrician (and other trades).
Includes all 18 sections from the markdown master plan PLUS vector diagrams
for foyer floor plan, wall elevations, cavity views, conduit routing, etc.

Source markdown:  electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md
Output PDF:       pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf

Audience: electrician (primary), mason, painter, carpenter, stone cladder,
false-ceiling contractor, smart-home installer, homeowner.
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUT = Path(__file__).parent / "FOYER_ELECTRICIAN_MASTER_PLAN.pdf"

# ============================================================
# COLOR PALETTE
# ============================================================
INK         = (38, 30, 22)
INK_SOFT    = (90, 78, 64)
INK_MUTED   = (130, 118, 102)
PAPER       = (252, 248, 240)
ACCENT      = (170, 110, 50)
ACCENT_DK   = (120, 75, 30)
ACCENT_LT   = (245, 232, 210)
HAIRLINE    = (210, 195, 170)
RULE        = (180, 155, 110)
TABLE_HEAD  = (50, 35, 20)
TABLE_ALT   = (250, 244, 232)
WARN_BG     = (255, 234, 222)
WARN_BD     = (200, 100, 60)
WARN_INK    = (130, 50, 20)
INFO_BG     = (228, 238, 246)
INFO_BD     = (90, 130, 170)
INFO_INK    = (40, 70, 110)
GOOD_BG     = (228, 240, 226)
GOOD_BD     = (90, 130, 80)
GOOD_INK    = (60, 100, 60)
RED_PVC     = (200, 60, 50)
GREY_PVC    = (110, 110, 115)
BLUE_PVC    = (60, 100, 180)
STONE_TONE  = (123, 92, 66)
STONE_LT    = (200, 181, 143)
STONE_DK    = (58, 54, 51)
WALNUT      = (74, 53, 38)
HALO_AMBER  = (255, 184, 119)
COVE_WARM   = (255, 228, 184)
BLACK       = (15, 14, 13)


def clean(s):
    """Strip markdown / unicode that doesn't render natively in Verdana."""
    if s is None:
        return ""
    return (
        str(s)
        .replace("`", "")
        .replace("–", "-")
        .replace("—", "-")
        .replace("→", "->")
        .replace("←", "<-")
        .replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("•", "-")
        .replace(" ", " ")
        .replace("×", "x")
        .replace("°", " deg")
        .replace("±", "+/-")
        .replace("²", "2")
        .replace("³", "3")
        .replace("✅", "[OK]")
        .replace("❌", "[NO]")
        .replace("⚠️", "[!]")
        .replace("⚠", "[!]")
        .replace("📝", "[NOTE]")
        .replace("⏳", "[ ]")
        .replace("🎯", "[GOAL]")
        .replace("🚩", "[FLAG]")
        .replace("🪟", "")
        .replace("🚨", "[!]")
        .replace("📋", "")
        .replace("📐", "")
        .replace("🎉", "")
        .replace("🔍", "")
        .replace("⊙", "(o)")
        .replace("●", "*")
        .replace("◄", "<")
        .replace("►", ">")
        .replace("⅛", "-1/8")
        .replace("⅓", "-1/3")
        .replace("⅙", "-1/6")
        .replace("¼", "-1/4")
        .replace("⅜", "-3/8")
        .replace("½", "-1/2")
        .replace("⅝", "-5/8")
        .replace("¾", "-3/4")
        .replace("⅞", "-7/8")
        .replace("Ω", "ohm")
        .replace("₹", "Rs.")
        .replace("☑", "[X]")
    )


# ============================================================
# PDF CLASS
# ============================================================
class ElectricianPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 22, 15)
        # Verdana for body, Georgia for accents
        font_dir = Path("/System/Library/Fonts/Supplemental")
        self.add_font("Verdana", "",  str(font_dir / "Verdana.ttf"))
        self.add_font("Verdana", "B", str(font_dir / "Verdana Bold.ttf"))
        self.add_font("Verdana", "I", str(font_dir / "Verdana Italic.ttf"))
        self.add_font("Verdana", "BI", str(font_dir / "Verdana Bold Italic.ttf"))
        self.add_font("Georgia", "",  str(font_dir / "Georgia.ttf"))
        self.add_font("Georgia", "B", str(font_dir / "Georgia Bold.ttf"))
        self.add_font("Georgia", "I", str(font_dir / "Georgia Italic.ttf"))

        self.section_label = "Foyer Electrician Plan"
        self.section_number = ""
        self.suppress_chrome = False

    # ---- header / footer ----
    def header(self):
        if self.page_no() == 1 or self.suppress_chrome:
            return
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(15, 12, 195, 12)
        if self.section_number:
            self.set_fill_color(*ACCENT)
            self.rect(15, 14, 10, 5, "F")
            self.set_xy(15, 14)
            self.set_font("Verdana", "B", 7)
            self.set_text_color(255, 255, 255)
            self.cell(10, 5, self.section_number, align="C")
        self.set_xy(27, 14)
        self.set_font("Verdana", "", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(0, 5, clean(self.section_label))
        self.set_xy(150, 14)
        self.set_font("Verdana", "B", 8)
        self.set_text_color(*INK)
        self.cell(45, 5, f"Page {self.page_no()}", align="R")

    def footer(self):
        if self.page_no() == 1 or self.suppress_chrome:
            return
        self.set_y(-14)
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(15, self.get_y(), 195, self.get_y())
        self.set_y(-11)
        self.set_font("Verdana", "I", 7.5)
        self.set_text_color(*INK_MUTED)
        self.cell(0, 5, clean("Foyer Electrician Master Plan  v1.1  -  2026-05-22  -  Ganesh Prasad, Chitradurga"),
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---- typography ----
    def section_open(self, number, title, subtitle=None):
        self.section_number = number
        self.section_label = f"Section {number} - {title}"
        self.add_page()
        self.set_y(28)
        self.set_text_color(*ACCENT)
        self.set_font("Georgia", "B", 60)
        self.set_xy(15, 22)
        self.cell(32, 28, number, align="L")
        self.set_xy(50, 30)
        self.set_text_color(*INK)
        self.set_font("Georgia", "B", 21)
        self.cell(0, 10, clean(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if subtitle:
            self.set_x(50)
            self.set_text_color(*INK_SOFT)
            self.set_font("Verdana", "I", 10.5)
            self.multi_cell(140, 5.5, clean(subtitle))
        self.ln(2)
        y = max(self.get_y() + 3, 56)
        self.set_draw_color(*RULE)
        self.set_line_width(0.5)
        self.line(15, y, 195, y)
        self.set_y(y + 6)
        self.set_text_color(*INK)

    def h2(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(3)
        self.set_font("Georgia", "B", 13)
        self.set_text_color(*INK)
        self.cell(0, 7, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.7)
        y = self.get_y()
        self.line(15, y, 35, y)
        self.set_line_width(0.2)
        self.set_draw_color(*HAIRLINE)
        self.line(35, y, 195, y)
        self.ln(3)

    def h3(self, text):
        self.ln(1)
        self.set_font("Verdana", "B", 10)
        self.set_text_color(*ACCENT_DK)
        self.cell(0, 6, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*INK)
        self.ln(0.5)

    def body(self, text, size=9.5):
        self.set_font("Verdana", "", size)
        self.set_text_color(*INK)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, clean(text))
        self.ln(1.5)

    def lede(self, text):
        self.ln(1)
        self.set_font("Georgia", "I", 11)
        self.set_text_color(*INK_SOFT)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.8, clean(text))
        self.ln(2)
        self.set_text_color(*INK)

    def kv(self, key, value, key_w=58):
        self.set_x(self.l_margin)
        self.set_font("Verdana", "B", 9.5)
        self.set_text_color(*ACCENT_DK)
        self.cell(key_w, 5.5, clean(key))
        self.set_font("Verdana", "", 9.5)
        self.set_text_color(*INK)
        avail = self.w - self.l_margin - self.r_margin - key_w
        self.multi_cell(avail, 5.5, clean(value))

    def bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font("Verdana", "B", 10)
        self.set_text_color(*ACCENT)
        self.cell(5, 5, "-")
        self.set_font("Verdana", "", 9.5)
        self.set_text_color(*INK)
        self.multi_cell(0, 5, clean(text))
        self.ln(0.2)

    def checklist(self, items):
        for it in items:
            if self.get_y() > 270:
                self.add_page()
            self.set_x(self.l_margin)
            x, y = self.get_x(), self.get_y()
            self.set_draw_color(*ACCENT)
            self.set_line_width(0.4)
            self.rect(x + 0.3, y + 0.8, 3.4, 3.4)
            self.set_xy(x + 6, y)
            self.set_font("Verdana", "", 9)
            self.set_text_color(*INK)
            self.multi_cell(0, 5, clean(it))
            self.ln(0.4)

    def callout(self, kind, title, text):
        if kind == "warn":
            bg, bd, ink, label = WARN_BG, WARN_BD, WARN_INK, "CRITICAL"
        elif kind == "info":
            bg, bd, ink, label = INFO_BG, INFO_BD, INFO_INK, "NOTE"
        else:
            bg, bd, ink, label = GOOD_BG, GOOD_BD, GOOD_INK, "TIP"

        if self.get_y() + 20 > 273:
            self.add_page()

        x = self.l_margin
        y = self.get_y() + 1
        w = self.w - self.l_margin - self.r_margin

        # Measure text height first
        self.set_xy(x + 6, y + 8)
        before = self.get_y()
        self.set_font("Verdana", "", 9)
        self.set_text_color(*ink)
        self.multi_cell(w - 12, 5, clean(text))
        end = self.get_y()
        text_h = end - before
        total_h = 8 + text_h + 3

        # Draw the panel
        self.set_fill_color(*bg)
        self.set_draw_color(*bd)
        self.set_line_width(0.4)
        self.rect(x, y, w, total_h, "DF")
        # Left band
        self.set_fill_color(*bd)
        self.rect(x, y, 1.5, total_h, "F")
        # Label
        self.set_xy(x + 5, y + 2)
        self.set_font("Verdana", "B", 8.5)
        self.set_text_color(*ink)
        self.cell(60, 4.5, clean(label))
        # Title
        self.set_xy(x + 30, y + 2)
        self.set_font("Verdana", "B", 9.5)
        self.set_text_color(*ink)
        self.cell(w - 35, 4.5, clean(title))
        # Body re-draw
        self.set_xy(x + 5, y + 8)
        self.set_font("Verdana", "", 9)
        self.set_text_color(*ink)
        self.multi_cell(w - 10, 5, clean(text))
        self.set_y(y + total_h + 2)
        self.set_text_color(*INK)

    def place_diagram(self, draw_fn, height, top_pad=4, bottom_pad=8, full_width=True, manual_x=None, manual_w=None):
        """Safely place a diagram on the current page.
        - Reserves height mm + padding for the diagram.
        - If not enough room, adds a new page.
        - Disables auto-page-break during drawing (so labels don't trigger pages).
        - Advances cursor past the diagram + padding.
        """
        needed = top_pad + height + bottom_pad
        # Leave 22mm for footer + buffer
        if self.get_y() + needed > self.h - 25:
            self.add_page()
        y_top = self.get_y() + top_pad
        if full_width:
            x = self.l_margin
            w = self.w - self.l_margin - self.r_margin
        else:
            x = manual_x if manual_x is not None else self.l_margin
            w = manual_w if manual_w is not None else (self.w - self.l_margin - self.r_margin)
        # Disable auto page break so labels in diagram don't trigger new pages
        prev_break = self.auto_page_break
        prev_b_margin = self.b_margin
        self.set_auto_page_break(False)
        try:
            draw_fn(x, y_top, w, height)
        finally:
            self.set_auto_page_break(prev_break, prev_b_margin)
        self.set_y(y_top + height + bottom_pad)
        # Reset colors / fonts after diagram (in case the diagram changed them)
        self.set_text_color(*INK)
        self.set_draw_color(*INK_SOFT)
        self.set_fill_color(255, 255, 255)
        self.set_font("Verdana", "", 9.5)
        self.set_line_width(0.2)

    def _safe_break(self, text, max_w):
        if not text:
            return ""
        words = clean(text).split(" ")
        out = []
        for w in words:
            if self.get_string_width(w) <= max_w - 1.5:
                out.append(w)
            else:
                chunk = ""
                for ch in w:
                    if self.get_string_width(chunk + ch) > max_w - 1.5:
                        out.append(chunk); chunk = ch
                    else:
                        chunk += ch
                if chunk: out.append(chunk)
        return " ".join(out)

    def table(self, headers, rows, col_widths, header_size=8, body_size=8,
              row_padding=1.4, header_fill=None, zebra=True):
        if header_fill is None:
            header_fill = TABLE_HEAD
        self.set_font("Verdana", "B", header_size)
        self.set_fill_color(*header_fill)
        self.set_text_color(255, 255, 255)
        self.set_draw_color(*header_fill)
        self.set_line_width(0.1)
        for h, w in zip(headers, col_widths):
            self.cell(w, 7, self._safe_break(h, w), border=0, align="L", fill=True)
        self.ln(7)

        self.set_text_color(*INK)
        self.set_font("Verdana", "", body_size)
        self.set_draw_color(*HAIRLINE)
        line_h = 3.8 + row_padding
        zebra_state = False
        for row in rows:
            cells = [self._safe_break(c, col_widths[i]) for i, c in enumerate(row)]
            lines_needed = []
            for cell, w in zip(cells, col_widths):
                if not cell:
                    lines_needed.append(1); continue
                segs = cell.split("\n")
                tot = 0
                for seg in segs:
                    sw = self.get_string_width(seg) if seg else 0
                    avail = max(w - 2, 5)
                    tot += max(1, -(-int(sw // avail) - 1))
                lines_needed.append(max(1, tot))
            row_h = max(max(lines_needed) * line_h, 6.5)

            if self.get_y() + row_h > self.h - 22:
                self.add_page()
                self.set_font("Verdana", "B", header_size)
                self.set_fill_color(*header_fill)
                self.set_text_color(255, 255, 255)
                for h, w in zip(headers, col_widths):
                    self.cell(w, 7, self._safe_break(h, w), border=0, align="L", fill=True)
                self.ln(7)
                self.set_text_color(*INK)
                self.set_font("Verdana", "", body_size)

            if zebra and zebra_state:
                self.set_fill_color(*TABLE_ALT)
            else:
                self.set_fill_color(255, 255, 255)
            x_start, y_start = self.get_x(), self.get_y()
            for i, (cell, w) in enumerate(zip(cells, col_widths)):
                self.rect(self.get_x(), self.get_y(), w, row_h, "F")
                self.set_x(self.get_x() + w)
            self.set_draw_color(*HAIRLINE)
            self.line(x_start, y_start + row_h, x_start + sum(col_widths), y_start + row_h)
            self.set_xy(x_start, y_start)
            for i, (cell, w) in enumerate(zip(cells, col_widths)):
                cur_x, cur_y = self.get_x(), self.get_y()
                content_h = max(1, lines_needed[i]) * line_h
                offset_y = max(0, (row_h - content_h) / 2)
                self.set_xy(cur_x + 1.6, cur_y + offset_y)
                self.multi_cell(w - 3, line_h, cell, border=0, align="L", fill=False)
                self.set_xy(cur_x + w, cur_y)
            self.set_xy(x_start, y_start + row_h)
            zebra_state = not zebra_state
        self.ln(2)

    # ============================================================
    # VECTOR DIAGRAMS
    # ============================================================
    def draw_foyer_floor_plan(self, x, y, w, h):
        """Top-down foyer floor plan with all zones marked."""
        # Outer envelope (slightly larger than foyer to show porch)
        # Section: porch above, foyer middle, S edge with feature wall + opening
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.3)
        self.set_fill_color(*PAPER)
        # porch zone
        porch_h = h * 0.22
        self.rect(x, y, w, porch_h, "DF")
        self.set_font("Verdana", "I", 7)
        self.set_text_color(*INK_MUTED)
        self.set_xy(x + 2, y + 2)
        self.cell(w - 4, 3, "PORCH (external, roofed - to gate ~7.5 ft N)")
        # Reolink on N wall portion of porch
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT)
        self.rect(x + w*0.50, y + porch_h - 3.5, 3, 3, "F")
        self.set_xy(x + w*0.50 + 4, y + porch_h - 3.5)
        self.set_font("Verdana", "B", 6); self.set_text_color(*ACCENT_DK)
        self.cell(20, 2.5, "Reolink")
        # CAM-1 spare on porch W wall
        self.set_fill_color(*INFO_INK); self.set_draw_color(*INFO_INK)
        self.rect(x + 1, y + porch_h/2 - 1.5, 3, 3, "F")
        self.set_xy(x + 5, y + porch_h/2 - 1.5)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INFO_INK)
        self.cell(28, 2.5, "CAM-1 spare")
        # CAM-2 stub on porch ceiling NE corner
        self.set_fill_color(*INFO_INK); self.set_draw_color(*INFO_INK)
        self.rect(x + w - 6, y + 2, 3, 3, "F")
        self.set_xy(x + w - 30, y + 2)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INFO_INK)
        self.cell(22, 2.5, "CAM-2 stub")

        # Main door slot on N wall of foyer
        door_x = x + w * 0.55
        door_w = w * 0.36
        self.set_draw_color(*ACCENT); self.set_line_width(0.6)
        self.line(door_x, y + porch_h, door_x + door_w, y + porch_h)
        self.set_xy(door_x, y + porch_h - 4)
        self.set_font("Verdana", "B", 6.5); self.set_text_color(*ACCENT_DK)
        self.cell(door_w, 3, "MAIN DOOR (hinged E)", align="C")

        # Window
        win_x = x + w * 0.05
        win_w = w * 0.36
        self.set_draw_color(50, 100, 160); self.set_line_width(0.5)
        self.line(win_x, y + porch_h, win_x + win_w, y + porch_h)
        self.set_xy(win_x, y + porch_h + 1)
        self.set_font("Verdana", "", 5.5); self.set_text_color(*INFO_INK)
        self.cell(win_w, 2, "corner window (3.5 ft)", align="C")

        # Wall section between (1.5 ft) - where switch panel + Reolink are
        wall_x = win_x + win_w
        wall_w = door_x - wall_x
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.8)
        self.line(wall_x, y + porch_h, wall_x + wall_w, y + porch_h)

        # Foyer area
        foyer_y = y + porch_h
        foyer_h = h * 0.55
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        self.set_fill_color(252, 246, 232)
        self.rect(x, foyer_y, w, foyer_h, "DF")

        # Open West side (no wall) - dashed (inside diagram bounds, not off-edge)
        self.set_draw_color(*INK_MUTED); self.set_line_width(0.3)
        for i in range(0, int(foyer_h), 3):
            self.line(x, foyer_y + i, x, foyer_y + i + 1.5)
        # Label inside foyer area on West side (not in margin)
        self.set_xy(x + 1, foyer_y + foyer_h/2 - 4)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.multi_cell(28, 2.2, clean("<- OPEN to\n   Living/Dining/\n   Staircase"))

        # E wall (exterior) with DB + cupboard
        self.set_fill_color(60, 60, 60); self.set_draw_color(60, 60, 60)
        # DB rect (smaller, behind door swing)
        db_x = x + w - 9
        db_y = foyer_y + 3
        self.rect(db_x, db_y, 7, 12, "F")
        self.set_xy(db_x - 1, db_y + 13.5)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INK)
        self.cell(15, 2.5, "DB+Cupboard")
        self.set_xy(db_x - 4, db_y + 16)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(20, 2.5, "(behind door)")

        # Switch panel on N wall, in 1.5 ft section
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT)
        sp_x = wall_x + wall_w/2 - 4
        sp_y = foyer_y + 0.5
        self.rect(sp_x, sp_y, 8, 3, "F")
        self.set_xy(sp_x - 8, sp_y + 4)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(24, 2.5, "Foyer Switch Panel")

        # Foyer label
        self.set_xy(x + w/2 - 18, foyer_y + foyer_h/2 - 4)
        self.set_font("Georgia", "B", 13); self.set_text_color(*INK_SOFT)
        self.cell(36, 5, "FOYER", align="C")
        self.set_xy(x + w/2 - 30, foyer_y + foyer_h/2 + 2)
        self.set_font("Verdana", "", 7); self.set_text_color(*INK_MUTED)
        self.cell(60, 3, "9.5 ft (E-W) x 5 ft (N-S)", align="C")
        self.set_xy(x + w/2 - 30, foyer_y + foyer_h/2 + 5)
        self.cell(60, 3, "False ceiling 9 ft", align="C")

        # S edge: stone feature wall (East 6 ft) + open passage (West 3.5 ft)
        s_y = foyer_y + foyer_h
        # Open passage on West (3.5 ft of S edge)
        opening_w = w * 0.36
        self.set_draw_color(*INK_MUTED); self.set_line_width(0.3)
        for i in range(0, int(opening_w), 3):
            self.line(x + i, s_y, x + i + 1.5, s_y)
        self.set_xy(x + 2, s_y + 1)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(opening_w, 2.5, "OPEN (3.5 ft to Living/Pooja)", align="C")

        # Stone feature wall on East 6 ft of S edge
        stone_x = x + opening_w
        stone_w = w - opening_w
        feat_h = h * 0.10
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.4)
        self.rect(stone_x, s_y, stone_w, feat_h, "DF")
        self.set_xy(stone_x, s_y + 1)
        self.set_font("Verdana", "B", 6.5); self.set_text_color(255, 245, 220)
        self.cell(stone_w, 3, "STONE FEATURE WALL (6 ft)", align="C")
        # cavity on stone (centered)
        cav_w = stone_w * 0.36
        cav_x = stone_x + (stone_w - cav_w)/2
        self.set_fill_color(*BLACK); self.set_draw_color(*HALO_AMBER)
        self.set_line_width(0.5)
        self.rect(cav_x, s_y + 4.2, cav_w, feat_h - 5.5, "DF")
        self.set_xy(cav_x - 6, s_y + feat_h + 0.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(cav_w + 12, 2.5, "Cavity", align="C")

        # Staircase niche area (below stone, indicating server location)
        niche_y = s_y + feat_h + 6
        niche_h = h - (niche_y - y)
        if niche_h > 8:
            self.set_fill_color(*PAPER); self.set_draw_color(*INK_SOFT)
            self.set_line_width(0.3)
            self.rect(x, niche_y, w * 0.40, niche_h - 2, "DF")
            self.set_xy(x + 2, niche_y + 1)
            self.set_font("Verdana", "B", 6.5); self.set_text_color(*INK_SOFT)
            self.cell(w * 0.40 - 4, 2.5, "STAIRCASE niche (server)")
            self.set_xy(x + 2, niche_y + 3.5)
            self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
            self.cell(w * 0.40 - 4, 2.5, "Beelink, PoE switch, router")
            # Waveshare above niche
            self.set_fill_color(*INFO_INK); self.set_draw_color(*INFO_INK)
            self.rect(x + w * 0.10, niche_y - 4, 8, 3, "F")
            self.set_xy(x + w * 0.10 - 4, niche_y - 7)
            self.set_font("Verdana", "B", 5.5); self.set_text_color(*INFO_INK)
            self.cell(20, 2.5, "Waveshare", align="C")

        # Compass at bottom-right corner
        comp_x = x + w + 2
        comp_y = y + h/2
        self.set_xy(comp_x - 5, y - 7)
        self.set_font("Verdana", "B", 8); self.set_text_color(*ACCENT_DK)
        self.cell(10, 3, "N", align="C")

        self.set_text_color(*INK)

    def draw_east_wall_elevation(self, x, y, w, h):
        """East wall elevation - DB + starter cupboard."""
        # Wall outline
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        self.set_fill_color(*PAPER)
        self.rect(x, y, w, h, "DF")
        # Title
        self.set_xy(x, y - 5)
        self.set_font("Verdana", "B", 8); self.set_text_color(*ACCENT_DK)
        self.cell(w, 3, "EAST WALL ELEVATION (interior view)", align="C")
        # door swing arc indicator (left side, ~975mm covers ~64% of width)
        door_w = w * 0.64
        self.set_draw_color(*HAIRLINE); self.set_line_width(0.3)
        for i in range(0, int(door_w), 3):
            self.line(x + i, y + 1, x + i + 1.5, y + 1)
        self.set_xy(x, y + 2)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.cell(door_w, 2.5, "<- door swing zone (~975 mm) ->", align="C")
        # DB recess - flush, within door swing
        db_x = x + door_w * 0.20
        db_y = y + h * 0.45
        db_w = door_w * 0.35
        db_h = h * 0.35
        self.set_fill_color(60, 60, 60); self.set_draw_color(50, 50, 50)
        self.set_line_width(0.4)
        self.rect(db_x, db_y, db_w, db_h, "DF")
        # DB rows representing MCBs
        self.set_fill_color(220, 220, 220); self.set_draw_color(220, 220, 220)
        for i in range(4):
            self.rect(db_x + 1, db_y + 1.5 + i*2.2, db_w - 2, 1.5, "F")
        self.set_xy(db_x, db_y + db_h + 0.5)
        self.set_font("Verdana", "B", 6.5); self.set_text_color(*INK)
        self.cell(db_w, 2.5, "DB (recessed)", align="C")
        self.set_xy(db_x, db_y + db_h + 3)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(db_w, 2.5, "400x600 mm", align="C")
        # Cupboard south of door swing (Option 1 layout)
        cup_x = x + door_w + 2
        cup_w = w - door_w - 4
        cup_h = h * 0.45
        cup_y = y + h * 0.30
        self.set_fill_color(*WALNUT); self.set_draw_color(WALNUT[0]-15, WALNUT[1]-15, WALNUT[2]-15)
        self.rect(cup_x, cup_y, cup_w, cup_h, "DF")
        # vent slats
        self.set_draw_color(230, 220, 195); self.set_line_width(0.4)
        for i in range(3):
            self.line(cup_x + 1, cup_y + 1.5 + i*0.8, cup_x + cup_w - 1, cup_y + 1.5 + i*0.8)
            self.line(cup_x + 1, cup_y + cup_h - 3 + i*0.8, cup_x + cup_w - 1, cup_y + cup_h - 3 + i*0.8)
        self.set_xy(cup_x, cup_y + cup_h + 0.5)
        self.set_font("Verdana", "B", 6.5); self.set_text_color(*INK)
        self.cell(cup_w, 2.5, "Starter cupboard", align="C")
        self.set_xy(cup_x, cup_y + cup_h + 3)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(cup_w, 2.5, "600x400x250mm", align="C")
        # FFL line at bottom
        self.set_draw_color(*ACCENT); self.set_line_width(0.4)
        self.line(x, y + h - 0.2, x + w, y + h - 0.2)
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "I", 6); self.set_text_color(*ACCENT_DK)
        self.cell(w, 2.5, "FFL (finished floor level)", align="C")
        self.set_text_color(*INK)

    def draw_cavity_front_view(self, x, y, w, h):
        """Cavity front view - what you see looking AT the cavity from foyer."""
        # Outer stone wall area
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "DF")
        # Inner cavity opening (with stone reveal lip - shown as a tone)
        pad = w * 0.08
        cx, cy, cw, ch = x + pad, y + pad, w - 2*pad, h - 2*pad
        # Stone reveal lip (inner edges, slightly lighter)
        self.set_fill_color(*STONE_LT); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.3)
        self.rect(cx, cy, cw, ch, "DF")
        # Inner opening (matte black) - smaller, after reveal
        rev = w * 0.025
        ix, iy, iw, ih = cx + rev, cy + rev, cw - 2*rev, ch - 2*rev
        self.set_fill_color(*BLACK); self.set_draw_color(*BLACK)
        self.rect(ix, iy, iw, ih, "F")
        # Halo glow around inner opening
        self.set_draw_color(*HALO_AMBER); self.set_line_width(1.5)
        self.rect(ix + 0.5, iy + 0.5, iw - 1, ih - 1, "D")
        # Monitor inside
        m_pad = iw * 0.08
        mx, my, mw, mh = ix + m_pad, iy + m_pad, iw - 2*m_pad, ih - 2*m_pad
        self.set_fill_color(25, 25, 30); self.set_draw_color(60, 60, 65)
        self.set_line_width(0.3)
        self.rect(mx, my, mw, mh, "DF")
        # Welcome text on monitor
        self.set_xy(mx, my + mh/2 - 3)
        self.set_font("Georgia", "I", 9); self.set_text_color(255, 220, 160)
        self.cell(mw, 4, "Welcome, Ganesh", align="C")
        # CAM-0 dot on top bezel
        self.set_fill_color(200, 200, 200); self.set_draw_color(160, 160, 160)
        self.ellipse(mx + mw/2 - 0.8, my + 0.8, 1.6, 1.6, "DF")
        # Title + dims below
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "CAVITY (front view) - monitor with halo glow", align="C")
        self.set_xy(x, y + h + 3.5)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.cell(w, 2.5, "Inner opening 540x340mm (after stone reveal)  -  Centre 1450mm FFL", align="C")
        self.set_text_color(*INK)

    def draw_cavity_back_wall(self, x, y, w, h):
        """Cavity back wall view - showing conduit entries + pockets."""
        # Back wall (matte black)
        self.set_fill_color(*BLACK); self.set_draw_color(*ACCENT)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "DF")
        # Halo conduit hole (top centre)
        self.set_fill_color(*GREY_PVC); self.set_draw_color(*GREY_PVC)
        cx_top = x + w/2
        self.ellipse(cx_top - 1.5, y + 2, 3, 3, "F")
        self.set_xy(cx_top + 3, y + 1.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*HALO_AMBER)
        self.cell(25, 2, "16mm GREY (Halo 24V)")
        # Socket pocket (centred, lower half)
        sk_w = w * 0.18
        sk_h = h * 0.18
        sk_x = x + w/2 - sk_w/2
        sk_y = y + h * 0.62
        self.set_fill_color(50, 50, 50); self.set_draw_color(180, 180, 180)
        self.rect(sk_x, sk_y, sk_w, sk_h, "DF")
        self.set_xy(sk_x + sk_w + 1, sk_y + 1)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(255, 220, 160)
        self.cell(30, 2.2, "Socket pocket (3x3x2.5\"")
        self.set_xy(sk_x + sk_w + 1, sk_y + 3.5)
        self.cell(30, 2.2, "centre at 53\" FFL)")
        # Speaker pocket (centred, vertical centre - directly behind monitor middle)
        sp_d = w * 0.10
        sp_x = x + w/2 - sp_d/2
        sp_y = y + h * 0.40
        self.set_fill_color(40, 40, 40); self.set_draw_color(150, 150, 150)
        self.ellipse(sp_x, sp_y, sp_d, sp_d, "DF")
        self.set_xy(sp_x + sp_d + 1, sp_y + 1)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(255, 220, 160)
        self.cell(30, 2.2, "Speaker pocket (3\" dia x 1\")")
        # Power conduit (bottom-left)
        pwr_x = x + 3
        pwr_y = y + h - 4
        self.set_fill_color(*RED_PVC); self.set_draw_color(*RED_PVC)
        self.ellipse(pwr_x, pwr_y, 3, 3, "F")
        self.set_xy(pwr_x - 1, pwr_y + 3.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(255, 200, 200)
        self.cell(30, 2.2, "25mm RED (Power)")
        # Data conduit (bottom-right)
        dat_x = x + w - 6
        dat_y = y + h - 4
        self.set_fill_color(*GREY_PVC); self.set_draw_color(*GREY_PVC)
        self.ellipse(dat_x, dat_y, 3, 3, "F")
        self.set_xy(dat_x - 14, dat_y + 3.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(220, 220, 220)
        self.cell(20, 2.2, "25mm GREY (Cat6)")
        # Speaker conduit (top wall, going up out of cavity)
        sk_cx = x + w * 0.85
        self.set_fill_color(*GREY_PVC); self.set_draw_color(*GREY_PVC)
        self.ellipse(sk_cx - 1.5, y + 1, 3, 3, "F")
        self.set_xy(sk_cx - 20, y + 1.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(180, 200, 230)
        self.cell(20, 2.2, "16mm GREY (Ceiling spkr provision)")
        # Title below
        self.set_xy(x, y + h + 1)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "CAVITY BACK WALL - conduit entries + sub-pockets", align="C")
        self.set_text_color(*INK)

    def draw_cavity_cross_section(self, x, y, w, h):
        """Side cross-section showing stone reveal depth vs matte black."""
        # Foyer side label
        self.set_xy(x, y - 4)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.cell(w*0.3, 2.5, "<- Foyer")
        self.set_xy(x + w - 30, y - 4)
        self.cell(30, 2.5, "Back wall (5\" masonry) ->", align="R")
        # Wall envelope (the masonry surrounding the cavity)
        wall_h = h * 0.15
        # Top wall mass
        self.set_fill_color(220, 215, 200); self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.3)
        self.rect(x, y, w, wall_h, "DF")
        # Bottom wall mass
        self.rect(x, y + h - wall_h, w, wall_h, "DF")
        # Cavity interior (between top and bottom walls)
        cy = y + wall_h
        cw = w
        ch = h - 2 * wall_h
        self.set_fill_color(*BLACK); self.set_draw_color(*BLACK)
        self.rect(x, cy, cw, ch, "F")
        # Stone reveal on front 30% of inner walls
        reveal_w = w * 0.22
        # Stone on top inner wall
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.3)
        self.rect(x, cy, reveal_w, ch * 0.18, "DF")
        # Stone on bottom inner wall
        self.rect(x, y + h - wall_h - ch*0.18, reveal_w, ch*0.18, "DF")
        # Front stone face (the wall's face on foyer side)
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.rect(x, y, w*0.04, h, "DF")
        # Halo strip position - at the step
        halo_x = x + reveal_w
        self.set_fill_color(*HALO_AMBER); self.set_draw_color(*HALO_AMBER)
        self.rect(halo_x, cy + ch*0.18, 1, 1, "F")
        self.rect(halo_x, y + h - wall_h - ch*0.18 - 1, 1, 1, "F")
        # Monitor inside cavity (middle area)
        mw = w * 0.20
        mh = ch * 0.55
        mx = x + w * 0.10
        my = cy + (ch - mh)/2
        self.set_fill_color(25, 25, 30); self.set_draw_color(80, 80, 85)
        self.rect(mx, my, mw, mh, "DF")
        self.set_xy(mx + mw + 1, my + mh/2 - 2)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(220, 220, 220)
        self.cell(30, 2.2, "Monitor (49mm deep)")
        # Components on back wall area (rear gap)
        comp_x = x + w * 0.65
        comp_y = cy + ch/2 - 4
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
        self.rect(comp_x, comp_y, 6, 8, "DF")
        self.set_xy(comp_x + 7, comp_y + 2)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(20, 2.2, "RPi+Amp")
        # Annotations at top
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INK)
        self.cell(reveal_w + w*0.04, 2.5, "Stone (30mm)", align="C")
        self.set_xy(x + reveal_w + w*0.04, y + h + 0.5)
        self.cell(w - (reveal_w + w*0.04), 2.5, "Matte black (70mm)", align="C")
        # Title below
        self.set_xy(x, y + h + 4)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "CAVITY CROSS-SECTION (looking from the side)", align="C")
        self.set_text_color(*INK)

    def draw_north_wall_elevation(self, x, y, w, h):
        """North wall elevation - door + window + 1'6\" wall section."""
        # Wall outline
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        self.set_fill_color(*PAPER)
        self.rect(x, y, w, h, "DF")
        # Title
        self.set_xy(x, y - 5)
        self.set_font("Verdana", "B", 8); self.set_text_color(*ACCENT_DK)
        self.cell(w, 3, "NORTH WALL ELEVATION (looking from inside foyer)", align="C")
        # Three sections: window (left/W) | wall 1.5ft | door zone 4.5ft
        # Proportions: 3.5 : 1.5 : 4.5 = ~37% : 16% : 47%
        win_w = w * 0.37
        wall_w = w * 0.16
        door_w = w * 0.47
        # Window section
        self.set_fill_color(220, 235, 250); self.set_draw_color(50, 100, 160)
        self.set_line_width(0.4)
        win_y = y + h * 0.30
        win_h = h * 0.45
        self.rect(x, win_y, win_w, win_h, "DF")
        # window mullion cross
        self.line(x + win_w/2, win_y, x + win_w/2, win_y + win_h)
        self.line(x, win_y + win_h/2, x + win_w, win_y + win_h/2)
        self.set_xy(x, win_y + win_h/2 - 2)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INFO_INK)
        self.cell(win_w, 3, "CORNER WINDOW", align="C")
        self.set_xy(x, win_y + win_h/2 + 1.5)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(win_w, 2.5, "3.5 ft wide, sill 3 ft FFL", align="C")
        # Wall section (1.5 ft) with switch panel + Reolink doorbell
        wall_x = x + win_w
        self.set_fill_color(245, 240, 220); self.set_draw_color(*INK_SOFT)
        self.rect(wall_x, y + 0.3, wall_w, h - 0.6, "DF")
        # Switch panel rect at 1200 mm FFL (~58% from top in this elevation)
        sp_y = y + h * 0.45
        sp_h = h * 0.07
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
        self.rect(wall_x + wall_w*0.10, sp_y, wall_w*0.80, sp_h, "DF")
        self.set_xy(wall_x + wall_w*0.10, sp_y - 3)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(wall_w*0.80, 2.5, "Switch Panel", align="C")
        self.set_xy(wall_x + wall_w*0.10, sp_y + sp_h + 0.5)
        self.set_font("Verdana", "I", 5); self.set_text_color(*INK_MUTED)
        self.cell(wall_w*0.80, 2, "1200 FFL", align="C")
        # Reolink doorbell on OUTSIDE of wall section - show as a dashed silhouette
        rl_y = y + h * 0.30
        rl_h = h * 0.18
        self.set_draw_color(*INFO_BD); self.set_line_width(0.3)
        for i in range(0, int(rl_h), 2):
            self.line(wall_x + wall_w*0.30, rl_y + i, wall_x + wall_w*0.30 + wall_w*0.40, rl_y + i)
            if rl_y + i + 1 < rl_y + rl_h:
                self.line(wall_x + wall_w*0.30, rl_y + i + 0.5, wall_x + wall_w*0.30, rl_y + i + 1)
                self.line(wall_x + wall_w*0.30 + wall_w*0.40, rl_y + i + 0.5, wall_x + wall_w*0.30 + wall_w*0.40, rl_y + i + 1)
        self.set_xy(wall_x - 16, rl_y + 1)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*INFO_INK)
        self.cell(16, 2.5, "Reolink", align="R")
        self.set_xy(wall_x - 16, rl_y + 4)
        self.set_font("Verdana", "I", 5); self.set_text_color(*INFO_INK)
        self.cell(16, 2, "(outside)", align="R")
        # Door zone (4.5 ft) - door + vascal
        door_x = x + win_w + wall_w
        self.set_fill_color(245, 240, 220); self.set_draw_color(*INK_SOFT)
        self.rect(door_x, y + 0.3, door_w, h - 0.6, "DF")
        # Door rectangle (door panel area)
        door_panel_w = door_w * 0.72
        door_h = h * 0.85
        door_panel_x = door_x + door_w * 0.04
        door_panel_y = y + h - door_h - 1
        self.set_fill_color(*WALNUT); self.set_draw_color(WALNUT[0]-15, WALNUT[1]-15, WALNUT[2]-15)
        self.rect(door_panel_x, door_panel_y, door_panel_w, door_h, "DF")
        # Door handle (latch) on West side
        self.set_fill_color(220, 200, 100); self.set_draw_color(180, 160, 80)
        self.ellipse(door_panel_x + 2, door_panel_y + door_h/2 - 1, 2, 2, "F")
        self.set_xy(door_panel_x, door_panel_y + door_h/2 + 2)
        self.set_font("Verdana", "I", 5); self.set_text_color(255, 245, 220)
        self.cell(door_panel_w, 2, "MAIN DOOR (hinged E)", align="C")
        # Vascal label
        self.set_xy(door_panel_x + door_panel_w, door_panel_y + door_h/2 - 1)
        self.set_font("Verdana", "I", 5); self.set_text_color(*INK_MUTED)
        self.cell(door_w * 0.20, 2, "Vascal", align="C")
        # FFL line
        self.set_draw_color(*ACCENT); self.set_line_width(0.4)
        self.line(x, y + h - 0.3, x + w, y + h - 0.3)
        self.set_text_color(*INK)

    def draw_south_wall_elevation(self, x, y, w, h):
        """South feature wall elevation - stone + cavity + walnut shelf."""
        # Open passage on left (West, 3.5 ft of S edge) - dashed
        opening_w = w * 0.37
        self.set_fill_color(*PAPER); self.set_draw_color(*INK_MUTED)
        self.set_line_width(0.3)
        for i in range(0, int(h), 3):
            self.line(x, y + i, x, y + i + 1.5)
            self.line(x + opening_w, y + i, x + opening_w, y + i + 1.5)
        self.set_xy(x, y + h/2 - 2)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.cell(opening_w, 3, "OPEN PASSAGE", align="C")
        self.set_xy(x, y + h/2 + 1.5)
        self.set_font("Verdana", "", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(opening_w, 2.5, "3.5 ft to Living/Pooja", align="C")
        # Stone feature wall on right (East, 6 ft)
        stone_x = x + opening_w
        stone_w = w - opening_w
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.4)
        self.rect(stone_x, y, stone_w, h, "DF")
        # Cavity in stone wall (centered, top half-ish at 1280-1620mm FFL)
        cav_w = stone_w * 0.32
        cav_h = h * 0.18
        cav_x = stone_x + (stone_w - cav_w)/2
        cav_y = y + h * 0.38
        self.set_fill_color(*BLACK); self.set_draw_color(*HALO_AMBER)
        self.set_line_width(0.7)
        self.rect(cav_x, cav_y, cav_w, cav_h, "DF")
        # Monitor inside cavity
        m_pad = 1.2
        self.set_fill_color(25, 25, 30); self.set_draw_color(60, 60, 65)
        self.rect(cav_x + m_pad, cav_y + m_pad, cav_w - 2*m_pad, cav_h - 2*m_pad, "DF")
        self.set_xy(cav_x, cav_y - 4)
        self.set_font("Verdana", "B", 6); self.set_text_color(*INK)
        self.cell(cav_w, 2.5, "CAVITY", align="C")
        self.set_xy(cav_x, cav_y + cav_h + 0.5)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_MUTED)
        self.cell(cav_w, 2.5, "centre 1450 FFL", align="C")
        # Walnut shelf below cavity at 900mm FFL
        shelf_y = y + h * 0.70
        shelf_h = h * 0.05
        self.set_fill_color(*WALNUT); self.set_draw_color(WALNUT[0]-15, WALNUT[1]-15, WALNUT[2]-15)
        self.set_line_width(0.3)
        self.rect(stone_x + 3, shelf_y, stone_w - 6, shelf_h, "DF")
        # Under-shelf LED hint
        self.set_draw_color(*HALO_AMBER); self.set_line_width(0.6)
        self.line(stone_x + 3, shelf_y + shelf_h + 0.5, stone_x + stone_w - 3, shelf_y + shelf_h + 0.5)
        self.set_xy(stone_x + 3, shelf_y + shelf_h + 1.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*WALNUT)
        self.cell(stone_w - 6, 2.5, "Walnut shelf 900 FFL (with under-LED)", align="C")
        # Title
        self.set_xy(x, y - 5)
        self.set_font("Verdana", "B", 8); self.set_text_color(*ACCENT_DK)
        self.cell(w, 3, "SOUTH FEATURE WALL ELEVATION", align="C")
        # FFL
        self.set_draw_color(*ACCENT); self.set_line_width(0.4)
        self.line(x, y + h - 0.3, x + w, y + h - 0.3)
        self.set_text_color(*INK)

    def draw_reflected_ceiling_plan(self, x, y, w, h):
        """Ceiling layout - cove, spots, drivers, hatch."""
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        self.set_fill_color(252, 248, 240)
        self.rect(x, y, w, h, "DF")
        # Cove pocket around perimeter
        self.set_draw_color(*HALO_AMBER); self.set_line_width(1.2)
        cp = 3
        self.rect(x + cp, y + cp, w - 2*cp, h - 2*cp, "D")
        # Inspection hatch on W edge
        hatch_w = w * 0.10
        hatch_h = h * 0.18
        self.set_fill_color(220, 215, 200); self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.3)
        self.rect(x + cp + 1, y + h/2 - hatch_h/2, hatch_w, hatch_h, "DF")
        self.set_xy(x + cp + 1, y + h/2 + hatch_h/2 + 0.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*INK_SOFT)
        self.cell(hatch_w, 2.2, "HATCH", align="C")
        # 2 spotlights (positions: 300mm from W, 609 and 1218 mm from N)
        for i, sx_frac in enumerate([0.28, 0.50]):
            sx = x + w * sx_frac
            sy = y + h * 0.32
            self.set_fill_color(255, 240, 200); self.set_draw_color(180, 130, 60)
            self.set_line_width(0.4)
            self.ellipse(sx - 2, sy - 2, 4, 4, "DF")
            self.set_xy(sx + 2.5, sy - 2)
            self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
            self.cell(20, 2.2, f"GU10 #{i+1}")
        # Drivers above hatch (small rectangles)
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
        for i in range(3):
            self.rect(x + cp + 1 + i*4.5, y + h/2 - hatch_h/2 - 4.5, 4, 3, "DF")
        self.set_xy(x + cp + 1, y + h/2 - hatch_h/2 - 7)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(16, 2.2, "Drivers (3)")
        # N label
        self.set_xy(x + w/2 - 5, y - 4)
        self.set_font("Verdana", "B", 7); self.set_text_color(*ACCENT_DK)
        self.cell(10, 2.5, "N (porch)", align="C")
        # Title
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "FOYER CEILING (cove + spots + drivers + hatch)", align="C")
        self.set_text_color(*INK)

    def draw_reolink_layering(self, x, y, w, h):
        """Cross-section showing back box + bracket + doorbell layering."""
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.3)
        self.set_fill_color(*PAPER)
        self.rect(x, y, w, h, "DF")
        # Wall mass (light grey)
        wall_w = w * 0.50
        self.set_fill_color(220, 215, 200); self.set_draw_color(*HAIRLINE)
        self.rect(x + (w - wall_w)/2, y + 2, wall_w, h - 4, "DF")
        wx = x + (w - wall_w)/2
        # Back box recessed in wall
        bb_w = w * 0.15
        bb_h = h * 0.32
        bb_x = wx + wall_w * 0.60
        bb_y = y + h/2 - bb_h/2
        self.set_fill_color(60, 60, 60); self.set_draw_color(50, 50, 50)
        self.rect(bb_x, bb_y, bb_w, bb_h, "DF")
        self.set_xy(bb_x + bb_w + 0.5, bb_y + bb_h/2 - 2)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*INK)
        self.cell(20, 2.2, "Back box")
        self.set_xy(bb_x + bb_w + 0.5, bb_y + bb_h/2 + 0.5)
        self.set_font("Verdana", "I", 5); self.set_text_color(*INK_MUTED)
        self.cell(20, 2, "75x75x65 mm")
        # Bracket (slightly larger than back box, on the outside face)
        br_w = w * 0.04
        br_h = h * 0.45
        br_x = wx + wall_w - 0.2
        br_y = y + h/2 - br_h/2
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
        self.rect(br_x, br_y, br_w, br_h, "DF")
        self.set_xy(br_x + br_w + 0.5, br_y - 2)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*ACCENT_DK)
        self.cell(20, 2.2, "Bracket")
        # Doorbell (proud of wall, similar height as bracket)
        db_w = w * 0.04
        db_h = h * 0.45
        db_x = br_x + br_w
        db_y = br_y
        self.set_fill_color(30, 30, 35); self.set_draw_color(15, 15, 15)
        self.rect(db_x, db_y, db_w, db_h, "DF")
        # Camera lens dot
        self.set_fill_color(180, 200, 220); self.set_draw_color(80, 100, 120)
        self.ellipse(db_x + db_w/2 - 0.8, db_y + 1.5, 1.6, 1.6, "DF")
        self.set_xy(db_x + db_w + 0.5, db_y + 2)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*INK)
        self.cell(30, 2.2, "Reolink doorbell")
        self.set_xy(db_x + db_w + 0.5, db_y + 4.5)
        self.set_font("Verdana", "I", 5); self.set_text_color(*INK_MUTED)
        self.cell(30, 2, "50 x 130 mm")
        # Conduit entering back box (Cat6 path) - drawn as a line
        self.set_draw_color(*GREY_PVC); self.set_line_width(0.8)
        self.line(wx, y + h - 4, bb_x + bb_w/2, bb_y + bb_h)
        self.set_xy(wx, y + h - 3)
        self.set_font("Verdana", "I", 5.5); self.set_text_color(*INK_SOFT)
        self.cell(40, 2.2, "Cat6 via conduit")
        # Foyer side label
        self.set_xy(x + 2, y + 2)
        self.set_font("Verdana", "I", 6); self.set_text_color(*INK_MUTED)
        self.cell(20, 2.2, "Foyer side")
        # Porch side label
        self.set_xy(x + w - 22, y + 2)
        self.cell(20, 2.2, "Porch side ->", align="R")
        # Title
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "REOLINK MOUNT - back box hidden behind bracket hidden behind doorbell", align="C")
        self.set_text_color(*INK)

    def draw_switch_panel_wiring(self, x, y, w, h):
        """6-gang switch panel showing wires + Sonoff."""
        # Panel face (champagne metallic look)
        self.set_fill_color(230, 215, 175); self.set_draw_color(180, 155, 110)
        self.set_line_width(0.4)
        self.rect(x, y, w, h * 0.60, "DF")
        # 6 gangs (rockers)
        gang_w = w / 6.5
        labels = ["Spots", "Cove+Halo", "Shelf", "Spare", "Porch C", "Porch W"]
        for i, lbl in enumerate(labels):
            gx = x + (w / 6) * i + (w / 6 - gang_w) / 2
            gy = y + h * 0.15
            self.set_fill_color(245, 235, 210); self.set_draw_color(180, 155, 110)
            self.rect(gx, gy, gang_w, h * 0.32, "DF")
            self.set_xy(gx, gy + h * 0.34)
            self.set_font("Verdana", "B", 5); self.set_text_color(*INK)
            self.cell(gang_w, 2, lbl, align="C")
        # Below panel: show back box with Sonoff
        bb_y = y + h * 0.65
        bb_h = h * 0.30
        self.set_fill_color(*PAPER); self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.4)
        self.rect(x, bb_y, w, bb_h, "DF")
        # Sonoff inside
        son_w = w * 0.20
        son_h = bb_h * 0.50
        son_x = x + w * 0.40
        son_y = bb_y + bb_h * 0.25
        self.set_fill_color(220, 220, 220); self.set_draw_color(*INK_SOFT)
        self.rect(son_x, son_y, son_w, son_h, "DF")
        self.set_xy(son_x, son_y + son_h + 0.5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*INK)
        self.cell(son_w, 2.2, "Sonoff (hidden)", align="C")
        # Incoming feed wire arrow
        self.set_draw_color(*RED_PVC); self.set_line_width(0.6)
        self.line(x - 6, bb_y + bb_h/2, son_x, bb_y + bb_h/2)
        self.set_xy(x - 26, bb_y + bb_h/2 - 1)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*RED_PVC)
        self.cell(20, 2.2, "FEED from DB ->", align="R")
        # Outgoing wires (4-6)
        out_y = bb_y + bb_h - 1
        for i in range(6):
            ox = x + (w / 6) * i + w / 12
            self.set_draw_color(*RED_PVC); self.set_line_width(0.5)
            self.line(ox, son_y + son_h/2, ox, out_y + 4)
        self.set_xy(x, out_y + 5)
        self.set_font("Verdana", "B", 5.5); self.set_text_color(*RED_PVC)
        self.cell(w, 2.2, "v  v  v  v  v  v  switched lives to loads", align="C")
        # Title
        self.set_xy(x, y - 5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "FOYER SWITCH PANEL (6-gang) - wiring detail", align="C")
        self.set_text_color(*INK)

    def draw_db_layout(self, x, y, w, h):
        """DB internal layout."""
        # DB enclosure
        self.set_fill_color(240, 240, 240); self.set_draw_color(80, 80, 80)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "DF")
        # Rows
        row_h = h / 8
        labels = [
            ("MAIN 63A INCOMER", (180, 50, 50)),
            ("100mA S-type RCCB", (50, 100, 180)),
            ("B-FOYER-LIGHTS  6A MCB", (60, 130, 60)),
            ("B-FOYER-CAVITY  6A + 30mA RCBO", (60, 130, 60)),
            ("(Living, Bedroom, Kitchen, etc.)", (140, 140, 140)),
            ("(Future house circuits...)", (140, 140, 140)),
            ("EARTH BUSBAR", (50, 50, 50)),
            ("", (200, 200, 200)),
        ]
        for i, (lbl, color) in enumerate(labels):
            if not lbl:
                continue
            ry = y + row_h * i
            self.set_fill_color(*color)
            self.rect(x + 1, ry + 0.5, 4, row_h - 1, "F")
            self.set_xy(x + 6, ry + row_h/2 - 1.5)
            self.set_font("Verdana", "B", 6.5); self.set_text_color(*INK)
            self.cell(w - 8, 3, lbl)
        # Title
        self.set_xy(x, y - 5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "DB INTERNAL LAYOUT - foyer-relevant slots", align="C")
        self.set_text_color(*INK)

    def draw_conduit_routing_map(self, x, y, w, h):
        """Map of all conduits from staircase niche."""
        self.set_fill_color(*PAPER); self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.3)
        self.rect(x, y, w, h, "DF")
        # Niche box at bottom-left
        niche_x = x + 3
        niche_y = y + h - 12
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
        self.rect(niche_x, niche_y, 18, 10, "DF")
        self.set_xy(niche_x, niche_y + 3)
        self.set_font("Verdana", "B", 6); self.set_text_color(255, 255, 255)
        self.cell(18, 2.5, "NICHE", align="C")
        self.set_xy(niche_x, niche_y + 6)
        self.set_font("Verdana", "I", 5); self.set_text_color(255, 250, 230)
        self.cell(18, 2, "Beelink", align="C")
        # 5 destinations
        dests = [
            ("Cavity", x + w*0.45, y + h*0.55, "Cat6 floor", (110, 110, 115)),
            ("Reolink", x + w*0.75, y + h*0.12, "Cat6 floor", (170, 110, 50)),
            ("CAM-1 spare", x + w*0.95 - 8, y + h*0.32, "string", (90, 130, 170)),
            ("CAM-2 stub", x + w*0.75, y + h*0.02, "string", (90, 130, 170)),
            ("Waveshare", x + 4, y + h*0.35, "Cat6", (90, 130, 170)),
        ]
        for label, dx, dy, route_desc, color in dests:
            # destination box
            self.set_fill_color(*color); self.set_draw_color(*color)
            self.rect(dx, dy, 12, 4, "DF")
            self.set_xy(dx - 1, dy - 3.5)
            self.set_font("Verdana", "B", 5.5); self.set_text_color(*INK)
            self.cell(14, 2.5, label)
            # route line from niche to dest
            self.set_draw_color(*color); self.set_line_width(0.5)
            self.line(niche_x + 9, niche_y, dx + 6, dy + 4)
            # route label midway
            midx = (niche_x + 9 + dx + 6) / 2
            midy = (niche_y + dy + 4) / 2
            self.set_xy(midx - 8, midy - 1)
            self.set_font("Verdana", "I", 4.5); self.set_text_color(*INK_MUTED)
            self.cell(16, 1.8, route_desc, align="C")
        # Title
        self.set_xy(x, y + h + 0.5)
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.cell(w, 3, "CONDUITS FROM STAIRCASE NICHE (5 destinations)", align="C")
        self.set_text_color(*INK)

    def colour_chip(self, x, y, w, h, hex_code, label):
        h_clean = hex_code.lstrip("#")
        r, g, b = int(h_clean[0:2], 16), int(h_clean[2:4], 16), int(h_clean[4:6], 16)
        self.set_fill_color(r, g, b)
        self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.3)
        self.rect(x, y, w, h, "DF")
        self.set_xy(x, y + h + 0.6)
        self.set_font("Verdana", "B", 6.5)
        self.set_text_color(*INK)
        self.cell(w, 2.5, clean(label), align="C")
        self.set_xy(x, y + h + 3.2)
        self.set_font("Verdana", "", 5.5)
        self.set_text_color(*INK_MUTED)
        self.cell(w, 2, hex_code, align="C")


# ============================================================
# COVER PAGE
# ============================================================
def cover_page(pdf):
    pdf.add_page()
    pdf.suppress_chrome = True
    # Top band - amber accent
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, 210, 36, "F")
    # Stone strip
    pdf.set_fill_color(*STONE_TONE)
    pdf.rect(0, 36, 210, 6, "F")
    # Title
    pdf.set_xy(15, 10)
    pdf.set_font("Georgia", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 10, "FOYER ELECTRICIAN MASTER PLAN")
    pdf.set_xy(15, 22)
    pdf.set_font("Verdana", "I", 11)
    pdf.cell(180, 6, "Pre-plaster conduit + wiring + sign-off reference")

    # Body section
    pdf.set_xy(15, 55)
    pdf.set_font("Georgia", "I", 13)
    pdf.set_text_color(*INK_SOFT)
    pdf.multi_cell(180, 7,
        clean("Everything the electrician (and other trades) need to lay conduits, "
              "cut cavities, install back boxes, pull wires, and sign off the foyer welcome "
              "system installation BEFORE plaster goes on."))

    pdf.ln(5)
    # Quick info table
    info = [
        ("Project", "Ganesh Prasad Home, Chitradurga"),
        ("Document version", "1.1  -  2026-05-22 (see Revision page next)"),
        ("Source", "electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md"),
        ("Audience", "Electrician (primary), mason, painter, carpenter, stone cladder, false-ceiling contractor, smart-home installer, homeowner"),
        ("Critical deadline", "Phase 1 marking + sign-off starts 2026-05-23. Plaster ~2026-05-30."),
        ("Sections", "18 total - design (1-10), schedules (11-14), BOM + build + sign-off (15-17), open items (18)"),
        ("Pages", "approx 50 (with diagrams)"),
        ("Cost estimate", "approx Rs. 1,06,230 for foyer welcome scope (excludes smart lock, dining speaker, Waveshare hardware)"),
    ]
    pdf.set_x(15)
    for k, v in info:
        pdf.set_x(15)
        pdf.set_font("Verdana", "B", 9.5)
        pdf.set_text_color(*ACCENT_DK)
        pdf.cell(38, 5.5, clean(k + ":"))
        pdf.set_font("Verdana", "", 9.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(140, 5.5, clean(v))
        pdf.ln(0.5)

    # Critical timeline banner
    pdf.ln(6)
    pdf.set_fill_color(*WARN_BG)
    pdf.set_draw_color(*WARN_BD)
    pdf.set_line_width(0.5)
    pdf.rect(15, pdf.get_y(), 180, 22, "DF")
    pdf.set_fill_color(*WARN_BD)
    pdf.rect(15, pdf.get_y(), 1.6, 22, "F")
    pdf.set_xy(20, pdf.get_y() + 2)
    pdf.set_font("Verdana", "B", 10)
    pdf.set_text_color(*WARN_INK)
    pdf.cell(170, 5, "CRITICAL")
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.set_font("Verdana", "", 9)
    pdf.multi_cell(170, 4.5, clean(
        "Plaster crew arrives ~2026-05-30. Once plaster goes on, no more changes. "
        "All conduits, back boxes, draw strings must be in place + sign-off form (Section 17) "
        "signed by homeowner BEFORE plaster starts."))

    # Bottom note (no diagram here - floor plan moves to Section 2)
    pdf.ln(6)
    pdf.set_font("Georgia", "I", 10.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_x(15)
    pdf.multi_cell(180, 5.5, clean(
        "The full top-down foyer floor plan with all zone markers, conduit endpoints, "
        "and device positions is in Section 2 (The Big Picture). Detailed wall elevations, "
        "cavity views, and the conduit routing map are in their respective sections."))

    # Footer note (disable auto-break to avoid spilling onto new page)
    pdf.set_auto_page_break(False)
    pdf.set_y(275)
    pdf.set_font("Verdana", "I", 7)
    pdf.set_text_color(*INK_MUTED)
    pdf.cell(0, 3, clean("Generated as part of the Home Interior & Automation project. Open this PDF on the phone on-site OR print and carry. Reference by section number for any question."),
             align="C")
    pdf.set_auto_page_break(True, 18)
    pdf.suppress_chrome = False


# ============================================================
# REVISION v1.1 PAGE (added 2026-05-22)
# ============================================================
def revision_page(pdf):
    """Revision summary page placed right after the cover, before TOC.
    Lists all 6 changes from v1.0 to v1.1 so the electrician sees them first."""
    pdf.section_open("R", "Revision v1.1 (2026-05-22)",
                     "6 changes from v1.0 (2026-05-20). Read this BEFORE the detail sections — "
                     "some prose below still uses v1.0 wording; these notes override.")
    pdf.callout("warn", "Important",
        "If you printed v1.0 already, the 6 changes below override the detail sections. "
        "Detail sections were not all re-edited — the revision summary is the canonical v1.1 update.")
    pdf.h2("The 6 changes")
    pdf.table(
        headers=["#", "What changed", "Where in doc"],
        rows=[
            ["1",
             "CAVITY SPEAKER -> CEILING SPEAKER. Visaton FR 8 + MDF baffle + 3 inch speaker pocket all DROPPED. 3 inch flush ceiling speaker added at foyer false-ceiling centre. PAM8403 amp stays in cavity. Speaker wire runs up Conduit #4 (16mm grey, cavity-top to false ceiling - previously pull-string-only, now 2-core speaker wire). Reason: electrician (nephew) flagged 3 inch blind pocket is hard to plaster reliably. Bonus: new monitor LS22F320GAW has no built-in speakers, so external speaker was always required.",
             "Sec 7 Comp 4, Sec 7.6 (pocket dropped), Sec 9 (ceiling speaker added)"],
            ["2",
             "CAVITY SOCKET PANEL: 2-module -> 8-module (8M). Adds a Cat6 keystone jack for the data conduit termination (proper structured cabling). Sonoff stays inside box. Both power AND data conduits terminate in this 8M box. Socket pocket grows to ~7 x 3 x 2 inch deep.",
             "Sec 7 Comp 5, Sec 7.6 (pocket size), Sec 14"],
            ["3",
             "FOYER SWITCH PANEL: 6-gang -> 18M VERTICAL grid. Pocket already cut on-site, fits vertically on the 1ft6inch N wall section. Extra modules reserved for porch switches + walnut shelf switch + possible foyer/living 2-way (living-hall 2-way scope deferred to electrician).",
             "Sec 8"],
            ["4",
             "SMART-SWITCH BOX APPROACH RELAXED: depth-as-needed + 2 extra modules per Sonoff. Supersedes blanket 65mm-everywhere mandate from 2026-05-06. General rule: standard 50mm box + 2 extra modules where feasible. Exception: high-density boards (Foyer Switch Panel with 6 Sonoffs) still need 65mm + 2M-per-Sonoff per Sec 8.5.",
             "Sec 8.5, Sec 14"],
            ["5",
             "DOORBELL: Reolink Video Doorbell PoE -> Hikvision DS-KV6113-WPE1(C). 2MP/1080p IP villa door station, 131 degree FOV, 120dB WDR, PoE, IP65. Datasheet confirms continuous RTSP + ONVIF -> works with Frigate 24/7 for the known-face auto-welcome flow (NOT press-only). Use accessory DS-KABV6113-A for theft resistance; TAMPER alarm built in. Same brand as CAM-3/4/5 -> unified NVR. Caveat: verify RTSP enabled in device config once in hand.",
             "Sec 2 hardware chain, Sec 5 Zone E, Sec 10 (all subsections), Sec 15"],
            ["6",
             "CAM-1 = PROVISION ONLY (confirmed). Conduit + flush-capable IP67 back box + pull string on porch W wall, NO camera installed now. Rationale: Hikvision doorbell does continuous face detection, and CAM-1 would sit only ~2-3 ft away (largely redundant). Future option: small flush anti-theft PoE pinhole if doorbell-only detection disappoints (wall stays ready).",
             "Sec 10"],
        ],
        col_widths=[7, 113, 60],
        body_size=7.5,
    )

    pdf.h2("Other context to know")
    pdf.body(
        "The welcome-screen MONITOR was also swapped in a separate 2026-05-26 update: LS22F350 -> "
        "Samsung LS22F320GAWXXL (VESA 100, IPS, 36.2mm deep, no built-in speakers, 1.6 kg, Rs.6,499). "
        "Sec 7 Components 1+2 already reflect this. The new thinner monitor gives ~64mm cavity rear gap "
        "(up from ~51mm), which makes the 8M socket box + RPi + amp layout comfortable.")
    pdf.body(
        "SMART SWITCH MODULE locked to Sonoff ZBMINI R2 (Wipro NextHome + Shelly rejected per "
        "2026-05-26 materials-checklist update).")
    pdf.body(
        "WAVESHARE INDOOR PANEL hardware locked 2026-05-25: Raspberry Pi 5 (4GB) + Waveshare PoE HAT "
        "(F) + 10.1 inch DSI touchscreen + PN532 NFC reader + walnut recessed bezel. See "
        "electrical/WAVESHARE_INDOOR_PANEL.md for full spec.")

    pdf.callout("info", "How to read the detail sections",
        "Where you see 'Reolink' in the prose: read as 'Hikvision DS-KV6113-WPE1(C)' (same install spot, "
        "same Cat6 PoE wiring, different brand/model). Where you see 'cavity speaker / Visaton FR 8 / "
        "speaker pocket': those are DROPPED - read 'ceiling speaker' instead. Where you see "
        "'2-module cavity socket': read '8M with Cat6 keystone'. Where you see '6-gang switch panel': "
        "read '18M vertical'. Where you see '65mm boxes everywhere': read 'depth-as-needed + 2 modules "
        "per Sonoff'. Section 10 has a doorbell brand-swap note at the top. Section 7 Components 4 + 5 + "
        "7.6 are fully rewritten for v1.1.")


# ============================================================
# BUILD CONTENT
# ============================================================
def build_pdf():
    pdf = ElectricianPDF()
    cover_page(pdf)
    revision_page(pdf)

    # ---------- TABLE OF CONTENTS ----------
    pdf.section_open("00", "Table of Contents",
                     "Sections, audiences, and where to find each one.")
    pdf.h2("Document map")
    pdf.table(
        headers=["#", "Section", "Primary audience"],
        rows=[
            ["1", "Document purpose + how to use this", "Everyone"],
            ["2", "The big picture - what we are building", "Everyone"],
            ["3", "Plain-English glossary", "Everyone"],
            ["4", "Foyer geometry (corrected)", "Mason + Electrician"],
            ["5", "The 6 installation zones (overview)", "Everyone"],
            ["6", "East wall - DB + starter cupboard", "Electrician + Carpenter"],
            ["7", "South wall - Screen cavity (most detail)", "Electrician + Painter + Stone cladder + Carpenter"],
            ["8", "North wall - Switch panel + door + window", "Electrician"],
            ["9", "Foyer ceiling - Spots + cove + drivers", "Electrician + False-ceiling contractor"],
            ["10", "Porch + niche routes - Doorbell + cameras + Waveshare", "Electrician"],
            ["11", "Complete conduit schedule (master table)", "Electrician"],
            ["12", "Wire schedule (every wire, gauge, colour)", "Electrician"],
            ["13", "MCB plan (2 MCBs for foyer)", "Electrician"],
            ["14", "Switch board + socket schedule", "Electrician"],
            ["15", "Bill of materials (line-item shopping list)", "Homeowner + Electrician"],
            ["16", "Phase-by-phase build order", "All trades"],
            ["17", "Pre-plaster sign-off checklist", "Homeowner + Electrician"],
            ["18", "Flagged open items (decide later)", "Homeowner"],
        ],
        col_widths=[12, 110, 58],
    )

    pdf.h2("How to use this document")
    pdf.body(
        "Each section is self-contained. Jump to the wall or zone you are working on. "
        "Section 17 is the FINAL gate before plaster - tick off every item before the "
        "plaster crew arrives. Section 11 is the master conduit list - the electrician "
        "ticks off each conduit as it gets laid.")

    # ---------- SECTION 1: PURPOSE ----------
    pdf.section_open("01", "Document Purpose",
                     "What this document is, who reads what, and the critical timeline.")
    pdf.h2("What this document is")
    pdf.body(
        "The single source of truth for the foyer welcome system installation. It contains "
        "everything needed to lay the right conduits in the right places BEFORE plastering, "
        "cut the right cavities, pull the right wires, and install the right switches, sockets, "
        "cameras, doorbell, and screens.")
    pdf.h2("Who reads what")
    pdf.table(
        headers=["Trade", "Sections"],
        rows=[
            ["Electrician (in this region, also cuts cavity + DB recess + chases + lays conduits + pulls wires + installs switches)", "4-14, 16, 17"],
            ["Mason (plastering after conduits in, stone wall building if applicable)", "4, 16, 17"],
            ["Painter (cavity interior matte black, side walls, ceiling)", "7, 9"],
            ["Carpenter (VESA mount, cupboard facade, Waveshare frame, walnut shelf)", "6, 7, 8, 10"],
            ["Stone cladder (S feature wall + cavity reveal wrap)", "7, 16"],
            ["False-ceiling contractor (gypsum, cove pocket, inspection hatch)", "9"],
            ["Smart-home installer (commissioning, camera config)", "2, 5-10"],
            ["Homeowner (decisions + sign-off)", "All; especially 3, 4, 17, 18"],
        ],
        col_widths=[120, 60],
    )
    pdf.callout("info", "Regional practice",
        "In Chitradurga construction, the ELECTRICIAN does cavity cutting, DB recess "
        "cutting, switch box cutting, and conduit chasing using core drills, wall "
        "grinders, and chisels. The mason's role is primarily plastering after the "
        "electrical work and any stone/brickwork. Trade assignments in this document "
        "reflect this practice.")

    pdf.h2("Critical timeline")
    pdf.table(
        headers=["Date", "Event", "Status"],
        rows=[
            ["2026-05-20", "Document v1.0 published, design locked", "Done"],
            ["2026-05-21 to 22", "On-site walkthrough with electrician + carpenter", "Done"],
            ["2026-05-23", "PHASE 1 starts: marking + sign-off", "Imminent"],
            ["2026-05-23 to 24", "Phase 2: wall chasing + cavity cutting", ""],
            ["2026-05-25 to 26", "Phase 3: conduit pulling", ""],
            ["2026-05-27 to 28", "Phase 4: wire pulling + DB install", ""],
            ["2026-05-29 to 31", "Phase 5: first plaster (rough coat)", ""],
            ["~2026-06-15", "Welcome system live + tested", "TARGET"],
        ],
        col_widths=[34, 110, 36],
    )
    pdf.callout("warn", "Once plaster goes on, you cannot change anything",
        "All conduits, back boxes, draw strings must be in place and the Section 17 "
        "sign-off form must be signed by the homeowner BEFORE the plaster crew arrives. "
        "There is no second chance.")

    # ---------- SECTION 2: BIG PICTURE ----------
    pdf.section_open("02", "The Big Picture",
                     "What the welcome system does and how the pieces connect.")
    pdf.lede(
        "Visitor approaches the main door. The face camera sees them. Two seconds later "
        "the screen in the foyer feature wall lights up with their name and a chime plays "
        "from a hidden cavity speaker. They feel expected. They feel welcomed. "
        "That is the whole idea.")
    pdf.h2("Three-step welcome flow")
    pdf.bullet("SEES: Reolink Video Doorbell on the N wall 1'6\" section captures the visitor's face as they approach the main door.")
    pdf.bullet("RECOGNISES: Beelink EQ12 in the staircase niche runs Frigate + CompreFace - matches face within ~2 seconds.")
    pdf.bullet("GREETS: Samsung 21.5\" monitor in the cavity lights up; halo LED glows warm amber around the screen; speaker plays a chime.")

    pdf.h2("Hardware chain (data flow)")
    pdf.table(
        headers=["#", "Component", "Where it lives", "What it does"],
        rows=[
            ["1", "Reolink Video Doorbell PoE", "Outside N wall, 1'6\" section, 1450 mm FFL", "Captures visitor's face + rings bell"],
            ["2", "Cat6 (PoE)", "From doorbell -> staircase niche", "Data + power"],
            ["3", "PoE switch (TP-Link TL-SG1210P)", "Staircase niche", "Powers cameras + Reolink + future cams"],
            ["4", "Beelink EQ12 (Frigate + CompreFace + HA)", "Staircase niche", "Identifies the face in 1-2 sec"],
            ["5", "Home Assistant automation", "Same server", "Decides what to display"],
            ["6", "Cat6 to cavity (PoE)", "Niche -> floor -> cavity bottom-right", "Pushes welcome payload + power for RPi"],
            ["7", "Raspberry Pi Zero 2W", "Inside cavity, behind monitor", "Drives the monitor + speaker"],
            ["8", "Samsung LS22F350 monitor", "Recessed in feature wall, centre 1450 mm FFL", "Shows the welcome"],
            ["9", "Pi Camera Module 3 (CAM-0)", "Top bezel of monitor", "Secondary face check at close range"],
            ["10", "Halo LED strip", "Inside cavity at 30 mm depth step, all 4 inner walls", "Warm amber glow around monitor"],
            ["11", "Visaton FR 8 speaker + PAM8403 amp", "Inside cavity, behind monitor", "Chime + welcome voice from screen"],
            ["12", "Foyer Switch Panel (6-gang)", "N wall, 1'6\" section, 1200 mm FFL", "Manual control + scene override"],
        ],
        col_widths=[7, 50, 53, 70],
        body_size=7.5,
    )

    pdf.h2("Visual: welcome system layout (top-down foyer floor plan)")
    pdf.place_diagram(pdf.draw_foyer_floor_plan, 130)

    # ---------- SECTION 3: GLOSSARY ----------
    pdf.section_open("03", "Plain-English Glossary",
                     "Every technical term used in this document, defined.")
    pdf.h2("Electrical terms")
    pdf.table(
        headers=["Term", "Plain-English meaning"],
        rows=[
            ["DB (Distribution Board)", "The panel of breakers in the wall. Every wire starts here. Ours is on the East wall of the foyer."],
            ["MCB (Miniature Circuit Breaker)", "A trip switch inside the DB. One per circuit. Trips on overload or short."],
            ["RCBO / RCCB", "Like an MCB but also trips on leakage to earth. Mandatory for electronics + wet circuits."],
            ["Circuit", "One wire run from a single MCB feeding a group of devices."],
            ["FFL (Finished Floor Level)", "Top of the installed floor tile. All heights are measured from FFL, NOT raw slab."],
            ["Conduit", "A plastic pipe inside the wall. Wires get pulled through it. Red = 230V power, Grey = low voltage."],
            ["Chase", "The groove cut into the wall where the conduit sits."],
        ],
        col_widths=[50, 130],
    )
    pdf.h2("Switch / socket terms")
    pdf.table(
        headers=["Term", "Plain-English meaning"],
        rows=[
            ["Gang", "One switch position on a plate. A 4-gang plate has 4 separate switches."],
            ["Switch Board / Switch Panel", "The wall plate + back box that holds the switches. We call ours the 'Foyer Switch Panel'."],
            ["Modular plate", "The removable face plate that snaps onto a back box."],
            ["Back box", "The metal box recessed into the wall behind the plate. 65 mm DEEP for smart switches."],
            ["5A socket", "Standard 3-pin Indian outlet, 230V, for low-current things (chargers, TVs, monitors)."],
            ["16A socket", "Bigger 3-pin outlet for heavy appliances (geyser, AC, microwave)."],
            ["Smart switch", "A switch that takes commands over WiFi/Zigbee in addition to manual press."],
            ["Sonoff", "WiFi smart relay that fits behind the switch plate as a hidden unit."],
        ],
        col_widths=[50, 130],
    )
    pdf.h2("Light + LED terms")
    pdf.table(
        headers=["Term", "Plain-English meaning"],
        rows=[
            ["LED strip", "A thin sticky strip with tiny LED dots. Comes in 24V or 12V. Sold in 5m rolls."],
            ["Driver (LED driver)", "A small electronic brick that converts 230V AC to 24V DC for LED strips. Like a phone charger."],
            ["Halo LED", "The warm amber strip stuck around the cavity inner edges. Glows around the monitor."],
            ["Cove LED", "The 2700K strip hidden in the cove pocket around the false ceiling perimeter."],
            ["Spotlight (GU10)", "A focused beam. GU10 bulbs run on 230V mains directly - NO driver needed."],
            ["CCT", "Colour temperature. 2200K = candle warm amber, 2700K = warm white."],
        ],
        col_widths=[50, 130],
    )
    pdf.h2("Camera / network terms")
    pdf.table(
        headers=["Term", "Plain-English meaning"],
        rows=[
            ["PoE", "Power over Ethernet - sending power AND data over the same Cat6 cable."],
            ["Cat6", "Category 6 Ethernet cable. Carries gigabit data + PoE power."],
            ["LSZH", "Low Smoke Zero Halogen - jacket material that doesn't produce toxic gas in fire."],
            ["UV-resistant", "Cable jacket that doesn't crack in sunlight. For outdoor / exposed cables."],
            ["RTSP", "Real-Time Streaming Protocol - the video stream format used by IP cameras."],
            ["NVR", "Network Video Recorder - records + processes camera streams. Ours = Beelink EQ12 with Frigate."],
            ["Home Assistant (HA)", "The smart-home brain software. Reads sensors, decides actions, controls devices."],
        ],
        col_widths=[50, 130],
    )
    pdf.h2("Cavity / door terms")
    pdf.table(
        headers=["Term", "Plain-English meaning"],
        rows=[
            ["Cavity", "The rectangular hole cut into the S feature wall for the monitor."],
            ["VESA bracket", "Metal plate (75x75 mm pattern) that screws into the back of the monitor + onto the wall."],
            ["Baffle (MDF)", "Small wooden plate that holds the speaker driver."],
            ["Vascal", "The wall return between the door jamb and the East exterior wall corner."],
            ["Niche", "The server cupboard built into the staircase wall."],
            ["Hinge side", "Where the door hinges are - ours is EAST."],
            ["Latch side", "Where the door handle is - ours is WEST."],
        ],
        col_widths=[50, 130],
    )

    # ---------- SECTION 4: GEOMETRY ----------
    pdf.section_open("04", "Foyer Geometry",
                     "Exact dimensions, walls, openings - the foundation everything else builds on.")
    pdf.h2("Foyer dimensions")
    pdf.table(
        headers=["Dimension", "Imperial", "Metric", "Notes"],
        rows=[
            ["N-S depth (door to feature wall)", "5 ft (60\")", "1524 mm", "Fixed - S feature wall is built"],
            ["E-W at S edge (stone feature wall)", "6 ft (72\")", "1828 mm", "The stone wall portion"],
            ["E-W at S edge (opening portion)", "3.5 ft", "1066 mm", "Open to Living/Pooja"],
            ["E-W at N edge (door wall)", "9.5 ft (114\")", "2895 mm", "Total N exterior wall length"],
            ["GF ceiling height (slab)", "11 ft", "3353 mm", "Raw slab"],
            ["Foyer false ceiling height", "9 ft", "2743 mm", "Drop of 2 ft from slab"],
            ["S feature wall thickness", "9\"", "228 mm", "Structural - NOT a 4\" partition"],
            ["N exterior wall thickness", "9\"", "228 mm", "Exterior brick/block masonry"],
            ["E exterior wall thickness", "9\"", "228 mm", "Exterior"],
        ],
        col_widths=[64, 32, 28, 56],
    )

    pdf.h2("Key reference heights (from FFL)")
    pdf.table(
        headers=["Reference", "Inches", "mm", "Why"],
        rows=[
            ["Cavity centre (screen eye level)", "57-1/8\"", "1450", "Standing eye level"],
            ["Cavity bottom edge", "50-1/2\"", "1280", "Ergonomic recess"],
            ["Cavity top edge", "63-7/8\"", "1620", "Auto-derived"],
            ["Walnut shelf top surface", "35-3/8\"", "900", "Below cavity"],
            ["Reolink doorbell centre", "57\"", "1450", "Face level for adult"],
            ["Foyer Switch Panel centre", "47-1/4\"", "1200", "Standard switch height"],
            ["DB bottom edge", "59\"", "1500", "MCBs at chest height"],
            ["False ceiling height", "108\"", "2743", "9 ft drop from 11 ft slab"],
        ],
        col_widths=[60, 30, 28, 62],
    )

    pdf.h2("Orientation convention")
    pdf.body(
        "When this document says LEFT or RIGHT for the cavity or any wall, it means: "
        "you are standing in the foyer, looking AT the wall in question. LEFT/RIGHT is "
        "from your perspective.\n\n"
        "For the South feature wall (looking SOUTH at the cavity from foyer):\n"
        "  LEFT = East side (the DB direction)\n"
        "  RIGHT = West side (the staircase niche direction)\n\n"
        "For the North wall (looking NORTH at the door from inside foyer):\n"
        "  LEFT = West side (where the corner window is)\n"
        "  RIGHT = East side (where the door + vascal are)")

    # ---------- SECTION 5: ZONES OVERVIEW ----------
    pdf.section_open("05", "The 6 Installation Zones",
                     "High-level map of all the work zones in the foyer welcome scope.")
    pdf.table(
        headers=["Zone", "Wall / area", "Detail section", "Key items"],
        rows=[
            ["A", "East wall (interior)", "6", "DB + starter cupboard"],
            ["B", "South feature wall", "7", "Screen cavity + walnut shelf"],
            ["C", "North wall", "8", "Switch panel + door + window"],
            ["D", "Foyer ceiling", "9", "Spots + cove + halo + drivers"],
            ["E", "Porch (external)", "10", "Reolink + CAM-1 spare + CAM-2 stub"],
            ["F", "Staircase indoor", "10", "Waveshare + server niche"],
        ],
        col_widths=[14, 50, 30, 86],
    )
    pdf.body(
        "Zones A through D are inside the foyer. Zone E is on the porch (outside the foyer "
        "but under the FF balcony slab overhang). Zone F is in the staircase area which is "
        "indoor but outside the foyer. All 5 external/indoor-non-foyer conduits originate "
        "from the staircase niche.")

    pdf.h2("Conduit count per zone")
    pdf.table(
        headers=["Zone", "Conduits"],
        rows=[
            ["A (East wall / DB)", "2 going OUT of DB + 5 incoming from water automation system"],
            ["B (South cavity)", "3 entering cavity (Power, Data, Halo 24V) + 1 provision exiting (ceiling speaker future)"],
            ["C (North switch panel)", "1 incoming from DB + 4-6 outgoing to loads (Spots, Cove+Halo, Shelf, Porch Ceiling, Porch Wall, Spare)"],
            ["D (Ceiling)", "Branch conduits from switch panel + driver-to-strip"],
            ["E (Porch external)", "3 long-runs from niche (Reolink, CAM-1 spare, CAM-2 stub)"],
            ["F (Staircase indoor)", "1 short-run (Waveshare)"],
        ],
        col_widths=[44, 136],
    )

    # ---------- SECTION 6: EAST WALL ----------
    pdf.section_open("06", "East Wall - DB + Starter Cupboard",
                     "Zone A. DB recessed in wall; starter cupboard surface-mounted alongside or below.")
    pdf.h2("Equipment on the East wall")
    pdf.table(
        headers=["Item", "Dimensions (W x H x D)", "Mount", "Centre / bottom height"],
        rows=[
            ["DB recess (Schneider Acti9 48-way)", "400 x 600 x 100 mm", "Flush recessed", "Bottom edge 1500 mm FFL"],
            ["Starter cupboard (P1 + P2 + Sonoff DUALR3 + terminals)", "600 x 400 x 250 mm", "SURFACE-MOUNTED", "TBD on-site"],
        ],
        col_widths=[60, 48, 30, 42],
    )

    pdf.h2("The geometric constraint")
    pdf.body(
        "East wall is 5 ft (1524 mm) long N-S. Main door (3.2 ft = 975 mm wide) swings "
        "against East wall when open. Door panel covers the first 975 mm from the N corner. "
        "That leaves only 549 mm of East wall South of the door panel arc.")
    pdf.body(
        "DB (400 mm wide) + Cupboard (600 mm wide) side-by-side need 1000 mm. They DON'T fit "
        "in 549 mm. Solution: stack them vertically OR DB sits behind door panel + cupboard "
        "south of swing (with small overhang).")
    pdf.callout("info", "Electrician decides on-site",
        "Final layout (Option 1 = side-by-side with cupboard slight overhang OR "
        "Option 2 = stacked vertically inside door swing zone) is chosen on-site after "
        "actual measurements. Homeowner signs off on the chosen layout.")

    pdf.h2("East wall elevation (visual)")
    pdf.place_diagram(pdf.draw_east_wall_elevation, 70)

    pdf.h2("Conduits originating from the DB (only 2 go out!)")
    pdf.body(
        "Only TWO conduits actually start at the DB to feed the foyer. Within each, multiple "
        "wires run together (L+N+E). Loads are then fed downstream from the Foyer Switch "
        "Panel - NOT directly from the DB.")
    pdf.table(
        headers=["#", "Conduit ID", "Size", "To", "Wires inside"],
        rows=[
            ["1", "C-DB-Foyer-Switch", "25 mm RED", "Foyer Switch Panel (N wall, 1200 FFL)", "1.5 sqmm L + N + E"],
            ["2", "C-DB-Cavity-Power", "25 mm RED", "Cavity bottom-LEFT corner of back wall", "2.5 sqmm L + N + E"],
        ],
        col_widths=[7, 45, 20, 70, 38],
    )

    pdf.h2("Conduits ENTERING the cupboard (water automation)")
    pdf.body("Cross-reference: water-automation-conduits.md")
    pdf.table(
        headers=["#", "Conduit ID", "Size", "From", "Carries"],
        rows=[
            ["1", "C-Sintex-2", "16 mm", "Sintex tank float (terrace)", "2-core 1.5 sqmm 220V"],
            ["2", "C-Sump-2", "16 mm", "Sump JB (east external wall)", "2-core 1.5 sqmm 220V"],
            ["3", "C-DB-Backup", "20 mm", "Staircase server niche", "Empty pull string"],
            ["4", "C-Motor-P1", "25 mm", "Outside (borewell)", "3-core 4 sqmm armoured"],
            ["5", "C-Motor-P2", "25 mm", "Outside (P2 pump)", "3-core 2.5 sqmm"],
        ],
        col_widths=[7, 28, 18, 72, 55],
    )

    pdf.h2("Pre-plaster sign-off for Zone A")
    pdf.checklist([
        "Final layout (Option 1 or 2) selected on-site by electrician + carpenter",
        "Homeowner sign-off photographed",
        "DB recess cut to 400 x 600 x 100 mm, flush, ready for DB shell",
        "Cupboard mounting position marked with ventilation considerations",
        "All 5 outgoing DB conduits routed and labelled",
        "All 5 incoming water automation conduits terminated at cupboard back panel",
        "Draw strings (nylon twine) inserted in every conduit",
        "All conduit ends capped with masking tape",
        "Earth wire (4 sqmm) routed from earth pit to DB",
        "Mounting bracket / rawl plugs for DB shell ready",
    ])

    # ---------- SECTION 7: CAVITY ----------
    pdf.section_open("07", "South Wall - Screen Cavity",
                     "Zone B. The most complex zone. Stone reveal wraps INTO the cavity for a premium framed look.")
    pdf.h2("Cavity overview")
    pdf.body(
        "Think of the cavity as a small medicine cabinet built into the wall. The cavity has "
        "5 surfaces inside: TOP inner wall, BOTTOM inner wall, LEFT inner wall, RIGHT inner "
        "wall, and BACK wall. Plus the OPEN front (where the monitor hangs). Stone slips are "
        "applied to all 4 INNER walls for the FRONT 30 mm of depth only. The back wall stays "
        "matte black across its full surface.")

    pdf.h2("Cavity cut dimensions")
    pdf.table(
        headers=["Dimension", "Imperial", "Metric", "Notes"],
        rows=[
            ["Cavity cut WIDTH (raw masonry)", "22-3/4\"", "580 mm", "Bigger than final, to fit stone slips"],
            ["Cavity cut HEIGHT (raw masonry)", "14-7/8\"", "380 mm", "Same reason"],
            ["Cavity DEPTH (into 9\" wall)", "4\"", "100 mm", "Leaves 5\" of masonry behind"],
            ["Inner usable opening AFTER stone slips", "21-1/4\" x 13-1/2\"", "540 x 340 mm", "What the monitor sees"],
            ["Stone reveal depth (front portion)", "1-1/4\"", "30 mm", "First 30mm of inner walls clad in stone"],
            ["Stone slip thickness", "3/4\"", "20 mm", "Per inner wall"],
        ],
        col_widths=[58, 36, 28, 58],
    )

    pdf.h2("Cavity front view (with monitor + halo)")
    pdf.place_diagram(pdf.draw_cavity_front_view, 100, full_width=False, manual_x=40, manual_w=130)

    pdf.h2("Cavity back wall - sub-pockets + conduit entries")
    pdf.place_diagram(pdf.draw_cavity_back_wall, 85)

    pdf.h2("Stone reveal cross-section")
    pdf.place_diagram(pdf.draw_cavity_cross_section, 70, full_width=False, manual_x=30, manual_w=150)

    pdf.h2("Sub-pockets cut INTO the cavity walls")
    pdf.table(
        headers=["#", "Pocket", "Wall", "Dimensions", "Depth INTO masonry", "Position"],
        rows=[
            ["1", "Socket pocket", "Cavity back wall", "3\" x 3\"", "2-1/2\"", "Centred horiz; centre at 53\" FFL"],
            ["2", "Speaker pocket", "Cavity back wall", "3\" diameter", "1\"", "Centred horiz; centre at 57-1/8\" FFL"],
        ],
        col_widths=[7, 30, 36, 24, 26, 57],
    )

    pdf.h2("The 4 conduits at the cavity (3 IN through back wall + 1 OUT through top)")
    pdf.table(
        headers=["#", "Conduit", "Size", "Colour", "Entry / exit point", "From / To"],
        rows=[
            ["1", "POWER", "25 mm", "RED", "Bottom-LEFT of back wall (1.5\" up + 2\" in)", "From DB (East wall)"],
            ["2", "DATA", "25 mm", "GREY", "Bottom-RIGHT of back wall (1.5\" up + 2\" in)", "From staircase niche (via floor)"],
            ["3", "HALO 24V", "16 mm", "GREY", "Top-CENTRE of back wall (3/4\" down)", "From halo driver (above false ceiling)"],
            ["4", "Ceiling speaker provision", "16 mm", "GREY", "TOP wall, going UP", "To future ceiling speaker (pull string only)"],
        ],
        col_widths=[7, 35, 16, 18, 50, 54],
    )

    pdf.h2("Components inside the cavity")
    pdf.table(
        headers=["#", "Component", "Position", "Spec"],
        rows=[
            ["1", "Monitor (Samsung LS22F350)", "Hangs on VESA bracket; front face flush with stone face", "21.5\", 491 x 291 x 49 mm, VESA 75"],
            ["2", "VESA bracket", "Centre of back wall, 1450 mm FFL", "Slim flat-mount, direct rawl plugs OR small 8\"x4\" ply"],
            ["3", "RPi Zero 2W + PoE splitter", "Stuck to back wall via 3M tape", "Powered by PoE + data via same Cat6"],
            ["4a", "Visaton FR 8 speaker + MDF baffle (PRIMARY)", "Back wall, behind monitor centre; magnet in 1\" pocket", "80 mm dia, fires forward through monitor back"],
            ["4b", "Ceiling speaker (FUTURE OPTION)", "Above false ceiling (if added later via Conduit #4)", "16mm grey conduit + pull string ready now"],
            ["5", "Cavity Socket Panel (2 sockets)", "Back wall, centre at 53\" FFL, in 3\"x3\"x2.5\" pocket", "Monitor + Spare; Sonoff Mini hidden inside box"],
            ["6", "Bezel CAM-0 (Pi Camera Module 3)", "Top-centre of monitor bezel", "CSI ribbon to RPi (no conduit needed)"],
            ["7", "Halo LED strip (24V 2200K)", "Inner walls at 30 mm depth step; ALL 4 sides", "Hidden behind stone reveal lip; ~2 m total"],
        ],
        col_widths=[7, 50, 60, 63],
    )

    pdf.h2("Painter scope inside cavity")
    pdf.kv("Back wall (all)", "Matte black acrylic emulsion, 2 coats - BEFORE stone cladding")
    pdf.kv("Inner walls DEEPER than 30 mm", "Matte black, 2 coats")
    pdf.kv("Inner walls FRONT 30 mm", "DO NOT paint - stone slips go here")
    pdf.kv("VESA backing ply (if used)", "Matte black, 1 coat before install")
    pdf.kv("MDF speaker baffle", "Matte black, 1 coat before install")

    pdf.h2("Stone cladder scope")
    pdf.kv("Main wall cladding", "Rustic ledgestone (tobacco + sandstone + charcoal mix), 6 ft x 11 ft S feature wall face")
    pdf.kv("Cavity reveal slips", "20 mm thick stone slips on FRONT 30 mm of all 4 inner walls. Stops cleanly at 30 mm depth line.")
    pdf.kv("DO NOT", "Apply stone deeper than 30 mm; cover the conduit stubs; cover socket / speaker pockets.")

    pdf.h2("Pre-plaster sign-off for Zone B")
    pdf.checklist([
        "Cavity cut to 22-3/4\" x 14-7/8\" x 4\" (580 x 380 x 100 mm)",
        "Cavity centred on 6 ft feature wall - 24-5/8\" from each side edge ON ACTUAL MEASURED WIDTH",
        "Bottom edge at 50-1/2\" (1280 mm) FFL",
        "Socket pocket cut: 3\" x 3\" x 2-1/2\" deep, centred horiz, centre at 53\" FFL",
        "Speaker pocket cut: 3\" diameter x 1\" deep, centred horiz, centre at 57-1/8\" FFL",
        "Conduit #1 (Power) hole: 1\" diameter, bottom-LEFT, 1.5\" up + 2\" in",
        "Conduit #2 (Data) hole: 1\" diameter, bottom-RIGHT, 1.5\" up + 2\" in",
        "Conduit #3 (Halo) hole: 5/8\" diameter, top-CENTRE, 3/4\" down",
        "Conduit #4 (Ceiling speaker provision) exit: 5/8\" diameter through TOP inner wall going up",
        "All 4 conduit stubs protrude 1-1.5\" into cavity, capped, draw strings, labelled",
        "Stone cladder briefed on the 30 mm reveal specification",
        "Painter briefed: do NOT paint front 30 mm of inner walls",
        "Cavity dimensions photographed",
        "Walnut shelf bracket positions chalked at 900 mm FFL on S wall",
    ])

    # ---------- SECTION 8: N WALL ----------
    pdf.section_open("08", "North Wall - Switch Panel + Door + Window",
                     "Zone C. The entry wall.")

    pdf.h2("N wall layout")
    pdf.place_diagram(pdf.draw_north_wall_elevation, 65)

    pdf.h2("Wall breakdown (W to E)")
    pdf.table(
        headers=["Section", "Width", "Contains"],
        rows=[
            ["Corner window", "3'6\" (1066 mm)", "Sill 3 ft FFL, height 5 ft; wraps NW corner extending N"],
            ["Wall section", "1'6\" (457 mm)", "Foyer Switch Panel (inside face) + Reolink doorbell (outside face)"],
            ["Door zone", "4'6\" (1372 mm)", "Door 3.2 ft + vascal ~1'4\" on East side"],
            ["TOTAL", "9'6\" (2895 mm)", ""],
        ],
        col_widths=[40, 45, 95],
    )

    pdf.h2("Foyer Switch Panel - position + specs (REVISED 2026-05-23)")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Wall section", "1'6\" section between window and door"],
            ["Centre height (FFL)", "1200 mm (47-1/4\") - standard switch height"],
            ["Back box (CUT ON SITE)", "18M VERTICAL GI MS, ~290 x 135 x 65 mm OR 225 x 195 x 65 mm"],
            ["Orientation", "VERTICAL - longer side runs top to bottom"],
            ["Box depth", "65 mm mandatory - confirm with tape (electrician said >=2 in)"],
            ["Wall capacity", "1'6\" = 457 mm; 18M vertical is 135 mm wide - fits with 322 mm spare"],
            ["Plate", "Schneider Unica 18M White (matching house-wide brand)"],
            ["Slack inside box", "12M slack accommodates 6 hidden Sonoffs + neutral bus (+2M per Sonoff rule)"],
        ],
        col_widths=[58, 122],
    )

    pdf.h2("Gang assignments")
    pdf.table(
        headers=["Gang", "Label", "Controls"],
        rows=[
            ["1 (left, near window)", "Foyer Spots", "2x GU10 ceiling spotlights"],
            ["2", "Cove + Halo", "Cove LED 2700K + Halo LED 2200K (linked)"],
            ["3", "Shelf", "Walnut shelf under-LED strip"],
            ["4", "Foyer Spare", "Future foyer addition (capped)"],
            ["5", "Porch Ceiling", "Porch ceiling light(s)"],
            ["6 (right, near door)", "Porch Wall", "Porch wall lights (future provision)"],
            ["7 (if 7-gang)", "Spare 7", "Future use"],
            ["8 (if 8-gang)", "Spare 8", "Future use"],
        ],
        col_widths=[36, 30, 114],
    )

    pdf.h2("Conduits in / out of Switch Panel")
    pdf.table(
        headers=["Conduit", "Size", "Direction", "Route"],
        rows=[
            ["C-DB-Foyer-Switch", "25 mm RED", "INCOMING from DB", "Up E wall -> false ceiling -> across to N wall -> drops to box"],
            ["C-SW-Spots", "25 mm RED", "OUT (Gang 1 -> spots)", "Up N wall -> false ceiling -> to 2 spot ceiling boxes"],
            ["C-SW-Cove-Halo", "25 mm RED", "OUT (Gang 2 -> drivers)", "Up N wall -> false ceiling -> splits to cove + halo drivers"],
            ["C-SW-Shelf", "16 mm RED", "OUT (Gang 3 -> shelf)", "Down N wall -> floor route -> up S wall -> to shelf"],
            ["C-SW-Spare", "16 mm RED", "OUT (Gang 4 -> spare)", "Up N wall -> false ceiling -> capped, pull string"],
            ["C-SW-Porch-Ceiling", "16 mm RED", "OUT (Gang 5 -> porch ceil)", "Up N wall -> through 9\" wall -> porch ceiling"],
            ["C-SW-Porch-Wall", "16 mm RED", "OUT (Gang 6 -> porch wall)", "Up N wall -> through 9\" wall -> outside near door (capped)"],
        ],
        col_widths=[36, 22, 38, 84],
    )

    pdf.h2("Switch panel wiring (visual)")
    pdf.place_diagram(pdf.draw_switch_panel_wiring, 60, full_width=False, manual_x=30, manual_w=150)

    pdf.h2("Walnut shelf (on S wall, electrically wired from Gang 3)")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Material", "Solid walnut OR veneered MDF"],
            ["Dimensions", "6 ft x 10\" deep x 1-1/4\" thick"],
            ["Top surface height (FFL)", "900 mm (35-3/8\")"],
            ["Under-LED strip", "24V, 6 W/m, 2700K, 1.8 m"],
            ["LED driver location", "Option 1: above false ceiling (default). Option 2: under shelf (alternative)."],
        ],
        col_widths=[58, 122],
    )

    pdf.h2("Pre-plaster sign-off for Zone C")
    pdf.checklist([
        "N wall total length verified (~9'6\" / 2895 mm)",
        "Door opening cut to 3'2\" wide x 7 ft tall",
        "Window opening cut to 3'6\" wide x 5 ft tall (corner wrap)",
        "Vascal wall section confirmed (~1'4\" East of door)",
        "1'6\" wall section between door and window confirmed",
        "Foyer Switch Panel back box: 18M VERTICAL GI MS, ~290 x 135 x 65 mm (or 225 x 195 x 65), centred horiz, centre 1200 mm FFL - confirm 65 mm depth with tape",
        "C-DB-Foyer-Switch conduit terminated at back box",
        "All outgoing conduits from switch panel routed",
        "Draw strings in all conduits",
        "All conduit ends capped",
        "Reolink doorbell back box installed on OUTSIDE face of 1'6\" section, 1450 mm FFL",
        "Homeowner sign-off photographed",
    ])

    # ---------- SECTION 9: CEILING ----------
    pdf.section_open("09", "Foyer Ceiling - Spots, Cove, Drivers",
                     "Zone D. False ceiling at 9 ft. Cove pocket around perimeter. Inspection hatch above W edge.")
    pdf.h2("False ceiling specs")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Slab height", "11 ft (3353 mm) FFL"],
            ["False ceiling height", "9 ft (2743 mm) FFL"],
            ["Drop", "2 ft (610 mm)"],
            ["Material", "12.5 mm gypsum board on GI grid"],
            ["Cove pocket", "100 mm wide x 75 mm deep around full perimeter"],
            ["Inspection hatch", "300 x 300 mm above W edge of foyer ceiling"],
        ],
        col_widths=[58, 122],
    )

    pdf.h2("Reflected ceiling plan")
    pdf.place_diagram(pdf.draw_reflected_ceiling_plan, 75, full_width=False, manual_x=40, manual_w=130)

    pdf.h2("Ceiling spotlights (GU10) - NO driver needed!")
    pdf.callout("info", "GU10 LED bulbs do NOT need a separate driver",
        "Each GU10 bulb has the driver electronics built into the bulb itself. They run "
        "on 230V AC mains directly. Unlike the cove / halo / shelf strips (which DO need "
        "24V drivers), the GU10 spots wire directly from the Foyer Switch Panel Gang 1.")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Fitting", "Recessed GU10 gimbal (adjustable angle)"],
            ["Bulb", "7W LED, 2700K, CRI 90+, 30 degree beam"],
            ["Spot #1 position", "300 mm from W wall area, 609 mm from N edge of foyer"],
            ["Spot #2 position", "300 mm from W wall area, 1218 mm from N edge of foyer"],
            ["Aim", "Graze the S feature wall at ~1700 mm FFL"],
            ["Driver", "NONE - built into the GU10 bulb"],
            ["Wire", "Direct 230V from Gang 1 (switched live + N + E)"],
        ],
        col_widths=[58, 122],
    )

    pdf.h2("Cove LED strip + driver")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Strip", "24V DC, 9.6 W/m, 2700K, CRI 90+, IP20"],
            ["Length", "~10 m around full perimeter"],
            ["Position", "Inside cove pocket, pointing UPWARD"],
            ["Driver", "Mean Well APV-100-24 (100W, 24V)"],
            ["Driver location", "Above false ceiling, beside inspection hatch"],
            ["Control", "Switched by Gang 2 (linked with halo)"],
        ],
        col_widths=[58, 122],
    )

    pdf.h2("Halo + Shelf LED drivers")
    pdf.table(
        headers=["Driver", "Location", "Powers"],
        rows=[
            ["Halo driver (Mean Well APV-12-24)", "Above false ceiling beside cove driver", "Cavity halo strip"],
            ["Shelf driver (Mean Well APV-12-24)", "Option 1: above false ceiling. Option 2: under shelf.", "Walnut shelf strip"],
        ],
        col_widths=[60, 70, 50],
    )

    pdf.h2("Pre-plaster sign-off for Zone D")
    pdf.checklist([
        "False ceiling drop confirmed at 2 ft (from 11 ft slab to 9 ft FFL)",
        "Cove pocket dimensions: 100 mm wide x 75 mm deep, around full perimeter",
        "Inspection hatch position marked (300 x 300 mm, W edge)",
        "2x GU10 ceiling box positions chalked on raw slab",
        "All conduits arriving at false ceiling terminated and labelled",
        "Driver shelf location marked (above hatch)",
        "Cove strip routing path confirmed (continuous loop)",
        "Homeowner sign-off photographed",
    ])

    # ---------- SECTION 10: PORCH + NICHE ----------
    pdf.section_open("10", "Porch + Niche Routes",
                     "Zones E + F. All external + indoor-non-foyer conduits originate at the staircase niche.")

    pdf.h2("Conduit routing overview")
    pdf.place_diagram(pdf.draw_conduit_routing_map, 95)

    pdf.h2("5 conduits from the niche")
    pdf.table(
        headers=["#", "Conduit ID", "Size", "Primary route", "To"],
        rows=[
            ["1", "C-Niche-Cavity-Data", "25 mm GREY", "FLOOR", "Cavity bottom-right (Cat6 for RPi)"],
            ["2", "C-Niche-Doorbell", "25 mm GREY", "FLOOR", "Reolink doorbell on N wall outside (1450 FFL)"],
            ["3", "C-Niche-CAM1", "25 mm GREY", "FLOOR", "Porch W wall capped (1650 FFL) - pull string only"],
            ["4", "C-Niche-CAM2", "25 mm GREY", "CEILING (only viable)", "Porch soffit NE corner (~2700 FFL) - pull string only"],
            ["5", "C-Niche-Waveshare", "25 mm GREY", "Short vertical", "Staircase S wall (1500 FFL) - Cat6 pulled"],
        ],
        col_widths=[7, 38, 22, 35, 78],
    )

    pdf.callout("warn", "Floor-route conduits MUST be laid before tiles",
        "Conduits #1, #2, #3 all share the same floor chase from niche going East. "
        "The electrician digs ONE channel in the floor screed and lays 3 conduits side-by-side. "
        "But this MUST be done BEFORE the tile contractor arrives. Once tiles are down, no more "
        "floor conduits.")

    pdf.h2("Reolink doorbell mount detail")
    pdf.place_diagram(pdf.draw_reolink_layering, 70)

    pdf.h2("Reolink doorbell back box specs")
    pdf.table(
        headers=["Property", "Value"],
        rows=[
            ["Doorbell unit dimensions", "2\" wide x 5-1/8\" tall (50 x 130 mm)"],
            ["Bracket footprint", "~50 x 130 mm (matches doorbell)"],
            ["Back box (default - electrician's discretion)", "3\" x 3\" x 2-1/2\" GI MS modular (75 x 75 x 65 mm)"],
            ["Why smaller than 4x4", "Must be smaller than bracket - so box stays HIDDEN behind bracket after install"],
            ["Position centre (FFL)", "1450 mm (57\") - face level for adults"],
            ["Distance from each side of 1'6\" section", "9\" (228 mm) - centred"],
            ["Mounting", "Flush recessed from OUTSIDE face; rim flush with finished plaster"],
            ["Conduit entry", "Bottom or side, 25mm grey"],
            ["Weather protection", "Apply silicone sealant around conduit entry (modular box not natively IP-rated; porch is roofed)"],
        ],
        col_widths=[64, 116],
    )

    pdf.h2("Reolink installation procedure summary")
    pdf.body(
        "Phase 1 (BEFORE plaster): mark position, cut 3\" x 3\" cavity in outside wall, cut "
        "conduit chase through 9\" wall, install back box, fit cable, leave 300 mm tail, cap.\n\n"
        "Phase 2 (AFTER plaster): strip Cat6, crimp RJ45, test with cable tester, plug into "
        "Reolink, mount bracket over back box, clip doorbell on. Configure in Reolink app + HA.")

    pdf.callout("info", "What to buy + when",
        "Generic 3x3x2.5 GI MS back box (Rs.100, BEFORE plaster). Silicone sealant tube (Rs.100). "
        "Outdoor LSZH UV Cat6 (~Rs.280). Order Reolink Video Doorbell PoE NOW so you can verify "
        "the bracket fits over the back box before plaster covers everything. NO separate "
        "conduit for chime - HA plays chime through cavity speaker / Waveshare / any networked "
        "device. Optional Reolink wireless chime device (Rs.1500) plugs into any 5A socket.")

    pdf.h2("Pre-plaster sign-off for Zones E + F")
    pdf.checklist([
        "All 5 conduits routed from niche to their endpoints",
        "Floor segment of conduits #1, #2, #3 laid BEFORE tile contractor arrives - CRITICAL",
        "Reolink back box installed at 1450 mm FFL on outside of 1'6\" N wall section",
        "CAM-1 spare back box installed on porch W wall, 1650 mm FFL, capped",
        "CAM-2 stub back box installed on porch soffit NE corner, ~2700 mm FFL, capped",
        "Waveshare back box installed on staircase S wall, 1500 mm FFL",
        "Cat6 cables pulled (Reolink, foyer cavity, Waveshare) - outdoor LSZH UV Cat6 for outdoor runs",
        "Pull strings inserted in unused conduits (CAM-1 spare, CAM-2 stub)",
        "All conduit ends capped",
        "Homeowner sign-off photographed for all 5 conduit routes + endpoints",
    ])

    # ---------- SECTION 11: CONDUIT SCHEDULE ----------
    pdf.section_open("11", "Master Conduit Schedule",
                     "Every conduit in one place. Print this and tick off as you lay each one.")
    pdf.h2("Conduit colour code")
    pdf.table(
        headers=["Colour", "Used for", "Sizes"],
        rows=[
            ["RED PVC", "230V power", "25 mm (heavy) and 16 mm (light loads)"],
            ["GREY PVC", "Low voltage - Cat6, sensor wires, LED 24V secondary", "25 mm (Cat6) and 16 mm (sensor, LED)"],
            ["BLUE PVC", "Mains incomer + sockets/AC/heavy circuits", "25 mm"],
        ],
        col_widths=[28, 78, 74],
    )

    pdf.body(
        "If coloured PVC unavailable in Chitradurga, wrap each conduit end with coloured "
        "electrical tape AND label with permanent marker BEFORE plaster covers them.")

    pdf.h2("Master conduit table")
    pdf.table(
        headers=["#", "Conduit ID", "Size", "From", "To", "Length", "Cable inside"],
        rows=[
            ["1", "C-Main-Incomer", "25mm BLUE", "Utility meter", "DB", "~5m", "Mains per BESCOM"],
            ["2", "C-Earth", "16mm", "Earth pit", "DB earth bus", "~3m", "4 sqmm Green/Yellow"],
            ["3", "C-DB-Foyer-Switch", "25mm RED", "DB", "Foyer Switch Panel", "~6m", "3x 1.5 sqmm L+N+E"],
            ["4", "C-DB-Cavity-Power", "25mm RED", "DB", "Cavity bottom-LEFT", "~3m", "3x 2.5 sqmm L+N+E"],
            ["5", "C-Niche-Cavity-Data", "25mm GREY", "Niche", "Cavity bottom-RIGHT (via floor)", "~12m", "1x outdoor LSZH UV Cat6"],
            ["6", "C-Halo-24V", "16mm GREY", "Halo driver (above ceiling)", "Cavity TOP-CENTRE", "~2m", "2-core 0.75 sqmm 24V DC"],
            ["7", "C-Cavity-Ceil-Spkr (provision)", "16mm GREY", "Cavity TOP wall", "Above false ceiling", "~2m", "Pull string only"],
            ["8", "C-SW-Spots", "25mm RED", "Switch Panel", "2x spotlight boxes", "~5m", "3x 1.5 sqmm"],
            ["9", "C-SW-Cove-Halo", "25mm RED", "Switch Panel", "Cove + halo drivers", "~5m", "3x 1.5 sqmm"],
            ["10", "C-SW-Shelf", "16mm RED", "Switch Panel", "Shelf area", "~5m", "3x 1.5 sqmm"],
            ["11", "C-SW-Spare", "16mm RED", "Switch Panel", "Above ceiling (capped)", "~3m", "Pull string"],
            ["12", "C-SW-Porch-Ceiling", "16mm RED", "Switch Panel", "Porch ceiling", "~4m", "3x 1.5 sqmm"],
            ["13", "C-SW-Porch-Wall", "16mm RED", "Switch Panel", "Outside near door (capped)", "~4m", "Pull string"],
            ["14", "C-Cove-24V", "16mm GREY", "Cove driver", "Cove strip start", "~3m", "2-core 1.5 sqmm 24V DC"],
            ["15", "C-Shelf-24V", "16mm GREY", "Shelf driver", "Under-shelf strip", "~3m (Opt 1) or 0.3m (Opt 2)", "2-core 0.75 sqmm 24V DC"],
            ["16", "C-Niche-Doorbell", "25mm GREY", "Niche", "Reolink doorbell outside (via floor)", "~7m", "1x outdoor LSZH UV Cat6"],
            ["17", "C-Niche-CAM1", "25mm GREY", "Niche", "Porch W wall CAM-1 spare (via floor)", "~7m", "Pull string only"],
            ["18", "C-Niche-CAM2", "25mm GREY", "Niche", "Porch soffit CAM-2 stub (ceiling)", "~7m", "Pull string only"],
            ["19", "C-Niche-Waveshare", "25mm GREY", "Niche", "Staircase S wall Waveshare", "~2m", "1x outdoor LSZH UV Cat6"],
        ],
        col_widths=[7, 38, 18, 22, 42, 18, 35],
        body_size=7,
    )

    pdf.h2("Conduit purchasing totals")
    pdf.table(
        headers=["Conduit type", "Total length", "Buy a..."],
        rows=[
            ["25 mm RED PVC", "~17 m", "30 m roll"],
            ["16 mm RED PVC", "~26 m", "40 m roll"],
            ["25 mm GREY PVC (LV-25)", "~31 m", "40 m roll"],
            ["16 mm GREY PVC (LV-16)", "~10 m", "15 m roll"],
            ["25 mm BLUE PVC", "~5 m", "10 m roll"],
        ],
        col_widths=[60, 50, 70],
    )

    # ---------- SECTION 12: WIRE SCHEDULE ----------
    pdf.section_open("12", "Wire Schedule",
                     "What goes inside each conduit. Use this to plan wire purchasing.")
    pdf.h2("Wire colour code (Indian standard - mandatory)")
    pdf.table(
        headers=["Colour", "Function", "Where"],
        rows=[
            ["RED", "LIVE (phase, 230V)", "Every live wire from MCB outward"],
            ["BLUE", "Switched LIVE leg", "Between switch and the load"],
            ["BLACK", "NEUTRAL", "Every switch board, every socket"],
            ["GREEN with YELLOW stripe", "EARTH", "Every switch, socket, metal back box, metal fitting"],
        ],
        col_widths=[44, 56, 80],
    )

    pdf.h2("Power wires (230V)")
    pdf.table(
        headers=["For conduit", "Wire", "Colours", "Total length"],
        rows=[
            ["C-DB-Foyer-Switch", "1.5 sqmm", "Red + Black + Green/Yellow", "~18 m (3-core)"],
            ["C-DB-Cavity-Power", "2.5 sqmm", "Red + Black + Green/Yellow", "~9 m (3-core)"],
            ["C-SW-Spots", "1.5 sqmm", "Blue + Black + Green/Yellow", "~15 m"],
            ["C-SW-Cove-Halo", "1.5 sqmm", "Blue + Black + Green/Yellow", "~15 m"],
            ["C-SW-Shelf", "1.5 sqmm", "Blue + Black + Green/Yellow", "~15 m"],
            ["C-SW-Porch-Ceiling", "1.5 sqmm", "Blue + Black + Green/Yellow", "~12 m"],
            ["C-Earth", "4 sqmm", "Green/Yellow only", "~3 m"],
        ],
        col_widths=[44, 22, 62, 52],
    )

    pdf.h2("Low-voltage 24V DC wires")
    pdf.table(
        headers=["For conduit", "Wire", "Length"],
        rows=[
            ["C-Halo-24V", "2-core 0.75 sqmm 24V DC", "~2 m"],
            ["C-Cove-24V", "2-core 1.5 sqmm 24V DC", "~13 m (incl strip route)"],
            ["C-Shelf-24V", "2-core 0.75 sqmm 24V DC", "~3 m (Opt 1) or 0.3 m (Opt 2)"],
        ],
        col_widths=[44, 66, 70],
    )

    pdf.h2("Network cables (Cat6)")
    pdf.table(
        headers=["For conduit", "Wire", "Length"],
        rows=[
            ["C-Niche-Cavity-Data", "Outdoor LSZH UV Cat6", "~12 m"],
            ["C-Niche-Doorbell", "Outdoor LSZH UV Cat6", "~8 m"],
            ["C-Niche-Waveshare", "Outdoor LSZH UV Cat6", "~3 m"],
            ["Subtotal outdoor Cat6", "", "~23 m - BUY A 30 m ROLL"],
        ],
        col_widths=[44, 66, 70],
    )

    pdf.h2("Spare conduits (pull string only)")
    pdf.table(
        headers=["Conduit", "Pull string length"],
        rows=[
            ["C-SW-Spare-4", "3 m"],
            ["C-SW-Porch-Wall", "4 m"],
            ["C-Cavity-Ceiling-Speaker", "2 m"],
            ["C-Niche-CAM1", "7 m"],
            ["C-Niche-CAM2", "7 m"],
            ["Subtotal", "~23 m (buy a 100 m roll - cheap)"],
        ],
        col_widths=[80, 100],
    )

    pdf.h2("Cavity-internal wires (no conduit - all short)")
    pdf.table(
        headers=["Wire", "Purpose", "Length"],
        rows=[
            ["3.5 mm audio cable", "RPi USB sound card -> PAM8403 amp input", "30 cm"],
            ["USB-A to micro-USB", "RPi USB port -> PAM8403 power", "30 cm"],
            ["2-core 1 sqmm speaker wire", "Amp output -> Visaton FR 8 speaker", "30 cm"],
            ["CSI ribbon cable", "RPi CSI port -> Pi Camera Module 3 (bezel cam)", "25 cm (comes w/ cam)"],
            ["Mini-HDMI to HDMI", "RPi HDMI output -> monitor HDMI input", "30 cm"],
            ["USB-C cable", "PoE splitter 5V -> RPi power input", "20 cm"],
            ["RJ45 patch cable", "PoE splitter -> USB OTG Ethernet adapter", "20 cm"],
            ["Monitor power cord", "Cavity Socket A -> Samsung monitor adapter", "50 cm"],
        ],
        col_widths=[50, 80, 50],
    )

    # ---------- SECTION 13: MCB PLAN ----------
    pdf.section_open("13", "MCB Plan",
                     "2 dedicated MCBs for the foyer welcome system.")
    pdf.callout("info", "Electrician's verification",
        "MCB selection below is the homeowner's plan based on load calculations. The on-site "
        "electrician should verify these against their experience + IS 8623. The 2-MCB structure "
        "(Lights + Cavity) should remain regardless of brand or exact rating choice.")

    pdf.h2("2 MCBs for the foyer")
    pdf.table(
        headers=["MCB", "Type", "Rating", "Protects"],
        rows=[
            ["B-Foyer-Lights", "6A MCB (B-curve)", "6 A", "All foyer + porch lighting (spots, cove, halo, shelf, porch lights)"],
            ["B-Foyer-Cavity", "6A MCB + 30mA RCBO", "6 A + leakage", "Cavity sockets (Monitor + Spare) - electronics + leakage protection"],
        ],
        col_widths=[36, 38, 28, 78],
    )

    pdf.h2("B-Foyer-Lights detail")
    pdf.kv("MCB", "6 A B-curve (Schneider / ABB / Legrand)")
    pdf.kv("RCBO needed?", "NO (no wet / electronic loads on lighting)")
    pdf.kv("Loads", "2x GU10 spots (14W) + cove ~96W + halo ~10W + shelf ~11W + porch ceiling ~9W = ~140W total")
    pdf.kv("Current draw", "140W / 230V = ~0.6 A (well below 6A rating)")
    pdf.kv("Wire from MCB", "1.5 sqmm")
    pdf.kv("Via conduit", "C-DB-Foyer-Switch -> Foyer Switch Panel -> 4-7 branches")

    pdf.h2("B-Foyer-Cavity detail")
    pdf.kv("MCB", "6 A B-curve")
    pdf.kv("RCBO", "YES - 30 mA RCBO (mandatory for electronics)")
    pdf.kv("Loads", "Monitor ~25W + RPi via PoE (0W from this) + halo via shared driver + speaker amp ~1W + spare = ~36W typical")
    pdf.kv("Current draw", "~0.16 A typical")
    pdf.kv("Wire from MCB", "2.5 sqmm")
    pdf.kv("Via conduit", "C-DB-Cavity-Power -> directly to cavity socket box")

    pdf.h2("DB layout")
    pdf.place_diagram(pdf.draw_db_layout, 85, full_width=False, manual_x=50, manual_w=110)

    pdf.h2("Earth + safety")
    pdf.table(
        headers=["Item", "Spec"],
        rows=[
            ["Main earth pit", "Separate copper plate pit (not shared with motor pit)"],
            ["Earth wire pit -> DB", "4 sqmm Green/Yellow via C-Earth conduit"],
            ["Earth bonding", "All metal back boxes + plates + socket earth terminals -> DB earth busbar"],
            ["Continuity test", "< 1 ohm between any metal body and earth bus (verify with multimeter BEFORE plaster)"],
        ],
        col_widths=[56, 124],
    )

    # ---------- SECTION 14: SWITCH / SOCKET SCHEDULE ----------
    pdf.section_open("14", "Switch Board + Socket Schedule",
                     "Every back box, location, height. Total 10 boxes.")
    pdf.h2("Inside foyer")
    pdf.table(
        headers=["#", "Box", "Location", "Centre FFL", "Size", "Contents"],
        rows=[
            ["1", "Foyer Switch Panel", "N wall, 1'6\" section, centred", "1200 mm", "18M VERT 290x135x65 (cut on site)", "6 rockers + 6 Sonoff ZBMINI R2 hidden"],
        ],
        col_widths=[7, 36, 50, 22, 32, 33],
    )

    pdf.h2("Inside the cavity")
    pdf.table(
        headers=["#", "Box", "Location", "Centre FFL", "Size", "Contents"],
        rows=[
            ["2", "Cavity Socket Panel", "Cavity back wall, in 3x3 pocket", "53\" (1346 mm)", "75x75x65 modular", "2x 5A sockets (Monitor + Spare) + Sonoff hidden"],
        ],
        col_widths=[7, 36, 50, 22, 32, 33],
    )

    pdf.h2("On porch (outside, weather-exposed but roofed)")
    pdf.table(
        headers=["#", "Box", "Location", "Centre FFL", "Type", "Contents"],
        rows=[
            ["3", "Reolink doorbell back box", "Outside face of 1'6\" N wall, centred", "1450 mm", "3x3x2.5 GI MS modular", "Cat6 termination behind doorbell"],
            ["4", "CAM-1 spare back box", "Porch W wall", "1650 mm", "4x4 IP67 outdoor", "Empty - pull string only"],
            ["5", "CAM-2 stub back box", "Porch soffit NE corner", "~2700 mm", "4x4 IP67 outdoor", "Empty - pull string only"],
            ["6", "Porch ceiling light box", "Centre of porch ceiling", "~10 ft", "B-type ceiling rose", "LED fitting TBD"],
            ["7", "Porch wall light box", "Outside near door (future)", "1900-2100 mm", "Standard wall box", "Empty - pull string"],
        ],
        col_widths=[7, 36, 50, 22, 32, 33],
    )

    pdf.h2("Indoor staircase")
    pdf.table(
        headers=["#", "Box", "Location", "Centre FFL", "Size", "Contents"],
        rows=[
            ["8", "Waveshare back box", "Staircase S wall", "1500 mm", "TBD (custom)", "Cat6 termination for future Waveshare"],
        ],
        col_widths=[7, 36, 50, 22, 32, 33],
    )

    pdf.h2("Ceiling boxes (inside false ceiling)")
    pdf.table(
        headers=["#", "Box", "Position", "Type", "Contents"],
        rows=[
            ["9", "Spotlight #1", "609 mm from N edge, 300 mm from W area", "B-type, 60 mm depth", "GU10 gimbal fitting"],
            ["10", "Spotlight #2", "1218 mm from N edge, 300 mm from W area", "B-type, 60 mm depth", "GU10 gimbal fitting"],
        ],
        col_widths=[7, 30, 75, 32, 36],
    )

    pdf.h2("Total back boxes: 10")

    # ---------- SECTION 15: BOM ----------
    pdf.section_open("15", "Bill of Materials",
                     "Line-item shopping list. Prices approximate (Chitradurga / online, mid-2026).")
    pdf.h2("A. Conduits + accessories")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["25 mm RED PVC conduit (ISI)", "30 m roll", "Rs. 400"],
            ["16 mm RED PVC conduit", "40 m roll", "Rs. 350"],
            ["25 mm GREY PVC conduit (LV-25)", "40 m roll", "Rs. 450"],
            ["16 mm GREY PVC conduit (LV-16)", "15 m roll", "Rs. 150"],
            ["25 mm BLUE PVC conduit (mains)", "10 m", "Rs. 150"],
            ["Conduit bends 25mm + 16mm", "40 pieces", "Rs. 250"],
            ["Conduit couplers", "30 pieces", "Rs. 140"],
            ["Conduit clamps / saddles", "50 pieces", "Rs. 150"],
            ["Nylon pull string", "100 m roll", "Rs. 150"],
            ["Masking tape (for capping)", "2 rolls", "Rs. 80"],
            ["Subtotal A", "", "~Rs. 2,270"],
        ],
        col_widths=[90, 50, 40],
    )

    pdf.h2("B. Wires (foyer-scope allocation; coils shared with whole house)")
    pdf.table(
        headers=["Item", "Quantity", "Brand", "Cost"],
        rows=[
            ["1.5 sqmm Red (90m coil)", "1 coil", "Polycab / Havells", "Rs. 1,200"],
            ["1.5 sqmm Blue (switched live)", "1 coil", "Polycab / Havells", "Rs. 1,200"],
            ["1.5 sqmm Black", "1 coil", "Polycab / Havells", "Rs. 1,200"],
            ["1.5 sqmm Green/Yellow", "1 coil", "Polycab / Havells", "Rs. 1,200"],
            ["2.5 sqmm Red + Black + Green/Yellow", "shared", "Polycab", "Rs. 6,600"],
            ["4 sqmm Green/Yellow (main earth)", "5 m", "Polycab", "Rs. 400"],
            ["2-core 0.75 sqmm 24V LED", "10 m", "Local LED supply", "Rs. 300"],
            ["2-core 1.5 sqmm 24V (cove)", "15 m", "Local LED supply", "Rs. 450"],
            ["Outdoor LSZH UV Cat6", "30 m", "D-Link / Commscope", "Rs. 1,200"],
            ["Indoor Cat6 patch", "2 m", "Any", "Rs. 50"],
            ["Subtotal B", "", "", "~Rs. 13,800"],
        ],
        col_widths=[70, 30, 42, 38],
    )

    pdf.h2("C. Back boxes + plates")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["6-gang GI MS modular back box (default)", "1", "Rs. 250"],
            ["2-module modular back box (cavity socket)", "1", "Rs. 120"],
            ["3x3 GI MS modular box (Reolink default)", "1", "Rs. 100"],
            ["4x4 IP67 outdoor box (CAM-1 + CAM-2)", "2", "Rs. 600"],
            ["B-type ceiling rose box", "3", "Rs. 150"],
            ["Standard wall box (porch wall future)", "1", "Rs. 80"],
            ["Waveshare back box (custom)", "1", "Rs. 200"],
            ["Schneider Unica 18M White plate + frame", "1", "Rs. 650"],
            ["2-module plate", "1", "Rs. 150"],
            ["5A sockets", "2", "Rs. 200"],
            ["Cover plates / blanks", "4", "Rs. 100"],
            ["Subtotal C", "", "~Rs. 2,550 - 5,050"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("D. MCBs + DB hardware")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["6A B-curve MCB", "2", "Rs. 500"],
            ["30 mA RCBO", "1", "Rs. 2,000"],
            ["100 mA S-type RCCB", "1 (shared)", "Rs. 2,500"],
            ["DB enclosure (Schneider Acti9 48-way)", "1", "Already planned"],
            ["Copper earth busbar", "1", "Already planned"],
            ["MCB labels", "1 set", "Rs. 150"],
            ["Subtotal D", "", "~Rs. 5,150"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("E. Smart hardware")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Sonoff ZBMINI R2 x 6 (hidden behind 6 rockers in 18M plate)", "6", "Rs. 4,200"],
            ["Sonoff Mini R2 (cavity socket)", "1", "Rs. 800"],
            ["RJ45 connectors (Cat6)", "20 pieces", "Rs. 100"],
            ["Cat6 cable tester", "1", "Rs. 500"],
            ["Crimping tool (RJ45)", "1", "Rs. 400"],
            ["Subtotal E", "", "~Rs. 3,300"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("F. Welcome screen + cavity components")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Samsung LS22F350 monitor (21.5\" IPS, VESA 75)", "1", "Rs. 9,000"],
            ["VESA 75 slim wall bracket", "1", "Rs. 500"],
            ["Raspberry Pi Zero 2W", "1", "Rs. 2,500"],
            ["Raspberry Pi Camera Module 3 (CAM-0)", "1", "Rs. 2,500"],
            ["PoE splitter (5V USB-C output)", "1", "Rs. 1,000"],
            ["USB OTG Ethernet adapter", "1", "Rs. 400"],
            ["USB sound card (dongle)", "1", "Rs. 400"],
            ["PAM8403 amplifier module", "1", "Rs. 150"],
            ["Mini-HDMI to HDMI cable (30 cm)", "1", "Rs. 200"],
            ["3.5 mm audio cable (30 cm)", "1", "Rs. 100"],
            ["3M VHB tape + Velcro + silicone + cable ties", "various", "Rs. 600"],
            ["Subtotal F", "", "~Rs. 17,350"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("G. Audio")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Visaton FR 8 speaker driver (80 mm)", "1", "Rs. 1,800"],
            ["MDF baffle (3.5\" x 3.5\" x 1/4\")", "1", "Rs. 50"],
            ["2-core speaker wire", "1 m", "Rs. 50"],
            ["Subtotal G", "", "~Rs. 1,900"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("H. Lighting")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["GU10 LED bulb (7W, 2700K, dimmable)", "2", "Rs. 1,000"],
            ["GU10 gimbal fitting", "2", "Rs. 2,000"],
            ["24V LED strip 2200K (5m roll - halo)", "1 roll", "Rs. 1,000"],
            ["24V LED strip 2700K (5m roll - shelf)", "1 roll", "Rs. 800"],
            ["24V LED strip 2700K (10m roll - cove)", "1 roll", "Rs. 1,500"],
            ["Mean Well APV-12-24 driver (halo + shelf)", "2", "Rs. 1,200"],
            ["Mean Well APV-100-24 driver (cove)", "1", "Rs. 1,500"],
            ["LED strip connectors + clips", "1 set", "Rs. 200"],
            ["Subtotal H", "", "~Rs. 9,200"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("I. Cameras + doorbell")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Reolink Video Doorbell PoE (TC541)", "1", "Rs. 8,000"],
            ["Reolink wireless chime (OPTIONAL hardware backup)", "0 or 1", "Rs. 1,500"],
            ["(Future) CAM-1 PoE camera", "0 - provision only", "Future Rs. 15,000"],
            ["(Future) CAM-2 overview camera", "0 - provision only", "Future Rs. 12,000"],
            ["Subtotal I (now)", "", "~Rs. 8,000"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("J. False ceiling + carpentry")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Inspection hatch (300x300 mm)", "1", "Rs. 500"],
            ["Walnut floating shelf (6 ft x 10\" x 1.25\")", "1", "Rs. 4,500"],
            ["Hidden steel L-brackets for shelf", "4", "Rs. 400"],
            ["Cupboard plywood facade", "1", "Rs. 3,000"],
            ["Cabinet hinges + lock", "per design", "Rs. 500"],
            ["Gypsum board + GI grid", "per spec", "Included in FC contractor"],
            ["Subtotal J", "", "~Rs. 8,900"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("K. Stone cladding")
    pdf.table(
        headers=["Item", "Quantity", "Cost"],
        rows=[
            ["Rustic ledgestone slips", "~6 sqm", "Rs. 15,000"],
            ["Extra stone slips for cavity reveal", "~0.5 sqm", "Rs. 1,250"],
            ["MS polymer adhesive (high-bond)", "5 kg", "Rs. 1,500"],
            ["Mechanical anchor clips", "per spec", "Rs. 500"],
            ["Subtotal K", "", "~Rs. 18,250"],
        ],
        col_widths=[90, 40, 50],
    )

    pdf.h2("L. Labour (foyer welcome scope only)")
    pdf.table(
        headers=["Trade", "Hours", "Cost"],
        rows=[
            ["Electrician (cuts cavity + DB + conduits + wiring + termination)", "40 hr", "Rs. 8,000"],
            ["Painter (cavity matte black + side walls)", "8 hr", "Rs. 2,000"],
            ["Stone cladder", "12 hr", "Rs. 4,800"],
            ["Carpenter (shelf + cupboard facade + baffle)", "6 hr", "Rs. 1,800"],
            ["False-ceiling contractor", "per spec", "Rs. 6,000"],
            ["Smart-home installer (Phase 11 commissioning)", "8 hr", "Rs. 4,000"],
            ["Subtotal L", "", "~Rs. 26,600"],
        ],
        col_widths=[100, 30, 50],
    )

    pdf.h2("Grand total estimate")
    pdf.callout("good", "Foyer welcome system - all-inclusive",
        "Conduits Rs.2,270 + Wires Rs.2,760 (allocation) + Boxes Rs.2,550 + MCBs Rs.5,150 + "
        "Smart Rs.3,300 + Screen Rs.17,350 + Audio Rs.1,900 + Lighting Rs.9,200 + Doorbell "
        "Rs.8,000 + FC + Carpentry Rs.8,900 + Stone Rs.18,250 + Labour Rs.26,600 = "
        "approx Rs. 1,06,230. Excludes smart lock, dining hall speaker, Waveshare hardware "
        "(flagged in Section 18 for separate sessions).")

    # ---------- SECTION 16: BUILD ORDER ----------
    pdf.section_open("16", "Phase-by-Phase Build Order",
                     "11 phases. Each has owner, duration, deliverable, and sign-off.")
    pdf.h2("Timeline")
    pdf.table(
        headers=["Date", "Phase", "Owner", "Status"],
        rows=[
            ["2026-05-23", "Phase 1: Marking + sign-off", "Electrician + Carpenter + Homeowner", "Imminent"],
            ["2026-05-23 to 24", "Phase 2: Wall chasing + cavity cutting", "Electrician", ""],
            ["2026-05-25 to 26", "Phase 3: Conduit pulling", "Electrician", ""],
            ["2026-05-27 to 28", "Phase 4: Wire pulling + DB install", "Electrician", ""],
            ["2026-05-29 to 31", "Phase 5: First plaster rough coat", "Mason", ""],
            ["2026-06-01", "Phase 6: Cavity matte black", "Painter", ""],
            ["2026-06-01", "Phase 7: VESA backing + carpenter prep", "Carpenter", ""],
            ["2026-06-02 to 05", "Phase 8: Stone cladding incl. reveal wrap", "Stone cladder", ""],
            ["2026-06-06 to 09", "Phase 9: False ceiling + cove + drivers", "FC contractor + Electrician", ""],
            ["2026-06-10 to 12", "Phase 10: Final paint", "Painter", ""],
            ["2026-06-13 to 15", "Phase 11: Smart-home commissioning", "Electrician + Smart-home installer", ""],
            ["2026-06-15", "Welcome system live + tested", "TARGET", ""],
        ],
        col_widths=[28, 78, 56, 18],
    )

    pdf.h2("Phase 1 - Marking (Day 1)")
    pdf.body(
        "Owner: Electrician + Carpenter + Homeowner. Duration: 1 day. "
        "On bare brick / block walls, chalk-mark every: cavity outline, DB recess, switch box "
        "positions, socket box positions, conduit chase lines, spotlight ceiling positions on "
        "slab, Reolink doorbell position on outside face, CAM-1 spare + CAM-2 stub + Waveshare "
        "back box positions. Take photos of every mark. Homeowner signs off BEFORE any cutting.")

    pdf.h2("Phase 2 - Chasing + cavity cutting (Day 2-3)")
    pdf.body(
        "Owner: Electrician. Tools: angle grinder, chisel + hammer, core drill, wall chaser. "
        "Cut main cavity (22-3/4 x 14-7/8 x 4\"); socket pocket (3x3x2.5\"); speaker pocket "
        "(3\" dia x 1\"); DB recess (15-3/4 x 23-5/8 x 4\"); 6-gang switch panel pocket "
        "(335x75x65); all other back box pockets; Reolink doorbell pocket on porch wall; all "
        "conduit chases vertical + horizontal.")

    pdf.h2("Phase 3 - Conduit pulling (Day 4-5)")
    pdf.body(
        "Lay all 19 main conduits per Section 11 schedule. Use coloured PVC where available, "
        "otherwise label with tape + permanent marker. Insert pull strings in every conduit. "
        "Cap all ends with masking tape. FLOOR-ROUTE CONDUITS (#1, #2, #3) MUST be laid in "
        "floor screed BEFORE tile contractor arrives.")

    pdf.h2("Phase 4 - Wire pulling + DB install (Day 6-7)")
    pdf.body(
        "Pull wires through conduits per Section 12. Every smart-switch box gets L+N+E. Mount "
        "Schneider Acti9 48-way DB. Connect MCBs + RCBOs per Section 13. Leave 300 mm tail of "
        "wires inside every switch box. Test earth continuity (< 1 ohm). Pull outdoor Cat6 "
        "through niche-to-cavity, niche-to-Reolink, niche-to-Waveshare.")

    pdf.h2("Phases 5-11 (after plaster)")
    pdf.table(
        headers=["Phase", "What happens"],
        rows=[
            ["5 - Plaster", "Apply rough coat. Conduits + back boxes flush with finished plaster line. Cure 48 hours."],
            ["6 - Matte black", "Paint cavity interior matte black (back wall + deeper 70mm of inner walls). NOT front 30mm."],
            ["7 - VESA backing", "Drill VESA pattern into masonry OR install small ply backing. Cut MDF speaker baffle."],
            ["8 - Stone cladding", "Clad 6 ft x 11 ft S feature wall + WRAP stone slips into cavity reveal (front 30mm, 4 sides)."],
            ["9 - False ceiling", "Drop ceiling to 9 ft. Build cove pocket. Install inspection hatch. Mount spotlights. Install drivers."],
            ["10 - Final paint", "N wall + side walls in warm ivory. Ceiling + cove inside in soft snow. Mask stone wall + boxes."],
            ["11 - Commissioning", "Install switches + sockets + plates + Sonoffs. Mount monitor + RPi + CAM-0 + speaker. Configure Frigate + CompreFace + HA. Train 3 family faces. Test welcome flow."],
        ],
        col_widths=[30, 150],
    )

    # ---------- SECTION 17: SIGN-OFF CHECKLIST ----------
    pdf.section_open("17", "Pre-Plaster Sign-Off Checklist",
                     "The MASTER CHECKLIST. Tick each item on-site BEFORE plaster crew arrives. Print + sign.")
    pdf.callout("warn", "Read this first",
        "Once plaster goes on the walls, NOTHING about the welcome system can be changed. "
        "This checklist is the FINAL gate. Print these pages, walk the site item by item, "
        "tick each box, and sign at the end. The plaster crew does NOT start until "
        "the homeowner has signed.")

    pdf.h2("General (before any zone sign-off)")
    pdf.checklist([
        "FFL chalk line drawn on every wall (so heights can be verified from real floor level)",
        "All conduit labels readable (tape + marker on every conduit end)",
        "All pull strings inserted in spare / empty conduits",
        "All conduit ends capped with masking tape",
        "All back boxes set with rims slightly recessed (so plaster goes around rim, not on top)",
    ])

    pdf.h2("Zone A - East wall (DB + starter cupboard)")
    pdf.checklist([
        "DB recess cut: 400 x 600 x 100 mm, flush, bottom 1500 mm FFL",
        "Starter cupboard mount position marked (Option 1 or 2 chosen on-site)",
        "Homeowner signed off on layout choice",
        "All 5 outgoing DB conduits routed and labelled",
        "All 5 incoming water-auto conduits terminated at cupboard back panel",
        "Draw strings in every conduit; ends capped",
        "DB shell mounting bracket / rawl plugs ready",
        "Earth wire (4 sqmm) routed from earth pit to DB",
    ])

    pdf.h2("Zone B - South feature wall (Screen Cavity)")
    pdf.checklist([
        "Cavity cut to 22-3/4\" x 14-7/8\" x 4\" (580 x 380 x 100 mm)",
        "Cavity centred on 6 ft feature wall (ON ACTUAL MEASURED WIDTH)",
        "Bottom edge at 50-1/2\" (1280 mm) FFL",
        "Socket pocket cut: 3\" x 3\" x 2-1/2\" deep, centred horiz, centre at 53\" FFL",
        "Speaker pocket cut: 3\" diameter x 1\" deep, centred horiz, centre at 57-1/8\" FFL",
        "Conduit #1 (Power) hole: 1\" diameter, bottom-LEFT, 1.5\" up + 2\" in",
        "Conduit #2 (Data) hole: 1\" diameter, bottom-RIGHT, 1.5\" up + 2\" in",
        "Conduit #3 (Halo) hole: 5/8\" diameter, top-CENTRE, 3/4\" down",
        "Conduit #4 (Ceiling speaker provision) exit through TOP inner wall going up",
        "All 4 cavity conduit stubs protrude 1-1.5\" into cavity, capped",
        "Stone cladder briefed on 30 mm reveal depth",
        "Painter briefed: do NOT paint front 30 mm of inner walls",
        "Cavity dimensions photographed",
        "Walnut shelf bracket positions chalked at 900 mm FFL on S wall",
    ])

    pdf.h2("Zone C - North wall (Switch Panel + door + window)")
    pdf.checklist([
        "N wall total length verified (~9'6\" / 2895 mm)",
        "Door opening cut to 3'2\" wide x 7 ft tall",
        "Window opening cut to 3'6\" wide x 5 ft tall (corner wrap)",
        "Vascal wall section confirmed (~1'4\" East of door)",
        "1'6\" wall section between door and window confirmed",
        "Foyer Switch Panel back box: 6-gang (or 7/8 if it fits), 335 x 75 x 65 mm, centred horiz, centre 1200 mm FFL",
        "C-DB-Foyer-Switch conduit terminated at back box",
        "All outgoing conduits from switch panel routed (4 mandatory + 2 porch + spare slots)",
        "Draw strings in all conduits",
        "Reolink doorbell back box installed on OUTSIDE face of 1'6\" section, 1450 mm FFL",
        "Cat6 pulled through C-Niche-Doorbell, 300 mm tail in box, capped",
    ])

    pdf.h2("Zone D - Foyer ceiling")
    pdf.checklist([
        "False ceiling drop confirmed at 2 ft (from 11 ft to 9 ft FFL)",
        "Cove pocket dimensions: 100 mm wide x 75 mm deep, around full perimeter",
        "Inspection hatch position marked (300 x 300 mm, W edge)",
        "2x GU10 ceiling box positions chalked on raw slab (609 + 1218 mm from N edge)",
        "All conduits arriving at false ceiling terminated and labelled",
        "Driver shelf location marked above inspection hatch",
    ])

    pdf.h2("Zone E - Porch (external)")
    pdf.checklist([
        "All 3 porch conduits routed from niche (Reolink, CAM-1, CAM-2)",
        "FLOOR SEGMENT of all 3 floor-route conduits laid BEFORE tile contractor arrives [CRITICAL]",
        "Reolink back box (outside 1'6\" N wall, 1450 mm FFL)",
        "CAM-1 spare back box (porch W wall, 1650 mm FFL) - capped",
        "CAM-2 stub back box (porch soffit NE corner, ~2700 mm FFL) - capped",
        "Pull strings in unused conduits (CAM-1, CAM-2)",
        "Cat6 pulled in C-Niche-Doorbell (300 mm tail in back box)",
        "All conduit ends capped",
    ])

    pdf.h2("Zone F - Staircase indoor")
    pdf.checklist([
        "Waveshare back box installed at 1500 mm FFL on staircase S wall",
        "C-Niche-Waveshare conduit terminated at box",
        "Cat6 pulled through, 300 mm tail in box, capped",
    ])

    pdf.h2("Photographs to take BEFORE plaster (minimum 25 photos)")
    pdf.body(
        "Store all photos in 'Inconstruction images/foyer-preplaster/' folder for permanent reference. "
        "At minimum: East wall DB area (3 angles); cavity front view + close-up of each conduit "
        "hole + close-up of sub-pockets; N wall elevation + switch panel; Reolink position outside; "
        "CAM-1 + CAM-2 + Waveshare back boxes; ALL 3 floor-route conduits before tile; false ceiling "
        "conduit ends.")

    pdf.h2("HOMEOWNER SIGN-OFF FORM")
    pdf.set_font("Verdana", "", 10)
    pdf.set_text_color(*INK)
    pdf.body("Date of sign-off: _________________________")
    pdf.body("\nI have verified the following:")
    pdf.checklist([
        "All zones above are checked off",
        "All photographs have been taken",
        "All conduit labels match the Section 11 master schedule",
        "All conduit ends are capped with masking tape",
        "All draw strings are in place",
        "FFL chalk line is visible on every wall",
        "DB + starter cupboard layout choice (Option 1 / Option 2) is decided",
        "Walnut shelf LED driver location choice is decided OR deferred to electrician's discretion",
        "6-gang vs 7-gang vs 8-gang switch panel choice is decided on-site",
        "Reolink back box choice is finalised (or delegated to electrician)",
    ])
    pdf.ln(4)
    pdf.set_font("Verdana", "B", 11)
    pdf.set_text_color(*ACCENT_DK)
    pdf.body("[X] I AUTHORISE the plaster crew to begin Phase 5.")
    pdf.ln(2)
    pdf.set_font("Verdana", "", 10)
    pdf.set_text_color(*INK)
    pdf.body("\n\nHomeowner signature: ____________________________________\n\n")
    pdf.body("Electrician acknowledgement: ____________________________\n\n")
    pdf.body("Date: ______________________________")

    # ---------- SECTION 18: OPEN ITEMS ----------
    pdf.section_open("18", "Flagged Open Items",
                     "Items NOT covered in this plan. Some may need conduit provisioning later; others can be designed in separate sessions.")
    pdf.table(
        headers=["#", "Item", "Status", "Cost when added"],
        rows=[
            ["1", "Smart door lock for 'tap to unlock'", "Battery deadbolt = no conduit needed now. Wired strike/maglock = conduit needed pre-plaster.", "Rs. 12,000-15,000"],
            ["2", "Dining hall speaker provision", "Decide in next 1-2 days if you want this (before dining hall plaster)", "Rs. 3,000-5,000"],
            ["3", "Waveshare indoor unit full hardware + dashboard", "Conduit + Cat6 ALREADY provisioned in this plan. Hardware design = separate session.", "Rs. 24,000"],
            ["4", "Door grill on East jamb (outside)", "Decorative only - decide in finishing phase", "varies"],
            ["5", "Switch plate brand", "Schneider Unica White house-wide (locked 2026-05-23, Aqara H1 dropped)", "Rs. 650 (foyer 18M)"],
            ["6", "Walnut shelf LED driver location", "Option 1 (above ceiling) vs Option 2 (under shelf) - electrician decides on-site", "no cost diff"],
            ["7", "Reolink back box exact spec", "Electrician's discretion (default 3x3 GI MS modular)", "Rs. 100-300"],
            ["8", "DB + starter cupboard final layout", "Arrangement Option 1 vs 2 - on-site decision", "no cost diff"],
        ],
        col_widths=[7, 65, 80, 28],
    )

    pdf.h2("Cross-references")
    pdf.table(
        headers=["Document", "What it covers"],
        rows=[
            ["conduits-and-cavities.md", "General conduit rules + whole-house conduit schedule"],
            ["water-automation-conduits.md", "Water automation system (5 conduits terminate in foyer DB cupboard)"],
            ["db-layout.md", "DB internal circuit layout (whole house)"],
            ["ground-floor-electrical.md", "All other GF electrical items"],
            ["materials-checklist.md", "Broader house materials list"],
            ["decisions/decision-log.md", "Locked design decisions across the project"],
        ],
        col_widths=[60, 120],
    )

    # ---------- BACK COVER ----------
    pdf.add_page()
    pdf.suppress_chrome = True
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_xy(15, 8)
    pdf.set_font("Georgia", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "End of Document")
    pdf.set_xy(15, 18)
    pdf.set_font("Verdana", "I", 10)
    pdf.cell(0, 5, "Foyer Electrician Master Plan  v1.1")

    pdf.ln(20)
    pdf.set_text_color(*INK)
    pdf.set_font("Georgia", "B", 14)
    pdf.set_xy(15, 50)
    pdf.cell(180, 8, "What to do RIGHT NOW (Phase 1 is imminent)")
    pdf.ln(10)
    pdf.set_x(15)
    pdf.set_font("Verdana", "", 10)
    items = [
        "1. PRINT Section 17 (sign-off checklist). Take it to site tomorrow morning.",
        "2. PRINT Section 11 (conduit schedule). Give to electrician for reference during install.",
        "3. PRINT Section 16 (build order). Share with all trades.",
        "4. ORDER NOW: Reolink Video Doorbell PoE (3 day shipping; want it on-site by Phase 11).",
        "5. ORDER NOW: Halo LED strip (24V 2200K 5m roll) - less common locally, order online.",
        "6. ORDER NOW: Visaton FR 8 speaker driver.",
        "7. BUY LOCALLY: All conduits + wires + back boxes + MCBs from Chitradurga electrical store.",
        "8. CALL: schedule electrician for Phase 1 (marking) and Phase 2 (cutting).",
        "9. ARRANGE: tile contractor timing - floor-route conduits MUST be laid BEFORE tiles.",
        "10. PHOTOGRAPH: take 'before' photos of every wall before any cutting starts.",
    ]
    for it in items:
        pdf.set_x(15)
        pdf.multi_cell(180, 5.5, clean(it))
        pdf.ln(1)

    pdf.ln(8)
    pdf.set_font("Georgia", "I", 11)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_x(15)
    pdf.multi_cell(180, 6, clean(
        "Document version 1.1  -  2026-05-22  -  Ganesh Prasad, Chitradurga\n\n"
        "If something on-site doesn't match a section, STOP and call the homeowner "
        "before proceeding."))

    pdf.set_auto_page_break(False)
    pdf.set_y(275)
    pdf.set_font("Verdana", "I", 7)
    pdf.set_text_color(*INK_MUTED)
    pdf.cell(0, 3, clean("Generated 2026-05-22 from electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md"), align="C")
    pdf.set_auto_page_break(True, 18)

    # ---------- OUTPUT ----------
    pdf.output(str(OUT))
    print(f"PDF written to: {OUT}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
