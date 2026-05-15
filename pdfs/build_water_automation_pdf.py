"""
Build the Water Automation Master Plan PDF.
For: Electrician, Plumber, Owner.

Source-of-truth markdown:
  electrical/water-automation-conduits.md
  decisions/decision-log.md (2026-05-13 entries)

Run: python3 build_water_automation_pdf.py
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "WATER_AUTOMATION.pdf"

# ---------- Editorial palette (matches SWITCH_LAYOUT.pdf) ----------
INK         = ( 28,  28,  30)
INK_SOFT    = ( 90,  90,  95)
INK_FAINT   = (140, 140, 145)
RULE        = (220, 215, 205)
ROW_TINT    = (250, 246, 238)
PAPER_TINT  = (252, 248, 240)

GOLD        = (172, 130,  50)
GOLD_DARK   = (130,  95,  30)
GOLD_PALE   = (245, 234, 210)
GOLD_BAR    = (190, 150,  70)

DANGER      = (180,  60,  50)
DANGER_PALE = (250, 230, 225)
INFO        = ( 50, 100, 160)
INFO_PALE   = (228, 238, 250)
GOOD        = ( 70, 125,  70)
GOOD_PALE   = (228, 244, 230)
WARN        = (180, 130,  40)
WARN_PALE   = (252, 240, 215)

WATER       = ( 60, 130, 175)   # for water symbols
WATER_PALE  = (220, 235, 245)
COPPER      = (175, 110,  60)   # for cable runs


class WaterPDF(FPDF):
    PAGE_MARGIN_X = 18
    PAGE_MARGIN_TOP = 18
    PAGE_MARGIN_BOTTOM = 16
    CONTENT_W = 210 - 2 * 18  # 174

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=self.PAGE_MARGIN_BOTTOM)
        self.set_margins(self.PAGE_MARGIN_X, self.PAGE_MARGIN_TOP, self.PAGE_MARGIN_X)
        self._section_label = ""

    # ---------- header / footer ----------
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(8)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*INK_FAINT)
        self.set_x(self.PAGE_MARGIN_X)
        self.cell(self.CONTENT_W / 2, 5,
                  self._section_label.upper() if self._section_label else "WATER AUTOMATION",
                  align="L")
        self.set_x(self.PAGE_MARGIN_X + self.CONTENT_W / 2)
        self.cell(self.CONTENT_W / 2, 5, f"{self.page_no():02d}", align="R")
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.25)
        self.line(self.PAGE_MARGIN_X, 15, 210 - self.PAGE_MARGIN_X, 15)
        self.set_xy(self.PAGE_MARGIN_X, self.PAGE_MARGIN_TOP)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*INK_FAINT)
        self.cell(0, 5,
                  "v1.0  -  2026-05-13  -  Hand to electrician BEFORE chasing or plastering",
                  align="C")

    # ---------- typography ----------
    def set_section(self, label):
        self._section_label = label

    def h1(self, text, subtitle=None):
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
        y = self.get_y() + 1
        self.set_draw_color(*GOLD_BAR)
        self.set_line_width(0.6)
        self.line(self.PAGE_MARGIN_X, y, self.PAGE_MARGIN_X + 22, y)
        self.set_line_width(0.2)
        self.ln(6)

    def h2(self, text):
        self.ln(2)
        y = self.get_y()
        self.set_fill_color(*GOLD_BAR)
        self.rect(self.PAGE_MARGIN_X, y + 1.2, 1.4, 5.6, "F")
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

    # ---------- callouts ----------
    def _callout(self, label, text, bar_color, label_color):
        self.ln(1)
        x0 = self.PAGE_MARGIN_X
        body_x = x0 + 5
        body_w = self.CONTENT_W - 5
        y_start = self.get_y()
        self.set_xy(body_x, y_start)
        self.set_font("Helvetica", "B", 9.2)
        self.set_text_color(*label_color)
        self.cell(0, 5.5, label.upper(), ln=1)
        self.set_x(body_x)
        self.set_font("Helvetica", "", 9.6)
        self.set_text_color(*INK)
        self.multi_cell(body_w, 5.0, text)
        y_end = self.get_y()
        self.set_fill_color(*bar_color)
        self.rect(x0, y_start + 0.5, 1.4, y_end - y_start - 0.5, "F")
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

    # ---------- key-value rows ----------
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

    # ---------- table ----------
    def table(self, headers, rows, col_widths, font=9, line_h=4.5, header_bg=None,
              header_fg=(255, 255, 255), zebra=True):
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
            x_start = self.get_x()
            y_start = self.get_y()
            if zebra and fill:
                self.set_fill_color(*ROW_TINT)
                self.rect(x_start, y_start, sum(col_widths), row_h, "F")
            for cell, w in zip(row, col_widths):
                tx = self.get_x()
                ty = self.get_y()
                self.set_xy(tx + 2, ty + 1.5)
                self.multi_cell(w - 4, line_h, str(cell) if cell else "")
                self.set_xy(tx + w, ty)
            self.ln(row_h)
            self.set_draw_color(*RULE)
            self.set_line_width(0.15)
            self.line(self.PAGE_MARGIN_X, self.get_y(),
                      self.PAGE_MARGIN_X + sum(col_widths), self.get_y())
            fill = not fill

    def divider(self):
        self.ln(2)
        y = self.get_y()
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(self.PAGE_MARGIN_X, y, 210 - self.PAGE_MARGIN_X, y)
        self.ln(3)

    # ============================================================
    #                  CUSTOM WATER DIAGRAMS
    # ============================================================

    def _node_box(self, x, y, w, h, title, sub=None, fill=PAPER_TINT, border=INK,
                  title_size=8.5, sub_size=6.8):
        """Draw a labelled node box. Title goes top-centred, sub goes bottom-centred.
        Both shrink fonts if needed; sub stays in the bottom half."""
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "FD")
        title_lines = (title or "").count("\n") + 1
        title_lh = title_size * 0.35  # mm
        title_block_h = title_lines * title_lh + 0.5
        # title
        self.set_font("Helvetica", "B", title_size)
        self.set_text_color(*INK)
        if sub:
            # title in upper portion
            self.set_xy(x + 1, y + 1.5)
        else:
            # title vertically centred
            self.set_xy(x + 1, y + (h - title_block_h) / 2)
        self.multi_cell(w - 2, title_lh, title, align="C")
        if sub:
            sub_lines = sub.count("\n") + 1
            sub_lh = sub_size * 0.4
            sub_block_h = sub_lines * sub_lh
            self.set_font("Helvetica", "", sub_size)
            self.set_text_color(*INK_SOFT)
            self.set_xy(x + 1, y + h - sub_block_h - 1)
            self.multi_cell(w - 2, sub_lh, sub, align="C")

    def _arrow(self, x1, y1, x2, y2, color=INK, lw=0.5, dashed=False, label=None,
               label_offset=2, head=True):
        """Draw a line from (x1,y1) to (x2,y2) with optional arrow head and label."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        if dashed:
            # poor-man's dashed: short segments
            import math
            dx, dy = x2 - x1, y2 - y1
            length = math.hypot(dx, dy)
            if length == 0:
                return
            ux, uy = dx / length, dy / length
            seg = 1.5
            gap = 1.2
            t = 0.0
            while t < length:
                x_a = x1 + ux * t
                y_a = y1 + uy * t
                t2 = min(t + seg, length)
                x_b = x1 + ux * t2
                y_b = y1 + uy * t2
                self.line(x_a, y_a, x_b, y_b)
                t = t2 + gap
        else:
            self.line(x1, y1, x2, y2)
        # arrow head
        if head:
            import math
            ang = math.atan2(y2 - y1, x2 - x1)
            ah = 1.6
            self.line(x2, y2,
                      x2 - ah * math.cos(ang - math.pi / 6),
                      y2 - ah * math.sin(ang - math.pi / 6))
            self.line(x2, y2,
                      x2 - ah * math.cos(ang + math.pi / 6),
                      y2 - ah * math.sin(ang + math.pi / 6))
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*color)
            self.text(mx + label_offset, my - 0.5, label)

    # ---------- SYSTEM OVERVIEW DIAGRAM ----------
    def system_overview(self, x, y, w, h):
        """Full water automation network diagram."""
        # background panel
        self.set_fill_color(*PAPER_TINT)
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.rect(x, y, w, h, "FD")

        # 3 horizontal "zones": Terrace top, Ground floor middle, Outside bottom
        zone_h = h / 3
        # zone labels (faint, left margin)
        zone_labels = [("TERRACE (SW corner)", y),
                       ("GROUND FLOOR - INSIDE",  y + zone_h),
                       ("OUTSIDE  (NE / E walls)", y + 2 * zone_h)]
        for label, zy in zone_labels:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*INK_FAINT)
            self.text(x + 2, zy + 4, label)
            # subtle dividing line
            self.set_draw_color(*RULE)
            self.set_line_width(0.15)
            self.line(x, zy, x + w, zy)

        # ---- TERRACE: Sintex tank + JB ----
        # Sintex tank (drawn as cylinder cross-section)
        tank_x = x + w * 0.18
        tank_y = y + 8
        tank_w = 26
        tank_h = zone_h - 14
        self.set_fill_color(*WATER_PALE)
        self.set_draw_color(*WATER)
        self.set_line_width(0.4)
        self.rect(tank_x, tank_y, tank_w, tank_h, "FD")
        # water fill
        water_top = tank_y + tank_h * 0.25
        self.set_fill_color(*WATER)
        self.rect(tank_x + 1, water_top, tank_w - 2, tank_h - (water_top - tank_y) - 1, "F")
        # label (inside tank, above water level)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WATER)
        self.set_xy(tank_x, tank_y + 2)
        self.cell(tank_w, 3, "SINTEX", align="C")
        self.set_font("Helvetica", "", 6)
        self.set_xy(tank_x, tank_y + 5)
        self.cell(tank_w, 3, "1500 L", align="C")
        # sensor riser on top
        riser_x = tank_x + tank_w / 2 - 2
        self.set_fill_color(*INK_SOFT)
        self.set_draw_color(*INK)
        self.rect(riser_x, tank_y - 6, 4, 6, "FD")
        # sensor symbol on top of riser (small ultrasonic cap)
        self.set_fill_color(*INFO_PALE)
        self.set_draw_color(*INFO)
        self.rect(riser_x - 2, tank_y - 10, 8, 4, "FD")
        self.set_font("Helvetica", "B", 6)
        self.set_text_color(*INFO)
        self.set_xy(riser_x - 2, tank_y - 10)
        self.cell(8, 4, "JSN", align="C")
        # label sensor model to the side
        self.set_font("Helvetica", "", 5.5)
        self.set_text_color(*INK_SOFT)
        self.text(riser_x + 8, tank_y - 7, "JSN-SR04T")
        # float symbol inside (a small circle)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*DANGER)
        self.set_line_width(0.4)
        self.ellipse(tank_x + 3, water_top - 2, 3, 3, "FD")
        self.set_font("Helvetica", "B", 5)
        self.set_text_color(*DANGER)
        self.text(tank_x + 3.4, water_top - 0.4, "F")

        # Sintex JB
        sjb_x = tank_x + tank_w + 14
        sjb_y = tank_y + 6
        sjb_w = 30
        sjb_h = 18
        self._node_box(sjb_x, sjb_y, sjb_w, sjb_h,
                       "SINTEX JB",
                       "WT32-ETH01 + PoE\nIP65 200x200x100",
                       fill=INFO_PALE, border=INFO)

        # Sensor cable from sensor to JB (orange)
        self._arrow(riser_x + 4, tank_y - 9, sjb_x, sjb_y + 4,
                    color=COPPER, lw=0.4, label="sensor", head=False)
        # Float cable from tank to JB (red, dashed)
        self._arrow(tank_x + tank_w, water_top - 2, sjb_x, sjb_y + sjb_h - 4,
                    color=DANGER, lw=0.4, dashed=True, label="float", head=False)

        # ---- GROUND FLOOR: Server + DB Cupboard ----
        # Server (left)
        srv_x = x + w * 0.18
        srv_y = y + zone_h + 8
        srv_w = 30
        srv_h = 22
        self._node_box(srv_x, srv_y, srv_w, srv_h,
                       "SERVER", "Staircase niche\nHome Assistant\nPoE switch",
                       fill=GOOD_PALE, border=GOOD)

        # DB Cupboard (center-right)
        db_x = x + w * 0.55
        db_y = y + zone_h + 6
        db_w = 60
        db_h = 32
        self.set_fill_color(*GOLD_PALE)
        self.set_draw_color(*GOLD_DARK)
        self.set_line_width(0.5)
        self.rect(db_x, db_y, db_w, db_h, "FD")
        # cupboard label
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GOLD_DARK)
        self.set_xy(db_x + 2, db_y + 1)
        self.cell(db_w - 4, 3.5, "DB CUPBOARD (foyer)", align="C")
        # contents inside cupboard
        inner_y = db_y + 6
        cell_w = (db_w - 8) / 3
        # P1 starter
        self._node_box(db_x + 2, inner_y, cell_w, 22,
                       "P1", "PSP1H\nborewell",
                       fill=PAPER_TINT, border=INK_SOFT,
                       title_size=9, sub_size=6.5)
        # P2 starter
        self._node_box(db_x + 3 + cell_w, inner_y, cell_w, 22,
                       "P2", "PSP1\nbooster",
                       fill=PAPER_TINT, border=INK_SOFT,
                       title_size=9, sub_size=6.5)
        # Sonoff
        self._node_box(db_x + 4 + 2 * cell_w, inner_y, cell_w, 22,
                       "SONOFF", "DUALR3\n2-ch WiFi",
                       fill=INFO_PALE, border=INFO,
                       title_size=8.5, sub_size=6.5)

        # Cat6 from Sintex JB -> Server (long line down + across)
        # We'll route through "zone wire path" : down from sjb, across to srv
        self._arrow(sjb_x + sjb_w / 2, sjb_y + sjb_h, sjb_x + sjb_w / 2, y + zone_h - 1,
                    color=INFO, lw=0.5, head=False)
        self._arrow(sjb_x + sjb_w / 2, y + zone_h + 1, sjb_x + sjb_w / 2, srv_y,
                    color=INFO, lw=0.5, head=True)
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*INFO)
        self.text(sjb_x + sjb_w / 2 + 1, y + zone_h + 5, "C-Sintex-1")
        self.text(sjb_x + sjb_w / 2 + 1, y + zone_h + 9, "Cat6 PoE")

        # Sintex float -> DB cupboard
        self._arrow(sjb_x + sjb_w, sjb_y + sjb_h - 2, db_x + db_w * 0.2, db_y,
                    color=DANGER, lw=0.4, dashed=True, head=True)
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*DANGER)
        self.text(sjb_x + sjb_w + 5, sjb_y + sjb_h + 3, "C-Sintex-2 (float, 220V)")

        # Server -> DB Cupboard (Cat6 backup, dashed)
        self._arrow(srv_x + srv_w, srv_y + srv_h / 2, db_x, db_y + db_h / 2,
                    color=GOOD, lw=0.4, dashed=True, head=True)
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*GOOD)
        self.text(srv_x + srv_w + 2, srv_y + srv_h / 2 - 1, "C-DB-Backup (empty conduit)")
        self.set_font("Helvetica", "", 6)
        self.set_text_color(*INK_FAINT)
        self.text(srv_x + srv_w + 2, srv_y + srv_h / 2 + 4, "(Sonoff reaches server via WiFi)")

        # ---- OUTSIDE: Sump JB + Sump + Borewell + P2 cage ----
        # Sump JB
        smjb_x = x + w * 0.30
        smjb_y = y + 2 * zone_h + 8
        smjb_w = 30
        smjb_h = 18
        self._node_box(smjb_x, smjb_y, smjb_w, smjb_h,
                       "SUMP JB",
                       "WT32-ETH01 + PoE\nIP66 outdoor",
                       fill=INFO_PALE, border=INFO)

        # Sump tank (wide rectangle below)
        sump_x = smjb_x - 6
        sump_y = smjb_y + smjb_h + 3
        sump_w = smjb_w + 12
        sump_h = zone_h - smjb_h - 14
        self.set_fill_color(*WATER_PALE)
        self.set_draw_color(*WATER)
        self.set_line_width(0.4)
        self.rect(sump_x, sump_y, sump_w, sump_h, "FD")
        # water fill
        wt = sump_y + sump_h * 0.3
        self.set_fill_color(*WATER)
        self.rect(sump_x + 1, wt, sump_w - 2, sump_h - (wt - sump_y) - 1, "F")
        # label
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WATER)
        self.set_xy(sump_x, sump_y + sump_h + 1)
        self.cell(sump_w, 3, "SUMP 5000 L", align="C")
        # pressure probe
        probe_x = sump_x + 5
        self.set_fill_color(*COPPER)
        self.set_draw_color(*COPPER)
        self.ellipse(probe_x, sump_y + sump_h - 3, 2.5, 2.5, "F")
        # low-level float (down low)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*DANGER)
        self.ellipse(sump_x + sump_w - 6, sump_y + sump_h * 0.7, 3, 3, "FD")
        self.set_font("Helvetica", "B", 5)
        self.set_text_color(*DANGER)
        self.text(sump_x + sump_w - 5.4, sump_y + sump_h * 0.7 + 1.5, "F")

        # sensor + float cables from sump up to JB
        self._arrow(probe_x, sump_y, probe_x, smjb_y + smjb_h,
                    color=COPPER, lw=0.4, head=False)
        self._arrow(sump_x + sump_w - 6, sump_y, smjb_x + smjb_w - 4,
                    smjb_y + smjb_h, color=DANGER, lw=0.4, dashed=True, head=False)

        # P2 cage (right side of outside zone)
        p2_x = x + w * 0.75
        p2_y = y + 2 * zone_h + 12
        p2_w = 22
        p2_h = 18
        self._node_box(p2_x, p2_y, p2_w, p2_h, "P2 PUMP", "in cage\nE wall",
                       fill=WARN_PALE, border=WARN)
        # Borewell (rightmost)
        bw_x = x + w - 25
        bw_y = y + 2 * zone_h + 8
        bw_w = 18
        bw_h = zone_h - 16
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.5)
        self.rect(bw_x, bw_y, bw_w, bw_h, "FD")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*INK)
        self.set_xy(bw_x, bw_y - 4)
        self.cell(bw_w, 3, "BOREWELL", align="C")
        # P1 motor down in borewell
        self.set_fill_color(*DANGER_PALE)
        self.set_draw_color(*DANGER)
        self.rect(bw_x + 4, bw_y + bw_h - 10, 10, 7, "FD")
        self.set_font("Helvetica", "B", 6)
        self.set_text_color(*DANGER)
        self.set_xy(bw_x + 4, bw_y + bw_h - 9)
        self.cell(10, 4, "P1", align="C")
        self.set_font("Helvetica", "", 5.5)
        self.text(bw_x + 4, bw_y + bw_h - 4, "submersible")

        # Cat6 from Sump JB up to server zone -> server
        self._arrow(smjb_x + smjb_w / 2, smjb_y, smjb_x + smjb_w / 2, y + zone_h * 2,
                    color=INFO, lw=0.5, head=False)
        # bend left to server
        self._arrow(smjb_x + smjb_w / 2, y + zone_h * 2 - 1, srv_x + srv_w / 2,
                    y + zone_h * 2 - 1, color=INFO, lw=0.5, head=False)
        self._arrow(srv_x + srv_w / 2, y + zone_h * 2, srv_x + srv_w / 2, srv_y + srv_h,
                    color=INFO, lw=0.5, head=True)
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*INFO)
        self.text(smjb_x - 18, smjb_y - 3, "C-Sump-1 (Cat6 PoE)")

        # Sump float -> DB cupboard (via interior wall chase, dashed)
        self._arrow(smjb_x, smjb_y + smjb_h / 2, db_x + db_w * 0.65, db_y + db_h,
                    color=DANGER, lw=0.4, dashed=True, head=True)
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*DANGER)
        self.text(smjb_x - 20, smjb_y + smjb_h / 2 + 4, "C-Sump-2")
        self.text(smjb_x - 20, smjb_y + smjb_h / 2 + 7, "(float, 220V)")

        # Motor power cables: DB cupboard -> P2 and -> Borewell
        # P2 motor power
        self._arrow(db_x + db_w * 0.55, db_y + db_h, p2_x + p2_w / 2, p2_y,
                    color=COPPER, lw=0.6, head=True)
        # P1 motor power
        self._arrow(db_x + db_w * 0.9, db_y + db_h, bw_x + bw_w / 2, bw_y,
                    color=COPPER, lw=0.7, head=True)
        # Conduit labels positioned mid-arrow, slightly offset to the left to avoid line overlap
        self.set_font("Helvetica", "B", 6)
        self.set_text_color(*COPPER)
        mid_p2_x = (db_x + db_w * 0.55 + p2_x + p2_w / 2) / 2
        mid_p2_y = (db_y + db_h + p2_y) / 2
        self.text(mid_p2_x - 12, mid_p2_y - 0.5, "C-Motor-P2")
        mid_p1_x = (db_x + db_w * 0.9 + bw_x + bw_w / 2) / 2
        mid_p1_y = (db_y + db_h + bw_y) / 2
        self.text(mid_p1_x + 2, mid_p1_y - 0.5, "C-Motor-P1")

        # Reset
        self.set_draw_color(*INK)
        self.set_line_width(0.2)

    # ---------- JB Interior Diagram ----------
    def jb_interior(self, x, y, w, h, title, contents, glands_bottom):
        """Draw a JB cross-section showing its internals."""
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK)
        self.set_line_width(0.6)
        self.rect(x, y, w, h, "FD")
        # title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*INK)
        self.set_xy(x + 3, y + 3)
        self.cell(w - 6, 4, title)
        # subtitle
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_FAINT)
        self.set_xy(x + 3, y + 7)
        self.cell(w - 6, 4, "IP65 / IP66 enclosure  -  200 x 200 x 100 mm")
        # interior region
        ix = x + 5
        iy = y + 14
        iw = w - 10
        ih = h - 26
        self.set_fill_color(*PAPER_TINT)
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.rect(ix, iy, iw, ih, "FD")
        # draw contents as small labelled boxes
        n = len(contents)
        avail_h = ih - 4
        box_h = min(10, avail_h / n - 1)
        for i, (label, sub, color) in enumerate(contents):
            by = iy + 2 + i * (box_h + 1.5)
            self.set_fill_color(*color[1])
            self.set_draw_color(*color[0])
            self.set_line_width(0.3)
            self.rect(ix + 3, by, iw - 6, box_h, "FD")
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(*color[0])
            self.set_xy(ix + 5, by + 1)
            self.cell(iw - 10, 3.5, label)
            self.set_font("Helvetica", "", 6.5)
            self.set_text_color(*INK_SOFT)
            self.set_xy(ix + 5, by + 5)
            self.cell(iw - 10, 3, sub)
        # cable glands at bottom
        gy = y + h - 4
        for i, (lbl, color) in enumerate(glands_bottom):
            gx = x + 6 + i * ((w - 12) / max(1, len(glands_bottom) - 1) if len(glands_bottom) > 1 else 0)
            self.set_fill_color(*color)
            self.set_draw_color(*INK_SOFT)
            self.set_line_width(0.3)
            self.ellipse(gx - 1.2, gy - 1.2, 2.4, 2.4, "FD")
            self.set_font("Helvetica", "", 6)
            self.set_text_color(*INK_SOFT)
            self.text(gx - 6, gy + 4, lbl)

    # ---------- DB Cupboard Interior ----------
    def db_cupboard_interior(self, x, y, w, h):
        """Show the DB cupboard layout."""
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK)
        self.set_line_width(0.6)
        self.rect(x, y, w, h, "FD")
        # title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*INK)
        self.set_xy(x + 3, y + 3)
        self.cell(w - 6, 4, "DB CUPBOARD INTERIOR  (foyer, adjacent to DB)")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_FAINT)
        self.set_xy(x + 3, y + 7)
        self.cell(w - 6, 4, "Lockable, ventilated,  >=  600 x 400 x 250 mm internal")
        # top vent
        self._draw_vent(x + 5, y + 13, w - 10, 4)
        # main inner area
        inner_y = y + 19
        inner_h = h - 32
        self.set_fill_color(*PAPER_TINT)
        self.set_draw_color(*RULE)
        self.rect(x + 5, inner_y, w - 10, inner_h, "FD")
        # P1 starter box (visualized as Magnum panel)
        p1_x = x + 8
        p1_y = inner_y + 3
        p1_w = (w - 16) * 0.35
        p1_h = inner_h - 6
        self._magnum_starter(p1_x, p1_y, p1_w, p1_h, "P1 - BOREWELL (existing)",
                             "Magnum Pradhaan PSP1H\n1.5HP, single-phase")
        # P2 starter
        p2_x = p1_x + p1_w + 2
        self._magnum_starter(p2_x, p1_y, p1_w, p1_h, "P2 - BOOSTER (new)",
                             "Magnum Pradhaan PSP1\n1HP, single-phase")
        # Sonoff + terminal block column
        sn_x = p2_x + p1_w + 2
        sn_w = (w - 16) - 2 * (p1_w + 2)
        # Sonoff
        self.set_fill_color(*INFO_PALE)
        self.set_draw_color(*INFO)
        self.set_line_width(0.5)
        self.rect(sn_x, p1_y, sn_w, p1_h * 0.5 - 1, "FD")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*INFO)
        self.set_xy(sn_x + 1, p1_y + 1)
        self.cell(sn_w - 2, 3.5, "SONOFF DUALR3")
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*INK_SOFT)
        self.set_xy(sn_x + 1, p1_y + 5)
        self.multi_cell(sn_w - 2, 3, "Ch1 -> P1 coil\nCh2 -> P2 coil\nWiFi to server", align="L")
        # Terminal blocks
        tb_y = p1_y + p1_h * 0.5 + 1
        tb_h = p1_h * 0.5 - 1
        self.set_fill_color(*DANGER_PALE)
        self.set_draw_color(*DANGER)
        self.rect(sn_x, tb_y, sn_w, tb_h, "FD")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*DANGER)
        self.set_xy(sn_x + 1, tb_y + 1)
        self.cell(sn_w - 2, 3.5, "FLOAT TERMINALS")
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*INK_SOFT)
        self.set_xy(sn_x + 1, tb_y + 5)
        self.multi_cell(sn_w - 2, 3, "Sintex high float\nSump low float\njumpered to coils", align="L")
        # bottom vent
        self._draw_vent(x + 5, y + h - 11, w - 10, 4)
        # cable entries label at bottom
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*INK_FAINT)
        self.set_xy(x + 3, y + h - 4)
        self.cell(w - 6, 3, "Cable entries from below: 7 conduits enter through cupboard back/bottom panel", align="C")

    def _draw_vent(self, x, y, w, h):
        """Slatted vent representation."""
        self.set_draw_color(*INK_SOFT)
        self.set_line_width(0.3)
        slats = 8
        for i in range(slats):
            sx = x + i * w / slats
            self.rect(sx + 0.5, y + 1, w / slats - 1, h - 2, "D")

    def _magnum_starter(self, x, y, w, h, title, sub):
        """Stylised Magnum Pradhaan starter."""
        self.set_fill_color(*GOLD_PALE)
        self.set_draw_color(*GOLD_DARK)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "FD")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*GOLD_DARK)
        self.set_xy(x + 1, y + 1)
        self.cell(w - 2, 3.5, title)
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*INK_SOFT)
        self.set_xy(x + 1, y + 5)
        self.multi_cell(w - 2, 3, sub, align="L")
        # Green + Red buttons at bottom
        btn_y = y + h - 8
        # green
        self.set_fill_color(*GOOD)
        self.set_draw_color(*GOOD)
        self.ellipse(x + w * 0.32 - 2, btn_y, 3.5, 3.5, "F")
        self.set_font("Helvetica", "B", 5.5)
        self.set_text_color(255, 255, 255)
        self.text(x + w * 0.32 - 1, btn_y + 2, "ON")
        # red
        self.set_fill_color(*DANGER)
        self.set_draw_color(*DANGER)
        self.ellipse(x + w * 0.62 - 2, btn_y, 3.5, 3.5, "F")
        self.text(x + w * 0.62 - 1.4, btn_y + 2, "OFF")
        # label below
        self.set_font("Helvetica", "I", 5.5)
        self.set_text_color(*INK_FAINT)
        self.set_xy(x, y + h - 3)
        self.cell(w, 3, "manual override", align="C")

    # ---------- STARTER WIRING DIAGRAM (the key circuit) ----------
    def starter_wiring(self, x, y, w, h):
        """Schematic: how Sonoff taps into Magnum starter's control circuit."""
        # outer frame
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "FD")
        # title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*INK)
        self.set_xy(x + 3, y + 3)
        self.cell(w - 6, 4, "STARTER CONTROL CIRCUIT  (Magnum Pradhaan + Sonoff tap)")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_FAINT)
        self.set_xy(x + 3, y + 7)
        self.cell(w - 6, 4, "Identical pattern for P1 and P2.  Manual + automated paths coexist.")

        # Schematic area
        sx = x + 5
        sy = y + 14
        sw = w - 10
        sh = h - 20

        # Define key node positions on a horizontal control rail
        # Layout:  L -- MCB -- OL -- RED -- [GREEN||AUX||SONOFF] -- FLOAT -- COIL -- N
        rail_y = sy + 22
        x_L     = sx + 6
        x_MCB   = sx + 22
        x_OL    = sx + 42
        x_RED   = sx + 62
        x_PAR_L = sx + 78
        x_PAR_R = sx + 118
        x_FLOAT = sx + 134
        x_COIL  = sx + 150
        x_N     = sx + sw - 4

        # base rail line (left + right of parallel block)
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.line(x_L, rail_y, x_PAR_L, rail_y)
        self.line(x_PAR_R, rail_y, x_N, rail_y)

        # L terminal
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*DANGER)
        self.text(x_L - 7, rail_y - 2.5, "L 220V")
        self.set_fill_color(*DANGER)
        self.ellipse(x_L - 1, rail_y - 1, 2, 2, "F")
        # N terminal
        self.set_text_color(*INK)
        self.text(x_N + 2, rail_y - 2.5, "N")
        self.set_fill_color(*INK)
        self.ellipse(x_N - 1, rail_y - 1, 2, 2, "F")

        # Inline components (label only inside box, no sub)
        self._inline_component(x_MCB,   rail_y, "MCB",   color=INFO)
        self._inline_component(x_OL,    rail_y, "OL",    color=GOLD_DARK)
        self._inline_component(x_RED,   rail_y, "RED",   color=DANGER)
        self._inline_component(x_FLOAT, rail_y, "FLOAT", color=DANGER)
        self._coil_symbol(x_COIL, rail_y, "COIL", "contactor")

        # Parallel branches between x_PAR_L and x_PAR_R
        branch_offsets = [-14, 0, 14]
        labels = [
            ("GREEN",  GOOD),
            ("AUX",    INK_SOFT),
            ("SONOFF", INFO),
        ]
        top_y = rail_y + branch_offsets[0]
        bot_y = rail_y + branch_offsets[-1]
        # vertical connectors at left + right edges of the parallel block
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.line(x_PAR_L, top_y, x_PAR_L, bot_y)
        self.line(x_PAR_R, top_y, x_PAR_R, bot_y)
        # individual horizontal branches + component on each
        for off, (lbl, col) in zip(branch_offsets, labels):
            by = rail_y + off
            self.line(x_PAR_L, by, x_PAR_R, by)
            self._inline_component((x_PAR_L + x_PAR_R) / 2, by, lbl, color=col)

        # "ADD" annotation pointing to the SONOFF branch (to the LEFT of parallel block)
        ay = rail_y + branch_offsets[-1]
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*INFO)
        self.text(x_PAR_L - 18, ay + 1, "ADD -->")

        # Component legend below the schematic (2 rows of labels)
        leg_y = sy + sh - 16
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(sx, leg_y - 2, sx + sw, leg_y - 2)
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*INK_SOFT)
        self.text(sx, leg_y + 2, "LEGEND:")
        legend_row1 = [
            ("MCB",   "16A Type C",       INFO),
            ("OL",    "thermal overload", GOLD_DARK),
            ("RED",   "manual stop (NC)", DANGER),
            ("FLOAT", "Sintex high (NC)", DANGER),
            ("COIL",  "contactor coil",   INFO),
        ]
        legend_row2 = [
            ("GREEN",  "manual start button (NO)", GOOD),
            ("AUX",    "latching contact (NO)",    INK_SOFT),
            ("SONOFF", "server start/stop (NO)",   INFO),
        ]

        def draw_row(items, row_y):
            lx = sx + 18
            for lbl, desc, col in items:
                self.set_font("Helvetica", "B", 6.8)
                self.set_text_color(*col)
                self.text(lx, row_y, lbl)
                lbl_w = self.get_string_width(lbl)
                self.set_font("Helvetica", "", 6.5)
                self.set_text_color(*INK)
                self.text(lx + lbl_w + 1.5, row_y, "= " + desc)
                desc_w = self.get_string_width("= " + desc)
                lx += lbl_w + 1.5 + desc_w + 6

        draw_row(legend_row1, leg_y + 2)
        draw_row(legend_row2, leg_y + 6)

        # Bottom path notes
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*INK_SOFT)
        self.text(sx, leg_y + 11, "Existing path:  L -> MCB -> OL -> RED(NC) -> [GREEN(NO) latched by AUX] -> FLOAT(NC) -> COIL -> N")
        self.text(sx, leg_y + 14, "Float failsafe:  Sintex high-level float opens (when full) -> coil drops -> motor stops, mechanically.")

    def _inline_component(self, cx, cy, label, color=INK):
        """Draw a small rectangular component with just a label inside."""
        cw = 14
        ch = 8
        self.set_fill_color(*PAPER_TINT)
        self.set_draw_color(*color)
        self.set_line_width(0.5)
        self.rect(cx - cw / 2, cy - ch / 2, cw, ch, "FD")
        self.set_font("Helvetica", "B", 7.2)
        self.set_text_color(*color)
        self.set_xy(cx - cw / 2, cy - 2)
        self.cell(cw, 4, label, align="C")

    def _coil_symbol(self, cx, cy, label, sub):
        """Draw a contactor coil as a small rectangle with diagonal pattern."""
        cw = 11
        ch = 7
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INFO)
        self.set_line_width(0.5)
        self.rect(cx - cw / 2, cy - ch / 2, cw, ch, "FD")
        # diagonal hatching
        self.set_line_width(0.25)
        for t in range(-2, 12, 2):
            self.line(cx - cw / 2 + t, cy - ch / 2,
                      cx - cw / 2 + t + ch, cy + ch / 2)
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*INFO)
        self.set_xy(cx - cw / 2, cy + ch / 2 + 0.5)
        self.cell(cw, 3, label, align="C")
        self.set_font("Helvetica", "", 5.5)
        self.set_text_color(*INK_SOFT)
        self.set_xy(cx - cw / 2, cy + ch / 2 + 3)
        self.cell(cw, 2.5, sub, align="C")

    # ---------- POWER CHAIN DIAGRAM ----------
    def power_chain(self, x, y, w, h):
        """How PoE delivers power to ESP32 and then to sensor."""
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*INK)
        self.set_xy(x + 3, y + 3)
        self.cell(w - 6, 4, "POWER CHAIN inside each JB  (PoE -> ESP32 -> sensor)")
        # node positions
        sx = x + 6
        sy = y + 16
        node_w = (w - 18) / 4
        node_h = h - 30
        nodes = [
            ("PoE Cat6", "48 V DC\n+ data", INFO, INFO_PALE),
            ("PoE splitter", "splits to:\n5V power + data", GOOD, GOOD_PALE),
            ("ESP32 board", "WT32-ETH01\n5V regulator\nADC reads sensor", INFO, INFO_PALE),
            ("Sensor", "JSN-SR04T\nor DFRobot probe", COPPER, WARN_PALE),
        ]
        last_x_end = None
        for i, (lbl, sub, c, fc) in enumerate(nodes):
            nx = sx + i * (node_w + 2)
            self._node_box(nx, sy, node_w, node_h, lbl, sub, fill=fc, border=c)
            if last_x_end is not None:
                self._arrow(last_x_end, sy + node_h / 2, nx, sy + node_h / 2,
                            color=c, lw=0.6, head=True)
            last_x_end = nx + node_w
        # bottom note
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*INK_SOFT)
        self.set_xy(x + 4, y + h - 8)
        self.multi_cell(w - 8, 3.5,
                        "One cable in (Cat6 PoE). Sensor draws ~15mA via ESP32's 5V output pin. "
                        "No separate 230V at the JB.")


