"""
⚠️ DEPRECATED 2026-05-22 ⚠️

This script generated FOYER_WELCOME_PLAN.pdf (v2, 2026-05-10), which has been
SUPERSEDED by the new master electrician plan.

USE INSTEAD:
  - Script:  pdfs/build_foyer_electrician_pdf.py
  - Output:  pdfs/FOYER_ELECTRICIAN_MASTER_PLAN.pdf
  - Source:  electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md

The old PDF has been renamed to FOYER_WELCOME_PLAN_v2_superseded.pdf and is kept
for historical reference only. Do not hand it to the electrician.

This script is preserved for reference (it contains good diagram helpers + the
original v2 content). Do not delete unless you've ported any unique content into
build_foyer_electrician_pdf.py.

------------------------------------------------------------------------------
Original docstring (v2, 2026-05-10):

Build the FOYER WELCOME PLAN PDF (visual redesign v2).

Polished, magazine-style layout for site teams:
  - Verdana TTF (clean, readable at small sizes)
  - Real drawn diagrams (no ASCII art)
  - Stripped markdown ticks, em dashes normalised
  - Section sidebars, numbered chips, breathing whitespace
  - Stone / cove / cavity diagrams drawn with primitives

Audience: electrician, mason, painter, stone cladder, carpenter,
smart-home installer, homeowner.
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUT = Path(__file__).parent / "FOYER_WELCOME_PLAN.pdf"

# ---------- Brand palette ----------
INK        = (38, 30, 22)
INK_SOFT   = (90, 78, 64)
INK_MUTED  = (130, 118, 102)
PAPER      = (252, 248, 240)
ACCENT     = (170, 110, 50)        # warm amber accent
ACCENT_DK  = (120, 75, 30)
ACCENT_LT  = (245, 232, 210)
HAIRLINE   = (210, 195, 170)
RULE       = (180, 155, 110)
TABLE_HEAD = (50, 35, 20)
TABLE_ALT  = (250, 244, 232)
WARN_BG    = (255, 234, 222)
WARN_BD    = (200, 100, 60)
WARN_INK   = (130, 50, 20)
INFO_BG    = (228, 238, 246)
INFO_BD    = (90, 130, 170)
INFO_INK   = (40, 70, 110)
GOOD_BG    = (228, 240, 226)
GOOD_INK   = (60, 100, 60)
STONE_TONE = (123, 92, 66)
STONE_LT   = (200, 181, 143)
STONE_DK   = (58, 54, 51)
WALNUT     = (74, 53, 38)
HALO_AMBER = (255, 184, 119)
COVE_WARM  = (255, 228, 184)
IVORY      = (242, 235, 221)
SOFT_SNOW  = (248, 244, 236)
BLACK      = (15, 14, 13)


def clean(s):
    """Strip markdown ticks / unicode dashes that don't render natively."""
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
        .replace(" ", " ")
        .replace("×", "x")
        .replace("°", " deg")
        .replace("±", "+/-")
        .replace("²", "2")
        .replace("³", "3")
    )


