"""
Build the Electrician Reference PDF.
Drilling, cavity depths, switch box specs, conduit routes, FF router runs.
Format: A4 portrait, large readable type, plain language for site use.
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "ELECTRICIAN_REFERENCE.pdf"

# ---------- PDF helpers ----------
class ElectricianPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(14, 14, 14)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, "Ganesh Prasad - Home Electrical Reference (Chitradurga)", ln=0, align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", ln=1)
        self.set_draw_color(180, 180, 180)
        self.line(14, 23, 196, 23)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, "v1.0 - 2026-05-06 - Hand to electrician + mason BEFORE chasing", align="C")

    # high-level building blocks
    def h1(self, text):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 20, 20)
        self.set_fill_color(245, 240, 220)
        self.cell(0, 12, text, ln=1, fill=True)
        self.ln(2)

    def h2(self, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 8, text, ln=1)
        self.set_draw_color(180, 140, 70)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(3)

    def h3(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 6, text, ln=1)
        self.ln(1)

    def body(self, text, size=10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def callout(self, label, text):
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(255, 245, 215)
        self.set_text_color(140, 90, 30)
        self.cell(0, 6, f"  >> {label}", ln=1, fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.set_fill_color(255, 250, 235)
        self.multi_cell(0, 5, "    " + text, fill=True)
        self.ln(2)

    def warning(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(255, 220, 220)
        self.set_text_color(150, 30, 30)
        self.cell(0, 6, "  CRITICAL", ln=1, fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(80, 30, 30)
        self.set_fill_color(255, 235, 235)
        self.multi_cell(0, 5, "    " + text, fill=True)
        self.ln(2)
        self.set_text_color(40, 40, 40)

    def kv(self, key, value):
        # key-value row
        x0 = self.l_margin
        self.set_x(x0)
        self.set_font("Helvetica", "B", 9.5)
        self.cell(60, 6, key, ln=0)
        self.set_font("Helvetica", "", 9.5)
        avail = self.w - x0 - 60 - self.r_margin
        if avail < 20:
            avail = 100
        self.multi_cell(avail, 6, value)

    def _safe_break(self, text, max_w):
        """Insert soft breaks into very long words that overflow a column."""
        if not text:
            return text
        words = text.split(" ")
        out_words = []
        for w in words:
            if self.get_string_width(w) <= max_w - 2:
                out_words.append(w)
            else:
                # split the long word into chunks
                chunk = ""
                for ch in w:
                    if self.get_string_width(chunk + ch) > max_w - 2:
                        out_words.append(chunk)
                        chunk = ch
                    else:
                        chunk += ch
                if chunk:
                    out_words.append(chunk)
        return " ".join(out_words)

    def table(self, headers, rows, col_widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(70, 50, 30)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_widths):
            self.cell(w, 7, self._safe_break(h, w), border=1, align="C", fill=True)
        self.ln(7)
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 9)
        # pre-process rows
        rows = [
            [self._safe_break(str(c), col_widths[i]) for i, c in enumerate(row)]
            for row in rows
        ]
        fill = False
        line_h = 4.5
        for row in rows:
            # estimate number of wrapped lines per cell
            lines_needed = []
            for cell, w in zip(row, col_widths):
                if not cell:
                    lines_needed.append(1)
                    continue
                # break by explicit newlines first
                segments = str(cell).split("\n")
                tot = 0
                for seg in segments:
                    sw = self.get_string_width(seg) if seg else 0
                    avail = max(w - 2, 5)
                    tot += max(1, -(-int(sw // avail) - 1))  # ceil-ish
                lines_needed.append(max(1, tot))
            row_lines = max(lines_needed)
            row_h = max(row_lines * line_h, 6)
            # page break check
            if self.get_y() + row_h > self.h - 22:
                self.add_page()
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(70, 50, 30)
                self.set_text_color(255, 255, 255)
                for h, w in zip(headers, col_widths):
                    self.cell(w, 7, h, border=1, align="C", fill=True)
                self.ln(7)
                self.set_text_color(40, 40, 40)
                self.set_font("Helvetica", "", 9)
            self.set_fill_color(248, 245, 235) if fill else self.set_fill_color(255, 255, 255)
            x_start, y_start = self.get_x(), self.get_y()
            # fill the row first
            for cell, w in zip(row, col_widths):
                self.rect(self.get_x(), self.get_y(), w, row_h, "DF")
                self.set_x(self.get_x() + w)
            # now write text in each cell
            self.set_xy(x_start, y_start)
            for cell, w in zip(row, col_widths):
                cur_x, cur_y = self.get_x(), self.get_y()
                # vertical centring offset
                content_h = max(1, lines_needed[row.index(cell)]) * line_h
                offset_y = max(0, (row_h - content_h) / 2)
                self.set_xy(cur_x + 1, cur_y + offset_y)
                self.multi_cell(w - 2, line_h, str(cell), border=0, align="L", fill=False)
                self.set_xy(cur_x + w, cur_y)
            self.set_xy(x_start, y_start + row_h)
            fill = not fill
        self.ln(2)


# ---------- BUILD PDF ----------
pdf = ElectricianPDF()

# COVER PAGE
pdf.add_page()
pdf.set_y(40)
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(60, 40, 20)
pdf.cell(0, 14, "ELECTRICIAN", ln=1, align="C")
pdf.cell(0, 14, "REFERENCE", ln=1, align="C")
pdf.ln(8)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(80, 60, 30)
pdf.cell(0, 8, "Drilling | Cavity Depths | Conduits | Switch Boards", ln=1, align="C")
pdf.ln(20)

# project box
pdf.set_fill_color(250, 240, 220)
pdf.set_draw_color(180, 140, 70)
pdf.rect(30, pdf.get_y(), 150, 70, "DF")
pdf.set_xy(35, pdf.get_y() + 4)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(80, 50, 20)
pdf.cell(0, 8, "PROJECT", ln=1)
pdf.set_x(35)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(40, 40, 40)
pdf.cell(0, 6, "Owner       : Ganesh Prasad D", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Location    : Chitradurga, Karnataka", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "House type  : 2-floor residential, North-facing main entrance", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "GF ceiling  : 11 ft           FF ceiling : 10 ft", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "DB location : West wall, foyer, behind door swing", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "DB size     : 48-way Schneider Acti9 IEF48", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Document    : v1.0  -  2026-05-06", ln=1)

pdf.set_y(180)
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(255, 230, 200)
pdf.cell(0, 8, "  READ THIS FIRST", ln=1, fill=True)
pdf.set_font("Helvetica", "", 10)
pdf.ln(2)
pdf.set_x(14)
pdf.multi_cell(0, 5,
    "1. THIS DOCUMENT REPLACES SITE INSTRUCTIONS. If anything on site differs from this PDF, "
    "STOP and call before chasing or drilling.\n\n"
    "2. EVERY SMART-SWITCH BOARD GETS A 65 mm DEEP BOX (not 50 mm). The Sonoff/Aqara relay "
    "module sits behind the switch plate; 50 mm is too shallow.\n\n"
    "3. EVERY SWITCH BOARD GETS A NEUTRAL WIRE (black). No exceptions, even on dumb switch zones, "
    "because we may convert them to smart later.\n\n"
    "4. EARTH WIRE (green/yellow) reaches every switch, socket, and metal fitting. Test continuity "
    "before plastering.\n\n"
    "5. Power conduits and Cat6 conduits are NEVER in the same pipe. Always separate.")

# PAGE 2 - The 5 Universal Rules + Wire Colour Code
pdf.add_page()
pdf.h1("1. The 5 Rules That Apply Everywhere")

rules = [
    ("Rule 1 - NEUTRAL EVERYWHERE",
     "Every switch board (smart or dumb) receives a NEUTRAL wire (black). "
     "Smart relay modules need it. Without neutral, the smart switch goes dead. "
     "Cap unused neutrals at the box; do not omit them."),
    ("Rule 2 - 65 mm DEEP BOXES AT SMART SWITCHES",
     "All smart-switch locations get a 65 mm-deep GI MS box, NOT the standard 50 mm. "
     "Sizes: 1-mod 75x75x65, 2-mod 130x75x65, 3-mod 175x75x65, 4-mod 230x75x65. "
     "Sonoff ZBMINI R2 / Aqara T1 relay sits behind the switch plate; 50 mm cannot fit "
     "module + bent wires + terminals."),
    ("Rule 3 - STANDARD HEIGHTS (FFL = Finished Floor Level)",
     "Switch boards: 1200 mm (centre of plate)\n"
     "Geyser switches: 1050 mm\n"
     "PIR bathroom switches: 1200 mm (outside door, handle side)\n"
     "Sockets (general): 300 mm\n"
     "Bedside sockets: 600 mm\n"
     "Counter sockets (kitchen): 1100 mm\n"
     "AC sockets: 1850 mm\n"
     "Geyser outlet (in attic): 1850 mm\n"
     "Wi-Fi router/AP wall plate (FF Living): 2400 mm"),
    ("Rule 4 - EARTH IS NOT OPTIONAL",
     "Green/yellow earth wire reaches every switch, every socket, every metal fitting. "
     "Test earth continuity at every metallic body with clamp meter (< 1 ohm) before plastering."),
    ("Rule 5 - POWER AND DATA NEVER IN THE SAME PIPE",
     "Cat6 picks up interference from 230V lines. ALWAYS use separate conduits: 25mm grey "
     "(LV-25) for Cat6 / network / camera data; 25mm red/blue for power."),
]
for label, txt in rules:
    pdf.callout(label, txt)

pdf.h2("Wire Colour Code (Indian Standard - Mandatory)")
pdf.table(
    headers=["Colour", "Function", "Where used"],
    rows=[
        ["RED", "LIVE (phase) - 230V hot", "Every live wire from MCB outward"],
        ["BLACK", "NEUTRAL - return", "Every switch board, every socket"],
        ["GREEN/YELLOW", "EARTH", "Every switch, socket, metal fitting"],
        ["BLUE", "Switched LIVE leg", "Between switch and the load (light)"],
    ],
    col_widths=[40, 55, 87],
)
pdf.warning("A black wire with current is ALWAYS NEUTRAL. A blue wire is the SWITCHED LIVE leg. Do not confuse them.")

# PAGE 3 - Conduit Colour Code
pdf.add_page()
pdf.h1("2. Conduit Colour Code")

pdf.body(
    "Use coloured PVC conduit where available. If only grey is available locally, "
    "wrap each conduit end in coloured insulation tape and label with permanent marker BEFORE "
    "plastering. Once plastering is done, the conduit is invisible - this is your only chance "
    "to mark it."
)

pdf.table(
    headers=["Colour", "Size", "Carries", "Wire inside"],
    rows=[
        ["RED", "25 mm", "Lighting power", "1.5 sqmm 3-core"],
        ["BLUE", "25 mm", "Sockets / AC / Geyser / Hob power", "2.5 or 4 sqmm 3-core"],
        ["GREY", "25 mm (LV-25)", "Cat6 / network / camera data", "1 or 2 Cat6 UTP"],
        ["GREY", "16 mm (LV-16)", "Speaker, sensor, doorbell, contact, LED 24V", "2-core 0.75 sqmm"],
    ],
    col_widths=[28, 32, 80, 42],
)

pdf.h2("Conduit Routes - Cheat Sheet")
pdf.table(
    headers=["Need", "Conduit", "Wire", "Box depth", "MCB"],
    rows=[
        ["Smart light point", "25mm RED", "1.5 sqmm", "60mm circular", "6A"],
        ["Smart switch (Sonoff)", "25mm RED", "1.5 sqmm + neutral", "65 mm", "6A"],
        ["Dumb light point", "25mm RED", "1.5 sqmm", "50 mm", "6A"],
        ["5A socket", "25mm BLUE", "2.5 sqmm", "50 mm", "16A"],
        ["16A socket", "25mm BLUE", "2.5 sqmm", "50 mm", "16A"],
        ["AC point (20A)", "25mm BLUE", "4 sqmm", "50 mm", "20A RCBO"],
        ["Geyser (20A)", "25mm BLUE", "2.5 sqmm", "50 mm", "20A RCBO"],
        ["Hob 25A", "25mm BLUE", "4 sqmm", "hardwire", "25A"],
        ["Cat6 / network", "25mm GREY", "Cat6 UTP", "50 mm plate", "-"],
        ["Camera (PoE)", "25mm GREY", "Cat6 UTP", "IP67 box", "-"],
        ["Speaker / LV", "16mm GREY", "2-core 0.75", "50 mm", "-"],
        ["LED strip 24V DC", "16mm GREY", "2-core 0.75", "driver only", "-"],
    ],
    col_widths=[42, 32, 38, 38, 32],
)

# PAGE 4 - Switch Box Cavity Depth
pdf.add_page()
pdf.h1("3. Switch-Box Cavity Depth (NEW - critical)")

pdf.warning(
    "OLD HABIT: 50 mm GI box at every switch.\n"
    "NEW REQUIREMENT: 65 mm deep GI box at every SMART-switch location.\n\n"
    "If you fit 50 mm boxes at smart-switch locations, the Sonoff / Aqara relay module "
    "WILL NOT FIT. The whole installation will need to be redone after plaster - this means "
    "breaking the wall, re-chasing, re-plastering, re-painting. DO NOT make this mistake."
)

pdf.body(
    "The wall plate (front cover) is the same modular size whether the box is 50 mm or 65 mm. "
    "Only the WALL HOLE is deeper for the 65 mm version. Buy 65 mm deep GI MS boxes from your "
    "hardware shop and physically check the depth before sending to site."
)

pdf.h2("Where 65 mm Deep Boxes Go")
pdf.body(
    "Anywhere the switch is marked 'Smart' on the room point schedule. Specifically:"
)
pdf.table(
    headers=["Floor", "Location", "Gangs", "Box size (mm)"],
    rows=[
        ["GF", "Foyer (W wall, near door)", "4", "230 x 75 x 65"],
        ["GF", "Foyer 2-way at staircase entry", "2", "130 x 75 x 65"],
        ["GF", "Living Area (W wall)", "4", "230 x 75 x 65"],
        ["GF", "Living Area 2-way (stair side)", "2", "130 x 75 x 65"],
        ["GF", "Dining", "2", "130 x 75 x 65"],
        ["GF", "Master Bedroom (door)", "4", "230 x 75 x 65"],
        ["GF", "Pooja (outside entry)", "2", "130 x 75 x 65"],
        ["GF", "Staircase base", "1", "75 x 75 x 65"],
        ["FF", "FF Living corridor", "2", "130 x 75 x 65"],
        ["FF", "FF Staircase top (2-way)", "1", "75 x 75 x 65"],
        ["FF", "Bedroom 1 (inside door)", "4", "230 x 75 x 65"],
        ["FF", "Bedroom 2 (inside door)", "4", "230 x 75 x 65"],
        ["FF", "Front balcony (inside)", "1", "75 x 75 x 65"],
    ],
    col_widths=[18, 95, 22, 47],
)

pdf.h2("Where 50 mm STANDARD Boxes Are OK")
pdf.body(
    "All sockets (5A, 16A, AC), geyser switches, PIR bathroom switches, kitchen / utility / "
    "store room switches (these are dumb - no relay), and Cat6/data wall plates."
)

# PAGE 5 - Universal smart switch wiring
pdf.add_page()
pdf.h1("4. Universal Smart-Switch Wiring (apply at every smart point)")

pdf.body(
    "At every smart-switch location, leave a 300 mm tail of L (red) / N (black) / E (green-yellow) "
    "wires inside the box. Cap them with insulated wire connectors. The Sonoff or Aqara module is "
    "inserted by the homeowner LATER - you do NOT install the module. You only need to:\n\n"
    "    1. Use the 65 mm-deep box.\n"
    "    2. Pull L + N + E into the box (3 wires).\n"
    "    3. Pull a switched-live (blue) leg out of the box, up the conduit, to the load.\n"
    "    4. Leave 300 mm tails on all wires.\n"
    "    5. Cap and label."
)

pdf.h2("Schematic")
pdf.set_font("Courier", "", 9)
pdf.multi_cell(0, 4.5,
    "                BOX  (75 x 75 x 65 mm GI MS)\n"
    "               +------------------------+\n"
    "FROM CEILING --|  L   N   E             |  <- 3 wires arrive\n"
    "(power feed)   |   .                    |\n"
    "               |  +-----------------+   |\n"
    "               |  |   SONOFF R2     |   |  <- module added LATER\n"
    "               |  |   Zigbee Relay  |   |     L IN  : Live\n"
    "               |  |                 |   |     N IN  : Neutral\n"
    "               |  +--+----------+---+   |     L OUT : to switch\n"
    "               |     |          |       |     S1/S2 : physical rocker\n"
    "               |  +--+--+       |       |\n"
    "               |  |SWITCH|      |       |\n"
    "               |  |rocker|      |       |\n"
    "               |  +------+    --+--     |\n"
    "               |              LOAD  ->  |  <- blue 'switched live' to light\n"
    "               +------------------------+\n"
    "                       |\n"
    "                  FRONT PLATE\n"
    "                  (modular cover)")
pdf.set_font("Helvetica", "", 10)

# PAGE 6 - GF Switch Boards
pdf.add_page()
pdf.h1("5. GF Switch-Board Schedule")

pdf.table(
    headers=["Location", "Gangs", "Box depth", "Smart gangs", "Notes"],
    rows=[
        ["Foyer (W wall, near door)", "4", "65 mm", "2 smart + 2 dumb", "Lights, screen, 2 spare"],
        ["Living (W wall)", "4", "65 mm", "3 smart", "Main, cove, TV wash, master off"],
        ["Living 2-way (stair side)", "2", "65 mm", "2 smart", "Pairs with W wall"],
        ["Dining", "2", "65 mm", "1 smart", "Pendant + cove"],
        ["Kitchen (entry)", "4", "50 mm", "0", "Lights + exhaust (DUMB)"],
        ["Utility", "1", "50 mm", "0", "Light only (DUMB)"],
        ["Store room", "1", "50 mm", "0", "Single LED (DUMB)"],
        ["MBR door", "4", "65 mm", "3 smart", "Main, reading L+R, master off"],
        ["GF Bath (outside door)", "2", "50 mm", "PIR auto", "PIR module + 20A geyser switch"],
        ["Staircase base", "1", "65 mm", "Smart 2-way", "Pairs with FF landing"],
        ["Pooja (outside entry)", "2", "65 mm", "2 smart", "Ceiling + niche backlight"],
    ],
    col_widths=[55, 18, 22, 30, 57],
)

pdf.callout("DB panel position",
    "DB recess: 400W x 600H x 100D mm at 1500 mm FFL on West wall, foyer (behind door swing). "
    "48-way Schneider Acti9 IEF48. Pull mains supply from meter, 25 mm conduit, into top of DB.")

# PAGE 7 - FF Switch Boards
pdf.add_page()
pdf.h1("6. FF Switch-Board Schedule")

pdf.table(
    headers=["Location", "Gangs", "Box depth", "Smart gangs", "Notes"],
    rows=[
        ["FF corridor", "2", "65 mm", "2 smart", "FF Living lights"],
        ["FF Staircase top (2-way)", "1", "65 mm", "Smart 2-way", "Pairs with GF base"],
        ["Bedroom 1 (inside door)", "4", "65 mm", "3 smart", "Main, reading L+R, master off"],
        ["BR1 geyser switch (outside T1)", "1", "50 mm", "0", "20A DP with neon, 1050 mm"],
        ["Bedroom 2 (inside door)", "4", "65 mm", "3 smart", "Main, reading L+R, master off"],
        ["BR2 geyser switch (outside T2)", "1", "50 mm", "0", "20A DP with neon, 1050 mm"],
        ["Front balcony (inside)", "1", "65 mm", "Smart", "Sunset schedule"],
    ],
    col_widths=[55, 18, 22, 30, 57],
)

pdf.h2("NEW Wall Plates on FF (Network)")
pdf.table(
    headers=["Location", "Type", "Height", "Notes"],
    rows=[
        ["FF Living central wall", "2x Cat6 keystone wall plate (50 mm box)", "2400 mm", "Run R-FF-1 (router/AP)"],
        ["FF Living beside Cat6", "1-gang 5A power socket (50 mm)", "2400 mm", "Power for AP / PoE injector"],
        ["BR1 study wall", "1x Cat6 keystone (50 mm)", "700 mm", "Run R-FF-3"],
        ["BR2 study wall", "1x Cat6 keystone (50 mm)", "700 mm", "Run R-FF-2"],
        ["FF Front balcony soffit", "Cat6 IP67 keystone", "soffit", "Run R-FF-4 - cap until used"],
    ],
    col_widths=[50, 60, 25, 47],
)

# PAGE 8 - Drilling/cavity reference
pdf.add_page()
pdf.h1("7. Drilling & Cavity Master Reference")

pdf.h2("Foyer Screen Cavity (most critical - do FIRST)")
pdf.kv("Cavity W x H x D", "540 x 340 x 100 mm")
pdf.kv("Bottom of cavity (FFL)", "1280 mm")
pdf.kv("Centre of cavity (FFL)", "1450 mm (eye level)")
pdf.kv("Top of cavity (FFL)", "1620 mm")
pdf.kv("Horizontal", "Centred on the 1828 mm (6 ft) wall")
pdf.kv("Conduit entries", "2 stubs, bottom-LEFT corner of cavity back wall")
pdf.kv("Conduit 1 (P-25 RED)", "Power - DB to cavity")
pdf.kv("Conduit 2 (LV-25 GREY)", "Cat6 - staircase niche to cavity")
pdf.kv("LV-16 sleeve", "Screen-bezel camera at 1600-1650 mm FFL (top centre)")
pdf.kv("Inside finish", "MATTE BLACK paint inside cavity before stone cladding")
pdf.kv("VESA backing", "12 mm ply, 600 x 400 mm, fixed to cavity back, rawl-plugged")
pdf.ln(2)

pdf.h2("DB Recess")
pdf.kv("Cavity W x H x D", "400 x 600 x 100 mm")
pdf.kv("Bottom of DB (FFL)", "1500 mm")
pdf.kv("Wall", "West wall, foyer, behind door swing")
pdf.kv("Min clearance from door frame", "100 mm")
pdf.ln(2)

pdf.h2("Ceiling Light Holes (use core drill)")
pdf.table(
    headers=["Light type", "Core hole", "Location", "Depth"],
    rows=[
        ["Recessed COB 12W", "85 mm core", "All bedrooms + living + dining centre", "60 mm"],
        ["Recessed COB 9W", "75 mm core", "Dining downlights, bath ceiling", "60 mm"],
        ["Recessed GU10 (gimbal)", "75 mm core", "Foyer spots + bedside reading", "65 mm"],
        ["LED panel 24W kitchen", "330 x 330 mm cut", "Ceiling centre kitchen", "Surface mount"],
        ["IP65 7W bath downlight", "75 mm core", "Bathroom shower zone", "60 mm"],
        ["IP65 exhaust fan", "165 mm core", "Bathroom shower zone corner", "thru slab"],
    ],
    col_widths=[55, 35, 75, 17],
)

pdf.h2("Niche Cavities (build before plaster/tile)")
pdf.kv("GF Bath upper niche", "600 W x 200 H x 120 D mm (south wall, x=7.25 ft, z=1.4 m)")
pdf.kv("GF Bath lower niche", "400 W x 120 H x 100 D mm (200 mm below upper)")
pdf.kv("FF T1 niche", "600 W x 300 H x 100 D mm (shower south wall)")
pdf.kv("FF T2 niche", "Same spec")
pdf.kv("Pooja idol niche", "TBD - confirm with carpenter; typical 600 W x 900 H x 200 D mm")

# PAGE 9 - FF router and Cat6 runs
pdf.add_page()
pdf.h1("8. FF Wi-Fi Router / AP Conduits (NEW)")

pdf.body(
    "These are NEW conduit runs. They were not in the earlier plan. They go from the staircase "
    "niche (GF) up the staircase wall, then branch on FF. They MUST be chased before plastering "
    "closes the FF walls."
)

pdf.h2("Run R-FF-1 - Primary FF Router/AP")
pdf.kv("Conduit", "25 mm LV-25 (grey)")
pdf.kv("Cables", "2 x Cat6 UTP + draw wire")
pdf.kv("Route", "Staircase niche -> vertical up staircase W wall -> FF slab level -> branch east along FF Living ceiling/wall -> terminate on FF Living CENTRAL wall, between BR1 and BR2 doors")
pdf.kv("Termination height", "2400 mm FFL (high mount, best signal)")
pdf.kv("Termination box", "50 mm wall plate, 2 x Cat6 keystone")
pdf.kv("Power", "5A socket on D9 circuit, 300 mm to side, same height (2400 mm FFL)")
pdf.ln(2)

pdf.h2("Run R-FF-2 - BR2 study Cat6 drop")
pdf.kv("Conduit", "25 mm LV-25 (grey)")
pdf.kv("Cables", "1 x Cat6 UTP + draw wire")
pdf.kv("Route", "Staircase niche -> vertical -> branch west into BR2 wall -> N wall study area")
pdf.kv("Termination height", "700 mm FFL (study desk level)")
pdf.ln(2)

pdf.h2("Run R-FF-3 - BR1 study Cat6 drop")
pdf.kv("Conduit", "25 mm LV-25 (grey)")
pdf.kv("Cables", "1 x Cat6 UTP + draw wire")
pdf.kv("Route", "Staircase niche -> vertical -> branch east into BR1 wall -> study area")
pdf.kv("Termination height", "700 mm FFL")
pdf.ln(2)

pdf.h2("Run R-FF-4 (optional) - Front Balcony AP future")
pdf.kv("Conduit", "16 mm LV-16 (grey)")
pdf.kv("Cables", "1 x Cat6 outdoor UV + draw wire (cap until needed)")
pdf.kv("Route", "FF Living AP wall plate -> through partition -> front balcony soffit")
pdf.kv("Termination", "Outdoor IP67 keystone box (cap unused)")
pdf.ln(2)

pdf.warning(
    "STAIRCASE WALL CHASE - cut 150 mm WIDE x 60 mm DEEP chase to fit:\n"
    "    5 x 25 mm power conduits (D circuits + ACs)\n"
    "    3 x 25 mm LV-25 grey (R-FF-1, R-FF-2, R-FF-3)\n"
    "    1 x 16 mm LV-16 grey (existing CAM/sensor runs)\n"
    "Total: 9 conduits vertical. Cut chase WIDE on first attempt - cutting twice = double labour."
)

# PAGE 10 - Pre-plaster checklist
pdf.add_page()
pdf.h1("9. Pre-Plaster Sign-Off Checklist")

pdf.body(
    "Walk through this checklist with the homeowner BEFORE the mason starts plastering. "
    "Once plaster goes on, opening it again is expensive and messy."
)

checklist = [
    "Foyer screen cavity: 540W x 340H x 100D mm at 1280 mm FFL bottom, centred on wall",
    "DB recess: 400W x 600H x 100D mm at 1500 mm FFL on West wall, foyer",
    "All smart-switch boxes ARE 65 mm deep (not 50) - physically checked at: Foyer (4-mod 230x75x65), Living main (4-mod), Living 2-way (2-mod), Dining (2-mod), MBR (4-mod), Pooja (2-mod), Staircase base (1-mod), FF Living (2-mod), FF Stair top (1-mod), BR1 (4-mod), BR2 (4-mod), Front balcony (1-mod)",
    "All dumb switch / socket / geyser switch boxes are 50 mm GI MS",
    "NEUTRAL wire (black) visible in tail bundle at every smart-switch box",
    "EARTH wire (green/yellow) visible at every switch and every socket",
    "All cable tails labelled with masking tape + permanent marker (circuit ID)",
    "Foyer screen cavity: 2 conduit stubs in bottom-LEFT corner (P-25 power + LV-25 Cat6)",
    "Foyer screen cavity: LV-16 sleeve to top-centre at 1600-1650 mm FFL (camera)",
    "Inside foyer screen cavity: matte black paint applied",
    "Cavity VESA backing: 12 mm ply 600 x 400 mm fixed",
    "CAM-1 stub (face camera, outside main door, latch side, 1650 mm FFL)",
    "CAM-2 stub (porch overview, 2400-2700 mm FFL)",
    "CAM-3 stub (FF front balcony NW corner soffit)",
    "CAM-4 stub (E-wall exterior at kitchen/utility, 2400-2600 mm FFL)",
    "CAM-5 stub (terrace staircase parapet, ~2500 mm from terrace floor)",
    "Doorbell stub (1400-1450 mm FFL, latch side)",
    "Door contact sensor (top of door frame, concealed)",
    "Staircase niche: 12-port Cat6 keystone patch panel space at 700 mm FFL (side wall)",
    "Staircase niche: UPS socket 16A at 300 mm FFL, server sockets 4 x 5A at 400 mm FFL",
    "RUN R-FF-1: LV-25 stub at FF Living central wall, 2400 mm FFL, 2x Cat6 + draw wire",
    "RUN R-FF-1 power: 5A socket at FF Living wall, 2400 mm FFL, 300 mm to side of Cat6 plate",
    "RUN R-FF-2: LV-25 stub at BR2 study wall, 700 mm FFL, 1x Cat6 + draw wire",
    "RUN R-FF-3: LV-25 stub at BR1 study wall, 700 mm FFL, 1x Cat6 + draw wire",
    "RUN R-FF-4 (optional): 16mm LV stub at front balcony soffit",
    "All AC points (E1-E6): 20A socket at 1850 mm FFL on each AC wall",
    "All geyser conduits: 25 mm BLUE, 2.5 sqmm wire, terminating at geyser height in attic",
    "Earth bus continuity tested at every metallic body (clamp meter < 1 ohm)",
    "RCD trip test: simulate 30 mA leakage on each RCBO - must trip in < 30 ms",
    "PIR switch test (3 bathrooms): walk in, light ON; walk out, wait 10 min, light OFF",
    "Geyser switch + neon (3 bathrooms): switches ON shows neon, OFF shows no neon",
    "Photograph EVERY wall before plastering with circuit IDs labelled - keep photos in project folder",
]

pdf.set_font("Helvetica", "", 9)
for item in checklist:
    pdf.set_x(14)
    pdf.cell(7, 5, "[  ]", ln=0)
    pdf.multi_cell(0, 5, item)
    pdf.ln(0.3)

# PAGE 11 - Common mistakes
pdf.add_page()
pdf.h1("10. Common Mistakes To AVOID")

mistakes = [
    ("50 mm box at smart-switch location",
     "The Sonoff/Aqara module will not fit. Whole installation has to be redone. "
     "Always 65 mm at smart-switch locations."),
    ("Skipping neutral at switch boards",
     "Smart relay needs neutral. Without it, the smart switch is dead the day it's installed. "
     "Every switch board gets neutral - even dumb ones, in case we upgrade later."),
    ("Power and Cat6 in same conduit",
     "Cat6 picks up 230V interference and slows the network. ALWAYS separate conduits."),
    ("Geyser switch INSIDE the bathroom",
     "Code violation (IS 3043). Always place geyser switch OUTSIDE bathroom door, on the dry side, "
     "at 1050 mm FFL."),
    ("AC socket low on the wall",
     "AC socket at 300 mm puts the cable in view and creates a trip hazard. AC socket is at "
     "1850 mm FFL, near where the indoor unit will mount."),
    ("Forgetting earth at sockets",
     "Every 3-pin socket gets earth (green/yellow). Test continuity before plastering."),
    ("Mixing wire colours",
     "Red = LIVE. Black = NEUTRAL. Green/Yellow = EARTH. Blue = SWITCHED LIVE. "
     "Never use random colours."),
    ("Cutting chase narrower than needed",
     "FF staircase chase needs 9 conduits. Cut 150 mm wide first time. "
     "Cutting twice = double the mason cost."),
    ("Foyer screen cavity painted normal colour",
     "Inside cavity must be MATTE BLACK before stone cladding. Otherwise edge shadows show "
     "around the screen."),
    ("Forgetting LV-16 to screen-bezel camera",
     "RPi camera at top centre of foyer screen needs a small CSI ribbon path. "
     "Pull 1x LV-16 sleeve from cavity back to top centre at 1600-1650 mm FFL."),
]

for label, txt in mistakes:
    pdf.callout(label, txt)

# PAGE 12 - Sign-off
pdf.add_page()
pdf.h1("11. Sign-Off")

pdf.body(
    "By signing below, the electrician confirms that the installation conforms to the layout, "
    "cavity depths, conduit colours, wire colours, and standard heights described in this "
    "document. Any deviation has been agreed in writing with the homeowner."
)
pdf.ln(8)

# Sign blocks
pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 7, "Pre-plaster sign-off:", ln=1)
pdf.ln(2)
pdf.cell(80, 7, "Electrician signature: __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Mason signature:        __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Homeowner signature:   __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(15)

pdf.cell(0, 7, "Post-installation sign-off (after fixtures installed):", ln=1)
pdf.ln(2)
pdf.cell(80, 7, "Electrician signature: __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Homeowner signature:   __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(20)

pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5,
    "Document prepared from: electrical/conduits-and-cavities.md, ground-floor-electrical.md, "
    "first-floor-electrical.md, db-layout.md, materials-checklist.md (project repo). "
    "For digital reference, see the markdown source files. v1.0 - 2026-05-06.")

pdf.output(str(OUT))
print(f"Generated: {OUT}")
print(f"Pages: {pdf.page_no()}")