# ===================================================================
#                          PAGES
# ===================================================================

def page_cover(pdf: WaterPDF):
    pdf.add_page()
    # full-bleed cream tint top
    pdf.set_fill_color(*PAPER_TINT)
    pdf.rect(0, 0, 210, 297, "F")

    # top bar
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 0, 210, 2.5, "F")

    # title block
    pdf.set_xy(18, 50)
    pdf.set_font("Helvetica", "", 36)
    pdf.set_text_color(*INK)
    pdf.cell(0, 16, "Water Automation")
    pdf.set_xy(18, 68)
    pdf.set_font("Helvetica", "", 36)
    pdf.cell(0, 16, "Master Plan")
    # subtitle
    pdf.set_xy(18, 92)
    pdf.set_font("Helvetica", "I", 13)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 7, "Pre-plaster conduit schedule + circuit diagrams")
    # gold rule
    pdf.set_draw_color(*GOLD_BAR)
    pdf.set_line_width(0.8)
    pdf.line(18, 110, 60, 110)

    # what's inside
    pdf.set_xy(18, 122)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 6, "WHAT'S INSIDE")
    pdf.set_xy(18, 130)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    items = [
        "1.  System overview  -  full network diagram",
        "2.  Master conduit schedule (7 conduits)",
        "3.  Per-conduit routing detail",
        "4.  Junction box specifications + interior diagrams",
        "5.  DB cupboard layout (where both starters live)",
        "6.  Starter control circuit  -  how Sonoff taps in",
        "7.  PoE power chain diagram",
        "8.  Materials checklist",
        "9.  Sequencing + acceptance checklist",
    ]
    for i, it in enumerate(items):
        pdf.set_xy(18, 138 + i * 6.5)
        pdf.cell(0, 6, it)

    # for whom
    pdf.set_xy(18, 210)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 6, "HAND THIS DOCUMENT TO")
    pdf.set_xy(18, 218)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    pdf.cell(0, 6, "Electrician (pre-plaster)  /  Plumber (pump piping)  /  Owner (reference)")

    # source file
    pdf.set_xy(18, 235)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*INK_FAINT)
    pdf.cell(0, 5, "Source: electrical/water-automation-conduits.md")
    pdf.set_xy(18, 240)
    pdf.cell(0, 5, "Project: Home Interior & Automation  -  v1.0  -  2026-05-13")

    # bottom bar
    pdf.set_fill_color(*GOLD_BAR)
    pdf.rect(0, 294.5, 210, 2.5, "F")


