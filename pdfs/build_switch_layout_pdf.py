"""
Build the Switch Layout Master Plan PDF.
For: Electrician, Mason, Civil contractor, Owner.

Visual design v2 — editorial, cream + warm-gold palette, vector diagrams
(no ASCII art), generous whitespace, switch-board info cards with a gold
left accent bar.

Source-of-truth markdown:
  electrical/ground-floor-electrical.md
  electrical/first-floor-electrical.md
  electrical/conduits-and-cavities.md
  electrical/materials-checklist.md
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "SWITCH_LAYOUT.pdf"

# ---------- Refined editorial palette ----------
INK         = ( 28,  28,  30)      # primary ink (warm black)
INK_SOFT    = ( 90,  90,  95)      # secondary text
INK_FAINT   = (140, 140, 145)      # captions, page numbers
RULE        = (220, 215, 205)      # thin grey rules
ROW_TINT    = (250, 246, 238)      # alternating table row tint
PAPER_TINT  = (252, 248, 240)      # soft page tint blocks

GOLD        = (172, 130,  50)      # accent
GOLD_DARK   = (130,  95,  30)      # accent dark
GOLD_PALE   = (245, 234, 210)      # subtle gold tint
GOLD_BAR    = (190, 150,  70)      # bars / vertical accents

DANGER      = (180,  60,  50)
DANGER_PALE = (250, 230, 225)
INFO        = ( 50, 100, 160)
INFO_PALE   = (228, 238, 250)
GOOD        = ( 70, 125,  70)
GOOD_PALE   = (228, 244, 230)
WARN        = (180, 130,  40)
WARN_PALE   = (252, 240, 215)


# ---------- PDF helpers ----------
class SwitchPDF(FPDF):
    PAGE_MARGIN_X = 18
    PAGE_MARGIN_TOP = 18
    PAGE_MARGIN_BOTTOM = 16
    CONTENT_W = 210 - 2 * 18  # 174

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=self.PAGE_MARGIN_BOTTOM)
        self.set_margins(self.PAGE_MARGIN_X, self.PAGE_MARGIN_TOP, self.PAGE_MARGIN_X)
        self._section_label = ""

    # ---------- running header / footer ----------
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(8)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*INK_FAINT)
        # left: section label
        self.set_x(self.PAGE_MARGIN_X)
        self.cell(self.CONTENT_W / 2, 5,
                  self._section_label.upper() if self._section_label else "SWITCH LAYOUT MASTER PLAN",
                  align="L")
        # right: page number
        self.set_x(self.PAGE_MARGIN_X + self.CONTENT_W / 2)
        self.cell(self.CONTENT_W / 2, 5, f"{self.page_no():02d}", align="R")
        # thin gold rule
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.25)
        self.line(self.PAGE_MARGIN_X, 15, 210 - self.PAGE_MARGIN_X, 15)
        self.set_xy(self.PAGE_MARGIN_X, self.PAGE_MARGIN_TOP)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*INK_FAINT)
        self.cell(0, 5,
                  "v2.0   -   2026-05-10   -   Hand to electrician + mason BEFORE chasing or plastering",
                  align="C")

    # ---------- typography ----------
    def set_section(self, label):
        self._section_label = label

    def h1(self, text, subtitle=None):
        """Big chapter title with thin gold rule."""
        self.set_x(self.PAGE_MARGIN_X)
        self.ln(2)
        self.set_x(self.PAGE_MARGIN_X)
        self.set_font("Helvetica", "", 24)
        self.set_text_color(*INK)
        self.multi_cell(0, 11, text)
        if subtitle:
            self.set_x(self.PAGE_MARGIN_X)
            self.set_font("Helvetica", "I", 11)
            self.set_text_color(*INK_SOFT)
            self.multi_cell(0, 5.5, subtitle)
        self.ln(1)
        # gold underline rule, short
        y = self.get_y() + 1
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.6)
        self.line(self.PAGE_MARGIN_X, y, self.PAGE_MARGIN_X + 22, y)
        self.set_line_width(0.2)
        self.ln(6)

    def h2(self, text):
        """Section heading with gold left bar."""
        self.ln(2)
        y = self.get_y()
        # gold bar
        self.set_fill_color(*GOLD_BAR)
        self.rect(self.PAGE_MARGIN_X, y + 1.2, 1.4, 5.6, "F")
        # text
        self.set_xy(self.PAGE_MARGIN_X + 4, y)
        self.set_font("Helvetica", "B", 12.5)
        self.set_text_color(*INK)
        self.cell(0, 8, text, ln=1)
        self.ln(0.5)

    def h3(self, text):
        self.ln(0.5)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 6, text, ln=1)

    def body(self, text, size=10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*INK)
        self.multi_cell(0, 5.2, text)
        self.ln(1.5)

    def lead(self, text):
        """Slightly larger italic intro paragraph."""
        self.set_font("Helvetica", "I", 10.5)
        self.set_text_color(*INK_SOFT)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
        self.set_text_color(*INK)

    def small(self, text):
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*INK_FAINT)
        self.multi_cell(0, 4.2, text)
        self.ln(1)

    # ---------- callouts (left bar style, much cleaner) ----------
    def _callout(self, label, text, bar_color, label_color, fill_color=None):
        self.ln(1)
        # measure body height
        self.set_font("Helvetica", "", 9.6)
        # Estimate text height
        x0 = self.PAGE_MARGIN_X
        body_x = x0 + 5
        body_w = self.CONTENT_W - 5
        # render in two passes: measure first
        y_start = self.get_y()
        # label line
        self.set_xy(body_x, y_start)
        self.set_font("Helvetica", "B", 9.2)
        self.set_text_color(*label_color)
        self.cell(0, 5.5, label.upper(), ln=1)
        # body
        self.set_x(body_x)
        self.set_font("Helvetica", "", 9.6)
        self.set_text_color(*INK)
        self.multi_cell(body_w, 5.0, text)
        y_end = self.get_y()
        # gold bar on the left
        self.set_fill_color(*bar_color)
        self.rect(x0, y_start + 0.5, 1.4, y_end - y_start - 0.5, "F")
        # subtle background tint if requested
        if fill_color:
            # redraw on top of background — easier: skip background to keep it clean
            pass
        self.ln(2)

    def callout(self, label, text):
        self._callout(label, text, GOLD_BAR, GOLD_DARK)

    def callout_info(self, label, text):
        self._callout(label, text, INFO, INFO)

    def callout_good(self, label, text):
        self._callout(label, text, GOOD, GOOD)

    def callout_warn(self, label, text):
        self._callout(label, text, WARN, WARN)

    def callout_danger(self, label, text):
        self._callout(label, text, DANGER, DANGER)

    # ---------- key-value rows (cleaner, no leading colon) ----------
    def kv(self, key, value, key_w=42):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*INK_SOFT)
        self.set_x(self.PAGE_MARGIN_X + 1)
        self.cell(key_w, 5.4, key, ln=0)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*INK)
        avail = self.CONTENT_W - key_w - 1
        self.multi_cell(avail, 5.4, value)

    # ---------- text safety ----------
    def _safe_break(self, text, max_w):
        if not text:
            return text
        words = str(text).split(" ")
        out = []
        for w in words:
            if self.get_string_width(w) <= max_w - 2:
                out.append(w)
            else:
                chunk = ""
                for ch in w:
                    if self.get_string_width(chunk + ch) > max_w - 2:
                        out.append(chunk)
                        chunk = ch
                    else:
                        chunk += ch
                if chunk:
                    out.append(chunk)
        return " ".join(out)

    # ---------- table (cleaner, hairline rules only) ----------
    def table(self, headers, rows, col_widths, font=9, line_h=4.5,
              header_bg=None, header_fg=(255, 255, 255), zebra=True):
        if header_bg is None:
            header_bg = INK

        def draw_header():
            self.set_font("Helvetica", "B", font)
            self.set_fill_color(*header_bg)
            self.set_text_color(*header_fg)
            self.set_draw_color(*header_bg)
            self.set_line_width(0.1)
            for h, w in zip(headers, col_widths):
                self.cell(w, 7, "  " + self._safe_break(h, w), border=0,
                          align="L", fill=True)
            self.ln(7)

        draw_header()
        self.set_text_color(*INK)
        self.set_font("Helvetica", "", font)
        rows = [
            [self._safe_break(c, col_widths[i]) for i, c in enumerate(r)]
            for r in rows
        ]
        fill = False
        for row in rows:
            lines_needed = []
            for cell, w in zip(row, col_widths):
                if not cell:
                    lines_needed.append(1)
                    continue
                segments = str(cell).split("\n")
                tot = 0
                for seg in segments:
                    sw = self.get_string_width(seg) if seg else 0
                    avail = max(w - 4, 5)
                    tot += max(1, -(-int(sw // avail) - 1))
                lines_needed.append(max(1, tot))
            row_lines = max(lines_needed)
            row_h = max(row_lines * line_h + 2, 6.5)
            if self.get_y() + row_h > self.h - self.PAGE_MARGIN_BOTTOM - 6:
                self.add_page()
                draw_header()
                self.set_text_color(*INK)
                self.set_font("Helvetica", "", font)
            x_start, y_start = self.get_x(), self.get_y()
            # row background (zebra)
            if zebra and fill:
                self.set_fill_color(*ROW_TINT)
                self.rect(x_start, y_start, sum(col_widths), row_h, "F")
            # cell text
            self.set_xy(x_start, y_start)
            for i, (cell, w) in enumerate(zip(row, col_widths)):
                cur_x, cur_y = self.get_x(), self.get_y()
                content_h = max(1, lines_needed[i]) * line_h
                offset_y = max(0, (row_h - content_h) / 2)
                self.set_xy(cur_x + 2, cur_y + offset_y)
                self.set_text_color(*INK)
                self.multi_cell(w - 4, line_h, str(cell), border=0, align="L", fill=False)
                self.set_xy(cur_x + w, cur_y)
            # bottom hairline rule
            self.set_draw_color(*RULE)
            self.set_line_width(0.15)
            self.line(x_start, y_start + row_h,
                      x_start + sum(col_widths), y_start + row_h)
            self.set_xy(x_start, y_start + row_h)
            fill = not fill
        self.ln(3)

    # ---------- switch-board card ----------
    def board_card(self, board_id, location, height_mm, plate, box_depth,
                   circuits, gangs=None, smart_count=None, note=None):
        """Render a switch-board info card with a gold left bar.

        gangs: list of (gang_label, controls, smart_label, note) tuples.
        """
        x0 = self.PAGE_MARGIN_X
        # title strip
        self.ln(2)
        y_start = self.get_y()
        # title row
        self.set_xy(x0 + 5, y_start)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*INK)
        self.cell(60, 6.5, board_id, ln=0)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*INK_SOFT)
        self.cell(0, 6.5, location, ln=1)
        # thin separator under title
        sep_y = self.get_y() + 0.5
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(x0 + 5, sep_y, x0 + self.CONTENT_W, sep_y)
        self.ln(2)

        # facts (two-column key/value)
        facts = [
            ("Height", f"{height_mm} mm FFL" if isinstance(height_mm, (int, str)) and str(height_mm) and str(height_mm) != "—" else str(height_mm)),
            ("Plate", plate),
            ("Box depth", box_depth),
            ("Circuit", circuits),
        ]
        if smart_count:
            facts.append(("Smart gangs", smart_count))
        for k, v in facts:
            self.set_x(x0 + 5)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*INK_SOFT)
            self.cell(28, 5.2, k, ln=0)
            self.set_font("Helvetica", "", 9.6)
            self.set_text_color(*INK)
            self.multi_cell(self.CONTENT_W - 5 - 28, 5.2, str(v))

        # gangs mini-table
        if gangs:
            self.ln(0.5)
            self.set_x(x0 + 5)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*GOLD_DARK)
            self.cell(0, 5.2, "Gang assignments", ln=1)
            self.set_x(x0 + 5)
            # column widths (within content area minus the 5mm bar offset)
            tbl_w = self.CONTENT_W - 5
            col_w = [10, tbl_w * 0.55 - 5, 22, tbl_w - 10 - (tbl_w * 0.55 - 5) - 22]
            # header
            self.set_font("Helvetica", "B", 8.5)
            self.set_fill_color(*INK)
            self.set_text_color(255, 255, 255)
            for h, w in zip(["#", "Controls", "Type", "Notes"], col_w):
                self.cell(w, 5.6, "  " + h, fill=True, ln=0, align="L")
            self.ln(5.6)
            # body rows with hairline
            self.set_font("Helvetica", "", 8.6)
            self.set_text_color(*INK)
            zebra = False
            for gang_no, controls, smart_lbl, gnote in gangs:
                self.set_x(x0 + 5)
                row_x, row_y = self.get_x(), self.get_y()
                # determine row height by wrapped text
                widths = col_w
                cells = [str(gang_no), self._safe_break(controls, widths[1]),
                         smart_lbl, self._safe_break(gnote or "", widths[3])]
                lines = []
                for c, w in zip(cells, widths):
                    if not c:
                        lines.append(1); continue
                    sw = self.get_string_width(c)
                    avail = max(w - 4, 5)
                    lines.append(max(1, -(-int(sw // avail) - 1)))
                rh = max(max(lines) * 4.2 + 2, 6)
                if zebra:
                    self.set_fill_color(*ROW_TINT)
                    self.rect(row_x, row_y, sum(widths), rh, "F")
                self.set_xy(row_x, row_y)
                for i, (c, w) in enumerate(zip(cells, widths)):
                    cx, cy = self.get_x(), self.get_y()
                    offset = (rh - lines[i] * 4.2) / 2
                    if i == 2:
                        # type badge styling
                        self._badge_inline(c, cx + 2, cy + offset - 0.4, w - 4)
                    else:
                        self.set_xy(cx + 2, cy + offset)
                        self.set_text_color(*INK)
                        self.set_font("Helvetica", "", 8.6)
                        self.multi_cell(w - 4, 4.2, c, border=0, align="L", fill=False)
                    self.set_xy(cx + w, cy)
                # bottom hairline
                self.set_draw_color(*RULE)
                self.set_line_width(0.15)
                self.line(row_x, row_y + rh, row_x + sum(widths), row_y + rh)
                self.set_xy(row_x, row_y + rh)
                zebra = not zebra

        if note:
            self.ln(1)
            self.set_x(x0 + 5)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*INK_SOFT)
            self.multi_cell(self.CONTENT_W - 5, 4.6, "Note  -  " + note)

        # gold left bar spanning the whole card
        y_end = self.get_y() + 1
        self.set_fill_color(*GOLD_BAR)
        self.rect(x0, y_start + 0.5, 1.6, y_end - y_start - 0.5, "F")

        self.ln(3)

    def _badge_inline(self, label, x, y, w):
        """Small colored badge for Smart / Dumb / Smart 2-way etc."""
        text = (label or "").strip()
        l = text.lower()
        if l.startswith("smart scene"):
            bg, fg = (220, 230, 248), (40,  80, 140)
        elif l.startswith("smart 2-way"):
            bg, fg = (220, 235, 246), (40,  90, 140)
        elif l.startswith("smart-ready"):
            bg, fg = (235, 240, 245), (90,  95, 110)
        elif l.startswith("smart"):
            bg, fg = (228, 238, 250), (40,  80, 140)
        elif "pir" in l or l.startswith("auto"):
            bg, fg = GOOD_PALE, GOOD
        elif "dumb" in l:
            bg, fg = (235, 235, 232), ( 90,  90,  90)
        else:
            bg, fg = GOLD_PALE, GOLD_DARK
        # draw badge
        self.set_xy(x, y)
        self.set_fill_color(*bg)
        self.set_text_color(*fg)
        self.set_font("Helvetica", "B", 7.6)
        # measured width
        tw = self.get_string_width(text) + 4
        if tw > w - 1: tw = w - 1
        self.rect(x, y + 0.4, tw, 4.4, "F")
        self.set_xy(x + 1.5, y + 0.4)
        self.cell(tw - 3, 4.4, text, align="L")

    # ---------- vector diagrams ----------
    def heights_diagram(self, x, y, w, h):
        """Draw an architectural elevation showing standard mounting heights."""
        # frame
        self.set_draw_color(*RULE)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "D")
        # interior wall fill (very subtle)
        self.set_fill_color(*PAPER_TINT)
        self.rect(x + 0.5, y + 0.5, w - 1, h - 1, "F")

        # max height shown = 2700mm; map to vertical pixels
        max_mm = 2700
        floor_y = y + h - 6   # FFL line position inside
        top_y = y + 6
        usable = floor_y - top_y

        def to_y(mm):
            return floor_y - (mm / max_mm) * usable

        # FFL ground hatch line
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.line(x + 4, floor_y, x + w - 4, floor_y)
        # hatching below FFL
        self.set_line_width(0.18)
        for i in range(0, int(w - 8), 3):
            self.line(x + 4 + i, floor_y, x + 4 + i + 2, floor_y + 2.5)
        # FFL label
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*INK)
        self.text(x + 6, floor_y + 4.5, "FFL  (Finished Floor Level)")

        # measurement points
        marks = [
            (2400, "Wi-Fi router / AP plate", "FF Living central wall only"),
            (1850, "AC sockets",               "20A, dedicated RCBO per AC"),
            (1200, "ALL switch boards",        "smart + dumb, every room"),
            (1100, "Kitchen counter sockets",  "above counter line"),
            (1050, "Geyser switches",          "always OUTSIDE bathroom"),
            ( 600, "Bedside sockets",          "5A + USB-C, both bedsides"),
            ( 300, "General wall sockets",     "perimeter, TV wall, fridge"),
        ]

        # left column = wall
        wall_x = x + 8
        # mark lines
        self.set_font("Helvetica", "", 8.6)
        for mm, label, sub in marks:
            my = to_y(mm)
            # tick line
            self.set_draw_color(*GOLD_BAR)
            self.set_line_width(0.5)
            self.line(wall_x, my, wall_x + 18, my)
            # dimension dot
            self.set_fill_color(*GOLD_DARK)
            self.ellipse(wall_x + 18 - 1.4, my - 1.4, 2.8, 2.8, "F")
            # mm label (bold)
            self.set_font("Helvetica", "B", 9.2)
            self.set_text_color(*GOLD_DARK)
            self.text(wall_x + 22, my + 1.2, f"{mm} mm")
            # label
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*INK)
            self.text(wall_x + 44, my - 0.6, label)
            # sub-label
            self.set_font("Helvetica", "I", 8.2)
            self.set_text_color(*INK_SOFT)
            self.text(wall_x + 44, my + 3.2, sub)

    def box_depth_diagram(self, x, y, w, h):
        """Side-by-side 50mm vs 65mm wall box drawings."""
        # split horizontally
        gap = 8
        bw = (w - gap) / 2
        # left = 50mm BAD
        self._single_box(x, y, bw, h, depth_mm=50, ok=False,
                         title="STANDARD 50 mm",
                         subtitle="Indian default - DO NOT USE for smart switches")
        # right = 65mm GOOD
        self._single_box(x + bw + gap, y, bw, h, depth_mm=65, ok=True,
                         title="SONOFF-READY 65 mm",
                         subtitle="USE for every smart-switch board")

    def _single_box(self, x, y, w, h, depth_mm, ok, title, subtitle):
        # outer card
        self.set_draw_color(*(GOOD if ok else DANGER))
        self.set_line_width(0.6)
        self.rect(x, y, w, h, "D")
        # title bar
        self.set_fill_color(*(GOOD_PALE if ok else DANGER_PALE))
        self.rect(x + 0.5, y + 0.5, w - 1, 9, "F")
        self.set_xy(x + 3, y + 1.2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*(GOOD if ok else DANGER))
        self.cell(w - 6, 7, title)
        # subtitle
        self.set_xy(x + 3, y + 11)
        self.set_font("Helvetica", "I", 8.4)
        self.set_text_color(*INK_SOFT)
        self.multi_cell(w - 6, 4.2, subtitle)

        # the BOX itself drawn proportionally (side cross-section view)
        # box area below subtitle
        box_top = y + 22
        box_h_avail = h - 22 - 4
        # depth scale: 65mm = full visible width slot
        # show both at same internal scale: 50→smaller slot, 65→bigger slot
        max_depth = 75  # mm visual scale
        # vertical box body
        body_w = w * 0.4
        body_x = x + (w - body_w) / 2
        body_h = box_h_avail * 0.7
        body_y = box_top
        # depth fill proportion
        fill_h = body_h * (depth_mm / max_depth)
        # outer wall of box
        self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.35)
        self.set_fill_color(255, 255, 255)
        self.rect(body_x, body_y, body_w, body_h, "FD")
        # depth fill (gold tint)
        self.set_fill_color(*(GOOD_PALE if ok else DANGER_PALE))
        self.rect(body_x + 1, body_y + body_h - fill_h, body_w - 2, fill_h - 1, "F")
        # depth label inside box
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*INK)
        cx = body_x + body_w / 2
        self.text(cx - self.get_string_width(f"{depth_mm} mm") / 2,
                  body_y + body_h - fill_h / 2 + 1.5, f"{depth_mm} mm")
        # depth side dimension arrow
        ax = body_x + body_w + 3
        self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.3)
        self.line(ax, body_y + body_h - fill_h, ax, body_y + body_h)
        self.line(ax - 1.5, body_y + body_h - fill_h, ax + 1.5, body_y + body_h - fill_h)
        self.line(ax - 1.5, body_y + body_h, ax + 1.5, body_y + body_h)
        # symbol below
        sym_y = body_y + body_h + 5
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*(GOOD if ok else DANGER))
        sym = "OK" if ok else "X"
        self.text(cx - self.get_string_width(sym) / 2, sym_y, sym)
        # caption
        self.set_font("Helvetica", "", 8.6)
        self.set_text_color(*INK_SOFT)
        cap = ("Aqara H1 / Sonoff relay\nfits behind plate"
               if ok else "Relay can't fit -\nplate won't sit flush")
        self.set_xy(x + 3, sym_y + 3)
        self.multi_cell(w - 6, 4, cap, align="C")

    def plate_diagram(self, x, y, gangs, smart=True, indicators=True,
                      label=None, sub=None):
        """Draw a switch plate (rectangle + rocker slots + indicator dots)."""
        # plate dimensions: each gang ~12mm wide, 18mm tall
        gang_w = 11
        plate_h = 18
        plate_w = gangs * gang_w + 6
        # plate body (glass-look)
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        if smart:
            self.set_fill_color(40, 40, 45)  # dark glass
        else:
            self.set_fill_color(245, 245, 240)  # light glass
        self.rect(x, y, plate_w, plate_h, "FD")
        # inner glow rim
        rim_color = GOLD_BAR if smart else (200, 200, 195)
        self.set_draw_color(*rim_color)
        self.set_line_width(0.25)
        self.rect(x + 1, y + 1, plate_w - 2, plate_h - 2, "D")
        # rockers
        rocker_color = (60, 60, 65) if smart else (235, 235, 230)
        rocker_outline = (90, 90, 95) if smart else (210, 210, 205)
        for i in range(gangs):
            rx = x + 3 + i * gang_w
            ry = y + 3
            self.set_draw_color(*rocker_outline)
            self.set_fill_color(*rocker_color)
            self.set_line_width(0.2)
            self.rect(rx, ry, gang_w - 2, plate_h - 6, "FD")
            # tiny indicator LED
            if indicators and smart:
                self.set_fill_color(255, 230, 150)
                self.ellipse(rx + (gang_w - 2) / 2 - 0.5, ry + plate_h - 8.5, 1, 1, "F")
        # label below
        if label:
            self.set_font("Helvetica", "B", 8.6)
            self.set_text_color(*INK)
            self.text(x, y + plate_h + 4.2, label)
        if sub:
            self.set_font("Helvetica", "I", 7.8)
            self.set_text_color(*INK_SOFT)
            self.text(x, y + plate_h + 8.2, sub)
        return plate_w, plate_h

    def special_plate(self, kind, x, y, label=None, sub=None):
        """PIR or geyser switch plate."""
        plate_w = 14
        plate_h = 18
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.set_fill_color(245, 245, 240)
        self.rect(x, y, plate_w, plate_h, "FD")
        self.set_draw_color(200, 200, 195)
        self.set_line_width(0.25)
        self.rect(x + 1, y + 1, plate_w - 2, plate_h - 2, "D")
        if kind == "pir":
            # circular sensor lens
            cx = x + plate_w / 2
            cy = y + plate_h / 2
            self.set_fill_color(60, 60, 65)
            self.ellipse(cx - 3, cy - 3, 6, 6, "F")
            self.set_fill_color(150, 150, 160)
            self.ellipse(cx - 1.5, cy - 1.5, 3, 3, "F")
        elif kind == "geyser":
            # rocker with neon dot
            self.set_fill_color(235, 235, 230)
            self.set_draw_color(210, 210, 205)
            self.rect(x + 2, y + 4, plate_w - 4, plate_h - 9, "FD")
            self.set_fill_color(220, 80, 60)
            self.ellipse(x + plate_w / 2 - 1, y + plate_h - 4, 2, 2, "F")
        if label:
            self.set_font("Helvetica", "B", 8.6)
            self.set_text_color(*INK)
            self.text(x, y + plate_h + 4.2, label)
        if sub:
            self.set_font("Helvetica", "I", 7.8)
            self.set_text_color(*INK_SOFT)
            self.text(x, y + plate_h + 8.2, sub)
        return plate_w, plate_h

    def smart_box_wiring(self, x, y, w, h):
        """Draw a clean wiring diagram of a 65mm smart-switch box."""
        # outer box
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.set_fill_color(255, 255, 255)
        self.rect(x, y, w, h, "FD")
        # title
        self.set_font("Helvetica", "B", 9.2)
        self.set_text_color(*GOLD_DARK)
        self.set_xy(x + 4, y + 3)
        self.cell(0, 5, "65 mm GI MS BOX  -  smart switch")
        # interior
        ix = x + 6
        iy = y + 14
        iw = w - 12
        ih = h - 22
        self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.3)
        self.set_fill_color(*PAPER_TINT)
        self.rect(ix, iy, iw, ih, "FD")
        # incoming wires (from top: L, N, E)
        wire_top_y = y - 1
        cols = [("L", DANGER, "red"), ("N", INK, "black"), ("E", GOOD, "green/yellow")]
        spacing = 7
        wire_x_start = ix + 8
        for i, (lbl, color, name) in enumerate(cols):
            wx = wire_x_start + i * spacing
            self.set_draw_color(*color)
            self.set_line_width(0.7)
            self.line(wx, wire_top_y + 2, wx, iy + 6)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*color)
            self.text(wx - 1.3, iy + 4, lbl)
            # label above
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*INK_SOFT)
            self.text(wx - 4, wire_top_y + 0, name)
        # Aqara module box
        mod_x = ix + 6
        mod_y = iy + 8
        mod_w = iw - 12
        mod_h = 12
        self.set_fill_color(*INFO_PALE)
        self.set_draw_color(*INFO)
        self.set_line_width(0.4)
        self.rect(mod_x, mod_y, mod_w, mod_h, "FD")
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*INFO)
        self.set_xy(mod_x + 2, mod_y + 2)
        self.cell(0, 4, "AQARA H1 EU relay (22 mm thick)")
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*INK_SOFT)
        self.set_xy(mod_x + 2, mod_y + 6.5)
        self.cell(0, 4, "sits behind plate; needs neutral + 65 mm depth")
        # output to load (blue switched live)
        out_y = iy + ih
        out_x = ix + iw - 10
        self.set_draw_color(*INFO)
        self.set_line_width(0.7)
        self.line(out_x, mod_y + mod_h, out_x, out_y + 5)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*INFO)
        self.text(out_x - 3, out_y + 8, "to LOAD")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_SOFT)
        self.text(out_x - 6, out_y + 11.5, "(blue switched live)")
        # box-depth callout on the right
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.3)
        ax = x + w + 2
        self.line(x + w - 1, y + 4, x + w - 1, y + h - 4)
        # Arrow heads
        # depth label outside (no-overflow): keep within box

    def divider(self):
        """Subtle divider rule."""
        self.ln(2)
        y = self.get_y()
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(self.PAGE_MARGIN_X, y, self.PAGE_MARGIN_X + self.CONTENT_W, y)
        self.ln(3)


# ============================================================================
# BUILD PDF
# ============================================================================
pdf = SwitchPDF()

# ---------------------------------------------------------------------------
# COVER PAGE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Cover")

# decorative left vertical rule (full page)
pdf.set_draw_color(*GOLD_BAR)
pdf.set_line_width(0.7)
pdf.line(14, 30, 14, 270)

# top label
pdf.set_xy(22, 28)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 5, "PROJECT REFERENCE  /  ELECTRICAL", ln=1)

# big title
pdf.set_xy(22, 42)
pdf.set_font("Helvetica", "", 36)
pdf.set_text_color(*INK)
pdf.cell(0, 16, "Switch Layout", ln=1)
pdf.set_xy(22, 60)
pdf.set_font("Helvetica", "B", 36)
pdf.cell(0, 16, "Master Plan", ln=1)

# thin gold rule
pdf.set_draw_color(*GOLD_BAR)
pdf.set_line_width(0.7)
pdf.line(22, 86, 80, 86)

# subtitle
pdf.set_xy(22, 92)
pdf.set_font("Helvetica", "I", 13)
pdf.set_text_color(*INK_SOFT)
pdf.multi_cell(170, 6, "Position  -  Cavity  -  Type  -  Function")

pdf.set_xy(22, 105)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(*INK_SOFT)
pdf.multi_cell(170, 5.6,
               "Every switch board in this house: where it goes on the wall, "
               "what each gang controls, what cavity to chase, what plate to fit, "
               "and how high to mount it.\n\n"
               "One document for electrician, mason, and owner.")

# project info card
card_x, card_y, card_w, card_h = 22, 145, 168, 60
pdf.set_fill_color(*PAPER_TINT)
pdf.set_draw_color(*RULE)
pdf.set_line_width(0.3)
pdf.rect(card_x, card_y, card_w, card_h, "FD")
# gold corner accent
pdf.set_fill_color(*GOLD_BAR)
pdf.rect(card_x, card_y, 1.6, card_h, "F")

pdf.set_xy(card_x + 6, card_y + 4)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 5, "PROJECT", ln=1)

proj_lines = [
    ("Owner",            "Ganesh Prasad D"),
    ("Location",         "Chitradurga, Karnataka"),
    ("House",            "2-floor residential, North-facing main entrance"),
    ("Ceiling heights",  "Ground Floor 11 ft   -   First Floor 10 ft"),
    ("DB location",      "West wall, foyer, behind door swing  (40-way Schneider Acti9)"),
    ("Smart family",     "Aqara H1 EU  -  Zigbee, glass face, with neutral"),
    ("Dumb family",      "Schneider AvatarOn-C Glass  /  Legrand Arteor Square Glass"),
    ("Document",         "v2.0   -   2026-05-10"),
]
for i, (label, val) in enumerate(proj_lines):
    pdf.set_xy(card_x + 6, card_y + 11 + i * 5.7)
    pdf.set_font("Helvetica", "B", 9.2)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(36, 5, label, ln=0)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, val, ln=1)

# read this first - clean left-bar callout
pdf.set_xy(22, 218)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 6, "READ THIS FIRST", ln=1)
pdf.set_x(22)
pdf.set_font("Helvetica", "", 9.6)
pdf.set_text_color(*INK)
pdf.multi_cell(168, 5,
    "1.  This PDF IS the site instruction. If anything on site differs, STOP and call before chasing.\n"
    "2.  Smart-switch boards need 65 mm-deep boxes. Standard 50 mm GI MS box is too shallow - the relay sits behind the plate.\n"
    "3.  Every switch board gets a NEUTRAL wire (black). Even at dumb zones - we may convert to smart later.\n"
    "4.  All switch boards at 1200 mm centre from FFL. Geyser switches at 1050 mm. AC sockets at 1850 mm. Bedside 600 mm.\n"
    "5.  Power and Cat6 NEVER share a conduit.")
# gold left bar for the read-this-first block
y_after = pdf.get_y()
pdf.set_fill_color(*GOLD_BAR)
pdf.rect(20, 218, 1.4, y_after - 218, "F")

# ---------------------------------------------------------------------------
# PAGE 2 - HOW TO USE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("How to use")
pdf.h1("How to use this document",
       "Three audiences, three reading paths. Find yours below.")

pdf.callout_info(
    "For the electrician",
    "Read pages 5-6 (heights + cavity rules), 7 (universal smart-switch wiring), and 9 onwards "
    "(room-by-room switch boards). Page 18 is the master schedule - the single table you keep "
    "on you while running cables. Page 21 is the pre-plastering sign-off checklist."
)

pdf.callout_warn(
    "For the mason / civil contractor",
    "Read pages 5 (heights) and 6 (cavity / box-depth rules). The CRITICAL number is the "
    "65 mm-deep GI MS box at every smart-switch position. Page 21 is your sign-off checklist - "
    "every box must be the correct depth BEFORE plastering."
)

pdf.callout_good(
    "For the owner (Ganesh)",
    "Read pages 3-4 (premium switch family + visual look you are choosing) and pages 18-20 "
    "(master schedule - what each switch in the house actually controls). Use this on site to "
    "verify what was chased matches the plan, and to brief the Aqara H1 EU app once switches "
    "are live."
)

pdf.h2("Status key used in tables")
pdf.table(
    headers=["Symbol", "Meaning", "Action"],
    rows=[
        ["[OK]",  "Confirmed - lock the position and depth",       "Chase + box this exactly as drawn"],
        ["[TBD]", "Position TBD - confirm on site before chasing", "Mark with chalk, owner sign-off, then chase"],
        ["[!!]",  "Pending decision - do NOT chase yet",           "Wait for written go-ahead in WhatsApp / site notebook"],
    ],
    col_widths=[20, 70, 84],
    font=9,
)

pdf.h2("Vocabulary you will see throughout")
pdf.table(
    headers=["Term", "Meaning"],
    rows=[
        ["FFL",            "Finished Floor Level - top of final tile / marble. ALL heights from FFL, not from rough slab."],
        ["Gang",           "One rocker / push-button on a switch plate. A 4-gang plate has 4 rockers."],
        ["Module",         "Width unit on a modular plate. 1-gang = 1 module wide, 4-gang = 4 modules wide."],
        ["Smart switch",   "Aqara H1 EU - Zigbee, talks to Home Assistant. Needs neutral + 65 mm box."],
        ["Dumb switch",    "Plain rocker, no electronics. Used in kitchen / utility / store / geyser / PIR."],
        ["GI MS box",      "Galvanised Iron Mounting Box, cemented into wall. 50 mm or 65 mm depth."],
        ["2-way switch",   "Two switches at different locations both control the same light (staircase)."],
        ["Master-off gang","One smart gang on a 4-gang bedroom plate that turns ALL room lights off in one tap."],
    ],
    col_widths=[36, 138],
    font=9,
)

# ---------------------------------------------------------------------------
# PAGE 3 - THE PREMIUM SWITCH FAMILY (GRAND LOOK)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Switch family")
pdf.h1("The switch family",
       "One coherent premium look across the whole house - smart and dumb side by side.")

pdf.body(
    "The owner's brief is simple: switches must look GRAND. Plain white plastic Anchor / Goldmedal "
    "rocker switches do not match a premium-finish home. Below is the recommended switch family - "
    "smart and dumb both use a tempered-glass face at the same height, so the eye reads continuity "
    "across every wall."
)

pdf.h2("Five visual properties of a premium plate")
pdf.body(
    "1.  FRAMELESS / hidden screws - the plate face is one continuous surface; no visible screw heads.\n"
    "2.  GLASS or brushed-metal face - tempered glass or brushed steel, never glossy plastic.\n"
    "3.  SOFT BACKLIT INDICATOR per gang - a tiny LED so you can find the switch in the dark.\n"
    "4.  UNIFORM SIZE - 1, 2, 3, 4-gang plates are all 86 mm tall; only the width changes.\n"
    "5.  SAME FAMILY across the house - foyer, bedroom, kitchen all share the same bezel and finish."
)

pdf.h2("Recommended family")
pdf.table(
    headers=["Use", "Brand + product", "Plate finish", "Approx Rs / gang"],
    rows=[
        ["All SMART boards (13)",
         "Aqara H1 EU (with neutral)",
         "Tempered glass face, frameless,\nbacklit LED indicator per gang",
         "2,200  (1-gang)\n2,800  (2-gang)\n3,400  (3-gang)"],
        ["All DUMB switches + sockets",
         "Schneider AvatarOn-C Glass\n  -or-  Legrand Arteor Square Glass\n  -or-  Norisys Cuboid Glass",
         "Tempered glass plate, frameless,\nhidden screws, same 86 mm height\nas Aqara",
         "350-600 per module\n(plate + frame: +800-1200)"],
        ["Optional premium spots",
         "Lutron Palladiom\n(import via Mumbai dealer)",
         "Solid brushed brass / nickel,\ntactile mechanical button\n(grandest available)",
         "15,000 - 25,000\nper gang"],
    ],
    col_widths=[36, 50, 50, 38],
    font=8.6,
    line_h=4.2,
)

pdf.callout(
    "Why this works as one look",
    "Aqara H1 EU and Schneider AvatarOn-C Glass (or Legrand Arteor Square Glass) both have an "
    "86 mm-tall glass face with no visible frame. Side-by-side on a wall they read as the same "
    "family, even though one is smart and one is dumb. This is the cheapest way to get a unified "
    "premium look without forcing every switch to be smart."
)

pdf.callout_warn(
    "Backup if Aqara H1 EU is hard to source",
    "Schneider Wiser AvatarOn smart switches use the same glass-plate bezel as the Schneider "
    "AvatarOn-C dumb plates - perfect visual match - but cost ~3x Aqara per gang and need a "
    "Schneider hub. Mention 'Wiser AvatarOn' to your Schneider distributor in Bangalore."
)

# ---------------------------------------------------------------------------
# PAGE 4 - VISUAL PLATE GUIDE (drawn, not ASCII)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Plate guide")
pdf.h1("Visual plate guide",
       "What each plate looks like on the wall. All plates 86 mm tall, frameless.")

pdf.body(
    "The Aqara smart plates and the Schneider / Legrand glass dumb plates use the same "
    "86 mm-tall frameless bezel. Smart and dumb side by side read as one family - this is what "
    "makes the wall feel grand."
)

pdf.h2("Smart switches  -  Aqara H1 EU (glass face, backlit LED indicator)")

# row of smart plates
y = pdf.get_y() + 4
plate_y = y
plate_x = pdf.PAGE_MARGIN_X + 4
spacing = 7
# 1-gang
w1, h1 = pdf.plate_diagram(plate_x, plate_y, gangs=1, smart=True,
                           label="1-gang", sub="86 x 86 mm")
# 2-gang
w2, h2 = pdf.plate_diagram(plate_x + w1 + spacing + 12, plate_y, gangs=2, smart=True,
                           label="2-gang", sub="146 x 86 mm")
# 3-gang
w3, h3 = pdf.plate_diagram(plate_x + w1 + w2 + spacing * 2 + 24, plate_y, gangs=3, smart=True,
                           label="3-gang", sub="206 x 86 mm")
# 4-gang
w4, h4 = pdf.plate_diagram(plate_x + w1 + w2 + w3 + spacing * 3 + 36, plate_y, gangs=4, smart=True,
                           label="4-gang", sub="266 x 86 mm")

pdf.set_y(plate_y + 32)
pdf.h2("Dumb switches  -  Schneider AvatarOn-C Glass (matching bezel)")

y = pdf.get_y() + 4
plate_y = y
pdf.plate_diagram(plate_x, plate_y, gangs=2, smart=False, indicators=False,
                  label="2-gang dumb", sub="kitchen / utility / store")
pdf.plate_diagram(plate_x + 30 + spacing, plate_y, gangs=4, smart=False, indicators=False,
                  label="4-gang dumb", sub="kitchen entry board")

pdf.set_y(plate_y + 32)
pdf.h2("Special-purpose plates")
y = pdf.get_y() + 4
plate_y = y
pdf.special_plate("pir", plate_x, plate_y, label="PIR auto", sub="bathrooms")
pdf.special_plate("geyser", plate_x + 30, plate_y, label="20A DP geyser", sub="outside bath, 1050 mm")

pdf.set_y(plate_y + 32)
pdf.callout_info(
    "The backlit dot you see on smart plates",
    "The small warm-white dot on each smart-plate gang is the backlit LED indicator. It glows soft "
    "white when the room is dim, which lets you find the switch at night without flooding the room "
    "with light. This single feature is what makes the plate read as premium. Confirm with the "
    "supplier you are buying the H1 EU 'with backlight' SKU."
)

# ---------------------------------------------------------------------------
# PAGE 5 - HEIGHTS DIAGRAM (drawn elevation)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Heights")
pdf.h1("Standard heights from FFL",
       "Every measurement in this house is from FFL = top of finished floor.")

pdf.body(
    "All heights are from FFL = Finished Floor Level (top of the final tile / marble), "
    "NOT from the rough slab. Re-measure after the floor is laid if there is any doubt."
)

# draw the elevation
y = pdf.get_y() + 2
pdf.heights_diagram(pdf.PAGE_MARGIN_X, y, pdf.CONTENT_W, 130)
pdf.set_y(y + 134)

pdf.h2("Horizontal placement (corner offset)")
pdf.body(
    "Mount any switch board MINIMUM 150 mm clear of the nearest corner, door frame, or window "
    "frame, so the plate sits flat against the wall and does not fight a skirting line, "
    "architrave, or curtain rod bracket. If a door swing is 100 mm proud, increase to 200 mm."
)

# ---------------------------------------------------------------------------
# PAGE 6 - CAVITY / BOX DEPTH (drawn comparison)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Box depth")
pdf.h1("Cavity / box depth",
       "The single most-ignored detail in Indian wiring. Get this right.")

pdf.callout_danger(
    "Critical rule",
    "If you only enforce ONE thing on this site, enforce this: every smart-switch board uses a "
    "65 mm-deep GI MS box, NOT the standard 50 mm. There is no fix once plastering is done."
)

pdf.h2("Why 65 mm matters")
pdf.body(
    "Aqara H1 / Sonoff ZBMINI / Aqara T1 relay modules sit BEHIND the switch plate inside the "
    "wall box. The relay is ~22 mm thick. Add the plate terminals, the bent earth wire, and the "
    "neutral block, and you need ~50 mm of free clearance just for the components. A standard 50 mm "
    "GI box leaves zero clearance - cables get crushed, the plate doesn't sit flush, and over time "
    "the relay can overheat. 65 mm gives clean working room and future flexibility."
)

# drawn comparison
y = pdf.get_y() + 2
pdf.box_depth_diagram(pdf.PAGE_MARGIN_X, y, pdf.CONTENT_W, 75)
pdf.set_y(y + 80)

pdf.h2("GI MS box sizes by gang count")
pdf.table(
    headers=["Gang", "Box (W x H x D, mm)", "Plate width", "Use case"],
    rows=[
        ["1-gang", "75 x 75 x 65",  "86 mm",  "Foyer 2-way / staircase / pooja niche / front balcony"],
        ["2-gang", "130 x 75 x 65", "146 mm", "Dining / corridor / pooja entry"],
        ["3-gang", "175 x 75 x 65", "206 mm", "Dining smart / Living 2-way (stair side)"],
        ["4-gang", "230 x 75 x 65", "266 mm", "Foyer entry / Living main / MBR / BR1 / BR2"],
    ],
    col_widths=[22, 50, 28, 74],
    font=9,
)

pdf.h2("Where 50 mm boxes are still OK")
pdf.body(
    "All sockets (5A, 16A, 20A AC), geyser 20A DP switches, PIR auto-switches, kitchen / utility / "
    "store dumb light switches, Cat6 keystone wall plates.\n\n"
    "Buy: 14 x 65 mm GI boxes (smart) and ~30 x 50 mm boxes (everything else). See materials "
    "checklist section 4 in the project for exact counts."
)

# ---------------------------------------------------------------------------
# PAGE 7 - UNIVERSAL SMART-SWITCH WIRING
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Wiring")
pdf.h1("Universal smart-switch wiring",
       "Every smart-switch board in this house is wired the same way.")

pdf.body(
    "Pull L (red) + N (black) + E (green/yellow) into the box, leave a 300 mm tail of each wire, "
    "label them, cap them. The Aqara H1 module is fitted by the owner later - the electrician does "
    "NOT install the smart module, only prepares the box."
)

# wiring diagram
y = pdf.get_y() + 2
pdf.smart_box_wiring(pdf.PAGE_MARGIN_X + 12, y, pdf.CONTENT_W - 24, 80)
pdf.set_y(y + 92)

pdf.h2("The 4 wires you must see at every smart-switch box")
pdf.table(
    headers=["Wire colour", "Function", "Mandatory at smart box?"],
    rows=[
        ["Red",          "Live (phase) - 230 V hot in",   "YES"],
        ["Black",        "Neutral - return",              "YES (this is the new rule - do not skip)"],
        ["Green/Yellow", "Earth",                         "YES (also reaches every metal fitting)"],
        ["Blue",         "Switched live leg - to load",   "YES (one per gang)"],
    ],
    col_widths=[36, 70, 68],
    font=9,
)

pdf.callout_danger(
    "Do not confuse black neutral with blue switched-live",
    "Black wire carrying current is ALWAYS neutral. Blue wire carrying current is ALWAYS the "
    "switched live leg between switch and load. If your old habit is to use black for switched "
    "live, BREAK IT for this site."
)

pdf.h2("Pre-plaster check on every smart-switch box")
pdf.body(
    "[  ]  65 mm-deep GI MS box of correct gang width is fixed flush to wall finish line.\n"
    "[  ]  L (red), N (black), E (green/yellow) wires present, each with 300 mm tail in box.\n"
    "[  ]  Each wire end has masking tape + permanent marker label with circuit ID (B1, C1, D9...).\n"
    "[  ]  Switched-live (blue) wires for each gang go to their respective ceiling boxes / loads.\n"
    "[  ]  All wire ends taped / capped so no exposed copper before plate fitment.\n"
    "[  ]  Box is plumb (vertical) and centre is at 1200 mm FFL (use spirit level + measure)."
)

# ---------------------------------------------------------------------------
# GROUND FLOOR DIVIDER
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Ground floor")
# Full-page section divider
pdf.set_y(80)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 6, "PART  -  ONE", align="C", ln=1)
pdf.set_y(95)
pdf.set_font("Helvetica", "", 36)
pdf.set_text_color(*INK)
pdf.cell(0, 14, "Ground Floor", align="C", ln=1)
pdf.set_y(115)
pdf.set_draw_color(*GOLD_BAR)
pdf.set_line_width(0.7)
pdf.line(85, 116, 125, 116)
pdf.set_y(124)
pdf.set_font("Helvetica", "I", 12)
pdf.set_text_color(*INK_SOFT)
pdf.cell(0, 6, "Foyer  -  Living  -  Dining  -  Kitchen  -  MBR  -  Bath  -  Pooja  -  Stair", align="C", ln=1)

# ---------------------------------------------------------------------------
# GF FOYER
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Foyer")
pdf.h1("Foyer",
       "North-side main entrance. Stone-clad feature wall with welcome screen + DB.")

pdf.lead(
    "Two switch boards: SB-FOYER-1 (the user-facing rocker plate) and the DB enclosure (40-way "
    "Schneider Acti9, behind the door swing - this is not a switch board in the user sense)."
)

pdf.board_card(
    "SB-FOYER-1",
    "W wall, LEFT of main door, 200 mm clear of door frame",
    height_mm=1200,
    plate="4-gang Aqara H1 EU smart, glass face, 266 x 86 mm",
    box_depth="65 mm GI MS  -  230 x 75 x 65",
    circuits="B1 (foyer lights)  /  B2 (screen + speaker)  /  B10 (cove)",
    smart_count="2 smart  +  2 smart-ready",
    gangs=[
        ("1", "Foyer ceiling spotlights (2x GU10) + walnut shelf strip", "Smart", "Group dimmable; warm 2700K"),
        ("2", "Welcome screen + amber halo around screen recess",        "Smart", "Comes on with motion / face detection"),
        ("3", "False ceiling cove (perimeter LED)",                      "Smart", "Default 30% at evening, scene-controlled"),
        ("4", "Spare (capped now) / future garden light",                "Smart-ready", "Pull wire + cap; convert later"),
    ],
)

pdf.h2("DB enclosure (not a switch)")
pdf.body(
    "40-way Schneider Acti9 distribution box, behind the foyer door swing on W wall. Bottom of DB "
    "at 1500 mm FFL. Recess size: 400 W x 600 H x 100 D mm. Owner / electrician access only - "
    "no rocker switches here."
)

# ---------------------------------------------------------------------------
# GF LIVING
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Living")
pdf.h1("Living area",
       "Solid-slab zone (W) + double-height void (E). False ceiling confirmed.")

pdf.lead(
    "Two boards: main entry board on W wall + a 2-way partner near the staircase entry, so you "
    "can turn the main lights off as you head upstairs."
)

pdf.board_card(
    "SB-LIVING-1",
    "W wall, near foyer-living boundary, 150 mm clear of door jamb",
    1200, "4-gang Aqara H1 EU smart, glass face",
    "65 mm GI MS  -  230 x 75 x 65",
    "B3 (main lights)  /  B4 (cove)",
    smart_count="3 smart  +  1 smart-ready",
    gangs=[
        ("1", "Main living downlights (4x recessed COB 12W)", "Smart", "Group dim, 2700K warm"),
        ("2", "False ceiling cove (B4)",                       "Smart", "Smooth dimmer, scene driven"),
        ("3", "TV-wall accent wash (2x GU10 spots)",           "Smart", "Stone wall grazing"),
        ("4", "Statement chandelier in double-height void",     "Smart", "[!!] Pending owner go-ahead"),
    ],
)

pdf.board_card(
    "SB-LIVING-2",
    "Wall opposite SB-LIVING-1, near staircase entry  -  2-way partner",
    1200, "2-gang Aqara H1 EU smart",
    "65 mm GI MS  -  130 x 75 x 65",
    "B3 / B4 (mirrors SB-LIVING-1)",
    gangs=[
        ("1", "Main living downlights (mirrors SB-LIVING-1 g1)", "Smart 2-way", "Both boards toggle same load"),
        ("2", "Cove (mirrors SB-LIVING-1 g2)",                    "Smart 2-way", "Either board can fade cove"),
    ],
    note="Both gangs PAIR with SB-LIVING-1 as Aqara 2-way groups in the app once installed.",
)

# ---------------------------------------------------------------------------
# GF DINING
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Dining")
pdf.h1("Dining area",
       "East wall zone, ~9'6 deep after kitchen. False ceiling confirmed with cove.")

pdf.board_card(
    "SB-DINING",
    "W side of dining entry, 150 mm clear of opening",
    1200, "3-gang Aqara H1 EU smart",
    "65 mm GI MS  -  175 x 75 x 65",
    "B6 (lights)  /  B9 (cove)",
    gangs=[
        ("1", "Dining table pendant",                              "Smart", "2700K dimmer, drop to 2100mm above table"),
        ("2", "Dining recessed downlights (2-3 in false ceiling)", "Smart", "Supplement pendant for full meals"),
        ("3", "False ceiling cove (B9)",                           "Smart", "Warm ambient dimmer"),
    ],
)

# ---------------------------------------------------------------------------
# GF KITCHEN
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Kitchen")
pdf.h1("Kitchen",
       "North wall, ~10ft deep. Task area - dumb switches for tactile feedback.")

pdf.lead(
    "Kitchen is kept on DUMB switches because cooking demands a tactile rocker. Same Schneider "
    "AvatarOn-C glass plate as the rest of the house for visual continuity, but no Aqara smart "
    "relay behind."
)

pdf.board_card(
    "SB-KITCHEN",
    "Entry to kitchen, N wall",
    1200, "4-gang Schneider AvatarOn-C Glass  -  DUMB",
    "50 mm GI MS  -  230 x 75 x 50",
    "A3 (kitchen lights + exhaust)",
    gangs=[
        ("1", "Kitchen ceiling LED panel (24W 4000K cool)",           "Dumb", "Bright task light"),
        ("2", "Under-cabinet LED strip (warm 2700K)",                 "Dumb", "Counter task light"),
        ("3", "Exhaust fan (6 inch / 8 inch)",                        "Dumb", "Top of N or E wall"),
        ("4", "Hob area downlight (optional)",                        "Dumb", "[TBD] Skip if chimney lights cooktop"),
    ],
)

pdf.h2("Counter sockets  -  separate boxes, NOT on the switch board")
pdf.body(
    "4 x 5A sockets at 1100 mm FFL spaced along N wall, behind counter (mixer, microwave, OTG, kettle).\n"
    "1 x 16A socket at 1900 mm FFL above hob position - chimney power.\n"
    "1 x 20A socket below counter at 150 mm FFL at hob - electric hob/cooktop on dedicated A6.\n"
    "1 x 5A socket at 300 mm FFL under sink - RO water purifier.\n"
    "1 x 15A socket at 300 mm FFL in fridge niche - dedicated A8 circuit, always live."
)

# ---------------------------------------------------------------------------
# GF UTILITY + STORE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Utility + Store")
pdf.h1("Utility + Store room",
       "Two small functional spaces sharing the kitchen ceiling-light circuit.")

pdf.board_card(
    "SB-UTILITY", "Near utility door, inside",
    1200, "1-gang Schneider AvatarOn-C Glass  -  DUMB",
    "50 mm GI MS  -  75 x 75 x 50",
    "A3 share (light)  +  A7 (washing machine 16A socket - SEPARATE box at 300 mm)",
    gangs=[("1", "Utility ceiling light", "Dumb", "Single on/off")],
)

pdf.board_card(
    "SB-STORE", "Outside store room door",
    1200, "1-gang Schneider AvatarOn-C Glass  -  DUMB",
    "50 mm GI MS  -  75 x 75 x 50",
    "A3 share (light)",
    gangs=[("1", "Store room bulkhead light", "Dumb", "Single on/off")],
)

# ---------------------------------------------------------------------------
# GF MASTER BEDROOM
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / M. Bedroom")
pdf.h1("Master bedroom",
       "South side, L-wardrobe on S wall (10'3) + W-wall tail (~3 ft).")

pdf.board_card(
    "SB-MBED", "Inside MBR, near bedroom door (handle side)",
    1200, "4-gang Aqara H1 EU smart",
    "65 mm GI MS  -  230 x 75 x 65",
    "C1 (lights)",
    gangs=[
        ("1", "Main ceiling light (recessed COB / surface LED)",     "Smart",        "Centred, 2700K"),
        ("2", "Bedside reading light L (E wall, north of headboard)","Smart",        "Independent of partner"),
        ("3", "Bedside reading light R (E wall, south of headboard)","Smart",        "Independent of partner"),
        ("4", "MASTER OFF  -  one tap turns all 3 above off",        "Smart scene",  "Aqara automation"),
    ],
)

pdf.callout_good(
    "Wardrobe light  -  not on this board",
    "Inside the L-wardrobe on the S wall + W-wall tail there is a 24V LED strip on a magnetic "
    "door sensor - it auto-on when the wardrobe opens. No switch; just a 16 mm LV conduit from "
    "C1 driver to the strip. Tell carpenter to leave a 50 mm gap above the wardrobe top rail "
    "for the strip channel."
)

# ---------------------------------------------------------------------------
# GF BATHROOM (PIR)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Bathroom")
pdf.h1("Common bathroom (GF)",
       "Door on EAST wall; fixtures along NORTH wall. PIR + geyser switch OUTSIDE.")

pdf.lead(
    "PIR auto-switch + geyser switch sit OUTSIDE the door so wet hands never touch a 230V "
    "switch. Lights inside are occupancy-driven - on with motion, off ~3 min after last motion."
)

pdf.board_card(
    "SB-GFBATH",
    "East wall, OUTSIDE bathroom, RIGHT of door  (PIR + geyser combo)",
    "1200 / 1050",
    "Mixed: 1x PIR module + 1x 20A DP geyser switch with red neon",
    "50 mm GI MS  -  130 x 75 x 50  (2-module plate)",
    "A1 (lights+exhaust via PIR)  +  A2 (15L geyser, dedicated 16A RCBO)",
    gangs=[
        ("1", "Bathroom ceiling light + mirror light + exhaust fan", "Auto PIR", "1200 mm; ~3 min hold-off"),
        ("2", "Geyser (15L) in attic above bathroom",                "Dumb 20A", "1050 mm; red neon = live"),
    ],
)

pdf.callout_good(
    "Why PIR (not a regular switch) for bathroom lights",
    "PIR (Passive Infra-Red) auto-detects motion as you enter and turns lights off after a delay. "
    "No fumbling for a switch with wet hands, no light left burning all night. The PIR module is "
    "dumb (no Aqara) - simpler, fewer parts to fail in a wet zone. Same Schneider AvatarOn-C "
    "glass plate so it visually matches every other switch in the house."
)

pdf.callout_danger(
    "Geyser switch is always OUTSIDE the bathroom",
    "Indian regulation + safety: never put a 230V switch where someone might touch it with wet "
    "hands. Inside-bathroom switches are a fire / shock risk and may violate insurance terms. "
    "Same rule applies to FF Toilet 1 and Toilet 2."
)

# ---------------------------------------------------------------------------
# GF POOJA
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Pooja")
pdf.h1("Pooja room",
       "Small 5 x 5 ft devotional room. Switch board OUTSIDE the entry.")

pdf.lead(
    "Switch board is outside the entry so you switch on as you approach the deity, not after. "
    "Niche backlight on a separate gang for silent devotional ambience without the bright ceiling."
)

pdf.board_card(
    "SB-POOJA",
    "Outside pooja entry, ~1200 mm clear of door",
    1200, "2-gang Aqara H1 EU smart",
    "65 mm GI MS  -  130 x 75 x 65",
    "B8",
    gangs=[
        ("1", "Pooja ceiling LED panel (12W, 2700K)",            "Smart", "Soft warm; dim to 30% for evening aarti"),
        ("2", "Niche backlight LED strip (amber, behind idol)",  "Smart", "Devotional glow; runs alone without ceiling"),
    ],
)

# ---------------------------------------------------------------------------
# GF STAIRCASE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("GF / Staircase")
pdf.h1("Staircase",
       "22 risers; FF flight continues to terrace. 2-way smart pair (GF + FF).")

pdf.lead(
    "Two 1-gang smart boards: one at GF base, one at FF top landing. Either toggles the entire "
    "staircase circuit. Aqara H1 handles 2-way pairing automatically once both modules are paired "
    "in Home Assistant."
)

pdf.board_card(
    "SB-STAIR-GF", "GF, base of stairs, on staircase wall",
    1200, "1-gang Aqara H1 EU smart",
    "65 mm GI MS  -  75 x 75 x 65",
    "B7",
    gangs=[("1", "Staircase wall lights + per-step LED nosing", "Smart 2-way", "Pairs with SB-STAIR-FF")],
)

pdf.board_card(
    "SB-STAIR-FF", "FF, top landing, near stair top",
    1200, "1-gang Aqara H1 EU smart",
    "65 mm GI MS  -  75 x 75 x 65",
    "B7",
    gangs=[("1", "Same load as SB-STAIR-GF (mirrored)", "Smart 2-way", "Pairs with SB-STAIR-GF")],
)

pdf.callout_info(
    "What both boards control together",
    "Both boards toggle the SAME load: 3-4 staircase wall lights + (optional) per-step LED "
    "nosing strips. Press either - lights toggle. The Aqara H1 handles 2-way pairing in software."
)

# ---------------------------------------------------------------------------
# FIRST FLOOR DIVIDER
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("First floor")
pdf.set_y(80)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 6, "PART  -  TWO", align="C", ln=1)
pdf.set_y(95)
pdf.set_font("Helvetica", "", 36)
pdf.set_text_color(*INK)
pdf.cell(0, 14, "First Floor", align="C", ln=1)
pdf.set_y(115)
pdf.set_draw_color(*GOLD_BAR)
pdf.set_line_width(0.7)
pdf.line(85, 116, 125, 116)
pdf.set_y(124)
pdf.set_font("Helvetica", "I", 12)
pdf.set_text_color(*INK_SOFT)
pdf.cell(0, 6, "FF Living  -  Bedroom 1  -  Bedroom 2  -  Toilets  -  Balconies", align="C", ln=1)

# ---------------------------------------------------------------------------
# FF LIVING
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("FF / Living")
pdf.h1("FF Living / corridor",
       "Central zone connecting both bedrooms, staircase landing, and front balcony.")

pdf.lead(
    "Beam runs along the cut-out edge (the double-height void below). One smart board for the "
    "corridor lights, plus the FF Wi-Fi access point wall plate at high level (data + power, "
    "not a switch)."
)

pdf.board_card(
    "SB-FFLIV", "Central wall, between BR1 and BR2 doors",
    1200, "2-gang Aqara H1 EU smart",
    "65 mm GI MS  -  130 x 75 x 65",
    "D9",
    gangs=[
        ("1", "FF corridor downlights (2-3x recessed LED, 9W)", "Smart",       "Avoid beam line"),
        ("2", "Spare / future feature light over staircase top", "Smart-ready", "[TBD] Decide before plaster"),
    ],
)

pdf.h2("FF Wi-Fi router / AP wall plate")
pdf.body(
    "Not a switch board, but on the same wall. Mount on the central FF Living wall, 300-500 mm "
    "to one side of SB-FFLIV.\n\n"
    "  Height (centre)   2400 mm FFL  (high mount, clear of furniture)\n"
    "  Plate              Cat6 keystone x2 (50 mm wall plate) + adjacent 1-gang 5A socket\n"
    "  Box depth          50 mm GI MS for plate; 50 mm GI MS for socket\n"
    "  Cables in          2x Cat6 from staircase niche (run R-FF-1, in 25 mm grey LV-25 conduit)\n"
    "  Power              5A socket on D9 lighting circuit, 300 mm beside Cat6 plate, same height"
)

# ---------------------------------------------------------------------------
# FF BR1
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("FF / Bedroom 1")
pdf.h1("Bedroom 1 (East side)",
       "No false ceiling. Attached Toilet 1 (8x5 ft, SINK-TOILET-SHOWER E to W).")

pdf.board_card(
    "SB-BR1", "Inside BR1, near bedroom door",
    1200, "4-gang Aqara H1 EU smart",
    "65 mm GI MS  -  230 x 75 x 65",
    "D1 (lights)",
    gangs=[
        ("1", "Main ceiling light (recessed COB 12W)",         "Smart",        "2700K, room centre"),
        ("2", "Bedside reading light L",                       "Smart",        ""),
        ("3", "Bedside reading light R",                       "Smart",        ""),
        ("4", "MASTER OFF  -  one tap turns all 3 above off",  "Smart scene",  "Aqara automation"),
    ],
)

pdf.board_card(
    "SB-BR1-GEYSER", "Just outside Toilet 1 door, BR1 side",
    1050, "1-gang 20A DP geyser switch (Schneider, dumb) with red neon",
    "50 mm GI MS  -  75 x 75 x 50",
    "D4 (15L geyser)",
    gangs=[("1", "Toilet 1 geyser  -  15L attic-mounted", "Dumb 20A", "Red neon = live")],
)

# ---------------------------------------------------------------------------
# FF BR2
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("FF / Bedroom 2")
pdf.h1("Bedroom 2 (West side)",
       "False ceiling CONFIRMED with cove. W-wardrobe (3ft deep). Attached Toilet 2.")

pdf.board_card(
    "SB-BR2", "Inside BR2, near bedroom door",
    1200, "4-gang Aqara H1 EU smart",
    "65 mm GI MS  -  230 x 75 x 65",
    "D5 (lights)  /  D11 (false ceiling cove)",
    gangs=[
        ("1", "Main ceiling light (recessed COB 12W)",                "Smart",        "2700K"),
        ("2", "Bedside reading lights L+R (paired) OR cove (D11)",    "Smart",        "[TBD] Pick which use - decide before chase"),
        ("3", "Bedside reading other / cove / study spot (TBD)",       "Smart",        "[TBD] As above"),
        ("4", "MASTER OFF",                                            "Smart scene",  "Aqara automation"),
    ],
)

pdf.callout_warn(
    "BR2 vs BR1  -  difference",
    "BR2 has a confirmed false ceiling with cove (circuit D11), so one of the four smart gangs "
    "drives the cove. BR1 is no-false-ceiling, so its 4 gangs are: main + reading L + reading R + "
    "master-off, with no cove gang. Confirm with owner before chasing the BR2 board so gang "
    "assignments are locked."
)

pdf.board_card(
    "SB-BR2-GEYSER", "Just outside Toilet 2 door, BR2 side",
    1050, "1-gang 20A DP geyser switch (Schneider, dumb) with red neon",
    "50 mm GI MS  -  75 x 75 x 50",
    "D8 (15L geyser)",
    gangs=[("1", "Toilet 2 geyser  -  15L attic-mounted", "Dumb 20A", "Red neon = live")],
)

# ---------------------------------------------------------------------------
# FF TOILETS (PIR INSIDE)
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("FF / Toilets")
pdf.h1("Toilets 1 & 2 (FF)",
       "Ceiling PIR inside each toilet - no wall switch.")

pdf.lead(
    "Both attached toilets use a PIR sensor INSIDE for occupancy-driven lights / exhaust. No "
    "wall switch inside - same wet-hand-safety logic as the GF bathroom. The geyser switch "
    "for each toilet sits on the bedroom side (covered on previous pages)."
)

pdf.h2("PIR module  -  ceiling, inside Toilet 1 and Toilet 2")
pdf.kv("Location",   "Ceiling, near door, inside each toilet")
pdf.kv("Mount",      "Ceiling-mounted PIR (NOT wall-mounted) - covers full toilet area")
pdf.kv("Box",        "Ceiling B-type box, 60 mm circular")
pdf.kv("Circuits",   "D3 (Toilet 1 lights+exhaust)  /  D7 (Toilet 2 lights+exhaust)")
pdf.kv("Behaviour",  "On with motion; auto-off ~3 min after last motion. Drives ceiling light + "
                     "mirror light + exhaust fan together as one circuit.")

pdf.callout_good(
    "Why ceiling PIR (not wall PIR) for FF toilets",
    "FF Toilets have a vanity, toilet, and shower in line. A wall PIR near the door would lose "
    "line-of-sight to someone in the shower, drop motion, and switch off mid-shower. A ceiling-"
    "mounted PIR sees the entire room from above and never loses motion. Standard product: "
    "Legrand Myrius ceiling PIR or Aqara FP1E ceiling presence sensor (smart option)."
)

# ---------------------------------------------------------------------------
# FF BALCONIES
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("FF / Balconies")
pdf.h1("Balconies (Front + West)",
       "Front balcony (11'9 x 7') on N. West balcony (3 ft projection). Shared D10.")

pdf.board_card(
    "SB-BALCONY-FRONT", "Inside, near front balcony door",
    1200, "1-gang Aqara H1 EU smart",
    "65 mm GI MS  -  75 x 75 x 65",
    "D10 (balcony shared)",
    gangs=[("1", "Front balcony ceiling light + outdoor socket", "Smart", "Sunset on, 11pm off (Aqara schedule)")],
)

pdf.board_card(
    "SB-BALCONY-WEST", "Inside, near west balcony door (or share corridor switch if door is shared)",
    1200, "1-gang Aqara H1 EU smart",
    "65 mm GI MS  -  75 x 75 x 65",
    "D10 (balcony shared)",
    gangs=[("1", "West balcony IP65 wall light + outdoor socket", "Smart", "Same schedule as front")],
)

# ---------------------------------------------------------------------------
# MASTER SCHEDULE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Master schedule")
pdf.h1("Master switch-board schedule",
       "Every board in the house, on one page. Keep this in your back pocket.")

pdf.body(
    "Cross-check this against the room-by-room pages and the materials checklist before chasing."
)

schedule = [
    # GF
    ["GF",  "SB-FOYER-1",       "W wall, foyer, L of door",        "1200", "4g smart",  "65", "B1 / B2 / B10",    "Foyer lights / screen / cove / spare"],
    ["GF",  "SB-LIVING-1",      "W wall, living, near foyer",      "1200", "4g smart",  "65", "B3 / B4",          "Main / cove / TV wash / chandelier [!!]"],
    ["GF",  "SB-LIVING-2",      "Stair-side wall (2-way partner)", "1200", "2g smart",  "65", "B3 / B4",          "Main lights + cove (2-way mirror)"],
    ["GF",  "SB-DINING",        "W of dining entry",               "1200", "3g smart",  "65", "B6 / B9",          "Pendant / downlights / cove"],
    ["GF",  "SB-KITCHEN",       "Entry to kitchen, N wall",        "1200", "4g DUMB",   "50", "A3",               "Ceiling LED / under-cab / exhaust / spare"],
    ["GF",  "SB-UTILITY",       "Near utility door",               "1200", "1g DUMB",   "50", "A3 share",         "Utility light only"],
    ["GF",  "SB-STORE",         "Outside store door",              "1200", "1g DUMB",   "50", "A3 share",         "Store light only"],
    ["GF",  "SB-MBED",          "Inside MBR, near door",           "1200", "4g smart",  "65", "C1",               "Main / read L / read R / master-off"],
    ["GF",  "SB-GFBATH",        "Outside bath, E wall, R of door", "1200/1050", "PIR + 20A", "50", "A1 / A2",      "PIR auto-bath / geyser switch"],
    ["GF",  "SB-POOJA",         "Outside pooja entry",             "1200", "2g smart",  "65", "B8",               "Ceiling panel / niche backlight"],
    ["GF",  "SB-STAIR-GF",      "Base of stairs",                  "1200", "1g smart",  "65", "B7",               "Stair lights (2-way w/ FF)"],
    ["GF",  "(DB enclosure)",   "W wall, foyer, behind door",      "1500", "n/a",       "100", "DB",              "40-way Acti9 (not a switch)"],
    # FF
    ["FF",  "SB-STAIR-FF",      "FF top landing",                  "1200", "1g smart",  "65", "B7",               "Stair lights (2-way partner)"],
    ["FF",  "SB-FFLIV",         "Central wall, between BRs",       "1200", "2g smart",  "65", "D9",               "Corridor downlights / spare"],
    ["FF",  "SB-BR1",           "Inside BR1, near door",           "1200", "4g smart",  "65", "D1",               "Main / read L / read R / master-off"],
    ["FF",  "SB-BR1-GEYSER",    "Outside Toilet 1 door",           "1050", "1g 20A DP", "50", "D4",               "Toilet 1 geyser (15L)"],
    ["FF",  "SB-BR2",           "Inside BR2, near door",           "1200", "4g smart",  "65", "D5 / D11",         "Main / read or cove / read or study / master-off"],
    ["FF",  "SB-BR2-GEYSER",    "Outside Toilet 2 door",           "1050", "1g 20A DP", "50", "D8",               "Toilet 2 geyser (15L)"],
    ["FF",  "SB-BALCONY-FRONT", "Near front balcony door",         "1200", "1g smart",  "65", "D10",              "Front balcony light + outdoor socket"],
    ["FF",  "SB-BALCONY-WEST",  "Near west balcony door",          "1200", "1g smart",  "65", "D10",              "West balcony light + outdoor socket"],
    ["FF",  "(Toilet 1 PIR)",   "Ceiling, inside Toilet 1",        "ceil", "ceil PIR",  "60", "D3",               "Lights + mirror + exhaust auto"],
    ["FF",  "(Toilet 2 PIR)",   "Ceiling, inside Toilet 2",        "ceil", "ceil PIR",  "60", "D7",               "Lights + mirror + exhaust auto"],
]

pdf.table(
    headers=["FL", "Board ID", "Location", "H mm", "Plate", "Box", "Circuit", "Controls"],
    rows=schedule,
    col_widths=[9, 30, 36, 14, 18, 11, 21, 35],
    font=7.6,
    line_h=3.8,
)

pdf.callout(
    "Total count  -  matches materials checklist",
    "Smart boards (65 mm box): 13.   Dumb boards (50 mm): 6 (kitchen, utility, store, GF bath, "
    "BR1 + BR2 geyser).   Plus 2x ceiling PIR in FF toilets and 1x DB enclosure recess.   "
    "Smart gangs total: ~32 (matches Aqara H1 SKU count in materials section 5)."
)

# ---------------------------------------------------------------------------
# SPECIAL SWITCHES
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Special switches")
pdf.h1("Special switches",
       "2-way pairs, master-off scenes, PIR auto-switches, geyser DP switches.")

pdf.h2("1.  The 2-way pair  -  staircase")
pdf.body(
    "Two physical switches at different locations, both controlling the SAME load. Used on the "
    "staircase so you can switch lights on at the bottom and off at the top (or vice versa) "
    "without retracing your steps.\n\n"
    "Locations: SB-STAIR-GF (base, GF) + SB-STAIR-FF (top landing, FF). Both 1-gang Aqara H1 EU. "
    "The Aqara modules pair as a 2-way group in the Home Assistant or Aqara app - no special "
    "wiring beyond pulling neutral to BOTH boxes (same as every smart switch)."
)

pdf.h2("2.  Master-off gang  -  bedrooms")
pdf.body(
    "On 4-gang bedroom plates (SB-MBED, SB-BR1, SB-BR2), the rightmost gang is configured as a "
    "MASTER-OFF SCENE: one tap turns off all room lights at once. Useful at bedtime - no "
    "wandering around switching each light off.\n\n"
    "Wiring: this gang controls NO physical load by itself. It is just a smart-button input that "
    "fires a Home Assistant scene. The electrician still pulls L+N+E to it, but no switched-live "
    "leg goes out from this gang. Owner programs the scene after move-in."
)

pdf.h2("3.  PIR (passive infra-red) auto-switches  -  bathrooms only")
pdf.body(
    "Bathrooms get PIR motion sensors instead of rocker switches because:\n"
    "  -  You don't want to touch a 230V switch with wet hands.\n"
    "  -  Lights left on overnight are common in family homes - PIR auto-off solves it.\n"
    "  -  Less plate clutter on the wall outside.\n\n"
    "GF Bathroom: WALL PIR outside the door (door swings on E wall, switches on E wall right of door).\n"
    "FF Toilets 1 + 2: CEILING PIR inside the toilet (covers shower zone, never loses motion mid-shower)."
)

pdf.h2("4.  Geyser switches  -  always outside bath, 1050 mm")
pdf.body(
    "Three geyser switches in the house:\n"
    "  -  GF Common Bathroom: outside, on E wall right of door, BELOW the PIR (1050 mm).\n"
    "  -  FF Toilet 1 (BR1 attached): outside Toilet 1 door, on BR1 side, 1050 mm.\n"
    "  -  FF Toilet 2 (BR2 attached): outside Toilet 2 door, on BR2 side, 1050 mm.\n\n"
    "All three are 1-gang 20A DP switches with a red neon indicator (Schneider AvatarOn-C glass "
    "plate, dumb). Red neon glows whenever the geyser circuit is live - visual confirmation. "
    "DEDICATED 16A or 20A RCBO at the DB - never share the geyser circuit with anything else."
)

# ---------------------------------------------------------------------------
# PRE-PLASTERING SIGN-OFF CHECKLIST
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Sign-off checklist")
pdf.h1("Pre-plastering sign-off",
       "Walk through this list with the electrician + mason BEFORE any plastering.")

pdf.body(
    "Tick each box. If anything is wrong, fix it NOW - once plaster is on, every fix means "
    "breaking and re-doing the wall."
)

pdf.h2("A.  Box depth  (the 50 vs 65 mm rule)")
pdf.table(
    headers=["#", "Item", "Tick"],
    rows=[
        ["A1",  "Foyer SB-FOYER-1 box is 65 mm, 4-gang (230 x 75 x 65)",    "[  ]"],
        ["A2",  "Living SB-LIVING-1 box is 65 mm, 4-gang",                  "[  ]"],
        ["A3",  "Living SB-LIVING-2 box is 65 mm, 2-gang",                  "[  ]"],
        ["A4",  "Dining SB-DINING box is 65 mm, 3-gang",                    "[  ]"],
        ["A5",  "MBR SB-MBED box is 65 mm, 4-gang",                         "[  ]"],
        ["A6",  "Pooja SB-POOJA box is 65 mm, 2-gang",                      "[  ]"],
        ["A7",  "Staircase SB-STAIR-GF box is 65 mm, 1-gang",               "[  ]"],
        ["A8",  "FF SB-STAIR-FF box is 65 mm, 1-gang",                      "[  ]"],
        ["A9",  "FF SB-FFLIV box is 65 mm, 2-gang",                         "[  ]"],
        ["A10", "FF SB-BR1 box is 65 mm, 4-gang",                           "[  ]"],
        ["A11", "FF SB-BR2 box is 65 mm, 4-gang",                           "[  ]"],
        ["A12", "FF SB-BALCONY-FRONT + SB-BALCONY-WEST are 65 mm, 1-gang",  "[  ]"],
        ["A13", "Kitchen / Utility / Store boxes are 50 mm (NOT 65 mm)",    "[  ]"],
        ["A14", "All 3 geyser-switch boxes are 50 mm at 1050 mm FFL",       "[  ]"],
        ["A15", "GF bath PIR/geyser combo box is 50 mm, 2-module",          "[  ]"],
    ],
    col_widths=[10, 148, 16],
    font=9,
)

pdf.h2("B.  Heights  (centre of plate from FFL)")
pdf.table(
    headers=["#", "Item", "Tick"],
    rows=[
        ["B1", "All 13 smart boards at 1200 mm FFL  +-5 mm",              "[  ]"],
        ["B2", "All 3 geyser switches at 1050 mm FFL",                    "[  ]"],
        ["B3", "GF bath: PIR at 1200 mm; geyser below at 1050 mm",        "[  ]"],
        ["B4", "AC sockets (4 total) all at 1850 mm FFL",                 "[  ]"],
        ["B5", "FF Wi-Fi AP wall plate at 2400 mm FFL, central wall",     "[  ]"],
        ["B6", "Sockets at 300 mm; bedside at 600 mm; counter at 1100",   "[  ]"],
        ["B7", "All boards >= 150 mm clear of any door frame / corner",   "[  ]"],
    ],
    col_widths=[10, 148, 16],
    font=9,
)

pdf.h2("C.  Wires inside box  (visible BEFORE plaster)")
pdf.table(
    headers=["#", "Item", "Tick"],
    rows=[
        ["C1", "Every smart-switch box has NEUTRAL (black) tail visible",    "[  ]"],
        ["C2", "Every box has earth (green/yellow) tail visible",            "[  ]"],
        ["C3", "Every wire end has masking-tape + marker label (circuit ID)","[  ]"],
        ["C4", "Switched-live leg colour is BLUE (NOT black)",               "[  ]"],
        ["C5", "Each gang has its own switched-live leg to correct load",    "[  ]"],
        ["C6", "All wires capped (no exposed copper) before plate fitment",  "[  ]"],
    ],
    col_widths=[10, 148, 16],
    font=9,
)

pdf.h2("D.  Conduit colour / labelling")
pdf.table(
    headers=["#", "Item", "Tick"],
    rows=[
        ["D1", "Power conduit (red 25 mm) separate from data (grey 25 mm)", "[  ]"],
        ["D2", "Every conduit end paint-marked or coloured-tape labelled",  "[  ]"],
        ["D3", "Conduit is plumb (vertical chases vertical)",               "[  ]"],
        ["D4", "Bends are 90 deg max; no flat-crushed bends; pull-string OK","[  ]"],
    ],
    col_widths=[10, 148, 16],
    font=9,
)

pdf.ln(4)
pdf.h2("Sign-off")
pdf.set_font("Helvetica", "", 10.5)
pdf.set_text_color(*INK)
pdf.multi_cell(0, 8,
    "Electrician        ____________________________________      Date  ______________\n\n"
    "Mason              ____________________________________      Date  ______________\n\n"
    "Owner              ____________________________________      Date  ______________"
)

# ---------------------------------------------------------------------------
# QUICK REFERENCE CARD - LAST PAGE
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_section("Quick reference")
pdf.h1("Quick reference card",
       "Photograph this page on your phone. Take it to site.")

# Three sections in framed boxes
def quick_box(y_start, h, title, body):
    x0 = pdf.PAGE_MARGIN_X
    pdf.set_fill_color(*PAPER_TINT)
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.rect(x0, y_start, pdf.CONTENT_W, h, "FD")
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(x0, y_start, 1.6, h, "F")
    pdf.set_xy(x0 + 6, y_start + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 5, title, ln=1)
    pdf.set_xy(x0 + 6, y_start + 9)
    pdf.set_font("Helvetica", "", 9.6)
    pdf.set_text_color(*INK)
    pdf.multi_cell(pdf.CONTENT_W - 10, 5, body)

y = pdf.get_y() + 2
quick_box(y, 50,
    "The 5 rules that never change",
    "1.  SMART BOARD = 65 mm box.   DUMB / SOCKET / GEYSER / PIR = 50 mm.\n"
    "2.  NEUTRAL (BLACK) at every switch board - even at dumb zones.\n"
    "3.  HEIGHTS:  switch boards 1200,  geyser 1050,  AC 1850,  bedside 600,  general socket 300,  counter 1100,  router 2400.\n"
    "4.  EARTH (green/yellow) at every switch, every socket, every metal fitting.  Continuity tested before plaster.\n"
    "5.  POWER (red/blue 25 mm) and DATA (grey 25 mm) NEVER share a conduit.")

y2 = y + 56
quick_box(y2, 60,
    "The heights that repeat across the house",
    "2400 mm    Wi-Fi router / AP wall plate   (FF Living central wall ONLY)\n"
    "1850 mm    AC sockets   (one per AC, dedicated RCBO)\n"
    "1200 mm    ALL switch boards (smart + dumb), all rooms, all floors\n"
    "1100 mm    Kitchen counter sockets   (above counter line)\n"
    "1050 mm    Geyser switches   (3x, all OUTSIDE bath doors)\n"
    " 600 mm    Bedside sockets   (5A + USB-C, both bedsides)\n"
    " 300 mm    General wall sockets   (TV wall, perimeter, fridge niche)")

y3 = y2 + 66
quick_box(y3, 50,
    "The premium look you are buying",
    "Smart switches    -    Aqara H1 EU   (tempered glass, frameless, backlit indicator, with neutral)\n"
    "Dumb switches     -    Schneider AvatarOn-C Glass   (or Legrand Arteor Square Glass / Norisys Cuboid Glass)\n"
    "Sockets           -    Same family as dumb switches   (matching glass plate)\n"
    "Geyser switch     -    20A DP, same glass plate family, with red neon indicator\n"
    "PIR (bathrooms)   -    Legrand Myrius PIR ceiling/wall, same glass-plate family\n\n"
    "All plates 86 mm tall, frameless, hidden screws.  Smart and dumb side-by-side read as one family.")

# Footer note
pdf.set_y(280)
pdf.set_font("Helvetica", "B", 9.5)
pdf.set_text_color(*GOLD_DARK)
pdf.cell(0, 5, "If anything on site differs from this PDF, STOP and call before chasing or plastering.",
         ln=1, align="C")
pdf.set_font("Helvetica", "I", 8.5)
pdf.set_text_color(*INK_FAINT)
pdf.cell(0, 5, "v2.0  -  2026-05-10  -  Ganesh Prasad D, Chitradurga", ln=1, align="C")

# ---------------------------------------------------------------------------
# WRITE
# ---------------------------------------------------------------------------
pdf.output(str(OUT))
print(f"Wrote: {OUT}  ({OUT.stat().st_size / 1024:.1f} KB)")
