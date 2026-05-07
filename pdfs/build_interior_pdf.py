"""
Build the Interior Suggestions PDF.
A-to-Z whole-house interior reference with palettes, finishes, lighting, furniture.
Format: A4 portrait, hex swatches inline, friendly to share with the interior contractor.
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "INTERIOR_SUGGESTIONS.pdf"

# ---------- PDF helpers ----------
class InteriorPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(14, 14, 14)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 90, 50)
        self.cell(0, 6, "Ganesh Prasad - Home Interior Suggestions (Chitradurga)", ln=0, align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", ln=1)
        self.set_draw_color(180, 140, 70)
        self.line(14, 23, 196, 23)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, "v1.0 - 2026-05-06 - Whole-house interior brief", align="C")

    # building blocks
    def h1(self, text):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(80, 50, 20)
        self.set_fill_color(245, 235, 215)
        self.cell(0, 12, text, ln=1, fill=True)
        self.ln(2)

    def h2(self, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(80, 60, 30)
        self.cell(0, 8, text, ln=1)
        self.set_draw_color(180, 140, 70)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(3)

    def h3(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(100, 70, 40)
        self.cell(0, 6, text, ln=1)
        self.ln(0.5)

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

    def hex_to_rgb(self, hex_str):
        h = hex_str.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    def color_swatch(self, hex_code, name, code_or_use):
        """Render a single colour swatch row."""
        x = self.get_x()
        y = self.get_y()
        r, g, b = self.hex_to_rgb(hex_code)
        # swatch rectangle
        self.set_fill_color(r, g, b)
        self.set_draw_color(180, 180, 180)
        self.rect(x, y, 24, 10, "DF")
        # name + hex + use
        self.set_xy(x + 26, y)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(40, 40, 40)
        self.cell(50, 5, name, ln=0)
        self.set_font("Courier", "", 9)
        self.cell(20, 5, hex_code, ln=0)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, code_or_use, ln=1)
        # second-line note slot
        self.set_xy(x + 26, y + 5)
        self.cell(0, 5, "", ln=1)
        self.set_xy(x, y + 11)

    def safe_break(self, text, max_w):
        if not text:
            return text
        words = text.split(" ")
        out_words = []
        for w in words:
            if self.get_string_width(w) <= max_w - 2:
                out_words.append(w)
            else:
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
        self.set_fill_color(120, 90, 50)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_widths):
            self.cell(w, 7, self.safe_break(h, w), border=1, align="C", fill=True)
        self.ln(7)
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 9)
        rows = [
            [self.safe_break(str(c), col_widths[i]) for i, c in enumerate(row)]
            for row in rows
        ]
        fill = False
        line_h = 4.5
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
                    avail = max(w - 2, 5)
                    tot += max(1, -(-int(sw // avail) - 1))
                lines_needed.append(max(1, tot))
            row_lines = max(lines_needed)
            row_h = max(row_lines * line_h, 6)
            if self.get_y() + row_h > self.h - 22:
                self.add_page()
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(120, 90, 50)
                self.set_text_color(255, 255, 255)
                for h, w in zip(headers, col_widths):
                    self.cell(w, 7, self.safe_break(h, w), border=1, align="C", fill=True)
                self.ln(7)
                self.set_text_color(40, 40, 40)
                self.set_font("Helvetica", "", 9)
            self.set_fill_color(252, 248, 240) if fill else self.set_fill_color(255, 255, 255)
            x_start, y_start = self.get_x(), self.get_y()
            for cell, w in zip(row, col_widths):
                self.rect(self.get_x(), self.get_y(), w, row_h, "DF")
                self.set_x(self.get_x() + w)
            self.set_xy(x_start, y_start)
            for i, (cell, w) in enumerate(zip(row, col_widths)):
                cur_x, cur_y = self.get_x(), self.get_y()
                content_h = max(1, lines_needed[i]) * line_h
                offset_y = max(0, (row_h - content_h) / 2)
                self.set_xy(cur_x + 1, cur_y + offset_y)
                self.multi_cell(w - 2, line_h, str(cell), border=0, align="L", fill=False)
                self.set_xy(cur_x + w, cur_y)
            self.set_xy(x_start, y_start + row_h)
            fill = not fill
        self.ln(2)


# ---------- BUILD PDF ----------
pdf = InteriorPDF()

# COVER PAGE
pdf.add_page()
pdf.set_y(35)
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(80, 50, 20)
pdf.cell(0, 14, "INTERIOR", ln=1, align="C")
pdf.cell(0, 14, "SUGGESTIONS", ln=1, align="C")
pdf.ln(8)
pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(120, 90, 50)
pdf.cell(0, 7, "Whole-house brief : palette | finishes | furniture | lighting", ln=1, align="C")
pdf.ln(2)
pdf.set_font("Helvetica", "I", 11)
pdf.cell(0, 6, "GF : Warm Contemporary Indian   |   FF : Warm Modern Luxe", ln=1, align="C")
pdf.ln(15)

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
pdf.cell(0, 6, "House       : 2-floor, North-facing main entrance", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Floors      : GF (11 ft ceiling) + FF (10 ft ceiling)", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Style anchor: existing teak windows (preserve, no paint)", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Hero space  : double-height living, 16'9 x 11' void", ln=1)
pdf.set_x(35)
pdf.cell(0, 6, "Document    : v1.0  -  2026-05-06", ln=1)

pdf.set_y(190)
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(255, 230, 200)
pdf.cell(0, 8, "  HOW TO USE THIS DOCUMENT", ln=1, fill=True)
pdf.ln(2)
pdf.set_font("Helvetica", "", 10)
pdf.set_x(14)
pdf.multi_cell(0, 5,
    "1. Hand this PDF to the interior contractor as the brief. Every paint, tile, fabric and wood "
    "decision is here in one place.\n\n"
    "2. The colour palette uses HEX codes. Bring the PDF to the Asian Paints / Berger / Dulux dealer "
    "and ask for a fan-deck match against each hex.\n\n"
    "3. Always paint a 2 ft x 2 ft sample on the actual wall and view at three times of day BEFORE "
    "approving any paint colour.\n\n"
    "4. The two floors share a neutral base (warm ivory) so they read as one home, not two themes.\n\n"
    "5. Any deviation from this brief must be agreed in writing with the homeowner.")

# PAGE 2 - Style direction
pdf.add_page()
pdf.h1("1. Style Direction")

pdf.h2("Ground Floor - Warm Contemporary Indian")
pdf.body(
    "Calm, premium, practical, not flashy. Teak windows already supply strong warmth - the "
    "surrounding palette stays lighter to avoid a heavy brown room. Layered lighting (cove, "
    "downlight, accent, decorative). Sunken living floor with brass step inlay. One large "
    "vertical chandelier in the double-height void. Microcement / travertine / fluted teak "
    "TV feature wall on the West side."
)
pdf.body(
    "Material vocabulary : warm ivory walls + warm greige stone + teak + dark walnut accents + "
    "antique brass / champagne hardware + oatmeal upholstery + sage / rust / brass cushions."
)

pdf.h2("First Floor - Warm Modern Luxe (Japandi-with-luxe-accents)")
pdf.body(
    "Moodier, richer materials than GF - Japandi bones with travertine + walnut + brass accents. "
    "Bedroom 2's North wall (already locked) is full-height honed Italian travertine cladding "
    "with two floating walnut shelves and a height-adjustable walnut-top desk. Bedroom 1 is "
    "lighter, sage-accented, no false ceiling. Both bedrooms get the same warm ivory walls and "
    "share the GF tile flow."
)

pdf.h2("Common Thread")
pdf.body(
    "Warm ivory base everywhere | no cool whites | no high-gloss surfaces | layered lighting "
    "(2700 K everywhere except kitchen/bathrooms) | one metal vocabulary per zone | brushed "
    "gold / champagne brass for all visible hardware | matte black for exterior + step-edge "
    "L-profiles only."
)

# PAGE 3 - Whole-house neutral base
pdf.add_page()
pdf.h1("2. Whole-House Neutral Base")

pdf.body(
    "Three colours appear everywhere - walls, ceilings, skirting - and tie the house together. "
    "Pick these first, paint samples on actual walls, then build the accent layers."
)
pdf.ln(2)

pdf.h3("BASE")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Asian Paints 0125 'Ivory Touch' or 7942 'White Sand' - all interior walls")
pdf.color_swatch("#F8F4EC", "Soft Snow",  "Asian Paints 7857 'Snow Storm' - all ceilings")
pdf.color_swatch("#FAF6EC", "Warm White", "Asian Paints 7860 'Almond Frost' - door frames, skirting")

pdf.ln(3)
pdf.callout("Painter's rule",
    "Walls in #F2EBDD, ceiling 1 shade lighter (#F8F4EC), trim 1 shade lighter again. This subtle "
    "gradient keeps ceilings reading as ceilings without harsh contrast - important for the double-"
    "height living area where ceiling shadows would otherwise be obvious."
)

# PAGE 4 - GF Palette
pdf.add_page()
pdf.h1("3. Ground Floor Palette")

pdf.h2("Foyer")
pdf.color_swatch("#7B5C42", "Tobacco Brown", "Stone cladding - rustic ledgestone")
pdf.color_swatch("#C8B58F", "Sandstone Beige", "Stone cladding accent stones")
pdf.color_swatch("#3A3633", "Charcoal", "Stone cladding accent stones")
pdf.color_swatch("#4A3526", "Dark Walnut", "Floating shelf - solid teak/walnut, oil finish")
pdf.color_swatch("#FFB877", "Warm Amber 2200K", "LED halo around screen")

pdf.h2("Living Area")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Main walls (washable matte emulsion)")
pdf.color_swatch("#B8A88F", "Warm Greige Stone", "TV feature wall (W) - microcement / travertine slab / matte stone")
pdf.color_swatch("#8B6F4E", "Natural Teak", "TV-side fluted panels, 18-24in wide")
pdf.color_swatch("#E8DCC8", "Warm Ivory-Greige", "Floor tiles 1200x1200mm matte porcelain")
pdf.color_swatch("#B08D57", "Antique Brass", "Sunken floor edge inlay 6mm strip")
pdf.color_swatch("#D4C4B0", "Oatmeal", "Sofa fabric - performance linen / chenille")

pdf.h3("Living Cushion Accents (3 only)")
pdf.color_swatch("#9CA68D", "Muted Sage", "Cushion accent #1 - linen with texture")
pdf.color_swatch("#B5673E", "Rust Ochre", "Cushion accent #2 - velvet or boucle")
pdf.color_swatch("#3F3A35", "Charcoal", "Cushion accent #3 - linen weave")

# PAGE 5 - GF continued
pdf.add_page()
pdf.h2("Dining Area")
pdf.body("Same palette as Living - keeps the open zone visually unified.")

pdf.h2("Master Bedroom (GF)")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Walls")
pdf.color_swatch("#A8967E", "Warm Taupe", "Headboard wall (accent)")
pdf.color_swatch("#4A3526", "Walnut", "Wardrobe shutters (mixed with cream) + bed frame")
pdf.color_swatch("#E8DCC8", "Warm Cream", "Wardrobe shutters - secondary panels")
pdf.color_swatch("#EFE8DA", "Pale Linen", "Bedding primary")
pdf.color_swatch("#9CA68D", "Olive Throw", "Bedding accent")

pdf.h2("Pooja Room")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Walls")
pdf.color_swatch("#C8A45C", "Antique Gold", "Idol niche back - lime wash with gold mica or brass-leaf laminate")
pdf.color_swatch("#FFA85C", "Devotional Amber", "Niche backlight 2200K")
pdf.color_swatch("#6E5234", "Burnished Teak", "Pooja unit wood - traditional carved panels")

pdf.h2("Kitchen")
pdf.color_swatch("#F0E9DC", "Off-white Subway", "Backsplash - 100x300mm matte ceramic stack-bond")
pdf.color_swatch("#E0D4C0", "Quartz Cream", "Counter top - quartz / engineered stone")
pdf.color_swatch("#3F3A35", "Charcoal Matte", "Lower cabinet shutters - PU laminate on BWP ply")
pdf.color_swatch("#E8DCC8", "Warm Cream Matte", "Upper cabinet shutters")
pdf.color_swatch("#B08D57", "Brushed Brass", "Handles + hardware (consistent with bath fittings)")
pdf.color_swatch("#C8B89C", "Warm Greige R10", "Floor tile - 600x600mm matte porcelain anti-slip")

pdf.h2("GF Common Bathroom (locked - Light Luxury Spa)")
pdf.color_swatch("#EFE5D2", "Warm Cream Marble", "Wall tiles 600x1200mm matte porcelain")
pdf.color_swatch("#C8B89C", "Warm Greige R10", "Floor tiles 600x600mm anti-slip")
pdf.color_swatch("#4A3526", "Walnut", "Vanity cabinet - marine ply + matte laminate")
pdf.color_swatch("#B08D57", "Brushed Gold", "All hardware - single brand throughout")
pdf.color_swatch("#8B6F4E", "Natural Teak", "Fold-down shower bench")

# PAGE 6 - FF Palette
pdf.add_page()
pdf.h1("4. First Floor Palette")

pdf.h2("FF Living / Corridor")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Walls (same as GF base)")
pdf.color_swatch("#EAE0C8", "Warmer Cream", "Beam edge / cut-out - 1 shade warmer than ceiling")
pdf.color_swatch("#E8DCC8", "Warm Ivory-Greige", "Floor tiles 1200x1200 (continuous from GF)")

pdf.h2("Bedroom 1 (East - no false ceiling)")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Walls")
pdf.color_swatch("#A8B0A0", "Soft Sage-Grey", "Headboard wall accent - lime wash or fluted PU panel")
pdf.color_swatch("#4A3526", "Walnut", "Wardrobe shutters (mixed) + bed + study desk")
pdf.color_swatch("#9CA68D", "Warm Sage", "Curtain drape - 1.8x fullness")
pdf.color_swatch("#F4EFE3", "Off-white", "Curtain sheer - 2x fullness")

pdf.h2("Bedroom 2 (West - false ceiling, Warm Modern Luxe)")
pdf.color_swatch("#F2EBDD", "Warm Ivory", "Walls (3 walls)")
pdf.color_swatch("#D6C5A8", "Travertine Cream", "N wall (LOCKED) - Italian travertine, vein-cut, honed")
pdf.color_swatch("#A89878", "Travertine Veins", "N wall - veining colour reference")
pdf.color_swatch("#A8967E", "Warm Taupe", "Headboard wall (S) emulsion + walnut fluted panel")
pdf.color_swatch("#4A3526", "Walnut", "Wardrobe + bed + floating shelves")
pdf.color_swatch("#3F3A35", "Charcoal", "Curtain drape (velvet, blackout)")
pdf.color_swatch("#1A1A1A", "Carbon Black", "Aeron office chair (already chosen)")
pdf.color_swatch("#B08D57", "Antique Brass", "Desk lamp + standoff hardware")

pdf.h2("FF Toilets 1 + 2")
pdf.body("Same palette as GF Common Bathroom for visual consistency. Hardware: brushed gold throughout.")

pdf.h2("Front Balcony")
pdf.color_swatch("#6E5234", "IPE Wood-look", "Floor tiles 200x1200mm porcelain R11 anti-slip")
pdf.color_swatch("#A8967E", "Warm Taupe", "Parapet inner cap")

# PAGE 7 - Lighting
pdf.add_page()
pdf.h1("5. Lighting Design")

pdf.body(
    "Each room has 4 layers : ambient + task + accent + decorative. Mix appropriately. Never use "
    "a single bright central light - it flattens the space."
)
pdf.ln(2)

pdf.h2("Lighting Colour Temperature - Whole-House Standard")
pdf.table(
    headers=["Zone", "Temp", "Visual", "Why"],
    rows=[
        ["Foyer screen halo", "2200 K", "warm amber", "Welcoming, slightly intimate"],
        ["Foyer + Living + Dining + Bedrooms", "2700 K", "warm white", "Skin-flattering, premium"],
        ["Pooja niche backlight", "2200 K", "warm amber", "Devotional warmth"],
        ["Kitchen", "4000 K", "neutral white", "Task accuracy without coldness"],
        ["All bathrooms", "3000 K", "warm-neutral", "Slightly cooler - better grooming"],
        ["Study spotlights (BR1+BR2)", "3000 K", "warm-neutral", "Focus, not as cool as kitchen"],
        ["Outdoor / staircase", "3000 K", "warm-neutral", "Standard outdoor warm"],
    ],
    col_widths=[60, 18, 32, 72],
)

pdf.callout("Rule",
    "Never mix colour temperatures inside a single visible space. Living + Foyer + Dining all see "
    "each other - all 2700 K. Kitchen is its own room - can be 4000 K. Bathroom is its own room - "
    "3000 K is fine."
)

pdf.h2("Best Lighting Selections - Per Room")
pdf.table(
    headers=["Room", "Decorative anchor"],
    rows=[
        ["Foyer", "Walnut shelf with under-shelf 2700 K LED + amber halo around screen"],
        ["Living", "Vertical cluster pendant in void - antique brass / champagne, 24-36in diameter, hung over coffee-table area"],
        ["Dining", "1x decorative pendant over dining table - warm 2700 K, drop to 2100 mm FFL"],
        ["Kitchen", "(no decorative - task only with under-cabinet warm LED)"],
        ["MBR", "Bedside table lamps with brass shades + 5W warm LED"],
        ["Pooja", "Niche backlight 2200 K behind brass-leaf or gold mica"],
        ["BR1", "Bedside lamp + ceiling COB"],
        ["BR2", "Brass desk lamp + walnut-shelf strips + bedside walnut lamp"],
        ["Bathrooms", "LED backlit mirror + IP44/IP65 downlights + niche LED"],
    ],
    col_widths=[40, 142],
)

# PAGE 8 - Materials & Finishes
pdf.add_page()
pdf.h1("6. Materials & Finishes")

pdf.h2("Tiles - Whole-house spec")
pdf.table(
    headers=["Zone", "Tile", "Size", "Brand"],
    rows=[
        ["Living + Dining + Foyer + MBR + Pooja", "Warm ivory-greige marble matte", "1200x1200", "Kajaria Eternity / Somany Slimtec"],
        ["Bedrooms (FF)", "Same", "1200x1200", "Same"],
        ["Kitchen + Utility floor", "Warm greige R10 anti-slip", "600x600", "Kajaria/Somany"],
        ["Bathroom walls (all)", "Warm cream marble matte", "600x1200", "Kajaria Eternity / RAK"],
        ["Bathroom floors (all)", "Warm greige R10 anti-slip", "600x600", "Same"],
        ["Front + W balcony", "Wood-look porcelain IPE", "200x1200 R11", "Kajaria Vintage Wood"],
        ["Kitchen backsplash", "Warm cream subway matte", "100x300", "Local OK"],
    ],
    col_widths=[60, 50, 25, 47],
)

pdf.h2("Wood Tones (3 standard tones - whole house)")
pdf.color_swatch("#8B6F4E", "Natural Teak",   "Existing windows + foyer shelf option + kitchen bar stools")
pdf.color_swatch("#4A3526", "Dark Walnut",    "Bedroom wardrobes + bed frames + BR2 floating shelves + dining table top")
pdf.color_swatch("#6E5234", "Burnished Teak", "Pooja unit + balcony flooring + BR1 study desk top")

pdf.h2("Accent Metals (whole-house)")
pdf.color_swatch("#B08D57", "Brushed Antique Brass / Champagne", "All bathroom hardware + kitchen handles + brass desk lamp BR2 + curtain finials")
pdf.color_swatch("#1F1B16", "Matte Black", "Step-edge L-profile (sunken floor) + exterior balcony railings + window grills")

pdf.callout("Rule",
    "Pick ONE metal vocabulary per zone. Bathrooms = brushed gold. Kitchen = brushed brass. "
    "Exterior = matte black. Switch plates and modular frames stay one finish across the whole "
    "house - recommended champagne / brushed brass (Schneider Unica or Legrand Mylinec)."
)

# PAGE 9 - Furniture
pdf.add_page()
pdf.h1("7. Furniture Brief (per room)")

pdf.h2("Living Area")
pdf.body(
    "L-shaped layout : long side along N wall (10-11 ft), return along E side (6-7 ft), pulled "
    "5in off N wall to clear the curtain track. Two accent chairs on the open S side. Coffee "
    "table 48x28in or 42in round, travertine top. 10x13ft rug inside the sunken zone."
)

pdf.h2("Dining")
pdf.body(
    "6-seater walnut-top table (6x3ft) with brass-clad legs. 6 walnut chairs with oatmeal "
    "upholstered seats. Sideboard 5-6ft along W wall."
)

pdf.h2("Master Bedroom (GF)")
pdf.body(
    "King bed 78x72in with cream linen upholstered headboard, walnut frame. Bedside tables 22x16in "
    "in walnut. Wardrobes : 12 ft N wall + 12'3 W wall, walnut + matte cream split shutters. "
    "Dressing table 4 ft on E or S wall."
)

pdf.h2("FF Bedroom 1")
pdf.body(
    "Queen bed 75x60in walnut, low-profile headboard. Bedside tables 18in round walnut. Wardrobe "
    "8 ft, walnut + cream split. Study desk 4x2 ft. Window seat (S wall) optional."
)

pdf.h2("FF Bedroom 2 (Warm Modern Luxe - work zone LOCKED)")
pdf.body(
    "Queen bed 75x60in walnut with cream linen upholstered headboard. N wall : 9 ft Italian "
    "travertine cladding (LOCKED), 2x 5 ft floating walnut shelves with under-shelf 2700 K LED, "
    "4 ft height-adjustable walnut-top desk, monitor on articulating arm, Aeron chair (already "
    "chosen), 2x3 ft frameless glass writing board with brass standoffs, brass desk lamp."
)

pdf.h2("Kitchen")
pdf.body(
    "L-shape, top-left corner. Lower cabinets BWP 18mm + charcoal matte PU laminate. Upper "
    "cabinets BWP + warm cream matte. Quartz cream counter. Off-white subway backsplash. "
    "Stainless undermount double-bowl 32x18in sink. Chimney 90cm auto-clean brushed black. "
    "Tall pantry 30in wide. Microwave + OTG niches at counter level. Refrigerator niche 30in."
)

# PAGE 10 - Sanitaryware
pdf.add_page()
pdf.h1("8. Sanitaryware - Brand Picks")

pdf.h3("Recommended single brand for all 3 bathrooms : Jaquar Lighthouse OR Kohler Composed (brushed gold)")
pdf.body(
    "Sticking to one brand and one finish across all bathrooms ensures shade match and reduces "
    "purchase friction."
)
pdf.ln(2)

pdf.table(
    headers=["Item", "Budget", "Mid pick", "Premium"],
    rows=[
        ["WC + concealed cistern", "Parryware / Hindware", "Jaquar Continental", "Kohler / TOTO"],
        ["Basin", "Parryware", "Jaquar", "Kohler"],
        ["Faucets / mixers", "Jaquar Continental", "Kohler Composed / Jaquar Lighthouse", "Grohe Essence (gold)"],
        ["Shower head", "Local", "Jaquar", "Hansgrohe"],
        ["Concealed cistern", "Geberit Sigma", "Geberit Sigma", "Geberit"],
        ["Geyser", "Bajaj 15L", "Racold Eterno 15L", "AO Smith 15L"],
        ["Mirror (LED)", "Local LED 600x800", "Branded LED frameless", "Custom"],
    ],
    col_widths=[42, 42, 60, 38],
)

pdf.h2("Geyser size and location (all 3 bathrooms)")
pdf.body("All 3 bathrooms : 15 L geyser, mounted in attic / above lintel where applicable.")

pdf.h2("Bathroom Hardware Checklist (brushed gold throughout)")
items = [
    "Basin faucet - single lever, deck mount",
    "WC flush plate - in-wall cistern type",
    "Rain shower head - ceiling mount, 200mm round",
    "Handheld shower + sliding rail 1.2m",
    "Diverter / thermostatic valve",
    "Towel bar (600mm)",
    "Robe hook (behind door swing)",
    "Toilet paper holder",
    "Shower door handle (D-pull) OR fixed-panel (no door)",
]
pdf.set_font("Helvetica", "", 10)
for it in items:
    pdf.cell(7, 5, "[ ]", ln=0)
    pdf.cell(0, 5, it, ln=1)

# PAGE 11 - Curtains and decor
pdf.add_page()
pdf.h1("9. Curtains & Soft Furnishings")

pdf.h2("Curtain Standard (whole house)")
pdf.body(
    "Ceiling-recessed double aluminium track : sheer + drape. Sheer in off-white #F4EFE3 (2x "
    "fullness ripple fold). Drape in warm greige #A89F8C (1.8x fullness, dim-out lining). For "
    "bedrooms : drape becomes blackout. North living-window curtain : motorized strongly "
    "recommended due to height."
)

pdf.h2("Rugs")
pdf.table(
    headers=["Room", "Rug", "Size", "Material"],
    rows=[
        ["Living", "Floor rug", "10 x 13 ft", "Low-pile wool, oatmeal/grey weave"],
        ["Dining", "Optional rug under table", "6 x 9 ft", "Flat-weave"],
        ["MBR", "Bedside runners", "2 x 6 ft each", "Wool dhurrie"],
        ["BR1", "Floor rug", "5 x 8 ft", "Wool"],
        ["BR2", "Floor rug", "6 x 9 ft", "Wool, charcoal/cream"],
        ["Foyer", "Optional runner", "2 x 4 ft", "Cotton dhurrie"],
    ],
    col_widths=[28, 50, 30, 74],
)

pdf.h2("Decor Rules")
pdf.body(
    "- LESS IS MORE. One large statement piece beats six small clutter items.\n"
    "- 1 large indoor plant per room (areca palm, fiddle leaf fig, rubber, snake plant, ZZ).\n"
    "- Art : ONE large piece in the living, ONE in MBR, ONE in dining. Max 3 framed photos in any "
    "single sightline.\n"
    "- Pillows : max 4 per sofa, mix of plain + texture + 1 accent.\n"
    "- Books on coffee tables : 3-5 books in a small stack, never sprawling.\n"
    "- Candles, vases, brass figures : group in odd numbers (1 or 3, never 2).\n"
    "- AVOID : tassels, fringes, very ornate frames, religious posters in living/foyer (pooja "
    "room is the right place)."
)

# PAGE 12 - Avoid list & Sample procurement
pdf.add_page()
pdf.h1("10. Avoid List (Whole House)")

pdf.body(
    "These colours and materials are NOT used anywhere - they fight the palette or look cheap "
    "at scale."
)
avoid_list = [
    "Stark cool white (#FFFFFF) - looks hospital-clean, kills warmth",
    "Cool blue-grey walls - fights the teak windows",
    "Glossy laminate on any visible surface - makes everything look cheap",
    "High-gloss white tiles - glare in the double-height room is unpleasant",
    "Strong contrast veining (black, gold, red) - fights with teak, dated in 5 years",
    "More than one feature wall in any contiguous open space",
    "Three different wood tones in the same room",
    "Mixing brass and chrome hardware in the same room",
    "Saturated colours on anything bigger than a cushion or vase",
    "Tassels, fringes, ornate frames",
    "Religious posters / calendars in living or foyer",
]
pdf.set_font("Helvetica", "", 10)
for it in avoid_list:
    pdf.cell(7, 5, "X", ln=0)
    pdf.multi_cell(0, 5, " " + it)
    pdf.ln(0.3)

pdf.h1("11. Sample Procurement Checklist")
pdf.body(
    "Do this BEFORE any bulk order. A Rs 500 sample saves Rs 50,000 in re-do."
)
checklist = [
    "Paint sample pots : #F2EBDD (Ivory Touch), #F8F4EC (Snow Storm), #A8967E (taupe), #9CA68D (sage) - paint 2x2 ft, view 3 times of day",
    "Tile samples : 1x full 1200x1200 living + 1x 600x1200 bath wall + 1x 600x600 floor - on actual floor in actual daylight",
    "Wood samples : walnut + teak + burnished teak laminates side-by-side under 2700 K bulb + natural light",
    "Stone slab samples : TV wall greige + BR2 travertine - bring home, view all times of day",
    "Hardware sample : 1x brushed-gold faucet handle + 1x champagne-brass cabinet handle - confirm shade match",
    "Curtain fabric : 12x12in swatch of sheer + main drape - drape in actual window for an evening",
    "Accent metal : 1x modular switch plate sample in champagne - confirm against bath fittings",
]
pdf.set_font("Helvetica", "", 9.5)
for it in checklist:
    pdf.cell(7, 5, "[  ]", ln=0)
    pdf.multi_cell(0, 5, it)
    pdf.ln(0.3)

# PAGE 13 - Vendor cheat-sheet
pdf.add_page()
pdf.h1("12. Vendor Cheat Sheet")

pdf.body(
    "One-shot list of who to contact for what. Fill in phone numbers as you go."
)

pdf.table(
    headers=["Category", "Vendor", "What to ask for"],
    rows=[
        ["Paint", "Asian Paints / Berger / Dulux dealer (Chitradurga)", "Fan-deck match for each hex code"],
        ["Tile premium", "Kajaria / Somany / RAK (Bangalore showroom)", "Warm ivory-greige marble 1200x1200 matte"],
        ["Quartz / stone", "Stone Studio / Classic Marbles (Bangalore)", "6x6in samples brought home"],
        ["Hardware", "Hettich / Hafele showroom (Bangalore)", "Brushed brass / champagne D-pulls"],
        ["Sanitaryware", "Jaquar showroom OR local Plumber's Choice", "Jaquar Lighthouse OR Kohler Composed (gold)"],
        ["Modular switches", "Schneider / Legrand authorised dealer", "Schneider Unica champagne (whole house)"],
        ["Wood / laminate", "Greenply / Century / Merino", "Walnut laminate + cream matte laminate"],
        ["CCTV / cameras", "I Secure India, Chitradurga (CONFIRMED)", "Hikvision DS-2CD2143G2-LU + others"],
        ["Curtains / blinds", "Local interior tailor + motor", "D'Decor / Marshalls fabric source"],
        ["Furniture custom", "Local carpenter; Pepperfry / Wooden Street for high-end", "BWP carcass + matte laminate"],
    ],
    col_widths=[38, 60, 84],
)

# PAGE 14 - Rough quantities + budget
pdf.add_page()
pdf.h1("13. Rough Quantities & Budget Pointers")

pdf.body(
    "Treat this as a *budgeting* take-off, not a contractor BOQ. Contractor will measure on site."
)

pdf.table(
    headers=["Item", "Approx qty", "Notes"],
    rows=[
        ["Tile 1200x1200 (living continuous)", "100 sqm", "Living + dining + foyer + bedrooms + pooja"],
        ["Tile 600x1200 bathroom wall", "70 sqm", "All 3 bathrooms"],
        ["Tile 600x600 floor", "30 sqm", "Bathrooms + kitchen + utility"],
        ["Tile 200x1200 wood-look", "25 sqm", "Both balconies"],
        ["Paint premium emulsion", "200 litres", "Whole house interior + primer"],
        ["Paint exterior", "50 litres", "Exterior face only"],
        ["Plywood BWP 18mm", "50 sheets", "All built-ins"],
        ["Laminate matte", "60 sheets", "All built-ins"],
        ["Curtain fabric (sheer + drape)", "80 metres", "All windows"],
        ["Cove LED strip 24V 2700K", "30 metres", "All cove zones"],
        ["Recessed COB downlights", "35 nos", "Whole house"],
        ["GU10 spots", "20 nos", "Foyer + bedside + study spots"],
    ],
    col_widths=[80, 32, 70],
)

pdf.h2("Budget Pointers (rough order-of-magnitude)")
pdf.table(
    headers=["Bucket", "Estimated cost"],
    rows=[
        ["Tiles + grouting + waterproofing", "Rs 4 - 6 L"],
        ["Paint (interior + exterior + labour)", "Rs 1.5 - 2 L"],
        ["Furniture (built-ins + loose) - whole house", "Rs 8 - 12 L"],
        ["Sanitaryware + bath fittings (3 baths)", "Rs 2 - 3 L"],
        ["Lighting + fittings", "Rs 1.5 - 2 L"],
        ["Curtains + soft furnishings", "Rs 1 - 1.5 L"],
        ["Kitchen modular (counter + cabinets + appliances)", "Rs 3 - 5 L"],
        ["TOTAL INTERIOR (rough envelope)", "Rs 21 - 31 L"],
        ["Electrical (separate, tracked in materials-checklist.md)", "Rs 3.7 - 4 L"],
        ["GRAND TOTAL FIT-OUT", "Rs 25 - 35 L"],
    ],
    col_widths=[120, 62],
)

# PAGE 15 - Sign-off
pdf.add_page()
pdf.h1("14. Sign-Off")

pdf.body(
    "By signing below, the homeowner confirms the colour palette, finish direction, and "
    "furniture brief described in this document. The interior contractor uses this as the "
    "primary brief and refers back here for any colour, finish, or material question."
)
pdf.ln(8)

pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 7, "Brief acceptance:", ln=1)
pdf.ln(2)
pdf.cell(80, 7, "Homeowner signature:    __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Interior contractor:    __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Carpenter (joinery):    __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(3)
pdf.cell(80, 7, "Painter:                __________________________", ln=0)
pdf.cell(0, 7, "Date: ___________", ln=1)
pdf.ln(20)

pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5,
    "Document prepared from: interior-design/master-interior-spec.md, "
    "materials-finishes/master-color-palette.md, interior-design/living-area.md, "
    "interior-design/gf-common-bathroom.md, materials-finishes/wall-finishes.md, "
    "materials-finishes/flooring.md (project repo). "
    "v1.0 - 2026-05-06.")

pdf.output(str(OUT))
print(f"Generated: {OUT}")
print(f"Pages: {pdf.page_no()}")