def page_system_overview(pdf: WaterPDF):
    pdf.set_section("01 System Overview")
    pdf.add_page()
    pdf.h1("System Overview",
           "What's connected to what  -  pumps, sensors, server, cupboard")
    pdf.lead("Two tanks (Sintex on terrace, sump outside). Two motors (P1 borewell, P2 booster). "
             "Both motor starters live inside a lockable cupboard adjacent to the foyer DB.")
    # the big diagram (no internal legend)
    y_diag = pdf.get_y() + 2
    pdf.system_overview(pdf.PAGE_MARGIN_X, y_diag, pdf.CONTENT_W, 140)
    pdf.set_y(y_diag + 142)
    # external legend strip
    lx = pdf.PAGE_MARGIN_X + 2
    ly = pdf.get_y()
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(lx, ly + 2, "LEGEND:")
    # data line
    pdf.set_draw_color(*INFO)
    pdf.set_line_width(0.7)
    pdf.line(lx + 16, ly + 1, lx + 26, ly + 1)
    pdf.set_text_color(*INFO)
    pdf.set_font("Helvetica", "", 7)
    pdf.text(lx + 27, ly + 2, "data (Cat6 / PoE)")
    # float dashed
    pdf.set_draw_color(*DANGER)
    pdf.set_line_width(0.5)
    for t in range(0, 10, 2):
        pdf.line(lx + 75 + t, ly + 1, lx + 76 + t, ly + 1)
    pdf.set_text_color(*DANGER)
    pdf.text(lx + 86, ly + 2, "float wire (220V, in series with coil)")
    # motor power
    pdf.set_draw_color(*COPPER)
    pdf.set_line_width(0.8)
    pdf.line(lx + 154, ly + 1, lx + 164, ly + 1)
    pdf.set_text_color(*COPPER)
    pdf.text(lx + 165, ly + 2, "motor power")
    pdf.set_y(ly + 6)
    pdf.callout_info("How automation flows",
                     "Sensors read levels -> JBs send digital values to server via Cat6 PoE -> "
                     "Server runs Home Assistant logic -> Sonoff in cupboard switches motor "
                     "contactor coils -> motor runs / stops. Manual override via starter buttons "
                     "(open cupboard, press green/red). Hardware failsafe via float switches "
                     "(direct break in coil supply, server-independent).")