# ---------- PDF class ----------
class FoyerPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 22, 18)
        # Embed Verdana TTFs (clean, screen-tested for tiny type)
        font_dir = Path("/System/Library/Fonts/Supplemental")
        self.add_font("Verdana", "",  str(font_dir / "Verdana.ttf"))
        self.add_font("Verdana", "B", str(font_dir / "Verdana Bold.ttf"))
        self.add_font("Verdana", "I", str(font_dir / "Verdana Italic.ttf"))
        self.add_font("Verdana", "BI", str(font_dir / "Verdana Bold Italic.ttf"))
        self.add_font("Georgia", "",  str(font_dir / "Georgia.ttf"))
        self.add_font("Georgia", "B", str(font_dir / "Georgia Bold.ttf"))
        self.add_font("Georgia", "I", str(font_dir / "Georgia Italic.ttf"))

        self.section_label = "Foyer Welcome Plan"
        self.section_number = ""
        self.suppress_chrome = False

    # ---- chrome (header / footer) ----
    def header(self):
        if self.page_no() == 1 or self.suppress_chrome:
            return
        # top thin amber rule
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(18, 12, 192, 12)
        # left: section number chip + title
        if self.section_number:
            self.set_fill_color(*ACCENT)
            self.set_draw_color(*ACCENT)
            self.rect(18, 14, 8, 5, "F")
            self.set_xy(18, 14)
            self.set_font("Verdana", "B", 7)
            self.set_text_color(255, 255, 255)
            self.cell(8, 5, self.section_number, align="C")
        self.set_xy(28, 14)
        self.set_font("Verdana", "", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(0, 5, clean(self.section_label))
        # right: page no
        self.set_xy(150, 14)
        self.set_font("Verdana", "B", 8)
        self.set_text_color(*INK)
        self.cell(42, 5, f"Page {self.page_no()}", align="R")

    def footer(self):
        if self.page_no() == 1 or self.suppress_chrome:
            return
        self.set_y(-14)
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(18, self.get_y(), 192, self.get_y())
        self.set_y(-11)
        self.set_font("Verdana", "I", 7.5)
        self.set_text_color(*INK_MUTED)
        self.cell(0, 5, clean("Foyer Welcome Plan  v2.0  -  2026-05-10  -  Ganesh Prasad, Chitradurga"),
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---- typography ----
    def section_open(self, number, title, subtitle=None):
        """Start a new section: page break + big title block + sets header crumb."""
        self.section_number = number
        self.section_label = f"Section {number} - {title}"
        self.add_page()
        self.set_y(28)
        # Big number on the left
        self.set_text_color(*ACCENT)
        self.set_font("Georgia", "B", 64)
        self.set_xy(18, 24)
        self.cell(28, 28, number, align="L")
        # Title to the right of the number
        self.set_xy(48, 30)
        self.set_text_color(*INK)
        self.set_font("Georgia", "B", 22)
        self.cell(0, 10, clean(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if subtitle:
            self.set_x(48)
            self.set_text_color(*INK_SOFT)
            self.set_font("Verdana", "I", 11)
            self.multi_cell(140, 5.5, clean(subtitle))
        self.ln(2)
        # amber separator under the title block
        y = max(self.get_y() + 3, 56)
        self.set_draw_color(*RULE)
        self.set_line_width(0.5)
        self.line(18, y, 192, y)
        self.set_y(y + 6)
        self.set_text_color(*INK)

    def h2(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(3)
        self.set_font("Georgia", "B", 14)
        self.set_text_color(*INK)
        self.cell(0, 7.5, clean(text),
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.7)
        y = self.get_y()
        self.line(18, y, 38, y)
        self.set_line_width(0.2)
        self.set_draw_color(*HAIRLINE)
        self.line(38, y, 192, y)
        self.ln(3)

    def h3(self, text):
        self.ln(1)
        self.set_font("Verdana", "B", 10.5)
        self.set_text_color(*ACCENT_DK)
        self.cell(0, 6, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*INK)
        self.ln(0.5)

    def body(self, text, size=10):
        self.set_font("Verdana", "", size)
        self.set_text_color(*INK)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.2, clean(text))
        self.ln(1.5)

    def lede(self, text):
        """Pull-quote / opening paragraph style."""
        self.ln(1)
        self.set_font("Georgia", "I", 12)
        self.set_text_color(*INK_SOFT)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, clean(text))
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
        self.cell(5, 5.2, "-")
        self.set_font("Verdana", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(0, 5.2, clean(text))
        self.ln(0.2)

    def checklist(self, items):
        for it in items:
            if self.get_y() > 270:
                self.add_page()
            self.set_x(self.l_margin)
            # Box
            x, y = self.get_x(), self.get_y()
            self.set_draw_color(*ACCENT)
            self.set_line_width(0.4)
            self.rect(x + 0.3, y + 1.0, 3.6, 3.6)
            self.set_xy(x + 6, y)
            self.set_font("Verdana", "", 9.5)
            self.set_text_color(*INK)
            self.multi_cell(0, 5.2, clean(it))
            self.ln(0.6)

    def callout(self, kind, title, text):
        """kind: 'warn', 'info', 'good'. Renders a rounded panel."""
        if kind == "warn":
            bg, bd, ink, label = WARN_BG, WARN_BD, WARN_INK, "CRITICAL"
        elif kind == "info":
            bg, bd, ink, label = INFO_BG, INFO_BD, INFO_INK, "NOTE"
        else:
            bg, bd, ink, label = GOOD_BG, (90, 130, 80), GOOD_INK, "TIP"

        # Pre-measure text height
        self.set_font("Verdana", "", 9.5)
        # Approximate height
        approx_h = 14 + 5.2 * max(2, len(text) // 80 + 1)
        if self.get_y() + approx_h > 273:
            self.add_page()

        x = self.l_margin
        y = self.get_y() + 1
        w = self.w - self.l_margin - self.r_margin

        # Compute body height by writing once into a temp position
        self.set_xy(x + 6, y + 8)
        before = self.get_y()
        self.set_font("Verdana", "", 9.5)
        self.set_text_color(*ink)
        self.multi_cell(w - 12, 5.2, clean(text))
        end = self.get_y()
        text_h = end - before
        total_h = 8 + text_h + 4

        # Now overdraw the panel and re-render text on top
        self.set_fill_color(*bg)
        self.set_draw_color(*bd)
        self.set_line_width(0.4)
        self.rect(x, y, w, total_h, "DF")
        # Left band
        self.set_fill_color(*bd)
        self.rect(x, y, 1.6, total_h, "F")
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
        self.set_font("Verdana", "", 9.5)
        self.set_text_color(*ink)
        self.multi_cell(w - 10, 5.2, clean(text))
        self.set_y(y + total_h + 2)
        self.set_text_color(*INK)

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

    def table(self, headers, rows, col_widths, header_size=8.5, body_size=8.5,
              row_padding=1.4, header_fill=None, zebra=True):
        if header_fill is None:
            header_fill = TABLE_HEAD
        # Header
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
        line_h = 4.2 + row_padding
        zebra_state = False
        for row in rows:
            cells = [self._safe_break(c, col_widths[i]) for i, c in enumerate(row)]
            # measure lines
            lines_needed = []
            for cell, w in zip(cells, col_widths):
                if not cell:
                    lines_needed.append(1)
                    continue
                segs = cell.split("\n")
                tot = 0
                for seg in segs:
                    sw = self.get_string_width(seg) if seg else 0
                    avail = max(w - 2, 5)
                    tot += max(1, -(-int(sw // avail) - 1))
                lines_needed.append(max(1, tot))
            row_h = max(max(lines_needed) * line_h, 7)

            # page break inside table
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
            # bottom hairline
            self.set_draw_color(*HAIRLINE)
            self.line(x_start, y_start + row_h, x_start + sum(col_widths), y_start + row_h)
            # text
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

    def colour_chip(self, x, y, w, h, hex_code, label):
        h_clean = hex_code.lstrip("#")
        r, g, b = int(h_clean[0:2], 16), int(h_clean[2:4], 16), int(h_clean[4:6], 16)
        self.set_fill_color(r, g, b)
        self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.3)
        self.rect(x, y, w, h, "DF")
        self.set_xy(x, y + h + 0.6)
        self.set_font("Verdana", "B", 7.5)
        self.set_text_color(*INK)
        self.cell(w, 3.4, clean(label), align="C")
        self.set_xy(x, y + h + 4.2)
        self.set_font("Verdana", "", 6.8)
        self.set_text_color(*INK_MUTED)
        self.cell(w, 3.4, hex_code.upper(), align="C")

    # ---- Custom drawn diagrams ----
    def draw_plan_view(self, x, y, w, h):
        """Top-down plan of the foyer."""
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.5)
        self.set_fill_color(252, 246, 232)
        self.rect(x, y, w, h, "DF")
        # door opening (north, top) - a gap at top of rect
        door_w = w * 0.45
        door_x = x + (w - door_w) / 2
        # break the top line with door arc
        self.set_fill_color(*PAPER); self.set_draw_color(*PAPER)
        self.rect(door_x, y - 0.4, door_w, 0.8, "F")
        self.set_draw_color(*ACCENT); self.set_line_width(0.6)
        self.line(door_x, y, door_x + door_w, y)  # threshold
        # arc for door swing
        self.set_draw_color(*RULE); self.set_line_width(0.3)
        self.line(door_x, y, door_x, y + door_w * 0.55)
        # stone wall on south face
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.rect(x + 1.5, y + h - 7, w - 3, 5, "DF")
        self.set_xy(x + 1.5, y + h - 6)
        self.set_font("Verdana", "B", 7); self.set_text_color(255, 245, 220)
        self.cell(w - 3, 3, "STONE FEATURE WALL (S)", align="C")
        # screen cavity marker on stone
        cav_w = (w - 3) * 0.30
        cav_x = x + 1.5 + ((w - 3) - cav_w) / 2
        self.set_fill_color(*BLACK); self.set_draw_color(*ACCENT)
        self.rect(cav_x, y + h - 6.2, cav_w, 3.4, "DF")
        # DB chip on west wall
        self.set_fill_color(60, 60, 60); self.set_draw_color(60, 60, 60)
        self.rect(x + 1.6, y + h * 0.55, 4, 9, "F")
        self.set_xy(x + 1.6, y + h * 0.55 + 9.3)
        self.set_font("Verdana", "", 6.5); self.set_text_color(*INK_MUTED)
        self.cell(10, 3, "DB")
        # Switch board chip
        self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT)
        self.rect(x + 1.6, y + h * 0.30, 4, 4, "F")
        self.set_xy(x + 1.6, y + h * 0.30 + 4.3)
        self.cell(10, 3, "SB1")
        # Open archway on east wall
        self.set_draw_color(*PAPER); self.set_line_width(2.5)
        self.line(x + w, y + 6, x + w, y + h - 9)
        self.set_draw_color(*ACCENT); self.set_line_width(0.3)
        self.line(x + w, y + 6, x + w + 4, y + 6)
        self.line(x + w, y + h - 9, x + w + 4, y + h - 9)
        self.set_xy(x + w + 0.5, y + h * 0.5 - 2)
        self.set_font("Verdana", "I", 6.5); self.set_text_color(*INK_MUTED)
        self.cell(20, 3, "to LIVING")
        # compass / labels
        self.set_xy(x + w/2 - 6, y - 7)
        self.set_font("Verdana", "B", 7.5); self.set_text_color(*ACCENT_DK)
        self.cell(12, 3, "N (porch)", align="C")
        self.set_xy(x + w/2 - 6, y + h + 1)
        self.cell(12, 3, "S (stone)", align="C")
        self.set_xy(x - 6, y + h/2 - 1.5)
        self.cell(6, 3, "W")
        self.set_xy(x + w + 0.5, y + h/2 - 1.5)
        self.cell(6, 3, "E")
        # foyer label
        self.set_xy(x + w/2 - 18, y + h/2 - 4)
        self.set_font("Georgia", "I", 11); self.set_text_color(*INK_SOFT)
        self.cell(36, 4, "FOYER", align="C")
        self.set_xy(x + w/2 - 28, y + h/2)
        self.set_font("Verdana", "", 7); self.set_text_color(*INK_MUTED)
        self.cell(56, 3, "6 ft x 4'9\" - false ceiling 9 ft", align="C")
        self.set_text_color(*INK)

    def draw_cavity_view(self, x, y, w, h):
        """Inside-cavity view (looking into the cavity)."""
        # Cavity outline (thicker stone "frame")
        self.set_fill_color(*STONE_TONE); self.set_draw_color(*STONE_DK)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "DF")
        # Inner cavity (matte black)
        pad = 8
        cx, cy, cw, ch = x + pad, y + pad, w - 2*pad, h - 2*pad
        self.set_fill_color(*BLACK); self.set_draw_color(*BLACK)
        self.rect(cx, cy, cw, ch, "F")
        # Halo glow
        self.set_draw_color(*HALO_AMBER); self.set_line_width(1.2)
        self.rect(cx + 0.8, cy + 0.8, cw - 1.6, ch - 1.6, "D")
        # VESA plate (centered)
        vw, vh = cw * 0.55, ch * 0.55
        vx, vy = cx + (cw - vw)/2, cy + (ch - vh)/2
        self.set_fill_color(40, 40, 40); self.set_draw_color(80, 80, 80)
        self.rect(vx, vy, vw, vh, "DF")
        # 4 VESA screws
        self.set_fill_color(190, 190, 190); self.set_draw_color(190, 190, 190)
        for sx, sy in [(vx + vw*0.18, vy + vh*0.18),
                       (vx + vw*0.82, vy + vh*0.18),
                       (vx + vw*0.18, vy + vh*0.82),
                       (vx + vw*0.82, vy + vh*0.82)]:
            self.ellipse(sx - 0.6, sy - 0.6, 1.2, 1.2, "F")
        # Conduit stubs at bottom-left
        cond_x = cx + 4
        cond_y = cy + ch - 5
        for i, color in enumerate([(220, 60, 50), (130, 130, 130), (130, 130, 130)]):
            self.set_fill_color(*color); self.set_draw_color(*color)
            self.ellipse(cond_x + i*4 - 1.2, cond_y - 1.2, 2.4, 2.4, "F")
        self.set_xy(cond_x - 2, cond_y + 1.5)
        self.set_font("Verdana", "", 5.5); self.set_text_color(255, 245, 220)
        self.cell(20, 2.2, "P  D  LV")
        # Labels around the cavity
        self.set_text_color(*INK)
        self.set_font("Verdana", "B", 7.5)
        self.set_xy(x, y - 5)
        self.cell(w, 3, "SCREEN CAVITY  -  back wall view  -  540 x 340 x 100 mm", align="C")
        # dim labels
        self.set_font("Verdana", "I", 7)
        self.set_text_color(*INK_MUTED)
        self.set_xy(x, y + h + 1)
        self.cell(w, 3, "Bottom of cavity at 1280 mm FFL  -  centre at 1450 mm FFL", align="C")
        self.set_text_color(*INK)

    def draw_elevation(self, x, y, w, h):
        """Wall elevation - feature wall with stone, cavity, shelf."""
        # outer wall outline
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        self.set_fill_color(*PAPER)
        self.rect(x, y, w, h, "DF")
        # stone region (everything is stone)
        stone_band_h = 4
        stone_y = y
        # draw stone-look pattern: alternating tobacco/sandstone/charcoal small rects
        import random
        random.seed(42)
        cursor_y = y
        while cursor_y < y + h - 0.4:
            cx = x + 0.4
            band_h = 3.5 + random.random() * 1.5
            while cx < x + w - 0.4:
                stone_w = 4 + random.random() * 8
                if cx + stone_w > x + w - 0.4:
                    stone_w = x + w - 0.4 - cx
                tone = random.choice([STONE_TONE, STONE_TONE, STONE_LT, STONE_DK])
                self.set_fill_color(*tone); self.set_draw_color(45, 35, 25)
                self.set_line_width(0.15)
                self.rect(cx, cursor_y, stone_w, band_h, "DF")
                cx += stone_w
            cursor_y += band_h

        # screen cavity (matte black with halo)
        cav_w = w * 0.42
        cav_h = h * 0.20
        cav_x = x + (w - cav_w) / 2
        cav_y = y + h * 0.32
        # halo glow
        self.set_fill_color(*HALO_AMBER)
        self.set_draw_color(*HALO_AMBER)
        self.rect(cav_x - 1.5, cav_y - 1.5, cav_w + 3, cav_h + 3, "F")
        # cavity
        self.set_fill_color(*BLACK); self.set_draw_color(*BLACK)
        self.rect(cav_x, cav_y, cav_w, cav_h, "F")
        # screen surface (small sheen)
        self.set_fill_color(20, 25, 30)
        self.rect(cav_x + 1.2, cav_y + 1.2, cav_w - 2.4, cav_h - 2.4, "F")
        # shelf
        shelf_y = y + h * 0.62
        self.set_fill_color(*WALNUT); self.set_draw_color(40, 25, 15)
        self.rect(x + 1, shelf_y, w - 2, 2.2, "DF")
        # under-shelf glow
        self.set_fill_color(*COVE_WARM); self.set_draw_color(*COVE_WARM)
        self.rect(x + 4, shelf_y + 2.4, w - 8, 1.0, "F")
        # FFL line
        self.set_draw_color(*ACCENT); self.set_line_width(0.4)
        self.line(x - 2, y + h, x + w + 2, y + h)

        # height ticks (right side)
        ticks = [
            (y + h, "FFL 0"),
            (shelf_y + 1.1, "900 mm shelf"),
            (cav_y + cav_h, "1280 cavity btm"),
            (cav_y + cav_h/2, "1450 centre"),
            (cav_y, "1620 cavity top"),
            (y, "11 ft  (3353)"),
        ]
        self.set_font("Verdana", "", 6.8)
        self.set_text_color(*INK_MUTED)
        for ty, label in ticks:
            self.set_draw_color(*HAIRLINE); self.set_line_width(0.2)
            self.line(x + w + 0.5, ty, x + w + 2.5, ty)
            self.set_xy(x + w + 3, ty - 1.5)
            self.cell(40, 3, label)
        # title
        self.set_text_color(*INK)
        self.set_font("Verdana", "B", 7.5)
        self.set_xy(x, y - 5)
        self.cell(w, 3, "FEATURE WALL ELEVATION  -  6 ft (1828 mm) wide  -  S facing", align="C")

    def draw_cove_section(self, x, y, w, h):
        """Cross section through wall + cove pocket."""
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.4)
        # slab on top
        slab_h = 6
        self.set_fill_color(220, 215, 200); self.set_draw_color(160, 150, 130)
        self.rect(x, y, w, slab_h, "DF")
        self.set_xy(x + 2, y + 1.5)
        self.set_font("Verdana", "", 7); self.set_text_color(*INK_SOFT)
        self.cell(40, 3, "RCC slab (11 ft)")
        # wall on left
        wall_w = 9
        self.set_fill_color(245, 240, 225); self.set_draw_color(190, 175, 145)
        self.rect(x, y + slab_h, wall_w, h - slab_h, "DF")
        self.set_xy(x + 1, y + slab_h + 4)
        self.set_text_color(*INK_SOFT)
        self.cell(20, 3, "wall")
        # ceiling drop (false ceiling 9 ft)
        ceil_top = y + slab_h + 18
        ceil_thickness = 2.2
        self.set_fill_color(248, 244, 236); self.set_draw_color(160, 150, 130)
        self.rect(x + wall_w, ceil_top, w - wall_w, ceil_thickness, "DF")
        self.set_xy(x + wall_w + 5, ceil_top + 4)
        self.set_font("Verdana", "", 7); self.set_text_color(*INK_SOFT)
        self.cell(60, 3, "false ceiling (9 ft)  -  gypsum 12.5 mm")
        # cove pocket detail
        cove_x = x + wall_w
        cove_y = ceil_top
        cove_w = 16
        cove_h = 8
        self.set_fill_color(*PAPER); self.set_draw_color(160, 150, 130)
        self.rect(cove_x, cove_y - cove_h, cove_w, cove_h, "DF")
        # LED strip at floor of cove
        self.set_fill_color(*COVE_WARM); self.set_draw_color(*COVE_WARM)
        self.rect(cove_x + 2, cove_y - 1.3, cove_w - 4, 0.8, "F")
        # cove arrow
        self.set_draw_color(*ACCENT); self.set_line_width(0.4)
        self.line(cove_x + cove_w + 2, cove_y - cove_h/2, cove_x + cove_w + 14, cove_y - cove_h/2)
        self.line(cove_x + cove_w + 2, cove_y - cove_h/2, cove_x + cove_w + 4, cove_y - cove_h/2 - 1)
        self.line(cove_x + cove_w + 2, cove_y - cove_h/2, cove_x + cove_w + 4, cove_y - cove_h/2 + 1)
        self.set_xy(cove_x + cove_w + 4, cove_y - cove_h/2 - 4)
        self.set_font("Verdana", "B", 7); self.set_text_color(*ACCENT_DK)
        self.cell(50, 3, "Cove pocket")
        self.set_xy(cove_x + cove_w + 4, cove_y - cove_h/2 - 0.8)
        self.set_font("Verdana", "", 7); self.set_text_color(*INK_SOFT)
        self.cell(50, 3, "100 mm wide x 75 mm deep")
        self.set_xy(cove_x + cove_w + 4, cove_y - cove_h/2 + 2.4)
        self.cell(50, 3, "LED strip 24V 2700K inside")
        # title
        self.set_text_color(*INK)
        self.set_font("Verdana", "B", 7.5)
        self.set_xy(x, y - 5)
        self.cell(w, 3, "COVE CROSS-SECTION  -  view from foyer interior", align="C")

    def draw_rcp(self, x, y, w, h):
        """Reflected ceiling plan (looking up)."""
        self.set_draw_color(*INK_SOFT); self.set_line_width(0.5)
        self.set_fill_color(*SOFT_SNOW)
        self.rect(x, y, w, h, "DF")
        # cove perimeter (inset rectangle)
        inset = 4
        self.set_fill_color(*COVE_WARM); self.set_draw_color(*COVE_WARM)
        # 4 thin strips
        self.rect(x + inset - 0.6, y + inset - 0.6, w - 2*inset + 1.2, 1.2, "F")  # top
        self.rect(x + inset - 0.6, y + h - inset - 0.6, w - 2*inset + 1.2, 1.2, "F")  # bottom
        self.rect(x + inset - 0.6, y + inset, 1.2, h - 2*inset, "F")  # left
        self.rect(x + w - inset - 0.6, y + inset, 1.2, h - 2*inset, "F")  # right
        # 2 spotlights
        for sy in [y + h * 0.30, y + h * 0.66]:
            sx = x + inset + 6
            self.set_fill_color(*ACCENT); self.set_draw_color(*ACCENT_DK)
            self.ellipse(sx - 1.6, sy - 1.6, 3.2, 3.2, "DF")
            # rays
            self.set_draw_color(*ACCENT); self.set_line_width(0.3)
            for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
                self.line(sx, sy, sx + dx, sy + dy)
        # speaker dot in center
        cx, cy = x + w/2, y + h/2
        self.set_fill_color(60, 60, 60); self.set_draw_color(60, 60, 60)
        self.ellipse(cx - 2, cy - 2, 4, 4, "DF")
        self.set_fill_color(120, 120, 120)
        self.ellipse(cx - 1.2, cy - 1.2, 2.4, 2.4, "F")
        # labels
        self.set_font("Verdana", "B", 7); self.set_text_color(*INK)
        self.set_xy(x + w * 0.34, y + h * 0.30 - 1.5)
        self.cell(20, 3, "Spot L")
        self.set_xy(x + w * 0.34, y + h * 0.66 - 1.5)
        self.cell(20, 3, "Spot R")
        self.set_xy(cx + 4, cy - 1.5)
        self.cell(20, 3, "Speaker")
        # corners labels
        self.set_font("Verdana", "I", 6.5); self.set_text_color(*INK_MUTED)
        self.set_xy(x + 2, y + 0.5)
        self.cell(40, 3, "cove perimeter (2700K)")
        # compass
        self.set_font("Verdana", "B", 7); self.set_text_color(*ACCENT_DK)
        self.set_xy(x + w/2 - 4, y - 5)
        self.cell(8, 3, "N (door)", align="C")
        self.set_xy(x + w/2 - 4, y + h + 1)
        self.cell(8, 3, "S (stone)", align="C")
        # title
        self.set_text_color(*INK)
        self.set_font("Verdana", "B", 7.5)
        self.set_xy(x, y - 9.5)
        self.cell(w, 3, "REFLECTED CEILING PLAN", align="C")


# ============================================================
#                        PDF CONTENT
# ============================================================
pdf = FoyerPDF()
pdf.suppress_chrome = True

# ---------- COVER ----------
pdf.add_page()
# Full-bleed amber band on the left
pdf.set_fill_color(*ACCENT)
pdf.rect(0, 0, 12, 297, "F")
# Top header rule
pdf.set_xy(24, 24)
pdf.set_font("Verdana", "B", 9)
pdf.set_text_color(*ACCENT_DK)
pdf.cell(0, 5, "GANESH PRASAD - HOME DESIGN BRIEF NO. 03")
pdf.set_xy(24, 30)
pdf.set_draw_color(*RULE); pdf.set_line_width(0.5)
pdf.line(24, 30, 186, 30)

# Title
pdf.set_xy(24, 45)
pdf.set_font("Georgia", "B", 56)
pdf.set_text_color(*INK)
pdf.cell(0, 22, "Foyer", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(24)
pdf.set_text_color(*ACCENT_DK)
pdf.cell(0, 22, "Welcome Plan", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.ln(2)
pdf.set_x(24)
pdf.set_font("Georgia", "I", 16)
pdf.set_text_color(*INK_SOFT)
pdf.cell(0, 8, clean("A comprehensive build guide for every trade"),
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ornament
pdf.ln(4); pdf.set_x(24)
pdf.set_draw_color(*ACCENT); pdf.set_line_width(1.2)
pdf.line(24, pdf.get_y(), 60, pdf.get_y())

# subtitle / what's inside
pdf.set_y(135)
pdf.set_x(24)
pdf.set_font("Verdana", "B", 10)
pdf.set_text_color(*ACCENT_DK)
pdf.cell(0, 5, "WHAT IS INSIDE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(24)
pdf.set_font("Verdana", "", 11)
pdf.set_text_color(*INK)
pdf.multi_cell(150, 6,
    clean("Step-by-step construction sequence  -  every cavity  -  every conduit  -  "
          "every wire  -  the stone, the screen, the smart welcome system  -  "
          "materials with quantities and sources  -  trade-by-trade sign-off."))

# Project box
pdf.set_y(170)
pdf.set_x(24)
pdf.set_font("Verdana", "B", 10)
pdf.set_text_color(*ACCENT_DK)
pdf.cell(0, 5, "THE PROJECT", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_x(24)
pdf.set_font("Verdana", "", 10)
pdf.set_text_color(*INK)
def cover_kv(k, v, x, y):
    pdf.set_xy(x, y)
    pdf.set_font("Verdana", "B", 9.5); pdf.set_text_color(*ACCENT_DK)
    pdf.cell(34, 5, k)
    pdf.set_font("Verdana", "", 9.5); pdf.set_text_color(*INK)
    pdf.cell(140, 5, v)

cover_kv("Owner",     "Ganesh Prasad D", 24, 178)
cover_kv("Location",  "Chitradurga, Karnataka", 24, 184)
cover_kv("House",     "Two-storey, North-facing main entrance", 24, 190)
cover_kv("Foyer",     "6'0\" wide  x  approx 4'9\" deep  -  GF, false ceiling 9 ft", 24, 196)
cover_kv("Stone wall","9\" thick  x  6 ft wide  x  11 ft tall, S facing", 24, 202)
cover_kv("Concept",   "Stone-clad welcome wall with 22\" recessed screen", 24, 208)
cover_kv("Smarts",    "Face-recognition welcome (CAM-1 -> Frigate -> RPi screen)", 24, 214)
cover_kv("Document",  "v2.0   -   2026-05-10", 24, 220)
cover_kv("For trades","Mason  -  Electrician  -  Stone cladder  -  Painter  -  Carpenter  -  Smart-home", 24, 226)

# bottom strip
pdf.set_xy(24, 252)
pdf.set_draw_color(*ACCENT); pdf.set_line_width(0.6)
pdf.line(24, 252, 186, 252)
pdf.set_xy(24, 256)
pdf.set_font("Georgia", "I", 11)
pdf.set_text_color(*INK_SOFT)
pdf.multi_cell(160, 5.5,
    clean("Hand a printed copy to every trade BEFORE work starts. Each trade signs "
          "their section on pages 26 to 28 before they leave site."))

pdf.suppress_chrome = False

# ---------- TABLE OF CONTENTS ----------
pdf.section_open("00", "Contents", "What is in this document, and where to find it.")

toc = [
    ("01", "The Vision",                          "What we are building and why",                    " 5"),
    ("02", "Foyer at a Glance",                   "Plan view, dimensions, palette",                  " 7"),
    ("03", "The Welcome System",                  "End-to-end smart-home flow",                      " 9"),
    ("04", "Construction Sequence",               "11 phases, every owner and sign-off",             "11"),
    ("05", "Cavities Required",                   "What the mason cuts and where",                   "15"),
    ("06", "Conduits Required",                   "Every conduit run in and out of the foyer",       "17"),
    ("07", "Wiring Schedule",                     "Wires, circuits and the smart switch",            "19"),
    ("08", "Lighting Plan",                       "Four layers of light",                            "20"),
    ("09", "False Ceiling",                       "Drop, cove, hatch",                               "22"),
    ("10", "Stone Cladding",                      "Material, application, the cavity rule",          "23"),
    ("11", "Painting",                            "Surfaces, colours, sequence",                     "25"),
    ("12", "Carpentry",                           "VESA backing and walnut shelf",                   "26"),
    ("13", "Materials & Costs",                   "Itemised list with quantities and sources",       "27"),
    ("14", "Sign-off Checklists",                 "One section per trade",                           "29"),
    ("A",  "Glossary & Cross-references",         "Definitions and where to read more",              "32"),
]

pdf.set_font("Verdana", "", 10.5)
for num, title, sub, page in toc:
    if pdf.get_y() > 250:
        pdf.add_page()
    y = pdf.get_y()
    # number chip
    pdf.set_fill_color(*ACCENT)
    pdf.set_draw_color(*ACCENT)
    pdf.rect(18, y + 1, 9, 6, "F")
    pdf.set_xy(18, y + 1)
    pdf.set_font("Verdana", "B", 8.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(9, 6, num, align="C")
    # title + sub
    pdf.set_xy(31, y)
    pdf.set_font("Verdana", "B", 11)
    pdf.set_text_color(*INK)
    pdf.cell(70, 4, clean(title))
    pdf.set_font("Verdana", "I", 9)
    pdf.set_text_color(*INK_MUTED)
    pdf.cell(75, 4, clean(sub))
    # leader dots
    pdf.set_xy(170, y)
    pdf.set_font("Verdana", "B", 11)
    pdf.set_text_color(*ACCENT_DK)
    pdf.cell(22, 4, f"p. {page}", align="R")
    pdf.set_xy(31, y + 5)
    pdf.set_draw_color(*HAIRLINE); pdf.set_line_width(0.15)
    pdf.line(31, y + 7, 192, y + 7)
    pdf.set_y(y + 9)

pdf.ln(4)
pdf.h2("Quick reference - key numbers")
pdf.set_font("Verdana", "", 10)
pdf.kv("Foyer wall",         "9 in thick  -  6 ft wide  -  11 ft tall (full GF height)")
pdf.kv("False ceiling",      "Drop from 11 ft slab to 9 ft (2 ft drop)")
pdf.kv("Floor tile",         "1200 x 1200 mm matte porcelain, warm ivory-greige #E8DCC8")
pdf.kv("Wall paint (sides)", "Warm ivory #F2EBDD, premium washable matte emulsion")
pdf.kv("Ceiling paint",      "Soft snow #F8F4EC, flat emulsion")
pdf.kv("Stone cladding",     "Rustic ledgestone (tobacco / sandstone / charcoal mix)")
pdf.kv("Welcome screen",     "Samsung LS22F350, 21.5 in IPS, recessed flush")
pdf.kv("Screen cavity",      "540 x 340 x 100 mm  -  bottom at 1280 mm FFL")
pdf.kv("Walnut shelf",       "6 ft x 10 in deep  -  top at 900 mm FFL")
pdf.kv("Spotlights",         "2 x recessed GU10 7W 2700K gimbal (stone-grazing)")
pdf.kv("DB panel",           "48-way Schneider Acti9, bottom edge 1500 mm FFL")

# ---------- SECTION 01 - VISION ----------
pdf.section_open("01", "The Vision",
                 "The foyer is the first six feet a visitor sees. It should welcome, not transit.")

pdf.h2("Five elements")
pdf.body(
    "1. STONE FEATURE WALL  -  rustic ledgestone cladding across the full 6 ft x 11 ft "
    "south-facing wall. A tobacco brown, sandstone beige and charcoal mix gives natural "
    "depth and shadow. This is the visual anchor of the whole entry."
)
pdf.body(
    "2. RECESSED WELCOME SCREEN  -  21.5 in Samsung monitor flush-mounted in a stone "
    "cavity at face height (centre 1450 mm FFL). When a known face is detected at the "
    "door, the screen displays a personalised welcome."
)
pdf.body(
    "3. AMBER HALO LED  -  24V LED strip at 2200K (warm amber) inside the cavity reveal, "
    "throwing a soft glow around the screen edges. Visible day or night."
)
pdf.body(
    "4. WALNUT FLOATING SHELF  -  6 ft x 10 in dark walnut shelf at 900 mm FFL with an "
    "under-shelf 24V LED strip washing the wall below. Holds keys, a small plant, mail."
)
pdf.body(
    "5. CEILING SPOTLIGHTS + COVE  -  two adjustable GU10 spots aimed to graze the stone "
    "and bring out its texture. False ceiling cove with 2700K LED gives ambient warmth."
)

pdf.h2("The welcome moment")
pdf.lede(
    "Visitor approaches the main door. The face camera sees them. Two seconds later the "
    "screen lights up with their name and a soft chime plays from the ceiling. They feel "
    "expected. They feel welcomed. That is the entire idea."
)
pdf.body(
    "Stranger? The screen stays in idle wallpaper mode (or shows a polite \"press the "
    "doorbell\" card). The doorbell and intercom (separate hardware) handle the "
    "introduction."
)

pdf.callout("info", "Why this matters for every trade",
    "The screen is recessed FLUSH into stone, so the cavity must be cut in masonry "
    "BEFORE plaster, conduits pulled BEFORE plaster, plaster done, then stone "
    "cladding applied AROUND the cavity (no stone goes inside the cavity). Get the "
    "sequence wrong and the wall is rebuilt. Read Section 04 carefully.")

# ---------- SECTION 02 - AT A GLANCE ----------
pdf.section_open("02", "Foyer at a Glance",
                 "Plan view, dimensions, the colour palette in one place.")

# Plan view diagram
pdf.h2("Plan view")
pdf.draw_plan_view(50, pdf.get_y() + 6, 110, 76)
pdf.set_y(pdf.get_y() + 92)

pdf.h2("Dimensions")
pdf.table(
    headers=["Item", "Value", "Notes"],
    rows=[
        ["Foyer width (E to W)",     "approx 6 ft (1828 mm)",  "Between W wall and start of Living Area"],
        ["Foyer depth (N to S)",     "approx 4 ft 9 in (1450 mm)", "Between main door and feature wall"],
        ["GF slab height",           "11 ft (3353 mm)",        "Raw slab, before false ceiling"],
        ["False ceiling height",     "9 ft (2743 mm)",         "Drop of 2 ft from slab"],
        ["Feature wall width",       "6 ft (1828 mm)",         "S-facing, full foyer width"],
        ["Feature wall thickness",   "9 in (228 mm)",          "Structural masonry"],
        ["Feature wall height",      "11 ft (3353 mm)",        "Floor to slab; stone clads full height"],
        ["Main door (existing)",     "Solid teak, 3 ft x 7 ft","Frame stained to match windows"],
    ],
    col_widths=[58, 48, 78],
)

pdf.h2("Colour palette - foyer")
pdf.body(
    "Eight tones drive the entire scheme. The first three are the stone mix; the next "
    "two are the painted side walls and ceiling; the last three are wood and the LED "
    "colour temperatures."
)
y0 = pdf.get_y() + 2
chips = [
    ("#7B5C42", "Tobacco"),
    ("#C8B58F", "Sandstone"),
    ("#3A3633", "Charcoal"),
    ("#F2EBDD", "Side wall"),
    ("#F8F4EC", "Ceiling"),
    ("#4A3526", "Walnut"),
    ("#FFB877", "Halo 2200K"),
    ("#FFE4B8", "Cove 2700K"),
]
for i, (h, l) in enumerate(chips):
    pdf.colour_chip(20 + i * 21.5, y0, 18, 14, h, l)
pdf.set_y(y0 + 28)

# ---------- SECTION 03 - WELCOME SYSTEM ----------
pdf.section_open("03", "The Welcome System",
                 "End-to-end hardware chain. If any one piece is missing, the welcome breaks.")

pdf.h2("Hardware chain (in the order data flows)")
pdf.table(
    headers=["#", "Component", "Where it lives", "What it does"],
    rows=[
        ["1", "CAM-1  -  Hikvision DS-2CD2143G2-LU 4MP ColorVu, 4mm, IP67, PoE",
              "Outside main door, latch-side wall, 1650 mm FFL",
              "Captures the visitor's face front-on. ColorVu = full colour at night."],
        ["2", "Cat6 from CAM-1",
              "Outside-door box -> staircase niche patch panel",
              "Carries the camera stream to the home server."],
        ["3", "PoE switch  -  TP-Link TL-SG1210P (8x PoE)",
              "Staircase niche, on UPS",
              "Powers and connects all 5 outdoor cameras and the FF AP."],
        ["4", "Beelink EQ12  -  Frigate NVR + CompreFace + HA",
              "Staircase niche on shelf, on UPS",
              "Identifies the face within 1-2 seconds. Brain of the system."],
        ["5", "Home Assistant automation",
              "Same server",
              "Decides what to display: known face -> personalised welcome."],
        ["6", "TP-Link AX55 router + Cat6 to foyer cavity",
              "Staircase niche -> foyer screen cavity (LV-25 conduit)",
              "Pushes the welcome payload to the screen RPi."],
        ["7", "Raspberry Pi Zero 2W",
              "Inside foyer screen cavity, behind monitor",
              "Receives the message, drives the HDMI output to the screen."],
        ["8", "Samsung LS22F350 monitor (21.5 in IPS)",
              "Recessed flush in stone cavity, centre 1450 mm FFL",
              "Displays the welcome message, family calendar, weather."],
        ["9", "RPi Camera Module 3 (CAM-0)",
              "Top-centre of screen bezel, 1600-1650 mm FFL",
              "Secondary close-range face check at the screen."],
        ["10", "Amber halo LED  -  24V, 4.8 W/m, 2200K",
              "Inside screen cavity reveal, perimeter",
              "Soft amber glow around the screen day or night."],
        ["11", "Ceiling speaker (3 in flush mount)",
              "Centre of foyer false ceiling",
              "Soft chime when welcome triggers."],
        ["12", "Smart switch  -  Aqara H1 EU 2-gang + Sonoff relay",
              "W wall switch board, 1200 mm FFL",
              "Manual override: spotlights + cove + halo, dimmable."],
    ],
    col_widths=[7, 60, 56, 61],
    body_size=8,
)

pdf.h2("How the trades enable this chain")
pdf.kv("Electrician", "Pulls Cat6 from staircase niche to (a) cavity, (b) outside door, "
                       "(c) porch ceiling. Drops 230V power into cavity. Wires smart switch with neutral.")
pdf.kv("Mason",       "Cuts the screen cavity (540 x 340 x 100 mm) and DB recess "
                       "(400 x 600 x 100 mm). Punches conduit entries. Maintains exact heights.")
pdf.kv("Stone cladder","Clads the 6 ft x 11 ft feature wall AROUND the cavity. Stops "
                       "stone exactly at cavity edge. Does not block conduit stubs.")
pdf.kv("Gypsum / POP", "Drops false ceiling to 9 ft, builds 100 mm cove pocket around "
                       "the perimeter, leaves an inspection hatch for the LED driver.")
pdf.kv("Painter",     "Matte black inside cavity (BEFORE stone), then ivory side walls "
                       "and soft snow ceiling.")
pdf.kv("Carpenter",   "Fixes the 12 mm ply VESA backing inside the cavity, builds the "
                       "walnut floating shelf.")
pdf.kv("Smart-home",  "Mounts CAM-1, CAM-0, monitor, RPi, speaker. Configures Frigate, "
                       "CompreFace, Home Assistant. Final commissioning.")

# ---------- SECTION 04 - CONSTRUCTION SEQUENCE ----------
pdf.section_open("04", "Construction Sequence",
                 "Eleven phases, in this order. Each has a trade owner, a deliverable, and a sign-off before the next phase starts.")

pdf.callout("warn", "Phase order is not optional",
    "Out-of-order work breaks walls. If you do stone before conduits, you cut stone "
    "to lay conduits. Total time wasted: 3 to 5 days plus material loss. Read the "
    "phase order and stick to it.")

phases = [
    ("PHASE 1  -  Marking and setup",
     "Mason + Electrician + Homeowner",   "Day 1",
     "On the bare brick or block wall, mark in chalk: (a) screen cavity outline at "
     "correct height, (b) DB recess, (c) all switch box positions, (d) all socket "
     "box positions, (e) all conduit chase lines, (f) ceiling spotlight positions "
     "on slab. Take photos of every mark. Get owner sign-off before any cutting "
     "starts.",
     "All marks photographed and signed off. NOTHING cut yet."),
    ("PHASE 2  -  Wall chasing and cavity cutting",
     "Mason",                             "Day 2 to 3",
     "Cut the screen cavity (540 W x 340 H x 100 D mm), DB recess "
     "(400 W x 600 H x 100 D mm), all switch box and socket box pockets "
     "(65 mm DEEP at smart-switch locations - see Section 05), and all conduit "
     "chases. Use angle grinder + chisel; do NOT use hammer drill alone (causes "
     "blowouts in the 9 in wall).",
     "Cavities verified to spec; conduit chases at correct heights."),
    ("PHASE 3  -  Conduit pulling",
     "Electrician",                       "Day 4 to 5",
     "Lay all 25 mm and 16 mm PVC conduits per Section 06. Use coloured PVC where "
     "available; otherwise wrap end-tape and label every conduit BEFORE plaster. "
     "Insert draw wires (fish tape) in every conduit. Cap conduit ends with masking "
     "tape so plaster does not enter.",
     "All conduits in place, ends labelled, draw wires inside, all caps fitted."),
    ("PHASE 4  -  Wire pulling and DB install",
     "Electrician",                       "Day 6 to 7",
     "Pull wires through conduits per Section 07. Every smart-switch box gets "
     "L+N+E (Live + Neutral + Earth)  -  cap unused neutrals, do not omit. Mount "
     "the 48-way Schneider Acti9 DB. Connect MCBs and RCBOs per the circuit list. "
     "Leave 300 mm tail of wires inside every switch box. Test earth continuity "
     "at every metallic body (less than 1 ohm).",
     "Wires labelled at both ends; earth continuity tested; tails inside boxes."),
]

for title, owner, days, desc, signoff in phases:
    if pdf.get_y() > 235:
        pdf.add_page()
    pdf.h3(title)
    pdf.set_font("Verdana", "", 9)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 4.5, clean(f"Owner: {owner}     Time: {days}"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*INK)
    pdf.set_font("Verdana", "", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 5, clean(desc))
    pdf.set_font("Verdana", "I", 9)
    pdf.set_text_color(*GOOD_INK)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 4.8, clean("SIGN-OFF: " + signoff))
    pdf.set_text_color(*INK)
    pdf.ln(2)

# Phases 5 to 8
phases2 = [
    ("PHASE 5  -  First plaster (rough coat)",
     "Mason",                             "Day 8 to 10",
     "Apply rough plaster coat over chased walls. Conduits and back boxes flush "
     "with finished plaster line. Plaster STOPS at: (a) screen cavity edge, "
     "(b) DB recess edge, (c) every switch and socket box rim. Cure 48 hours minimum.",
     "Plaster level, no conduits visible, no boxes buried beyond rim."),
    ("PHASE 6  -  Cavity interior paint (BLACK)",
     "Painter",                           "Day 11",
     "Paint INSIDE the screen cavity matte black. All five interior surfaces "
     "(back wall + 4 sides). This is done BEFORE stone cladding because once "
     "stone wraps around the cavity edge, you cannot paint inside cleanly. Use "
     "2 coats matte black acrylic emulsion or chalkboard paint.",
     "Cavity interior fully matte black, no shiny spots, edges crisp."),
    ("PHASE 7  -  VESA backing board",
     "Carpenter",                         "Day 11",
     "Fix 12 mm BWP plywood backing board (600 x 400 mm) to the back wall of the "
     "cavity, centred. Use 4 x rawl plug + screw at corners. This is the structural "
     "anchor for the VESA mount. Backing board face flush with painted black "
     "surface (slightly behind, never proud).",
     "Backing board dead centre, screws not stripped, surface ready for VESA bracket."),
    ("PHASE 8  -  Stone cladding",
     "Stone cladder",                     "Day 12 to 15",
     "Clad the 6 ft x 11 ft S-facing feature wall in rustic ledgestone (tobacco "
     "brown / sandstone beige / charcoal mix). Stone STOPS exactly at the cavity "
     "edge  -  NO STONE INSIDE THE CAVITY. Conduit stubs at cavity bottom-left "
     "remain accessible. Use high-bond MS polymer adhesive plus mechanical clips "
     "for stones over 5 kg. See Section 10 for full guide.",
     "Stone cladding complete, no protrusion into cavity, conduits accessible, "
     "no loose stones, mortar joints raked clean."),
]
for title, owner, days, desc, signoff in phases2:
    if pdf.get_y() > 235:
        pdf.add_page()
    pdf.h3(title)
    pdf.set_font("Verdana", "", 9)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 4.5, clean(f"Owner: {owner}     Time: {days}"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*INK)
    pdf.set_font("Verdana", "", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 5, clean(desc))
    pdf.set_font("Verdana", "I", 9)
    pdf.set_text_color(*GOOD_INK)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 4.8, clean("SIGN-OFF: " + signoff))
    pdf.set_text_color(*INK)
    pdf.ln(2)

# Phases 9 to 11
phases3 = [
    ("PHASE 9  -  False ceiling and cove",
     "Gypsum / POP contractor",           "Day 16 to 19",
     "Drop ceiling from 11 ft to 9 ft (2 ft drop) using a GI grid + 12.5 mm "
     "gypsum board. Build a 100 mm wide x 75 mm deep cove pocket around the FULL "
     "perimeter of the foyer false ceiling. Leave a 300 x 300 mm inspection hatch "
     "above the W wall (DB side) for accessing the LED driver. Do NOT block "
     "ceiling spotlight boxes - leave clean cut-outs at the marked positions.",
     "Ceiling level, cove pocket continuous, hatch operable, spotlight cut-outs clean."),
    ("PHASE 10  -  Final paint",
     "Painter",                           "Day 20 to 22",
     "Side walls (W and partition wall to Living): warm ivory #F2EBDD, premium "
     "washable matte emulsion, 2 coats. Ceiling and cove inside: soft snow "
     "#F8F4EC, flat emulsion. Sample 2 ft x 2 ft on each surface, view at 3 "
     "times of day, BEFORE bulk paint. Mask the stone wall fully. Mask all "
     "switch and socket boxes.",
     "Paint even, no roller marks under raking light, masking removed cleanly."),
    ("PHASE 11  -  Switch and socket fitting plus lighting plus smart-home",
     "Electrician + Smart-home installer", "Day 23 to 25",
     "Fit modular plates (Schneider Unica champagne) on all switch boxes. Install "
     "smart switches (Aqara H1 2-gang) on the foyer board. Install 2 x recessed "
     "GU10 gimbal spotlights in ceiling. Lay cove LED strip (2700K, 9.6 W/m) "
     "inside cove pocket and amber halo (2200K, 4.8 W/m) inside cavity perimeter. "
     "Install drivers above false ceiling. Mount VESA bracket and Samsung monitor "
     "in cavity. Insert RPi Zero 2W behind monitor and camera at top-bezel. Mount "
     "CAM-1 outside main door. Configure Frigate, CompreFace, Home Assistant. "
     "Test welcome flow with 3 family faces.",
     "Welcome flow tested with 3 known faces; unknown person triggers idle "
     "screen; doorbell works; spotlights, cove, halo all dim; speaker chimes."),
]
for title, owner, days, desc, signoff in phases3:
    if pdf.get_y() > 235:
        pdf.add_page()
    pdf.h3(title)
    pdf.set_font("Verdana", "", 9)
    pdf.set_text_color(*INK_SOFT)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 4.5, clean(f"Owner: {owner}     Time: {days}"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*INK)
    pdf.set_font("Verdana", "", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 5, clean(desc))
    pdf.set_font("Verdana", "I", 9)
    pdf.set_text_color(*GOOD_INK)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 4.8, clean("SIGN-OFF: " + signoff))
    pdf.set_text_color(*INK)
    pdf.ln(2)

pdf.h2("Total estimated time")
pdf.kv("Calendar days", "approx 25 working days (about 5 weeks with weekends)")
pdf.kv("Critical path", "Plaster cure (48 hr) and stone adhesive cure (24 hr) cannot be rushed")
pdf.kv("Dependencies",  "Floor tile must be laid BEFORE Phase 1 - FFL set on tile, not on slab")

# ---------- SECTION 05 - CAVITIES ----------
pdf.section_open("05", "Cavities Required",
                 "All measurements from Finished Floor Level (FFL = top of installed floor tile, not raw slab).")

pdf.callout("warn", "FFL  =  Finished Floor Level",
    "If the floor tile is not laid yet, mark the future tile line in chalk and "
    "reference all heights from there  -  NOT from the bare slab. Even 10 mm of "
    "screed makes the cavity look wrong.")

pdf.h2("5.1  Screen cavity (most critical)")
pdf.draw_cavity_view(58, pdf.get_y() + 4, 95, 56)
pdf.set_y(pdf.get_y() + 70)

pdf.table(
    headers=["Dimension", "Value", "Why"],
    rows=[
        ["Cavity width",                  "540 mm (21.3 in)", "Panel 491 mm + 25 mm clearance each side"],
        ["Cavity height",                 "340 mm (13.4 in)", "Panel 291 mm + 25 mm clearance top + bottom"],
        ["Cavity depth",                  "100 mm (4 in)",    "Panel 49 mm + 51 mm for HDMI / power / RPi"],
        ["Bottom of cavity from FFL",     "1280 mm (50.4 in)","Sets screen centre at 1450 mm"],
        ["Centre of cavity from FFL",     "1450 mm (57.1 in)","Comfortable standing eye level"],
        ["Top of cavity from FFL",        "1620 mm (63.8 in)","Auto-derived from above"],
        ["Horizontal position",           "Centred on 6 ft (1828 mm) wall",
            "Left edge 644 mm from L wall, right edge 644 mm from R wall"],
    ],
    col_widths=[58, 58, 68],
)

pdf.h3("Conduit entries inside the cavity")
pdf.body(
    "Two 25 mm conduit stubs and one 16 mm conduit stub enter the cavity from the "
    "BOTTOM-LEFT CORNER of the back wall, coming horizontally from the staircase "
    "niche direction (i.e. from the W side):"
)
pdf.bullet("25 mm conduit (Circuit B2 power) from DB - carries 230V for monitor and RPi")
pdf.bullet("25 mm conduit LV-25 grey from staircase niche - carries Cat6")
pdf.bullet("16 mm conduit LV-16 grey from inside cavity to top-bezel of monitor (CAM-0 ribbon route)")
pdf.body(
    "Stubs protrude 30 to 40 mm into cavity. Cap with masking tape until commissioning."
)

pdf.h3("VESA backing - inside the cavity")
pdf.body(
    "Carpenter fixes a 12 mm BWP ply backing board (600 mm wide x 400 mm tall) flat "
    "against the cavity back wall, centred. 4 x rawl plug + screw at the four corners. "
    "VESA pattern is 75 x 75 mm so the screw holes for the bracket itself land well "
    "inside this board. Painter applies matte black to ply face along with the rest "
    "of the cavity (Phase 6)."
)

# 5.2 / 5.3 / 5.4 on next page
pdf.h2("5.2  DB (Distribution Board) recess")
pdf.table(
    headers=["Dimension", "Value", "Why"],
    rows=[
        ["Width",                 "400 mm",   "Schneider Acti9 IEF48 outline + clearance"],
        ["Height",                "600 mm",   "48-way DB; tall format"],
        ["Depth",                 "100 mm",   "Flush-mount enclosure depth"],
        ["Bottom edge from FFL",  "1500 mm",  "Top within reach, MCBs at chest height"],
        ["Wall",                  "W wall of foyer", "Behind door swing - hidden when door is open"],
        ["Min offset from frame", "100 mm",   "Door must clear DB cover when open"],
    ],
    col_widths=[58, 50, 76],
)

pdf.h2("5.3  Switch boxes (foyer board on W wall)")
pdf.table(
    headers=["Item", "Box size", "Depth", "Height (FFL)", "Notes"],
    rows=[
        ["Foyer SB1  -  smart 4-gang",
            "230 x 75 mm GI MS",  "65 mm",  "1200 mm centre",
            "FOR SMART SWITCH - 65 mm depth mandatory"],
        ["Foyer 2-way SB (optional, near Living)",
            "75 x 75 mm GI MS",   "65 mm",  "1200 mm centre",
            "If 2-way to Living - 65 mm if smart"],
    ],
    col_widths=[60, 38, 18, 30, 38],
)
pdf.callout("warn", "65 mm boxes, not 50 mm",
    "Smart-switch boxes are 65 mm DEEP, not the standard 50 mm. The Sonoff or "
    "Aqara relay module sits behind the switch plate - 50 mm is too shallow and "
    "the module will not fit. Box sizes (mm): 1-mod 75x75x65, 2-mod 130x75x65, "
    "3-mod 175x75x65, 4-mod 230x75x65.")

pdf.h2("5.4  Conduit chases (channels in the wall)")
pdf.table(
    headers=["Run", "Chase height (FFL)", "Wall", "Conduits"],
    rows=[
        ["DB to ceiling spotlights B1",     "Vertical from DB up to slab", "W", "1 x 25 mm RED"],
        ["DB to screen cavity B2 (power)",  "Vertical + horizontal at 1300 mm", "W -> S", "1 x 25 mm RED"],
        ["DB to switch board SB1",          "Vertical from DB up to 1200 mm", "W", "1 x 25 mm RED"],
        ["Niche to screen cavity",          "Horizontal at 1300 mm",
            "W -> S",   "1 x 25 mm GREY (LV-25)"],
        ["Niche to ceiling speaker",        "Up W wall, then to centre of foyer false ceiling",
            "W -> ceiling",   "1 x 16 mm GREY (LV-16)"],
        ["Cavity to screen-bezel camera",   "Inside cavity wall up to 1620 mm",
            "S wall reveal", "1 x 16 mm GREY (LV-16) sleeve"],
        ["DB to cove driver B10",           "Up W wall, branch above false ceiling",
            "W -> false ceiling",
            "1 x 16 mm GREY (24V DC, secondary side)"],
        ["Door-side run (out to porch)",
            "Horizontal at 1700 mm + branch up to 2400 mm",
            "Inside N wall (around door frame)",
            "2 x 25 mm GREY (CAM-1, CAM-2) + 1 x 16 mm GREY (doorbell + door contact)"],
    ],
    col_widths=[52, 50, 30, 50],
)

pdf.callout("info", "Wall chase rule",
    "Never chase HORIZONTALLY across a 9 in structural wall for more than 1.2 m "
    "without a vertical break. Vertical chases are unrestricted. If a long "
    "horizontal run is needed, drop down then across then back up - never one "
    "long cut.")

# ---------- SECTION 06 - CONDUITS ----------
pdf.section_open("06", "Conduits Required",
                 "Every conduit run that touches the foyer, with size, colour, contents.")

pdf.h2("Conduit colour code")
pdf.table(
    headers=["Colour", "Size", "Carries", "Wire inside"],
    rows=[
        ["RED",  "25 mm",         "Lighting power",                   "1.5 sqmm 3-core"],
        ["BLUE", "25 mm",         "Sockets / AC / heavy power",       "2.5 or 4 sqmm 3-core"],
        ["GREY", "25 mm (LV-25)", "Cat6 / network / camera",          "1 or 2 x Cat6 UTP"],
        ["GREY", "16 mm (LV-16)", "Speaker / sensor / 24V LED",       "2-core 0.75 sqmm"],
    ],
    col_widths=[28, 32, 76, 46],
)
pdf.body(
    "If coloured PVC is not available locally, label every conduit end in coloured "
    "insulation tape AND permanent marker BEFORE plaster covers them. Once plaster "
    "is on, the conduit is invisible - this is the only chance to mark."
)

pdf.h2("All conduits in and out of the foyer")
pdf.table(
    headers=["#", "Run", "Size", "Colour", "Pull cable", "Purpose"],
    rows=[
        ["1",  "DB to 2x ceiling spots (B1)",     "25 mm", "RED",  "3-core 1.5 sqmm",          "Smart spotlights"],
        ["2",  "DB to SB1 switch board feed",     "25 mm", "RED",  "3-core 1.5 + spare neutral","Smart switch with neutral"],
        ["3",  "DB to screen cavity (B2 power)",  "25 mm", "RED",  "3-core 2.5 sqmm",          "230V monitor + RPi"],
        ["4",  "Niche to screen cavity",          "25 mm", "GREY", "1 x Cat6 + draw wire",     "Welcome data to RPi"],
        ["5",  "Niche to ceiling speaker",        "16 mm", "GREY", "2-core 1.5 sqmm speaker",  "Welcome chime"],
        ["6",  "Cavity to top-bezel camera",      "16 mm", "GREY", "RPi CSI ribbon",           "CAM-0 secondary face check"],
        ["7",  "DB to cove driver (B10)",         "16 mm", "GREY", "2-core 1.5 sqmm 24V DC",   "Cove LED secondary side"],
        ["8",  "DB to driver primary",            "25 mm", "RED",  "3-core 1.5 sqmm 230V",     "Cove LED driver mains"],
        ["9",  "Cavity to halo driver",           "16 mm", "GREY", "2-core 0.75 sqmm 24V",     "Halo LED secondary"],
        ["10", "Cavity to shelf driver",          "16 mm", "GREY", "2-core 0.75 sqmm 24V",     "Walnut shelf under-LED"],
        ["11", "Niche to CAM-1 (latch side)",     "25 mm", "GREY", "1 x Cat6 + draw wire",     "Primary face camera"],
        ["12", "Niche to CAM-2 (porch ceiling)",  "25 mm", "GREY", "1 x Cat6 + draw wire",     "Porch overview camera"],
        ["13", "Niche to doorbell (1450 mm)",     "16 mm", "GREY", "1 x Cat6 + 2-core LV",     "Video doorbell + intercom"],
        ["14", "Niche to door contact sensor",    "16 mm", "GREY", "2-core 0.75 sqmm",         "Door-open trigger"],
    ],
    col_widths=[7, 56, 16, 18, 38, 49],
    body_size=8,
)

pdf.callout("warn", "Face-recognition rule",
    "CAM-1 (the face camera) MUST be at face level - 1600 to 1700 mm FFL - "
    "NOT at ceiling height. A high camera sees the top of heads, which gives "
    "Frigate garbage data. Mount on the latch-side wall or jamb so visitors "
    "approach front-on. The high porch camera (CAM-2) is for context and "
    "security only.")

pdf.h2("Outside-the-door conduit terminations")
pdf.table(
    headers=["Point", "Box", "Height (FFL)", "Position", "Note"],
    rows=[
        ["CAM-1 face-capture", "Weatherproof 4 x 4 in IP67",
            "1650 mm", "Latch-side, 150-250 mm from frame",
            "Aim at 1-1.8 m outside threshold"],
        ["CAM-2 porch overview", "Weatherproof 4 x 4 in IP67",
            "2400-2700 mm", "Porch ceiling/soffit corner",
            "Wide 2.8 mm lens, context only"],
        ["Video doorbell", "Modular doorbell box",
            "1400-1450 mm", "Latch side, 150-200 mm from frame",
            "Cat6 + 2-core for flexibility"],
        ["Door contact sensor", "Concealed 16 mm pocket",
            "Door head", "Top of door frame, hinge side",
            "Magnetic reed - dry contact"],
    ],
    col_widths=[36, 38, 24, 50, 40],
)

pdf.h2("Cable budget for the foyer alone")
pdf.table(
    headers=["Cable", "Length", "Where used"],
    rows=[
        ["1.5 sqmm Red (live)",          "approx 25 m", "B1 lighting + B10 driver primary"],
        ["1.5 sqmm Black (neutral)",     "approx 25 m", "Same"],
        ["1.5 sqmm Green/Yellow (earth)","approx 15 m", "Same"],
        ["2.5 sqmm Red",                 "approx 12 m", "B2 cavity power"],
        ["2.5 sqmm Black",               "approx 12 m", "Same"],
        ["2.5 sqmm Green/Yellow",        "approx 6 m",  "Same"],
        ["Cat6 UTP",                     "approx 30 m", "Cavity + CAM-1 + CAM-2 + doorbell"],
        ["2-core 0.75 sqmm 24V",         "approx 10 m", "Halo + shelf + cove (secondary)"],
        ["2-core 1.5 sqmm speaker",      "approx 8 m",  "Niche to ceiling speaker"],
        ["2-core 0.75 sqmm LV",          "approx 6 m",  "Doorbell + door contact sensor"],
    ],
    col_widths=[58, 30, 92],
)

# ---------- SECTION 07 - WIRING ----------
pdf.section_open("07", "Wiring Schedule",
                 "Wire colours, foyer circuits, and the smart switch.")

pdf.h2("Wire colour code (Indian standard, mandatory)")
pdf.table(
    headers=["Colour", "Function", "Where it goes"],
    rows=[
        ["RED",          "LIVE (phase) - 230V hot",   "Every live wire from MCB outward"],
        ["BLACK",        "NEUTRAL - return",          "Every switch board, every socket"],
        ["GREEN/YELLOW", "EARTH",                     "Every switch, socket, metal fitting"],
        ["BLUE",         "Switched LIVE leg",         "Between switch and the load (light)"],
    ],
    col_widths=[40, 56, 84],
)

pdf.h2("Foyer circuit list")
pdf.table(
    headers=["Circuit", "Wire", "MCB / RCBO", "Loads"],
    rows=[
        ["B1  -  Foyer lights",         "1.5 sqmm",            "6A MCB",
            "2 x GU10 spots + walnut shelf strip"],
        ["B2  -  Foyer screen + speaker","1.5 + 2.5 sqmm",     "6A + 16A RCBO",
            "Monitor + RPi USB-C, halo LED secondary, ceiling speaker"],
        ["B10 -  Foyer cove",           "1.5 sqmm + 2-core 24V","6A MCB",
            "24V LED 2700K cove via Meanwell driver"],
    ],
    col_widths=[44, 34, 28, 74],
)

pdf.h2("Foyer SB1  -  4-gang smart, 65 mm box, 1200 mm FFL")
pdf.table(
    headers=["Gang", "Function", "Smart?", "Wired to"],
    rows=[
        ["1 (left)",  "Foyer ceiling spotlights",     "Aqara H1 + Sonoff (65 mm req)", "B1 spotlights"],
        ["2",         "Foyer cove + halo LED scene",  "Smart dimmer", "B10 cove + halo (linked)"],
        ["3",         "Walnut shelf LED strip",       "Smart dimmer", "B1 shelf strip"],
        ["4 (right)", "Spare / future",               "Smart spare",  "Loop wire only, capped"],
    ],
    col_widths=[20, 64, 50, 46],
)

pdf.h3("Smart switch wiring rule")
pdf.body(
    "At every smart-switch gang, leave a 300 mm tail of L + N + E wires inside the "
    "65 mm box. Cap the tails. The Sonoff ZBMINI R2 module is inserted later by "
    "the homeowner - the electrician does NOT install the module. Front of the "
    "box stays open; modular plate fits later."
)

pdf.h3("Welcome screen socket inside cavity")
pdf.body(
    "ONE double 5A socket flush-mounted on the RIGHT inner wall of the cavity at "
    "1300 mm FFL. Hidden behind the monitor when the screen is installed. Both "
    "the monitor power adapter and the RPi USB-C charger plug here."
)

pdf.h3("Speaker wiring")
pdf.body(
    "2-core 1.5 sqmm speaker wire from the staircase niche, through 16 mm grey "
    "conduit, into a B-type ceiling rose box at the centre of the foyer false "
    "ceiling. The 3 in flush ceiling speaker hangs off this rose. Speaker is "
    "driven by a small USB amplifier board (PAM8403) plugged into the home "
    "server's 3.5 mm audio output."
)

# ---------- SECTION 08 - LIGHTING ----------
pdf.section_open("08", "Lighting Plan",
                 "Four layers of light. All 2700K except the amber halo at 2200K.")

# RCP diagram
pdf.draw_rcp(60, pdf.get_y() + 8, 90, 70)
pdf.set_y(pdf.get_y() + 90)

pdf.h2("Foyer lighting layers")
pdf.table(
    headers=["Layer", "Fitting", "Spec", "Position", "Switch"],
    rows=[
        ["Ambient",   "2 x recessed GU10 gimbal",
            "7W 2700K, CRI 90+, adjustable 30 deg",
            "300 mm from W wall, 609 mm and 1218 mm from N edge",
            "SB1 g1"],
        ["Cove",      "24V LED strip in cove pocket",
            "9.6 W/m, 2700K, CRI 90+",
            "Full perimeter of false ceiling, approx 10 m",
            "SB1 g2"],
        ["Accent",    "24V LED inside cavity reveal",
            "4.8 W/m, 2200K (warm amber)",
            "All 4 inner edges of screen cavity, approx 1.7 m",
            "SB1 g2"],
        ["Decorative","24V LED under walnut shelf",
            "6 W/m, 2700K",
            "Under-shelf, full 6 ft, soffit at 900 mm",
            "SB1 g3"],
    ],
    col_widths=[28, 38, 38, 50, 30],
    body_size=8,
)

pdf.h2("Spotlight aiming")
pdf.body(
    "Stone has texture only when light grazes it. Mount the GU10 fittings with "
    "an ADJUSTABLE GIMBAL ring so the beam can be angled 30 degrees toward the "
    "stone wall AFTER installation. Standard fixed downlights point straight "
    "down and miss the texture - do NOT use them."
)
pdf.body(
    "Aim each spot at a point on the stone wall at 1700 mm FFL, with the "
    "spotlight centre 300 mm out from the W wall. Result: two soft circular "
    "pools of light rake across the stone face from above, picking out shadow."
)

pdf.h2("LED drivers (above false ceiling)")
pdf.table(
    headers=["Driver", "Brand / spec", "Output", "Powers"],
    rows=[
        ["DRV-1 (cove)",           "Meanwell 24V 60W",   "24V DC, 2.5A",
            "Cove strip 2700K (10 m at 9.6 W/m = 96W)"],
        ["DRV-2 (halo + shelf)",   "Meanwell 24V 30W",   "24V DC, 1.25A",
            "Halo 1.7 m + Shelf 1.8 m = approx 19W"],
    ],
    col_widths=[36, 50, 30, 68],
)
pdf.callout("info", "Driver sizing",
    "DRV-1 needs to be 60W minimum because cove run is 96W. Use a Meanwell "
    "HLG-100H-24 or run TWO 60W drivers in parallel (split the cove into 2 "
    "halves at the inspection hatch). Never underspec drivers - LED strips "
    "will flicker or burn the driver.")

pdf.h2("Inspection hatch")
pdf.body(
    "Both drivers sit ABOVE the false ceiling. Install ONE 300 x 300 mm gypsum "
    "board hatch with magnet catches in the false ceiling, positioned over the "
    "W wall (DB side, behind the door swing). Hatch must allow hand access to "
    "both drivers for future replacement without removing the whole ceiling."
)

# Wall elevation diagram
pdf.h2("Feature-wall elevation")
pdf.draw_elevation(40, pdf.get_y() + 4, 110, 110)
pdf.set_y(pdf.get_y() + 122)

# ---------- SECTION 09 - FALSE CEILING ----------
pdf.section_open("09", "False Ceiling",
                 "Drop, cove, hatch. The light moves through this volume.")

pdf.h2("Specs")
pdf.kv("Drop from slab",      "2 ft (610 mm) - 11 ft slab to 9 ft finished")
pdf.kv("Material",            "12.5 mm gypsum board on GI grid (Saint-Gobain Gyproc or USG Boral)")
pdf.kv("Cornice",             "Simple POP cornice 75-100 mm at the wall-ceiling junction")
pdf.kv("Cove pocket",         "100 mm wide x 75 mm deep, returns up to slab; full perimeter")
pdf.kv("Inspection hatch",    "1 x 300 x 300 mm with magnet catches, over W wall (DB side)")
pdf.kv("Spotlight cut-outs",  "2 x 75 mm circular cut-outs at marked positions (Section 08)")
pdf.kv("Speaker rose box",    "1 x B-type ceiling rose, foyer centre")
pdf.kv("Finish",              "1.5 mm POP skim + primer + flat emulsion soft snow #F8F4EC")

pdf.h2("Cove cross-section")
pdf.draw_cove_section(35, pdf.get_y() + 8, 130, 50)
pdf.set_y(pdf.get_y() + 60)

pdf.callout("warn", "Don't seal the cove yet",
    "Do NOT seal the cove pocket until the LED strip is laid AND tested. The "
    "strip lives inside the pocket lip. If the cove is closed before strip "
    "install, the whole perimeter has to be re-opened.")

# ---------- SECTION 10 - STONE CLADDING ----------
pdf.section_open("10", "Stone Cladding",
                 "Material, application, and the most-broken rule on stone projects.")

pdf.h2("Material and palette")
pdf.body(
    "Style: RUSTIC LEDGESTONE  -  long, narrow, irregular stones stacked like a "
    "dry stone wall but bonded with mortar. Visual emphasis on texture and shadow."
)
pdf.body(
    "Three colours mixed approximately 50% / 35% / 15%."
)
y0 = pdf.get_y() + 2
chips = [("#7B5C42", "Tobacco 50%"), ("#C8B58F", "Sandstone 35%"), ("#3A3633", "Charcoal 15%")]
for i, (h, l) in enumerate(chips):
    pdf.colour_chip(40 + i * 36, y0, 30, 18, h, l)
pdf.set_y(y0 + 32)

pdf.h2("Coverage and quantity")
pdf.kv("Wall area",          "6 ft x 11 ft = 66 sq ft (6.13 sq m)")
pdf.kv("Less screen cavity", "0.54 m x 0.34 m = 0.18 sq m")
pdf.kv("Net clad area",      "approx 5.95 sq m (64 sq ft)")
pdf.kv("Order qty",          "75 sq ft / 7.0 sq m (with 15% wastage)")
pdf.kv("Adhesive",           "MS polymer high-bond stone adhesive (Pidilite Roff Stone Bond, Fevicol SH-9999, or equivalent) - approx 3 kg per sq m = 21 kg total")
pdf.kv("Mechanical clips",   "SS304 anchor clips for any stone over 5 kg - approx 10 clips")
pdf.kv("Grout",              "RAKED joints (recessed 5 mm) in matching tobacco-brown cement grout")

pdf.h2("Substrate prep")
pdf.bullet("Plaster must be FULLY CURED (minimum 14 days from final coat).")
pdf.bullet("Sand the plaster lightly with 80-grit to give the adhesive bite.")
pdf.bullet("Wipe down with damp cloth and let dry 24 hours.")
pdf.bullet("Apply ONE coat of stone-bond primer (Fosroc Nitobond AR or similar) to "
           "the full wall - even where stone will not go.")
pdf.bullet("Mark the cavity outline + DB recess + switch box positions in chalk.")

pdf.callout("warn", "Stone stops at the cavity edge",
    "NO STONE INSIDE THE CAVITY. The cavity interior was painted matte black "
    "in Phase 6  -  it stays that way. The stone wraps AROUND the cavity, with "
    "the front face of the last stone aligned to the wall's plaster face. "
    "The conduit stubs poking into the cavity from the bottom-left MUST remain "
    "accessible. If a stone covers them, the screen install fails and the wall "
    "has to be cut. Mark the conduit positions on the substrate before cladding "
    "starts.")

pdf.h2("Application sequence")
pdf.bullet("Start at the BOTTOM-CENTRE row. Work outward in both directions, then upward row by row.")
pdf.bullet("Vary stone lengths in each row (ledgestone is irregular by design - avoid vertical seam alignment).")
pdf.bullet("At cavity boundary, CUT stones to land cleanly at the rim. Do not force a long stone over the cavity edge.")
pdf.bullet("At shelf boundary (900 mm FFL), again cut stones to land cleanly. The walnut shelf will be fixed AFTER stone cures (24 hr min).")
pdf.bullet("Press each stone firmly; tap with rubber mallet to seat. Wipe excess adhesive immediately.")
pdf.bullet("Cure 48 hours before grouting; cure another 24 hours before any further trade.")

pdf.h2("Sample procurement (do BEFORE bulk order)")
pdf.checklist([
    "Bring home a 6 in x 6 in sample of each colour (tobacco, sandstone, charcoal).",
    "View the sample on the actual foyer wall location at 3 times: 9 AM, 2 PM, 7 PM.",
    "Test 1 sq ft trial cladding on a hidden wall with the proposed adhesive + grout.",
    "Confirm stone supplier can deliver consistent batch (within 1 dye-lot of trial sample).",
    "Confirm 1 L sample of adhesive to test on plaster.",
])

pdf.h2("Common mistakes to avoid")
pdf.bullet("Using gypsum-based primer or old-style cement slurry as bond coat. Use what the adhesive maker specifies.")
pdf.bullet("Cladding before plaster cures fully. Wet plaster outgases moisture; stones pop off in 6-12 months.")
pdf.bullet("Using flush grout. Ledgestone needs RAKED joints (recessed 5 mm) so stones look stacked, not glued.")
pdf.bullet("Mixing two adhesive batches mid-wall. Mix the whole wall's adhesive in one go.")
pdf.bullet("Forgetting to mask the cavity edge. Adhesive squeeze-out into cavity = uneven cavity edge after cure.")

pdf.kv("Source",      "Local stone specialist in Chitradurga or Bangalore")
pdf.kv("Ask for",     "Rustic ledgestone wall cladding panel - tobacco/sandstone/charcoal mix - matte natural finish - 60-100 mm strip width, 200-400 mm length, 15-25 mm thick")
pdf.kv("Verify",      "6 x 6 in sample home, view in evening light, before bulk order")

# ---------- SECTION 11 - PAINTING ----------
pdf.section_open("11", "Painting",
                 "Three colours, three surfaces. The order matters more than the colours.")

pdf.h2("Surfaces and finishes")
pdf.table(
    headers=["Surface", "Colour (hex)", "Type", "Coats"],
    rows=[
        ["Inside screen cavity (5 surfaces)",     "Matte black #0A0A0A",
            "Acrylic emulsion matte / chalkboard paint", "2"],
        ["Side walls (W + partition)",             "Warm ivory #F2EBDD",
            "Premium washable matte emulsion (Asian Paints Royale Aspira / Berger Silk Glamour)",
            "1 primer + 2 finish"],
        ["False ceiling (gypsum)",                 "Soft snow #F8F4EC",
            "Flat emulsion (Asian Paints Premium / Berger Easy Clean)",
            "1 primer + 2 finish"],
        ["Cove inside surface",                    "Soft snow #F8F4EC",
            "Flat emulsion", "2"],
        ["DB cover plate",                         "(factory finish)",
            "No paint", "-"],
    ],
    col_widths=[58, 36, 70, 20],
)

pdf.callout("warn", "Cavity black BEFORE stone cladding",
    "Inside the screen cavity must be painted before stone (Phase 6, not Phase "
    "10). Once stone wraps the cavity edge, you cannot paint inside cleanly. "
    "Two coats matte black acrylic emulsion. The cavity reads as a deep shadow "
    "behind the screen.")

pdf.h2("Sample procurement (do BEFORE bulk paint)")
pdf.checklist([
    "Sample pots: ivory #F2EBDD, soft snow #F8F4EC, matte black.",
    "Paint 2 ft x 2 ft swatch on each surface.",
    "View at 9 AM (cool morning), 2 PM (bright midday), 7 PM (warm artificial 2700K).",
    "Confirm matte black does NOT shine when raked by the LED halo  -  if it shines, switch to chalkboard or 'flat' interior, never satin or eggshell.",
])

pdf.h2("Masking required during painting")
pdf.checklist([
    "Stone wall: full mask with kraft paper + low-tack tape.",
    "All switch and socket boxes: blue painters tape inside the box opening.",
    "DB recess: cover the whole opening with kraft.",
    "Floor tile: drop sheet across the foyer + 2 m into the Living area.",
    "Cavity edge after stone: protect with painter tape so emulsion does not bleed onto stone.",
])

pdf.kv("Vendor",      "Asian Paints / Berger / Dulux dealer in Chitradurga")
pdf.kv("How to ask",  "Bring this PDF + the master colour palette. Ask for a fan-deck match for each hex - NOT 'off-white'.")
pdf.kv("Volume buy",  "10 L premium emulsion ivory + 5 L flat emulsion soft snow + 1 L matte black")

# ---------- SECTION 12 - CARPENTRY ----------
pdf.section_open("12", "Carpentry",
                 "VESA backing inside the cavity, the walnut floating shelf, the modular plate finish.")

pdf.h2("Item 1  -  VESA backing board (inside cavity)")
pdf.table(
    headers=["Spec", "Value"],
    rows=[
        ["Material",  "12 mm BWP marine ply"],
        ["Size",      "600 mm wide x 400 mm tall"],
        ["Position",  "Centred on back wall of screen cavity, painted matte black face out"],
        ["Fixing",    "4 x rawl plug + 4 x SS countersunk screw (12 mm into masonry)"],
        ["Tolerance", "Face flush or up to 5 mm BEHIND plaster line - never proud"],
    ],
    col_widths=[35, 139],
)

pdf.h2("Item 2  -  Walnut floating shelf")
pdf.table(
    headers=["Spec", "Value"],
    rows=[
        ["Material",      "Solid teak/walnut OR walnut-veneered 25 mm BWP ply"],
        ["Stain",         "Dark walnut #4A3526, oil finish (no high-gloss varnish)"],
        ["Size",          "1828 mm (6 ft) wide x 254 mm (10 in) deep x 35-40 mm thick"],
        ["Top of shelf",  "900 mm FFL"],
        ["Fixing",        "Concealed iron strap brackets (3 nos), 50 x 6 mm flat MS, drilled into masonry then plastered over - shelf slides over straps"],
        ["LED groove",    "Routed channel 12 mm wide x 6 mm deep, 50 mm in from front edge, full 6 ft length"],
        ["LED termination","2-core 0.75 sqmm cable runs through 16 mm conduit (C10) to driver above false ceiling"],
        ["Install order", "AFTER stone cladding has cured 24 hr. Stone receives the brackets BEFORE final stones above shelf line are placed; shelf slides on"],
    ],
    col_widths=[40, 134],
)

pdf.callout("warn", "Brackets are STRUCTURAL",
    "The shelf brackets hold up to 25 kg. They must drill into MASONRY, not "
    "just plaster. Drill through the stone if necessary, plug with high-strength "
    "epoxy + threaded rod. Test pull-out with body weight before placing the "
    "shelf - a shelf falling onto floor tile is expensive.")

pdf.h2("Item 3  -  Optional sub-shelf cubby")
pdf.body(
    "If desired, a small 12 in wide x 4 in deep x 3 in tall cubby can be carved "
    "into the walnut shelf top to discreetly hold keys or a phone. Must be "
    "discussed with the homeowner BEFORE the shelf is finalised - cannot be "
    "retrofitted neatly."
)

pdf.h2("Item 4  -  Modular plate frames")
pdf.body(
    "Schneider Unica champagne (or Legrand Mylinec bronze) modular plates fit on "
    "all switch and socket boxes in the foyer. Single finish across the whole "
    "house. The carpenter does not install these - the electrician does in "
    "Phase 11. Listed here so the carpenter does not match a different finish "
    "on shelf hardware."
)

# ---------- SECTION 13 - MATERIALS ----------
pdf.section_open("13", "Materials & Costs",
                 "Itemised list for the foyer alone. Whole-house items are in ELECTRICIAN_REFERENCE.pdf.")

pdf.body(
    "All prices in INR, approximate as of April 2026, may vary +/- 15% by city. "
    "Whole-house material total is approx 3,38,325 INR  -  many items shared with "
    "other rooms. Foyer-only share below."
)

pdf.h2("A. Civil and finishes")
pdf.table(
    headers=["#", "Item", "Qty", "Unit", "Total", "Source"],
    rows=[
        ["A1",  "Rustic ledgestone (tobacco/sandstone/charcoal)", "75 sq ft", "180/sqft", "13,500", "Local stone, Chitradurga / Bangalore"],
        ["A2",  "MS polymer stone bond (Pidilite Roff)",          "21 kg",    "180/kg",   "3,780",  "Hardware shop"],
        ["A3",  "Tobacco-brown grout (cement-based)",             "5 kg",     "120/kg",   "600",    "Hardware shop"],
        ["A4",  "Stone-bond primer (Fosroc Nitobond AR)",         "2 L",      "550/L",    "1,100",  "Hardware shop"],
        ["A5",  "SS304 mechanical anchor clips",                  "10",       "60",       "600",    "Hardware shop"],
        ["A6",  "Premium washable matte ivory #F2EBDD",           "10 L",     "650/L",    "6,500",  "Asian Paints / Berger"],
        ["A7",  "Flat emulsion soft snow #F8F4EC",                "5 L",      "550/L",    "2,750",  "Same"],
        ["A8",  "Matte black emulsion (cavity)",                  "1 L",      "450/L",    "450",    "Same"],
        ["A9",  "Wall primer + roller / brush kit",               "1 set",    "1,500",    "1,500",  "Same"],
        ["A10", "Solid walnut shelf 6 ft x 10 in x 35 mm",        "1",        "8,000",    "8,000",  "Local carpenter"],
        ["A11", "Concealed flat MS shelf brackets",               "3",        "350",      "1,050",  "Welder + powder coater"],
        ["A12", "12 mm BWP ply VESA backing (600 x 400)",          "1",        "300",      "300",    "Hardware shop"],
        ["A13", "Gypsum board + GI grid + cornice (foyer)",        "1 lot",    "12,000",   "12,000", "Saint-Gobain / USG"],
        ["A14", "Floor tile 1200x1200 warm ivory porcelain",      "30 sq ft", "180/sqft", "5,400",  "Kajaria / Somany"],
    ],
    col_widths=[7, 60, 22, 22, 22, 41],
    body_size=8,
)

pdf.h2("B. Electrical and smart-home (foyer subset)")
pdf.table(
    headers=["#", "Item", "Qty", "Unit", "Total", "Source"],
    rows=[
        ["B1",  "Samsung LS22F350 (21.5 in IPS)",            "1", "8,500", "8,500", "Amazon / Flipkart"],
        ["B2",  "Raspberry Pi Zero 2W",                      "1", "1,800", "1,800", "Robu.in / Evelta.in"],
        ["B3",  "RPi Camera Module 3 + CSI ribbon",          "1", "1,800", "1,800", "Robu.in / Evelta.in"],
        ["B4",  "32 GB microSD (Samsung Class 10)",          "1", "400",   "400",   "Amazon"],
        ["B5",  "Mini HDMI to HDMI 0.5 m",                   "1", "350",   "350",   "Amazon"],
        ["B6",  "USB-C 5V 3A power adapter",                 "1", "500",   "500",   "Amazon"],
        ["B7",  "USB OTG micro to ethernet adapter",         "1", "400",   "400",   "Amazon"],
        ["B8",  "Slim VESA 75 wall mount",                   "1", "600",   "600",   "Amazon"],
        ["B9",  "Recessed GU10 adjustable gimbal",           "2", "350",   "700",   "Amazon"],
        ["B10", "GU10 LED 7W 2700K (Philips)",               "2", "250",   "500",   "Amazon"],
        ["B11", "24V LED strip 9.6 W/m 2700K (cove)",        "10 m", "220/m", "2,200", "Amazon"],
        ["B12", "24V LED strip 4.8 W/m 2200K (halo)",        "2 m",  "180/m", "360",   "Amazon"],
        ["B13", "24V LED strip 6 W/m 2700K (shelf)",         "2 m",  "200/m", "400",   "Amazon"],
        ["B14", "Meanwell 24V 60W LED driver",               "1", "650",   "650",   "Amazon"],
        ["B15", "Meanwell 24V 30W LED driver",               "1", "450",   "450",   "Amazon"],
        ["B16", "Aluminium LED profile + diffuser",          "12 m", "150/m", "1,800", "Amazon"],
        ["B17", "Aqara H1 EU smart switch 2-gang",           "1", "2,800", "2,800", "Amazon"],
        ["B18", "Sonoff ZBMINI R2 Zigbee relay",             "2", "950",   "1,900", "Amazon"],
        ["B19", "65 mm GI MS box 4-mod (230x75x65)",         "1", "150",   "150",   "Hardware shop"],
        ["B20", "Schneider Unica champagne 4-mod plate",     "1", "350",   "350",   "Schneider dealer"],
        ["B21", "Flush ceiling speaker 3 in + rose box",     "1", "1,500", "1,500", "Amazon"],
        ["B22", "Mini USB amp board PAM8403",                "1", "600",   "600",   "Amazon"],
        ["B23", "Hikvision DS-2CD2143G2-LU 4MP 4mm (CAM-1)", "1", "7,000", "7,000", "I Secure India"],
        ["B24", "Hikvision DS-2CD2347G2-LU 2.8mm (CAM-2)",   "1", "6,000", "6,000", "Same"],
        ["B25", "Weatherproof IP67 4x4 in back box",         "2", "600",   "1,200", "Amazon"],
        ["B26", "Wired magnetic reed door contact",          "1", "500",   "500",   "Amazon"],
        ["B27", "Godrej video doorbell + smart lock",        "1", "15,000","15,000","Godrej dealer"],
    ],
    col_widths=[7, 60, 22, 22, 22, 41],
    body_size=8,
)

pdf.h2("C. Conduits, wires, small electricals (foyer subset)")
pdf.table(
    headers=["#", "Item", "Qty", "Unit", "Total"],
    rows=[
        ["C1",  "25 mm PVC conduit (3 m lengths)",       "10 lengths", "80/length",  "800"],
        ["C2",  "16 mm PVC conduit (3 m lengths)",       "5 lengths",  "50/length",  "250"],
        ["C3",  "25 mm 90 deg bends",                    "8",          "15",         "120"],
        ["C4",  "16 mm 90 deg bends",                    "5",          "10",         "50"],
        ["C5",  "Junction boxes 4 x 4 in PVC",            "6",          "35",         "210"],
        ["C6",  "Circular ceiling boxes 60 mm",          "2",          "40",         "80"],
        ["C7",  "1.5 sqmm Red FR-LSH",                   "30 m",       "22/m",       "660"],
        ["C8",  "1.5 sqmm Black FR-LSH",                 "30 m",       "22/m",       "660"],
        ["C9",  "1.5 sqmm Green/Yellow FR-LSH",          "20 m",       "22/m",       "440"],
        ["C10", "2.5 sqmm Red FR-LSH",                   "15 m",       "35/m",       "525"],
        ["C11", "2.5 sqmm Black FR-LSH",                 "15 m",       "35/m",       "525"],
        ["C12", "Cat6 UTP",                              "30 m",       "10.5/m",     "315"],
        ["C13", "2-core 0.75 sqmm 24V",                  "12 m",       "20/m",       "240"],
        ["C14", "2-core 1.5 sqmm speaker",               "10 m",       "30/m",       "300"],
        ["C15", "Cat6 keystone jack",                    "2",          "120",        "240"],
        ["C16", "Cat6 wall plate 1-port",                "1",          "150",        "150"],
        ["C17", "Double 5A modular socket + plate",      "1",          "350",        "350"],
        ["C18", "Conduit draw wire / fish tape",         "1",          "500",        "500"],
    ],
    col_widths=[7, 80, 30, 26, 26],
    body_size=8,
)

pdf.h2("Total foyer materials estimate")
pdf.table(
    headers=["Group", "Subtotal (INR)"],
    rows=[
        ["A. Civil + finishes",                                       "57,430"],
        ["B. Electrical + smart home (foyer subset)",                 "53,210"],
        ["C. Conduits + wires + small electricals",                   "6,415"],
        ["FOYER MATERIALS SUBTOTAL",                                   "approx 1,17,055"],
        ["+ Labour estimate (foyer-only share, 6 trades)",            "30,000 to 50,000"],
        ["GRAND TOTAL (foyer only, materials + labour)",              "approx 1,47,000 to 1,67,000"],
    ],
    col_widths=[122, 56],
)

pdf.callout("info", "Not double-counted",
    "Foyer materials are a SUBSET of the whole-house list (in "
    "ELECTRICIAN_REFERENCE.pdf, total approx 3,38,325 INR). Items like the DB, "
    "MCBs, server, PoE switch, router serve the whole house but enable foyer "
    "features  -  they are NOT double-counted here.")

# ---------- SECTION 14 - SIGN-OFFS ----------
pdf.section_open("14", "Sign-off Checklists",
                 "Each trade signs their section before the next phase begins. If any check fails, the trade does not leave site.")

def signoff_block(title, items):
    if pdf.get_y() > 230:
        pdf.add_page()
    pdf.h2(title)
    pdf.checklist(items)
    pdf.ln(1)
    pdf.set_font("Verdana", "I", 9)
    pdf.set_text_color(*INK_MUTED)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 5, "Name: ____________________________     Date: __________     Signature: ____________________________",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*INK)
    pdf.ln(3)

signoff_block("14.1  Mason / Civil", [
    "Screen cavity cut to 540 W x 340 H x 100 D mm (verify with tape).",
    "Bottom of cavity at 1280 mm FFL (measure from finished floor tile).",
    "Cavity centred on the 6 ft wall (644 mm from each side).",
    "DB recess 400 W x 600 H x 100 D mm at 1500 mm FFL (bottom edge).",
    "All switch boxes set: Foyer SB1 = 65 mm DEEP GI MS box (4-mod 230x75x65).",
    "Conduit chases at correct heights (300 mm sockets, 1200 mm switches, ceiling).",
    "Three conduit stubs visible inside cavity bottom-left corner.",
    "Plaster cured 14 days before stone cladding starts.",
    "All conduits flush with finished plaster - no protrusion, no burial.",
])

signoff_block("14.2  Electrician", [
    "All conduits laid per Section 06 with correct colours (or labelled if grey).",
    "Draw wires inserted in every conduit and ends taped.",
    "Wires pulled per Section 07 with correct colours (R live / B neutral / G-Y earth).",
    "Every smart-switch box has L + N + E tail (300 mm long, capped).",
    "Earth continuity tested at every box and metal fitting (less than 1 ohm).",
    "DB Schneider Acti9 IEF48 mounted at 1500 mm FFL, MCBs/RCBOs per circuit list.",
    "Foyer screen socket at 1300 mm FFL inside cavity (right inner wall).",
    "B1 spotlight ceiling boxes at correct positions (300 mm from W; 609/1218 mm from N).",
    "Cove driver primary fed from B10 conduit.",
    "Cat6 from staircase niche to: cavity, CAM-1 (door), CAM-2 (porch). Tested.",
    "16 mm sleeve from cavity bottom to top-bezel (CAM-0 ribbon route) clear.",
    "Speaker wire to ceiling rose box terminated.",
])

signoff_block("14.3  Gypsum / POP contractor", [
    "False ceiling at 9 ft uniformly (max 5 mm tolerance corner-to-corner).",
    "Cove pocket 100 mm wide x 75 mm deep, full perimeter, no gaps.",
    "Inspection hatch 300 x 300 mm with magnet catch over W wall (DB side).",
    "Spotlight cut-outs at exact marked positions.",
    "Speaker rose box at foyer centre.",
    "POP cornice continuous, mitred at corners.",
    "Cove inside surface skim-coated and primed (ready for paint).",
    "Cove pocket NOT sealed (LED strip lays in later).",
])

signoff_block("14.4  Painter", [
    "PHASE 6 - Inside cavity: 2 coats matte black, all 5 surfaces, no shine.",
    "PHASE 6 - VESA backing ply included in matte black.",
    "PHASE 10 - Side walls: warm ivory #F2EBDD, 1 primer + 2 finish coats, even.",
    "PHASE 10 - Ceiling: soft snow #F8F4EC, 1 primer + 2 finish.",
    "PHASE 10 - Cove inside: same soft snow.",
    "Stone wall fully masked during side wall + ceiling paint - no overspray.",
    "All switch + socket boxes masked - paint does not enter modular openings.",
    "Drop sheet protection of floor tile - no paint marks on tile after de-mask.",
    "Sample 2 ft x 2 ft viewed at 9 AM, 2 PM, 7 PM and approved by homeowner BEFORE bulk.",
])

signoff_block("14.5  Stone cladder", [
    "Substrate prep done (sanded, primed with stone-bond primer).",
    "Sample (6 in x 6 in each colour) viewed and approved by homeowner.",
    "Trial 1 sq ft cladding done on hidden wall to verify bond and grout.",
    "Mix proportion: approx 50% tobacco / 35% sandstone / 15% charcoal.",
    "Stone STOPS at cavity edge - cavity opening is clean rectangle.",
    "Stone STOPS at shelf line - clean horizontal break for shelf brackets.",
    "Conduit stubs in cavity bottom-left REMAIN ACCESSIBLE.",
    "All stones over 5 kg backed with SS304 mechanical clip.",
    "Joints raked 5 mm (recessed grout) for stacked-stone look.",
    "Adhesive squeeze-out cleaned within working time (before cure).",
    "48 hr cure before grouting; 72 hr total before next trade.",
])

signoff_block("14.6  Carpenter", [
    "VESA ply backing 12 mm BWP, 600 x 400 mm, fixed centred to cavity back wall.",
    "VESA ply face flush or recessed (max 5 mm) - never proud of cavity wall.",
    "Walnut shelf 6 ft x 10 in x 35-40 mm, dark walnut oil finish.",
    "Shelf top at 900 mm FFL, level (max 1 mm corner-to-corner).",
    "3 x concealed flat MS brackets drilled into masonry behind stone.",
    "Brackets pull-tested to 25 kg before shelf placement.",
    "LED groove routed under shelf, 12 mm wide x 6 mm deep, 50 mm in from front.",
    "LED cable led through 16 mm conduit to driver above ceiling.",
    "Modular plate finish (Schneider Unica champagne) confirmed before order.",
])

signoff_block("14.7  Smart-home installer", [
    "Samsung LS22F350 mounted on VESA bracket inside cavity, level.",
    "RPi Zero 2W secured behind monitor, microSD with HA-Dashboard image.",
    "RPi Camera Module 3 mounted top-bezel, ribbon routed through 16 mm sleeve.",
    "CAM-1 mounted outside main door, latch side, 1650 mm FFL.",
    "CAM-1 aim verified: face-on to visitor at 1-1.8 m from door.",
    "CAM-2 mounted porch ceiling/soffit corner.",
    "Both cameras connected to TP-Link TL-SG1210P PoE switch in staircase niche.",
    "Frigate NVR running on Beelink EQ12, all cameras streaming RTSP.",
    "CompreFace registered with min 3 family members (multiple angles each).",
    "HA automation: known face -> welcome + chime; unknown -> idle.",
    "Foyer ceiling speaker connected, chime audible at conversational distance.",
    "Smart switch (Aqara H1 EU 2-gang) bound to HA, dimming works for: spots, cove, halo, shelf.",
    "End-to-end test: 3 family faces detected, welcome shown, chime played.",
    "Stranger test: idle screen, no false trigger.",
    "Doorbell + lock (Godrej) tested: ring -> intercom on screen, lock release works.",
    "Door contact sensor: door open -> HA event recorded -> screen wakes from idle.",
])

signoff_block("14.8  Homeowner final acceptance", [
    "All 7 trade sign-offs above are signed.",
    "Foyer photos: day light, evening with lights on, with welcome screen active.",
    "Walk-through: stand at door, approach, watch welcome trigger, enter foyer.",
    "Manual override of all lights via foyer SB1 (4-gang) tested.",
    "All cables labelled in DB, photo of DB taken and stored.",
    "Spare keys to DB cabinet handed over.",
    "Driver inspection hatch operable.",
    "Stone wall touch-test: no loose stones, no visible adhesive, joints clean.",
    "Welcome system source code + HA config exported to USB and stored offline.",
    "1 month warranty period documented for: stone, paint, electrical, smart-home.",
])

# ---------- APPENDIX ----------
pdf.section_open("A", "Glossary & Cross-references",
                 "Definitions, where to read more, and emergency contacts.")

pdf.h2("A.1  Glossary")
glossary = [
    ("FFL",       "Finished Floor Level - top of installed floor tile (NOT raw slab)."),
    ("DB",        "Distribution Board - panel with MCBs / RCCBs / RCBOs that splits incoming mains."),
    ("MCB",       "Miniature Circuit Breaker - trips on overload."),
    ("RCCB",      "Residual Current Circuit Breaker - trips on earth leakage (life safety)."),
    ("RCBO",      "Combined MCB + RCCB on a single circuit (used for AC, geyser, wet rooms)."),
    ("PIR",       "Passive Infra-Red occupancy sensor - turns lights on when motion detected."),
    ("PoE",       "Power over Ethernet - power + data on one Cat6 cable."),
    ("CAM-1",     "Primary face-capture camera - outside main door, latch-side, 1650 mm FFL."),
    ("CAM-0",     "Screen-bezel camera - inside cavity bezel, secondary close-range face check."),
    ("RPi",       "Raspberry Pi - small Linux computer; here a Zero 2W drives the welcome screen."),
    ("Frigate",   "Open-source NVR with on-device AI; identifies people from RTSP streams."),
    ("CompreFace","Open-source face recognition service, runs on home server."),
    ("HA",        "Home Assistant - the central automation hub."),
    ("LV-25",     "Low-voltage 25 mm grey conduit - Cat6 / network / camera data."),
    ("LV-16",     "Low-voltage 16 mm grey conduit - speaker / sensor / 24V LED."),
    ("Cove",      "Recessed channel along ceiling perimeter that hides an LED strip."),
    ("VESA",      "Standard mounting hole pattern on the back of monitors (here 75 x 75 mm)."),
]
for k, v in glossary:
    pdf.kv(k, v, key_w=22)

pdf.h2("A.2  Cross-references")
pdf.kv("Whole-house electrical", "electrical/conduits-and-cavities.md")
pdf.kv("Whole-house circuits",   "electrical/db-layout.md")
pdf.kv("Whole-house master spec","interior-design/master-interior-spec.md")
pdf.kv("Whole-house palette",    "materials-finishes/master-color-palette.md")
pdf.kv("Foyer render (approved)","interior-design/generated-images/foyer-wall-rustic-stone-v1.png")
pdf.kv("Living-from-foyer",      "interior-design/generated-images/living-from-foyer-warm-premium-v2.png")
pdf.kv("Materials (whole-house)","electrical/materials-checklist.md")
pdf.kv("Electrician PDF",        "pdfs/ELECTRICIAN_REFERENCE.pdf")
pdf.kv("Interior PDF",           "pdfs/INTERIOR_SUGGESTIONS.pdf")
pdf.kv("Decisions log",          "decisions/decision-log.md")

pdf.h2("A.3  Emergency contacts (fill in)")
contacts = [
    "Mason",
    "Electrician",
    "Stone cladder",
    "Painter",
    "Carpenter",
    "Gypsum / POP",
    "Smart-home installer",
    "Schneider DB dealer",
    "Stone supplier",
    "I Secure India (Hikvision dealer, Chitradurga)",
    "Asian Paints / Berger dealer",
]
for label in contacts:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Verdana", "B", 9.5); pdf.set_text_color(*ACCENT_DK)
    pdf.cell(60, 6, clean(label))
    pdf.set_font("Verdana", "", 9.5); pdf.set_text_color(*INK_MUTED)
    pdf.cell(0, 6, "______________________________________________",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.ln(4)
pdf.set_font("Georgia", "I", 9)
pdf.set_text_color(*INK_MUTED)
pdf.multi_cell(0, 5,
    clean("End of document. v2.0 - 2026-05-10. Regenerable from "
          "pdfs/build_foyer_pdf.py. Update the script and re-run to produce a "
          "new version. Hand a printed copy to every trade BEFORE work starts."))

# ---------- WRITE ----------
pdf.output(str(OUT))
print(f"Wrote: {OUT}")
print(f"Pages: {pdf.page_no()}")