def page_master_schedule(pdf: WaterPDF):
    pdf.set_section("02 Master Conduit Schedule")
    pdf.add_page()
    pdf.h1("Master Conduit Schedule",
           "All 7 conduits to lay before plastering")
    pdf.callout_danger("Critical timing",
                       "Horizontal terrace runs (C-Sintex-1 and C-Sintex-2) MUST be embedded under "
                       "the terrace screed BEFORE tiling / waterproofing. Cannot retrofit later "
                       "without breaking tile work.")
    headers = ["ID", "Size", "From -> To", "Carries", "Length"]
    widths = [22, 14, 64, 50, 24]
    rows = [
        ["C-Sintex-1", "20 mm",
         "Server niche  ->  Sintex JB on terrace SW parapet",
         "Cat6 PoE (data + 48V)", "~ 42 ft"],
        ["C-Sintex-2", "16 mm",
         "Sintex JB  ->  DB cupboard",
         "2-core 1.5 mm2 (Sintex float, 220V)", "~ 45 ft"],
        ["C-Sump-1", "20 mm",
         "Server niche  ->  Sump JB on east external wall",
         "Cat6 PoE (data + 48V)", "~ 25 ft"],
        ["C-Sump-2", "16 mm",
         "Sump JB  ->  DB cupboard",
         "2-core 1.5 mm2 (Sump float, 220V)", "~ 25 ft"],
        ["C-DB-Backup", "20 mm",
         "Server niche  ->  DB cupboard",
         "EMPTY  (pull string  -  future Cat6)", "~ 12 ft"],
        ["C-Motor-P1", "25 mm",
         "DB cupboard  ->  Borewell head (outside)",
         "3-core 4 mm2 armoured", "depends"],
        ["C-Motor-P2", "25 mm",
         "DB cupboard  ->  P2 cage on east outside wall",
         "3-core 2.5 mm2 PVC", "~ 5 ft"],
    ]
    pdf.table(headers, rows, widths, font=8.5)
    pdf.ln(2)
    pdf.callout("Five rules",
                "(1) Data and mains conduits NEVER share. "
                "(2) Parallel data + mains separated by  >=  50 mm. "
                "(3) Every conduit gets a pull-string left inside. "
                "(4) Horizontal terrace runs done before tiling. "
                "(5) All JBs IP65 minimum; outdoor JBs IP66.")


def page_conduit_details(pdf: WaterPDF):
    pdf.set_section("03 Per-Conduit Routing")
    pdf.add_page()
    pdf.h1("Per-Conduit Routing",
           "Detail for each of the 7 runs")
    details = [
        ("C-Sintex-1  -  Server  ->  Sintex JB",
         "Vertical through staircase shaft to terrace level; horizontal embedded in terrace "
         "screed (under tile bed) to SW corner; rise up parapet to JB at  ~ 1.2 m AGL.",
         "Outdoor-rated LSZH Cat6. Slab penetration sealed with fire mastic before waterproofing layer."),
        ("C-Sintex-2  -  Sintex JB  ->  DB cupboard",
         "Parallel to C-Sintex-1, 50 mm separated. Through screed -> staircase shaft -> "
         "horizontal in chase to DB cupboard.",
         "2-core 1.5 mm2 double-insulated 220V cable. Mains-class. Separate from Cat6."),
        ("C-Sump-1  -  Server  ->  Sump JB",
         "Horizontal in ceiling chase to east external wall; sleeved penetration (slope outward); "
         "vertical drop on outside face to JB at  ~ 1.2 m AGL above sump manhole.",
         "Outdoor-rated LSZH Cat6. Wall penetration sealed."),
        ("C-Sump-2  -  Sump JB  ->  DB cupboard",
         "Parallel to C-Sump-1 outdoors, separate sleeved penetration through east wall, "
         "indoor chase to DB cupboard.",
         "2-core 1.5 mm2 double-insulated 220V cable."),
        ("C-DB-Backup  -  Server  ->  DB cupboard",
         "Through ceiling chase to DB cupboard at standard switch height. Pull string ONLY, no cable.",
         "Future Cat6 if ESP32 motor control is wanted later. Cap both ends, label clearly."),
        ("C-Motor-P1  -  DB cupboard  ->  Borewell",
         "Exit DB cupboard at floor -> through east wall -> outdoor buried conduit to borewell head -> "
         "submersible cable continues in casing.",
         "3-core 4 mm2 XLPE armoured. Verify existing run if any. Motor earth pit dedicated."),
        ("C-Motor-P2  -  DB cupboard  ->  P2 cage",
         "Exit DB cupboard at floor -> through east wall -> short run to steel cage on east wall.",
         "3-core 2.5 mm2 PVC double-insulated. Short distance, no armouring needed above grade."),
    ]
    for title, route, note in details:
        pdf.h3(title)
        pdf.kv("Route", route)
        pdf.kv("Cable / Notes", note)
        pdf.ln(1)


def page_jbs(pdf: WaterPDF):
    pdf.set_section("04 Junction Boxes")
    pdf.add_page()
    pdf.h1("Junction Boxes",
           "Two identical JBs, one per tank")
    pdf.lead("Each JB houses an ESP32 (WT32-ETH01), a PoE splitter, terminal blocks, "
             "and acts as the cable transition point between indoor conduit and tank-side cabling.")

    # Two JB diagrams side by side
    y0 = pdf.get_y()
    box_h = 80
    half_w = (pdf.CONTENT_W - 6) / 2

    sintex_contents = [
        ("WT32-ETH01", "ESP32 + Ethernet", (INFO, INFO_PALE)),
        ("PoE splitter", "48 V  ->  5 V regulated", (GOOD, GOOD_PALE)),
        ("4-way term. block", "for sensor wires (R/B/Y/G)", (GOLD_DARK, GOLD_PALE)),
        ("2-way term. block", "for float transit", (DANGER, DANGER_PALE)),
    ]
    sintex_glands = [
        ("Cat6", INFO),
        ("Float", DANGER),
        ("Sensor", COPPER),
        ("Float-in", DANGER),
    ]
    pdf.jb_interior(pdf.PAGE_MARGIN_X, y0, half_w, box_h,
                    "SINTEX JB  -  terrace SW parapet",
                    sintex_contents, sintex_glands)

    sump_contents = [
        ("WT32-ETH01", "ESP32 + Ethernet", (INFO, INFO_PALE)),
        ("PoE splitter", "48 V  ->  5 V regulated", (GOOD, GOOD_PALE)),
        ("3-way term. block", "pressure transducer (R/B/Y)", (GOLD_DARK, GOLD_PALE)),
        ("Float terminals", "transit + telemetry tap", (DANGER, DANGER_PALE)),
    ]
    sump_glands = [
        ("Cat6", INFO),
        ("Float", DANGER),
        ("Probe", COPPER),
        ("Float-in", DANGER),
    ]
    pdf.jb_interior(pdf.PAGE_MARGIN_X + half_w + 6, y0, half_w, box_h,
                    "SUMP JB  -  east external wall",
                    sump_contents, sump_glands)

    pdf.set_y(y0 + box_h + 4)
    pdf.callout_info("Mounting notes",
                     "Sintex JB: mount on parapet, shaded side. Add fibre-cement sun shield if "
                     "direct afternoon sun. Sump JB: mount  ~ 1.2 m AGL directly above the sump "
                     "manhole on the east wall. Both: gland the bottom face only (top stays clean).")

    pdf.h2("Power chain inside each JB")
    pdf.power_chain(pdf.PAGE_MARGIN_X, pdf.get_y() + 2, pdf.CONTENT_W, 55)
    pdf.set_y(pdf.get_y() + 58)


def page_db_cupboard(pdf: WaterPDF):
    pdf.set_section("05 DB Cupboard")
    pdf.add_page()
    pdf.h1("DB Cupboard",
           "Where both motor starters live, plus Sonoff and float terminals")
    pdf.lead("Lockable wooden cupboard adjacent to the existing DB. Ventilated top + bottom "
             "(starters dissipate heat). All 7 conduits enter from below.")

    pdf.db_cupboard_interior(pdf.PAGE_MARGIN_X, pdf.get_y() + 2, pdf.CONTENT_W, 95)
    pdf.set_y(pdf.get_y() + 98)

    pdf.h3("Why starters inside the home")
    pdf.body("Moving both starters from outside (original plan) to inside (final plan) means: "
             "(a) manual operation does not need going outside; (b) HOA switches no longer needed "
             "(starter green/red buttons serve as manual override); (c) float wiring terminates "
             "in one place where both starters can be jumpered in series.")


def page_starter_wiring(pdf: WaterPDF):
    pdf.set_section("06 Starter Control Circuit")
    pdf.add_page()
    pdf.h1("Starter Control Circuit",
           "How the Sonoff taps in without breaking manual operation")
    pdf.lead("Identical pattern for both P1 and P2. The Sonoff channel is paralleled across the "
             "Green button + Aux latching contact. Manual buttons keep working; Sonoff can "
             "start/stop independently.")

    pdf.starter_wiring(pdf.PAGE_MARGIN_X, pdf.get_y() + 2, pdf.CONTENT_W, 75)
    pdf.set_y(pdf.get_y() + 78)

    pdf.callout_good("Why this design",
                     "(1) Manual override preserved (green/red buttons work normally). "
                     "(2) Thermal overload preserved (we don't bypass it). "
                     "(3) Hardware failsafe preserved (Sintex high float in series with coil). "
                     "(4) Server can start/stop via Sonoff channel. "
                     "(5) Sonoff failure: motor stops, manual still works. Failsafe.")

    pdf.callout_danger("Wiring rule",
                       "The Sonoff's switched output goes in PARALLEL with the green button. "
                       "Never break the existing manual circuit; only add a parallel path. "
                       "Test manual operation BEFORE energising the Sonoff for the first time.")


def page_materials(pdf: WaterPDF):
    pdf.set_section("07 Materials Checklist")
    pdf.add_page()
    pdf.h1("Materials Checklist",
           "Buy in advance so plaster doesn't wait on parts")

    pdf.h3("Conduits + accessories")
    pdf.table(
        ["Item", "Qty", "Notes"],
        [
            ["20 mm grey PVC conduit", "~ 80 m",
             "C-Sintex-1 (13 m) + C-Sump-1 (8 m) + C-DB-Backup (4 m) + spare"],
            ["16 mm PVC conduit", "~ 50 m",
             "C-Sintex-2 (14 m) + C-Sump-2 (8 m) + spare"],
            ["25 mm blue PVC conduit", "~ 30 m",
             "C-Motor-P1 + C-Motor-P2 + spare"],
            ["Conduit bends, couplings, junctions", "as needed", "Same brand as conduit"],
            ["Pull string (nylon twine)", "200 m", "Leave in every conduit"],
            ["Slab + wall penetration sleeves", "4", "+ fire-mastic for sealing"],
        ],
        col_widths=[58, 22, 94], font=8.5)

    pdf.h3("Cables")
    pdf.table(
        ["Cable", "Qty", "Notes"],
        [
            ["Outdoor LSZH Cat6 UTP", "~ 50 m", "UV-resistant outer jacket"],
            ["2-core 1.5 mm2 220V flexible", "~ 45 m", "Double-insulated"],
            ["3-core 4 mm2 XLPE armoured", "?", "C-Motor-P1; verify existing first"],
            ["3-core 2.5 mm2 PVC", "~ 5 m", "C-Motor-P2 + spare"],
        ],
        col_widths=[58, 22, 94], font=8.5)

    pdf.h3("Junction boxes + glands")
    pdf.table(
        ["Item", "Qty"],
        [
            ["200 x 200 x 100 IP65 / IP66 enclosure", "2"],
            ["20 mm cable gland (for Cat6 entry)", "2"],
            ["16 mm cable gland (for float transit)", "2"],
            ["12 mm cable gland (sensor + float tank exits)", "4"],
            ["Fibre cement sun shield (if Sintex JB direct sun)", "1"],
        ],
        col_widths=[140, 34], font=8.5)

    pdf.h3("DB cupboard contents")
    pdf.table(
        ["Item", "Qty", "Notes"],
        [
            ["Magnum Pradhaan PSP1 starter (1HP single-phase)", "1", "New for P2;  ~ Rs 3000"],
            ["Sonoff DUALR3 (Wi-Fi smart switch, 2 ch)", "1", " ~ Rs 1500; flash with Tasmota"],
            ["4-way 220V terminal block", "1", "For float wire junction"],
            ["DIN rail (if cupboard is large enough)", "1", "Optional, for cleaner mounting"],
            ["Earthing busbar", "1", "All motor earths terminate here"],
        ],
        col_widths=[80, 18, 76], font=8.5)


def page_sequencing(pdf: WaterPDF):
    pdf.set_section("08 Sequencing")
    pdf.add_page()
    pdf.h1("Sequencing",
           "Order of operations  -  who does what, when")
    pdf.table(
        ["Step", "Task", "Depends on"],
        [
            ["1", "Mark conduit routes on walls (chalk / paint)", "  -  "],
            ["2", "Chase wall channels for conduit", "Step 1"],
            ["3", "Lay all 7 conduits + pull strings", "Step 2"],
            ["4", "Drill terrace slab + east wall penetrations; install sleeves", "Step 3"],
            ["5", "Mount JB backplates (Sintex, Sump)", "Step 4"],
            ["6", "Plastering team takes over", "1-5 complete"],
            ["7", "Terrace tiling / waterproofing (with C-Sintex-1/2 already embedded)", "4 + 6"],
            ["8", "Paint completion", "Step 7"],
            ["9", "Install JBs on backplates, connect glands", "Step 8"],
            ["10", "Pull Cat6 + float cables through conduits", "Step 9"],
            ["11", "Mount DB cupboard + install starters + Sonoff", "Step 9"],
            ["12", "Install sensors (ultrasonic in Sintex riser, probe in sump) + floats", "Step 10"],
            ["13", "Wire and test", "Step 12"],
        ],
        col_widths=[14, 122, 38], font=8.5)


def page_acceptance(pdf: WaterPDF):
    pdf.set_section("09 Acceptance Checklist")
    pdf.add_page()
    pdf.h1("Electrician Acceptance Checklist",
           "Sign-off BEFORE plastering proceeds")
    pdf.lead("Walk the site with the electrician. Tick each box only after physical verification. "
             "Sign at the bottom.")

    items = [
        "All 7 conduits routed per the master table",
        "All conduits have pull strings left inside",
        "Data conduits (20 mm) and mains conduits (16/25 mm) separated by  >=  50 mm in parallel runs",
        "No data and mains cables sharing the same conduit anywhere",
        "Slab + external wall penetrations sleeved and marked",
        "JB mounting points identified and backplates fixed (Sintex parapet + east wall)",
        "DB cupboard cable entry positions match the 7 conduit endpoints",
        "Conduit ends sealed with caps to prevent debris during plastering",
        "Both ends of each conduit labelled with conduit ID (C-Sintex-1, C-Sump-2, etc.)",
        "Conduit colour code matches scheme: grey = data, blue = motor power, white = float",
        "Photos taken of each conduit run before plastering (for future reference)",
        "Owner has reviewed the routes on-site and approved",
    ]
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    for it in items:
        # tick box + text
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_draw_color(*INK)
        pdf.set_line_width(0.4)
        pdf.rect(x, y + 1.2, 3.8, 3.8, "D")
        pdf.set_xy(x + 6, y)
        pdf.multi_cell(pdf.CONTENT_W - 6, 5.4, it)
        pdf.ln(0.5)

    pdf.ln(8)
    # sign-off lines
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 6, "SIGN-OFF", ln=1)
    pdf.ln(2)
    for who, role in [("Electrician", "Name + signature + date"),
                      ("Owner",        "Name + signature + date"),
                      ("Mason (plastering)", "Acknowledges conduits in place")]:
        y0 = pdf.get_y()
        pdf.set_draw_color(*INK_SOFT)
        pdf.set_line_width(0.3)
        pdf.line(pdf.PAGE_MARGIN_X, y0 + 8, pdf.PAGE_MARGIN_X + 100, y0 + 8)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*INK)
        pdf.set_xy(pdf.PAGE_MARGIN_X, y0 + 9)
        pdf.cell(0, 4, who)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*INK_FAINT)
        pdf.set_xy(pdf.PAGE_MARGIN_X, y0 + 13)
        pdf.cell(0, 4, role)
        pdf.ln(18)


# ===================================================================
#                              BUILD
# ===================================================================

def build():
    pdf = WaterPDF()
    page_cover(pdf)
    page_system_overview(pdf)
    page_master_schedule(pdf)
    page_conduit_details(pdf)
    page_jbs(pdf)
    page_db_cupboard(pdf)
    page_starter_wiring(pdf)
    page_materials(pdf)
    page_sequencing(pdf)
    page_acceptance(pdf)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
