"""
Build the Whole-House Lighting Design PDF.

Comprehensive lighting brief: layers, color temperature, fixture-by-fixture
positions per room, magnetic COB track system, brands, prices, and shopping list.

Format: A4 portrait, hero photographs embedded, fixture schedule tables,
ready to hand to lighting contractor + electrician.
"""
from fpdf import FPDF
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = Path(__file__).parent / "HOUSE_LIGHTING.pdf"
IMG_DIR = ROOT / "interior-design" / "generated-images"

# -------- Image registry ----------
# Filename -> caption
IMAGES = {
    "magnetic_cob_living": ("lighting-magnetic-cob-track-living-v1.png",
        "Magnetic COB track in the living-room ceiling. Recessed matte-black channel "
        "carries cylindrical COB spots, a linear grazer and a small pendant -- all "
        "warm 2700K, all repositionable."),
    "double_height": ("lighting-double-height-vertical-cluster-v1.png",
        "Hero piece: vertical cluster pendant in the 16'9\" x 11' double-height void. "
        "Antique brass, 24-36\" wide cluster, 10-12 cascading frosted-glass stems, "
        "2700K. Drop terminus ~2400mm above the sunken living floor."),
    "foyer_grazing": ("lighting-foyer-stone-grazing-v1.png",
        "Foyer stone-grazing -- 2x recessed GU10 gimbal spotlights at 300mm from the "
        "ledgestone wall, beams angled 30 degrees down. Texture sells the wall."),
    "dining_pendant": ("lighting-dining-pendant-cove-v1.png",
        "Dining: single decorative pendant centred over the table dropped to 2100mm + "
        "perimeter cove LED + 2x flanking recessed COB. Warm and intimate."),
    "bedroom_layered": ("lighting-bedroom-layered-v1.png",
        "Master bedroom: brass wall sconces flanking the headboard at 1400mm + bedside "
        "lamps with brass shades + warm wardrobe-strip glow. No false ceiling -- height "
        "preserved, layers do the work."),
    "br2_track_study": ("lighting-bedroom2-magnetic-track-study-v1.png",
        "FF Bedroom 2: 1.5m matte-black recessed magnetic track over the walnut "
        "height-adjustable desk. Two cylindrical COB spots + one linear grazer aimed "
        "at the honed travertine N wall. The track defines the work zone."),
}


# ---------- PDF helpers ----------
class LightingPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(14, 14, 14)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 90, 50)
        self.cell(0, 6, "Ganesh Prasad - Whole-House Lighting Design (Chitradurga)", ln=0, align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", ln=1)
        self.set_draw_color(180, 140, 70)
        self.line(14, 23, 196, 23)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, "v1.0 - 2026-05-10 - Lighting design + fixture schedule + buy list",
                  align="C")

    # building blocks
    def h1(self, text):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(80, 50, 20)
        self.set_fill_color(245, 235, 215)
        self.cell(0, 12, text, ln=1, fill=True)
        self.ln(2)

    def h2(self, text):
        self.set_font("Helvetica", "B", 13)
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

    def bullet(self, text, size=10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(40, 40, 40)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, "    - " + text)

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
        self.set_fill_color(255, 230, 200)
        self.set_text_color(150, 60, 0)
        self.cell(0, 6, "  !! IMPORTANT", ln=1, fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.set_fill_color(255, 245, 230)
        self.multi_cell(0, 5, "    " + text, fill=True)
        self.ln(2)

    def safe_break(self, text, max_w):
        if not text:
            return text
        words = str(text).split(" ")
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

    def image_with_caption(self, key, max_h=85):
        if key not in IMAGES:
            return
        fn, cap = IMAGES[key]
        path = IMG_DIR / fn
        if not path.exists():
            self.set_fill_color(245, 240, 230)
            self.set_text_color(150, 110, 60)
            self.set_font("Helvetica", "I", 9)
            self.multi_cell(0, 6, f"  [image placeholder: {fn} -- not yet rendered]", fill=True)
            self.ln(1)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(80, 60, 30)
            self.multi_cell(0, 5, "  Caption: " + cap)
            self.ln(2)
            return
        avail_w = 196 - 14 - 14
        # render with auto height up to max_h
        try:
            self.image(str(path), x=14, w=avail_w, h=max_h, keep_aspect_ratio=True)
        except TypeError:
            self.image(str(path), x=14, w=avail_w)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 60, 30)
        self.multi_cell(0, 5, cap)
        self.ln(2)

    def kelvin_strip(self):
        """Visual kelvin temperature strip 2200K -> 6500K."""
        x0 = self.get_x()
        y0 = self.get_y()
        bands = [
            ("2200K", (255, 197, 143), "Candle / Niche"),
            ("2700K", (255, 214, 165), "Warm white\n(this house)"),
            ("3000K", (255, 226, 185), "Soft white\n(bathrooms)"),
            ("4000K", (255, 245, 220), "Neutral\n(kitchen)"),
            ("5000K", (235, 240, 255), "Daylight\n(study task)"),
            ("6500K", (215, 230, 255), "Cool / hospital\n(avoid here)"),
        ]
        bw = (196 - 28) / len(bands)
        for i, (label, rgb, use) in enumerate(bands):
            self.set_fill_color(*rgb)
            self.set_draw_color(180, 180, 180)
            self.rect(x0 + i * bw, y0, bw, 14, "DF")
            self.set_xy(x0 + i * bw, y0 + 1)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(50, 30, 10)
            self.cell(bw, 5, label, align="C", ln=0)
            self.set_xy(x0 + i * bw, y0 + 6)
            self.set_font("Helvetica", "", 7)
            self.multi_cell(bw, 3, use, align="C")
        self.set_xy(x0, y0 + 16)


# ====================  BUILD PDF  ====================
pdf = LightingPDF()

# ---------- COVER PAGE ----------
pdf.add_page()
pdf.set_y(35)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(80, 50, 20)
pdf.cell(0, 14, "WHOLE-HOUSE", ln=1, align="C")
pdf.cell(0, 14, "LIGHTING DESIGN", ln=1, align="C")
pdf.ln(5)
pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(120, 90, 50)
pdf.cell(0, 7, "Layers, fixtures, positions, smart control, vendors", ln=1, align="C")
pdf.ln(2)
pdf.set_font("Helvetica", "I", 11)
pdf.cell(0, 6, "Lighting is the single biggest mood lever in a finished house.", ln=1, align="C")
pdf.cell(0, 6, "Get it right and even average finishes glow.  Get it wrong and ", ln=1, align="C")
pdf.cell(0, 6, "premium tile and walnut go flat.", ln=1, align="C")
pdf.ln(15)

pdf.set_fill_color(250, 240, 220)
pdf.set_draw_color(180, 140, 70)
pdf.rect(30, pdf.get_y(), 150, 76, "DF")
pdf.set_xy(35, pdf.get_y() + 4)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(80, 50, 20)
pdf.cell(0, 8, "PROJECT", ln=1)
pdf.set_x(35)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(40, 40, 40)
for line in [
    "Owner       : Ganesh Prasad D",
    "Location    : Chitradurga, Karnataka",
    "House       : 2-floor, North-facing main entrance",
    "Floors      : GF (11 ft slab) + FF (10 ft slab)",
    "Hero space  : 16'9 x 11' double-height void above living",
    "Style anchor: warm 2700K everywhere; 4000K only in kitchen + bathrooms",
    "Document    : v1.0  -  2026-05-10",
]:
    pdf.set_x(35)
    pdf.cell(0, 6, line, ln=1)

pdf.set_y(200)
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(255, 230, 200)
pdf.cell(0, 8, "  HOW TO USE THIS DOCUMENT", ln=1, fill=True)
pdf.ln(2)
pdf.set_font("Helvetica", "", 10)
pdf.set_x(14)
pdf.multi_cell(0, 5,
    "1. Print this PDF and hand to the lighting contractor + electrician on site.\n\n"
    "2. The fixture schedule (Section 6) tells the electrician where each light box "
    "must be cut into the false ceiling -- positions are in mm from finished floor and "
    "from named walls. Cross-check against electrical/conduits-and-cavities.md.\n\n"
    "3. The buy list (Section 11) is your shopping list. Quantities and SKUs included.\n\n"
    "4. Photographs are AI-rendered references for mood and fitting type, not exact "
    "site photos. Use them to communicate intent to the contractor.\n\n"
    "5. Anything that disagrees with the live floor plan or the master interior spec "
    "must be flagged before plastering -- after plastering it costs 5x to fix.")

# ---------- TABLE OF CONTENTS ----------
pdf.add_page()
pdf.h1("Contents")
toc = [
    ("1.  Lighting philosophy - the 4 layers",  "3"),
    ("2.  Colour temperature + CRI guide",      "4"),
    ("3.  Magnetic COB track system (deep dive)", "5"),
    ("4.  Whole-house lighting plan at a glance", "8"),
    ("5.  Smart control + dimming + scenes",     "9"),
    ("6.  Fixture schedule - room by room",      "10"),
    ("    6a. Foyer",                            "10"),
    ("    6b. Living area + double-height void", "11"),
    ("    6c. Dining",                           "13"),
    ("    6d. Kitchen + utility",                "14"),
    ("    6e. Pooja",                            "15"),
    ("    6f. Master Bedroom (GF)",              "15"),
    ("    6g. Bathrooms (3)",                    "16"),
    ("    6h. Staircase",                        "17"),
    ("    6i. FF Living + corridor",             "17"),
    ("    6j. FF Bedroom 1",                     "18"),
    ("    6k. FF Bedroom 2 (with magnetic track)", "18"),
    ("    6l. Balconies + outdoor",              "19"),
    ("7.  Brands - good / better / best",        "20"),
    ("8.  Where to buy (vendors + links)",       "21"),
    ("9.  Wattage + circuit summary",            "22"),
    ("10. Decorative fixtures - hero pieces",    "23"),
    ("11. Buy list (printable)",                 "24"),
    ("12. Installation checklist",               "25"),
    ("13. Things to AVOID",                      "26"),
]
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(40, 40, 40)
for label, page in toc:
    pdf.cell(0, 6.5, f"{label} ............................ {page}", ln=1)
pdf.ln(4)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(120, 100, 70)
pdf.multi_cell(0, 5, "Cross-references: electrical/conduits-and-cavities.md (PART 3), "
               "interior-design/master-interior-spec.md (Section L), electrical/db-layout.md")

# ---------- 1. LIGHTING PHILOSOPHY ----------
pdf.add_page()
pdf.h1("1. Lighting Philosophy - the 4 Layers")

pdf.body("Lighting is not a single fitting per room. Every well-lit room is built from "
         "FOUR independent layers, each on its own switch / dimmer. You should be able "
         "to turn any one layer off without losing the room.")

pdf.h2("The four layers")
pdf.table(
    ["Layer", "Job", "Typical fittings (this house)", "Switching"],
    [
        ["1. Ambient",  "General fill - lets you walk around safely. Soft, even.",
            "Recessed COB downlights 9-12W, perimeter cove LED 9.6 W/m, ceiling panel (kitchen only)",
            "Smart relay - dimmable"],
        ["2. Task",     "Direct light at a working surface.",
            "Mirror bar 12W (bath), under-cabinet strip (kitchen), study spot, bedside reading sconce",
            "Local switch / motion / dimmer"],
        ["3. Accent",   "Picks out texture - travertine, stone, niches, art.",
            "GU10 gimbal 5-7W, magnetic COB cylinder + linear grazer, niche LED",
            "Smart relay - separate scene"],
        ["4. Decorative", "The thing the eye lands on - the jewellery.",
            "Vertical cluster pendant in void, dining pendant, brass bedside lamps, brass arc floor lamp",
            "Smart relay - own dimmer"],
    ],
    [22, 60, 70, 30]
)

pdf.h2("The cardinal rule: never rely on one layer")
pdf.bullet("If you only have ambient -- the room looks flat. No texture, no mood.")
pdf.bullet("If you only have decorative -- pretty but you can't read.")
pdf.bullet("If you only have task -- spotty, harsh, like a hospital.")
pdf.bullet("Mix all four. Dim the ambient, leave the cove on, switch off the task, "
           "let the decorative carry the evening. That is the magic.")

pdf.callout("Designer trick (used everywhere in this house)",
    "Always run the cove LED on its own dimmer. Then on a movie night you can drop "
    "ambient to zero, kill the decorative pendant, leave the cove at 30 percent. "
    "The cove glow alone is enough to walk around -- the room reads like a film. "
    "Try that on a single ceiling-bulb setup -- impossible.")

# ---------- 2. COLOUR TEMPERATURE ----------
pdf.add_page()
pdf.h1("2. Colour Temperature + CRI")

pdf.h2("Kelvin scale - what each value looks like")
pdf.kelvin_strip()
pdf.ln(2)
pdf.body("This house standardises on 2700K everywhere except kitchen and bathrooms. "
         "2700K is the warmth of an old incandescent / Edison bulb -- it flatters skin, "
         "warms wood, and reads as evening even at noon. Kitchen and bathrooms run cooler "
         "(4000K) for accurate task vision. The pooja niche dips warmer still (2200K) "
         "for the amber, lamp-like glow.")

pdf.h2("CRI - the number that decides whether colours look real")
pdf.body("CRI (Colour Rendering Index) measures how faithfully a light reveals colour. "
         "100 = sunlight. 80 = the cheap LED bulb you have at the office. 90+ = good. "
         "95+ = professional / gallery.")
pdf.bullet("All recessed COB downlights and cove strips in this house must be CRI >= 90.")
pdf.bullet("All accent / decorative fittings (where the light is the visual feature) "
           "should be CRI >= 95 if you can afford it.")
pdf.bullet("Kitchen task light: CRI >= 90, 4000K (food colour reads accurately).")
pdf.bullet("Bathroom mirror light: CRI >= 95, 4000K (skin / makeup needs accuracy).")

pdf.warning(
    "If a bulb does not state CRI on the box, assume it is below 80 -- skip it. "
    "Indian local-brand 'warm white' LED bulbs are often CRI 70 -- ivory walls go yellow-green, "
    "skin looks sickly, and travertine reads like cardboard. Check the box.")

pdf.h2("This house - by zone")
pdf.table(
    ["Zone", "Kelvin", "CRI min", "Why"],
    [
        ["Foyer / Living / Dining / Bedrooms / Pooja main", "2700K", "90+", "Premium warm mood, flatters teak + walnut + travertine."],
        ["Pooja niche backlight",  "2200K", "90+", "Amber / lamp-like - traditional feel."],
        ["Kitchen ceiling + task", "4000K", "90+", "Vegetables, spices, wet/dry food prep need real colour."],
        ["Bathroom mirror",        "4000K", "95+", "Skin tones, makeup, shaving accuracy."],
        ["Bathroom ceiling",       "3000K", "90+", "Slightly warmer than mirror - calms the room."],
        ["Study desk task",        "3000-4000K", "90+", "Reading focus without harshness."],
        ["Cove LEDs (everywhere they appear)", "2700K", "90+", "Soft halo - must match other warm fittings."],
        ["Outdoor / balconies",    "3000K", "80+", "Slightly cooler reads as 'outdoor' / awake."],
    ],
    [70, 30, 22, 60]
)

# ---------- 3. MAGNETIC COB TRACK ----------
pdf.add_page()
pdf.h1("3. Magnetic COB Track System -- the modular hero layer")

pdf.image_with_caption("magnetic_cob_living", max_h=80)

pdf.h2("Why this is worth fighting for")
pdf.body("A magnetic track is a slim aluminium channel (typically 20-35mm wide) that "
         "houses a 48V DC bus. Light modules - cylindrical COB spotlights, linear grazers, "
         "small pendants, floods - clip onto it magnetically. Once the track is in, you "
         "can move, swap, add, or remove fittings without touching the wiring or the "
         "ceiling again. You wanted the look -- you also get the future-proofing.")

pdf.h3("What you can mix on one track")
pdf.bullet("Cylindrical COB spotlight 6W / 12W / 18W - the small black cylinders, your "
           "core ask. Beam angles 24deg / 36deg / 60deg - choose narrower for accent, wider "
           "for ambient.")
pdf.bullet("Linear COB grazer 12W / 24W (300mm or 600mm long) - a bar of even, soft "
           "wash light. Beautiful for travertine / stone walls.")
pdf.bullet("Small pendant module 6W with a 200-400mm drop - decorative element on the same track.")
pdf.bullet("Magnetic flood / panel module 12-24W - if you want extra ambient.")
pdf.bullet("Magnetic grille light 9W - reduced glare for above dining or coffee zones.")

pdf.h2("Specs to insist on (do not compromise)")
pdf.table(
    ["Spec", "Recommended", "Why"],
    [
        ["Voltage",              "48V DC",          "Safe to touch. Standardised across all major brands."],
        ["Track width",          "20mm (slim)",     "Almost invisible in a gypsum false ceiling. 35mm reads chunky."],
        ["Mount type",           "RECESSED",        "Track sits flush with the ceiling face. Surface track is fine over a TV wall but reads more 'office'."],
        ["Track finish",         "Matte black",     "Disappears against gypsum shadow. Champagne / brass also OK if you prefer."],
        ["Driver",               "Mean Well or equivalent, 100W or 150W per track run", "Cheap drivers buzz when dimmed. Mean Well does not."],
        ["Module Kelvin",        "2700K (CRI >= 90)", "House standard."],
        ["Dimming",              "0-10V or DALI or Tuya/Zigbee smart-dimmable", "Must be dimmable. A track at 100% is rarely the right level."],
        ["Driver location",      "Above false ceiling, accessible via inspection hatch", "Drivers fail before LEDs. Plan for replacement."],
        ["Track run length",     "1-3m per zone",   "Longer runs sag and are harder to repair."],
    ],
    [38, 70, 74]
)

pdf.h2("Recessed vs surface vs suspended")
pdf.table(
    ["Mount", "Look",                 "Where in this house"],
    [
        ["Recessed",  "Flush with ceiling - track is invisible from below, only the modules read.",
            "Living TV-wall wash, FF Bedroom 2 above desk (preferred everywhere we have false ceiling)"],
        ["Surface",   "Sits on the ceiling face - reads like a slim black bar.",
            "Optional alternative for living wall wash if false ceiling depth is tight"],
        ["Suspended", "Drops on cables 300-600mm from slab - reads like a horizontal pendant.",
            "Could work over the dining table as a different look from the single pendant - optional"],
    ],
    [25, 70, 87]
)

pdf.h2("Where in this house we recommend installing magnetic track")
pdf.bullet("Living area, west wall TV / travertine zone - 2.5m recessed track with 2x cylindrical COB + 1x linear grazer + optional small pendant. Replaces the planned 'TV wall wash 2x GU10 + cove' line in the master spec for a cleaner, more flexible look.")
pdf.bullet("FF Bedroom 2 north wall (travertine + walnut shelf zone) - 1.5m recessed track over the height-adjustable desk. Two cylindrical COB spots aimed at the travertine, one linear grazer for even wash. This becomes the room's hero light.")
pdf.bullet("OPTIONAL: Foyer ledgestone wall - 1.2m recessed track instead of the 2x fixed GU10 spotlights. Same visual effect (stone grazing) but you can angle / re-aim later.")

pdf.h2("Brand options - magnetic track in India (May 2026)")
pdf.table(
    ["Tier", "Brand", "Notes", "Indicative price"],
    [
        ["Budget / OK", "Ankur Lighting (20mm)", "Decent build, wide module range, dealer in Bengaluru.", "Track ~Rs 500-700/foot. Modules Rs 700-1500 each."],
        ["Mid", "Arihant Star LED",     "Good Indian brand, 2-yr warranty, online + dealers.",  "Track ~Rs 700-950/foot. Modules Rs 900-1800."],
        ["Mid", "JSL Lights",           "Strong recessed channel range - MT-TR202 30mm.",       "Track ~Rs 600-900/foot. Modules Rs 800-1700."],
        ["Mid+", "Harold Electricals",  "Sold on Amazon.in - cylindrical COB spots are clean.", "Track ~Rs 800-1100/foot. Modules Rs 1000-2000."],
        ["Mid+", "Wipro / Crompton",    "Available through electrical dealers - slightly limited module range vs specialists.", "Track ~Rs 900-1200/foot. Modules Rs 1200-2200."],
        ["Premium", "Philips Magnetic Track", "Cleanest finish, best driver, in.shop.lighting.philips.com", "Track ~Rs 1100-1500/foot. Modules Rs 1500-2800."],
        ["Premium", "Belltrix (Mumbai distributor of imported lines)", "Imports + premium options. Get a sample first.", "Track Rs 1200-1800/foot. Modules Rs 1800-3500."],
    ],
    [16, 32, 80, 50]
)

pdf.callout("Recommendation",
    "For the living TV wall - go MID tier (Arihant Star or JSL). The fittings are visible "
    "and matter, but a Rs 50,000 Philips premium fitting is overkill on a 2.5m run. For "
    "FF Bedroom 2 above the desk - same call. Total magnetic-track budget across the "
    "house: Rs 35,000 - 50,000 if you stay mid tier. Rs 80,000 - 1.2L if you go premium.")

pdf.warning(
    "When ordering: ALWAYS order driver + track + modules from the SAME brand. "
    "Mixing brands across the bus voltage works in theory but the magnetic alignment "
    "is brand-specific - modules from brand A do not sit flat on brand B's track. "
    "Order the spare 1-2 modules at the same time -- if discontinued in 18 months you "
    "cannot replace them.")

# ---------- 4. WHOLE-HOUSE LIGHTING PLAN ----------
pdf.add_page()
pdf.h1("4. Whole-House Lighting Plan -- at a glance")

pdf.body("This is the bird's-eye summary. Detailed positions are in Section 6.")

pdf.h2("Ground floor")
pdf.table(
    ["Zone", "Ambient", "Task", "Accent", "Decorative"],
    [
        ["Foyer (false ceiling)",
         "2x recessed GU10 7W gimbal (stone grazing)",
         "-",
         "Cove + screen halo + shelf strip",
         "Walnut shelf with under-LED"],
        ["Living (false ceiling, double-height void)",
         "4x recessed COB 12W 2700K",
         "-",
         "**Magnetic COB track on TV wall** (2x cylinder + 1x linear) + cove",
         "Vertical cluster pendant in void (24-36in, brass)"],
        ["Dining (false ceiling)",
         "2x recessed COB 9W + cove",
         "-",
         "Cove perimeter",
         "Decorative pendant over table"],
        ["Kitchen (no false ceiling)",
         "1x LED panel 24W 4000K",
         "Under-cabinet 24V warm strip",
         "-",
         "-"],
        ["Master Bedroom (no false ceiling)",
         "Recessed COB 12W centre",
         "Wardrobe LED + bedside reading",
         "Headboard wall wash (optional)",
         "Bedside lamps with brass shade"],
        ["Pooja",
         "Soft warm 12W LED panel 2700K",
         "-",
         "Niche backlight 2200K",
         "-"],
        ["GF Bathroom",
         "1x IP44 9W 4000K (centre)",
         "Mirror bar 12W 4000K",
         "Niche 24V LED 3000K",
         "-"],
        ["Staircase",
         "Mid-flight wall light 5W + landing 9W",
         "-",
         "Step lights LED nosing",
         "-"],
    ],
    [40, 35, 30, 50, 33]
)

pdf.h2("First floor")
pdf.table(
    ["Zone", "Ambient", "Task", "Accent", "Decorative"],
    [
        ["FF Living + corridor",
         "2x recessed COB 12W (above stair head + corridor centre)",
         "-",
         "-",
         "AP wall plate stays clean (no decorative)"],
        ["FF Bedroom 1 (no false ceiling)",
         "Recessed COB 12W centre + 2x GU10 5W bedside",
         "Study spot 7W 3000K + wardrobe LED",
         "Headboard accent (optional)",
         "Bedside lamp"],
        ["FF Bedroom 2 (false ceiling)",
         "Recessed COB 12W + 2x GU10 5W bedside + cove",
         "**Magnetic COB track over desk** (2x cylinder + 1x linear) + walnut-shelf strips",
         "Travertine grazer (within track)",
         "Brass desk lamp + bedside walnut lamp"],
        ["Toilet 1 (BR1)",
         "IP44 9W 3000K",
         "Mirror bar 12W 4000K",
         "Niche LED 3000K",
         "-"],
        ["Toilet 2 (BR2)",
         "IP44 9W 3000K",
         "Mirror bar 12W 4000K",
         "Niche LED 3000K",
         "-"],
        ["Front Balcony",
         "1x IP65 9W 3000K",
         "-",
         "-",
         "-"],
        ["W Balcony",
         "1x IP65 7W 3000K",
         "-",
         "-",
         "-"],
    ],
    [40, 35, 30, 50, 33]
)

# ---------- 5. SMART CONTROL ----------
pdf.add_page()
pdf.h1("5. Smart Control + Dimming + Scenes")

pdf.body("Every light layer in this house is wired through a smart relay (Sonoff ZBMINI R2 "
         "or Aqara T1) sitting behind the modular switch plate. The switch box depth is "
         "65mm everywhere (NOT the standard 50mm) to fit the relay. This is locked in the "
         "electrical brief - do not let the electrician downsize the box.")

pdf.h2("Per-room scene set")
pdf.table(
    ["Room", "Scenes you should be able to call", "Why"],
    [
        ["Foyer",
         "ARRIVE (cove 60% + spots 80%) | NIGHT (cove 20% + shelf strip only)",
         "Welcome on entry; nightlight on motion"],
        ["Living + dining + void",
         "DAY (ambient 100% + cove off) | EVENING (ambient 40% + cove 60% + chandelier 70% + magnetic track 60%) | MOVIE (cove 20% + magnetic track on TV wall 30% + everything else off) | LATE NIGHT (cove 10%)",
         "The double-height void is your hero - the chandelier should be dimmable independently"],
        ["Master bedroom",
         "READ (one bedside lamp only) | WIND-DOWN (sconces 20% + wardrobe strip on) | SLEEP (all off, nightlight strip 5%)",
         "Couples sleeping on different schedules need independent bedside switching"],
        ["BR2 (work zone)",
         "WORK (track grazer 80% + shelf strip 100%) | RELAX (track 30% + cove 50%) | OFF",
         "Same room, two moods - the magnetic track was chosen to enable this"],
        ["Kitchen",
         "PREP (panel 100% + under-cabinet 100%) | WIND-DOWN (under-cabinet only)",
         "Late night water / snack does not need the full panel on"],
        ["Pooja",
         "ARATI (niche 100% + ambient 60%) | QUIET (niche only)",
         "Different ritual moments need different intensities"],
        ["Bathrooms",
         "PIR auto-on / 10-min auto-off",
         "No scenes needed - motion sensor handles it"],
    ],
    [38, 90, 50]
)

pdf.h2("Dimming - the right kind")
pdf.bullet("Cove LEDs (24V DC) - PWM dimmable via smart driver; smooth 1-100%.")
pdf.bullet("Recessed COB downlights - phase-cut TRIAC dimmable on the input side via smart relay; ensure the LED driver is marked 'TRIAC dimmable' on the box.")
pdf.bullet("Magnetic COB track - uses 0-10V or DALI dimmable driver; choose a driver compatible with your hub. Do NOT mix non-dimmable modules with a dimmable track - they buzz.")
pdf.bullet("Kitchen LED panel + bathroom IP44 fittings - typically NOT dimmed (pointless for task light).")

pdf.warning(
    "Dimmable LED still flickers if (a) the LED driver and the dimmer are not matched, "
    "(b) the load on a dimmer falls below its minimum (most TRIAC dimmers need >= 10% "
    "load = >= 10W on the circuit). If the cove LED on your bedroom flickers when dimmed "
    "below 30%, the issue is the driver / dimmer pairing, not the LED. Replace the driver, "
    "not the LED.")

# ---------- 6. FIXTURE SCHEDULE - room by room ----------
pdf.add_page()
pdf.h1("6. Fixture Schedule -- room by room")

pdf.body("Every position is given as (mm from named walls), measured from inside face of "
         "finished wall. Heights are from finished floor level (FFL). Cross-check against "
         "electrical/conduits-and-cavities.md PART 3 - which has the same numbers.")

# 6a Foyer
pdf.h2("6a. Foyer (6ft x 4ft9, false ceiling at 9ft)")
pdf.image_with_caption("foyer_grazing", max_h=70)
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["F1", "Recessed GU10 gimbal spot L", "7W 2700K CRI90 - 30deg gimbal trim", "300mm from W wall, 609mm from N wall", "FC 2743mm", "B1"],
        ["F2", "Recessed GU10 gimbal spot R", "7W 2700K CRI90 - 30deg gimbal trim", "300mm from W wall, 1218mm from N wall", "FC 2743mm", "B1"],
        ["F3", "Cove LED strip", "24V 2700K CRI90 9.6W/m", "Perimeter of false ceiling cove", "Inside cove reveal", "B10"],
        ["F4", "Walnut shelf under-LED strip", "24V 2700K CRI90 6W/m", "Under shelf, full 1828mm width", "900mm soffit", "B1"],
        ["F5", "Screen halo LED", "24V 2200K warm amber 4.8W/m", "Inside screen cavity reveal", "Cavity edge", "B2"],
    ],
    [10, 50, 40, 40, 25, 17]
)
pdf.callout("Optional upgrade",
    "If you have the budget: replace F1 + F2 with a 1.2m RECESSED MAGNETIC TRACK above the "
    "stone wall. Mount 2x cylindrical COB 6W spots + 1x linear grazer 12W on it. Same "
    "stone-grazing effect, but you can re-aim or swap modules later. Indicative cost addition "
    "vs the 2x GU10 spec: +Rs 6,000 - 9,000.")

pdf.add_page()
# 6b Living + void
pdf.h2("6b. Living + double-height void (16'11 x 16'11, false ceiling at 9ft)")
pdf.image_with_caption("magnetic_cob_living", max_h=72)
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["L1", "Recessed COB downlight", "12W 2700K CRI90 - fixed 60deg", "1200mm from W wall, 900mm from N wall", "FC 2743mm", "B3"],
        ["L2", "Recessed COB downlight", "12W 2700K CRI90 - fixed 60deg", "1200mm from W wall, 2700mm from N wall", "FC 2743mm", "B3"],
        ["L3", "Recessed COB downlight", "12W 2700K CRI90 - fixed 60deg", "2400mm from W wall, 900mm from N wall", "FC 2743mm", "B3"],
        ["L4", "Recessed COB downlight", "12W 2700K CRI90 - fixed 60deg", "2400mm from W wall, 2700mm from N wall", "FC 2743mm", "B3"],
        ["L5", "**Magnetic track** (TV wall)", "20mm matte black recessed 2.5m + 2x cylindrical COB 12W 2700K CRI90 + 1x linear grazer 12W 2700K + Mean Well 100W driver", "300mm from W wall, runs N-S parallel to wall", "FC 2743mm", "B3 (dimmer)"],
        ["L6", "Cove LED", "24V 2700K CRI90 9.6W/m", "Perimeter cove all 4 sides", "Inside cove", "B4"],
        ["L7", "**Vertical cluster pendant** (HERO)", "24-36in wide cluster, 10-12 cascading frosted-glass tubes, antique brass, 2700K CRI90 dimmable", "Centred over coffee-table area in void, terminus 2400mm above sunken floor", "Drop from FF beam (~5500mm)", "B3 (dimmer)"],
    ],
    [10, 55, 75, 50, 30, 22]
)
pdf.callout("Why magnetic track wins on the TV wall",
    "The original spec called for 2x recessed GU10 wall-washers. They work. But once "
    "the TV unit is built and the travertine cladding is up, the wall washers are fixed "
    "in position. If you ever change the TV size or shift the unit by 200mm, the wash is "
    "off-centre forever. With a magnetic track, you slide the modules to re-aim. Same "
    "look on day one, future-proof on day 1000.")
pdf.warning(
    "Confirm the void size + FF beam position BEFORE ordering the cluster pendant. The "
    "spec is for a 16'9\" x 11' void with the chandelier centred on the coffee-table area. "
    "If the beam is offset, the cascade lands wrong. Measure twice.")

pdf.add_page()
pdf.image_with_caption("double_height", max_h=120)

pdf.add_page()
# 6c Dining
pdf.h2("6c. Dining (false ceiling at 9ft)")
pdf.image_with_caption("dining_pendant", max_h=70)
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["D1", "Decorative pendant over table", "1x antique brass + frosted glass dome 24in dia, 2700K CRI90, 30W LED equiv, dimmable", "Centred over dining table position", "Drop to 2100mm FFL", "B6 (dimmer)"],
        ["D2", "Recessed COB downlight", "9W 2700K CRI90", "800mm from N wall, 600mm from E wall", "FC 2743mm", "B6"],
        ["D3", "Recessed COB downlight", "9W 2700K CRI90", "800mm from N wall, 600mm from W wall", "FC 2743mm", "B6"],
        ["D4", "Cove LED", "24V 2700K CRI90 9.6W/m", "Perimeter cove all 4 sides", "Inside cove", "B7 (dimmer)"],
    ],
    [10, 50, 60, 45, 25, 25]
)
pdf.body("Lighting math: a 6-seater table at 6ft x 3ft eats 1828mm x 914mm of floor. The "
         "single pendant should hang 750-900mm above the table top (so 2100mm FFL given "
         "table height ~750mm). Pendant width should be ~50-65% of the longer table edge - "
         "so a 24-30in (610-760mm) pendant is right. Anything wider visually overwhelms "
         "the table; anything narrower vanishes.")

# 6d Kitchen
pdf.h2("6d. Kitchen + utility (no false ceiling, GF 11ft)")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["K1", "LED ceiling panel", "24W 4000K CRI90 - square 600x600 surface mount", "Centred in kitchen", "Slab 3353mm", "A3"],
        ["K2", "Under-cabinet LED strip", "24V 2700K CRI90 9.6W/m + driver", "Underside of all wall cabinets, run continuous", "1700mm (cabinet soffit)", "A3"],
        ["K3", "Hob area downlight (optional)", "9W 4000K CRI90 - only if chimney has no light", "Above hob, 400mm from N wall", "Slab", "A3"],
        ["K4", "Utility ceiling light", "12W 4000K CRI90 surface batten", "Centred in utility", "Slab", "A3"],
        ["K5", "Store room ceiling light", "9W 4000K", "Centred", "Slab", "A3"],
    ],
    [10, 45, 60, 45, 30, 17]
)

pdf.add_page()
# 6e Pooja
pdf.h2("6e. Pooja (5x5)")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["P1", "Ambient LED panel", "12W 2700K CRI90 - round 200mm flush", "Centre ceiling", "Slab", "B8"],
        ["P2", "Niche backlight", "24V 2200K amber-warm CRI90 4.8W/m, hidden behind brass-leaf laminate", "Idol niche perimeter", "Inside niche", "B8 (dimmer)"],
    ],
    [10, 45, 60, 35, 30, 22]
)

# 6f Master Bedroom
pdf.h2("6f. Master Bedroom GF (11ft slab, no false ceiling)")
pdf.image_with_caption("bedroom_layered", max_h=70)
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["M1", "Recessed COB downlight (centre)", "12W 2700K CRI90", "Centred in room (final position locked after bed marking)", "Slab 3353mm", "C1"],
        ["M2", "Wall sconce L", "Brass arm + cream linen shade, E27 LED 6W 2700K CRI90", "E wall, 600mm N of bed centreline", "1400mm FFL", "C1"],
        ["M3", "Wall sconce R", "Same as M2", "E wall, 600mm S of bed centreline", "1400mm FFL", "C1"],
        ["M4", "Wardrobe LED strip", "24V 2700K 9.6W/m on door-actuated reed switch", "Inside top rail of S+W wardrobe", "Top rail", "C1"],
        ["M5", "Reading nook arc lamp", "Brushed brass arc floor lamp, E27 8W 2700K CRI90", "Plug-in on N wall middle - free-standing", "Floor lamp", "C2 socket"],
        ["M6", "Bedside lamp L", "Walnut + brushed brass shade, E27 6W 2700K CRI95 dimmable", "On L bedside table", "Table-top", "C2 socket"],
        ["M7", "Bedside lamp R", "Same as M6", "On R bedside table", "Table-top", "C2 socket"],
    ],
    [10, 45, 60, 50, 25, 22]
)

pdf.add_page()
# 6g Bathrooms
pdf.h2("6g. Bathrooms (3 total - GF + 2 FF)")
pdf.body("Bathrooms have NO false ceiling and NO 2700K. They are the only spaces in the "
         "house running cooler temperatures (3000K ambient, 4000K mirror).")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "IP rating"],
    [
        ["BG1", "GF Bath ceiling", "9W 4000K CRI90 IP44 recessed", "Centred ceiling", "3353mm slab", "IP44"],
        ["BG2", "GF Bath mirror bar", "12W 4000K CRI95 IP44 LED bar", "150mm above mirror top, centred over sink", "1900mm", "IP44"],
        ["BG3", "GF Bath niche LED", "24V 3000K IP65 9.6W/m", "Upper niche perimeter (south wall)", "Inside niche", "IP65"],
        ["BG4", "GF Bath exhaust fan", "4in IP44 100mm dia", "Above shower zone, NE corner", "2400mm", "IP44"],
        ["BT1.1", "Toilet 1 (BR1) ceiling", "9W 3000K CRI90 IP44", "Centred", "3048mm", "IP44"],
        ["BT1.2", "Toilet 1 mirror bar", "12W 4000K CRI95 IP44", "150mm above mirror, centred sink", "1900mm", "IP44"],
        ["BT1.3", "Toilet 1 niche LED", "24V 3000K IP65 4.8W/m", "Single niche shower zone", "Inside niche", "IP65"],
        ["BT1.4", "Toilet 1 exhaust", "4in IP44", "Shower corner", "2200mm", "IP44"],
        ["BT2.1", "Toilet 2 (BR2) ceiling", "9W 3000K CRI90 IP44", "Centred", "3048mm", "IP44"],
        ["BT2.2", "Toilet 2 mirror bar", "12W 4000K CRI95 IP44", "150mm above mirror, centred sink", "1900mm", "IP44"],
        ["BT2.3", "Toilet 2 niche LED", "24V 3000K IP65 4.8W/m", "Single niche shower zone", "Inside niche", "IP65"],
        ["BT2.4", "Toilet 2 exhaust", "4in IP44", "Shower corner", "2200mm", "IP44"],
    ],
    [12, 50, 55, 45, 22, 18]
)
pdf.warning(
    "IP44 minimum for any bathroom fitting outside the immediate shower zone. IP65 inside "
    "the shower or directly above niches that receive shower spray. PIR motion sensor on "
    "ALL bathroom lights with 10-minute auto-off. Geyser switches OUTSIDE the bathroom "
    "(20A DP, 1050mm FFL).")

# 6h Staircase
pdf.h2("6h. Staircase (22 risers GF + FF flight)")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height"],
    [
        ["S1", "Step nosing LED", "3W 2700K each riser, recessed in left wall (one side only)", "L side of every step", "Step level"],
        ["S2", "Mid-flight wall light", "Recessed 5W 2700K", "Mid-flight W wall", "1500mm"],
        ["S3", "Top landing light", "Recessed 9W 2700K", "FF landing centre ceiling", "3048mm"],
        ["S4", "Niche light", "Pull from staircase circuit, 5W 2700K", "Top of staircase niche", "Inside niche top"],
    ],
    [10, 45, 60, 55, 25]
)
pdf.callout("Wiring tip", "Step-nosing lights run on a single 24V driver in the staircase niche. "
            "Don't switch them - leave them on a dusk-to-dawn photocell or motion-on. They are "
            "essentially nightlights / safety lights.")

pdf.add_page()
# 6i FF Living
pdf.h2("6i. FF Living + corridor (ceiling height 10ft)")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["FL1", "Recessed COB downlight - stair head", "12W 2700K CRI90", "Above top stair landing", "Slab 3048mm", "D9"],
        ["FL2", "Recessed COB downlight - corridor centre", "12W 2700K CRI90", "Centred between BR1 + BR2 doors", "Slab 3048mm", "D9"],
        ["FL3", "Wall plate + AP power - keep area clean", "(no decorative light here)", "On the central FF Living wall (between BR1/BR2 doors), 2400mm FFL", "n/a", "n/a (router only)"],
    ],
    [10, 50, 50, 65, 30, 22]
)

# 6j FF Bedroom 1
pdf.h2("6j. FF Bedroom 1 (East, no false ceiling, 10ft slab)")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["B1.1", "Recessed COB downlight (centre)", "12W 2700K CRI90", "Centred", "Slab 3048mm", "D1"],
        ["B1.2", "Recessed adjustable GU10 - bedside L", "5W 2700K CRI90 - 30deg gimbal", "600mm from L bed edge", "Slab, angled toward pillow zone", "D1"],
        ["B1.3", "Recessed adjustable GU10 - bedside R", "5W 2700K CRI90 - 30deg gimbal", "600mm from R bed edge", "Slab, angled toward pillow zone", "D1"],
        ["B1.4", "Study spotlight", "Recessed GU10 7W 3000K CRI90", "400mm from study-table wall, above table", "Slab", "D1"],
        ["B1.5", "Wardrobe LED strip", "24V 2700K 9.6W/m on door-actuated reed switch", "Top rail of wardrobe", "Top rail", "D1"],
        ["B1.6", "Bedside lamp", "E27 6W 2700K CRI95 + brass shade", "On L or R bedside table", "Table-top", "D2 socket"],
    ],
    [12, 55, 60, 45, 30, 22]
)

# 6k FF Bedroom 2
pdf.h2("6k. FF Bedroom 2 (West - false ceiling at 9ft, 10ft slab) -- magnetic track room")
pdf.image_with_caption("br2_track_study", max_h=70)
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["B2.1", "Recessed COB downlight (centre)", "12W 2700K CRI90", "Centred", "FC 2743mm", "D5"],
        ["B2.2", "Recessed adjustable GU10 - bedside L", "5W 2700K CRI90 - gimbal", "600mm from L bed edge", "FC angled", "D5"],
        ["B2.3", "Recessed adjustable GU10 - bedside R", "5W 2700K CRI90 - gimbal", "600mm from R bed edge", "FC angled", "D5"],
        ["B2.4", "**MAGNETIC TRACK over desk** (HERO)", "20mm matte black recessed 1.5m + 2x cylindrical COB 12W 2700K CRI90 (24deg) + 1x linear grazer 12W 2700K + Mean Well 60W driver, 0-10V dimmable", "Above 4ft desk on N wall - centred over desk top, 200mm offset toward travertine", "FC 2743mm", "D5 (dimmer)"],
        ["B2.5", "Walnut shelf under-LED strip", "24V 2700K CRI90 6W/m", "Under each of 2 floating shelves", "Shelf soffit", "D5"],
        ["B2.6", "Cove LED", "24V 2700K CRI90 9.6W/m", "Perimeter false ceiling cove", "Inside cove", "D11 (smart dimmer)"],
        ["B2.7", "Wardrobe LED strip", "24V 2700K 9.6W/m on reed switch", "Top rail W-wall wardrobe", "Top rail", "D5"],
        ["B2.8", "Brass desk lamp", "E27 6W 2700K CRI95 dimmable + brass shade", "Plug-in on desk top", "Desk top", "D6 socket"],
    ],
    [12, 50, 70, 45, 25, 22]
)

pdf.callout("Why this room earns the magnetic track",
    "BR2 has the locked travertine N wall - the most expensive surface in the house. "
    "A static fixture lights it once. A magnetic track lets you tune the wash on day 1 "
    "and re-tune it after the desk arrives, after the chair arrives, after you've lived "
    "with it for a month. The grazer reveals the travertine veins; the spots mark "
    "specific zones. Both on, dim independently.")

pdf.add_page()
# 6l Balconies + outdoor
pdf.h2("6l. Balconies + outdoor")
pdf.table(
    ["#", "Fitting", "Spec", "Position", "Height", "Circuit"],
    [
        ["O1", "Front balcony wall light", "9W 3000K IP65 - cylindrical wall mount in matte black", "Inner balcony wall, near door", "2200mm", "D10"],
        ["O2", "W balcony wall light", "7W 3000K IP65 - same family", "Inner wall", "2200mm", "D10"],
        ["O3", "Compound / porch overview light", "12W 4000K IP65 - canopy mount", "Porch ceiling", "2700mm", "GF outdoor"],
        ["O4", "Step lights (front porch, optional)", "3W 3000K IP65 recessed", "If you have steps in/out", "Step level", "GF outdoor"],
    ],
    [10, 45, 60, 50, 25, 22]
)
pdf.warning(
    "All outdoor fittings IP65 minimum. Use UV-stable PVC conduit for the last 500mm "
    "outdoors. Brass / champagne brass outdoor fittings will tarnish in monsoon - matte "
    "black or dark bronze powder coat is more honest for the climate. The inside hardware "
    "(door hardware) stays brushed gold; outside, matte black.")

# ---------- 7. BRANDS ----------
pdf.add_page()
pdf.h1("7. Brands -- good / better / best")

pdf.body("Indian market for LED downlights, cove strips, and modular fittings has matured. "
         "You can hit good results on the budget tier; the premium tier is mostly about driver "
         "quality, finish consistency, and 5-year warranty. Note - decorative / pendant brands "
         "(international) are listed separately because the market is different.")

pdf.h2("Recessed COB downlights / GU10 spots / Cove LED strip")
pdf.table(
    ["Tier", "Brand", "Strengths", "Where to source"],
    [
        ["Budget", "Halonix / Eveready / Bajaj", "Local availability, low price, decent CRI 80+",
         "Local electrical store - Chitradurga"],
        ["Mid",    "Wipro / Crompton / Polycab", "CRI 90, longer warranty (3-5 yr), driver quality",
         "Authorised dealer Chitradurga / Bengaluru"],
        ["Mid",    "Syska / Orient",             "Solid mid-tier, dimmable variants stocked",
         "Online (Amazon.in) + dealers"],
        ["Mid+",   "Havells",                    "Premium-feeling at mid price, better trims",
         "Bengaluru showroom, Amazon.in"],
        ["Premium", "Philips Hue / Philips Coreline", "Smart hub native, App control, premium driver",
         "Philips lighting online India + Bengaluru showroom"],
        ["Premium", "Wipro Garnet (commercial)",  "Office-grade COB, very flat beam",
         "Wipro Lighting authorised distributor"],
        ["Custom",  "Local fabrication (Bengaluru)", "For oddly sized cove channel or non-standard trim",
         "Discuss with interior contractor"],
    ],
    [16, 32, 70, 60]
)

pdf.h2("Magnetic Track System (covered in detail in Section 3)")
pdf.body("Re-stating the recommendation here: for this house go MID tier - either "
         "Arihant Star LED, JSL Lights, or Harold Electricals. Avoid the cheapest no-brand "
         "Amazon listings; the magnetic alignment is poor and the driver buzzes when dimmed.")

pdf.h2("Decorative pendants (chandelier, dining pendant, sconces)")
pdf.table(
    ["Tier", "Brand / Source", "Notes"],
    [
        ["Budget", "Pepperfry, Wooden Street, Urban Ladder",
         "Wide brass + pendant range. Quality varies - read reviews. Returnable."],
        ["Mid",    "Whispering Homes / Anemos / Hashtag Decor",
         "Specialised decorative-lighting brands. Better quality control."],
        ["Mid",    "Fabindia / The Home Hub / Address Home",
         "For India-flavoured decorative pieces (brass, terracotta accents)."],
        ["Mid+",   "FOS Lighting (Mumbai)",
         "Curated import + Indian design. Good for the void cluster pendant."],
        ["Premium", "Klove / Sage Living / Studio Wood",
         "Bespoke lighting. The cluster pendant could be commissioned here."],
        ["International", "Flos, Tom Dixon, Vibia, Articolo (via Bengaluru showrooms)",
         "Premium - typically 1-3L for a hero pendant. Mention if budget allows."],
    ],
    [16, 50, 100]
)

# ---------- 8. WHERE TO BUY ----------
pdf.add_page()
pdf.h1("8. Where to Buy -- vendors + links")

pdf.h2("Online (mid-tier, fast delivery)")
pdf.table(
    ["Vendor", "Best for", "Link / contact"],
    [
        ["Amazon.in",                 "Recessed COB, GU10 spots, magnetic track entry, decorative",
         "amazon.in - search 'magnetic track light 48V'"],
        ["Philips Lighting India",    "Coreline downlights, Hue smart, magnetic track premium",
         "in.shop.lighting.philips.com"],
        ["Wipro Consumer Lighting",   "Garnet downlights, modular panels",
         "wiproconsumerlighting.com"],
        ["Arihant Star LED",          "Mid-tier magnetic track + modules",
         "arihantstarled.com"],
        ["JSL Lights",                "Recessed magnetic track channel + spots",
         "jsllights.com"],
        ["Ankur Lighting",            "20mm magnetic track + decorative",
         "ankurlighting.com"],
        ["Harold Electricals",        "Cylindrical COB modules, premium-look modules",
         "haroldelectricals.com OR Amazon.in (Harold)"],
        ["Belltrix India",            "Imported / premium magnetic + decorative (Mumbai)",
         "belltrixindia.in"],
        ["Pepperfry / Wooden Street", "Decorative pendants + sconces + table lamps",
         "pepperfry.com / woodenstreet.com"],
    ],
    [40, 60, 80]
)

pdf.h2("Offline (Bengaluru)")
pdf.bullet("Brigade Road / Lighting Plaza - cluster of lighting showrooms; useful to see Philips, Havells, Wipro, decorative brands side by side. Allow 2 hrs.")
pdf.bullet("Stone Studio / Sleek Kitchens (Indiranagar) - usually have one or two magnetic track demos in the kitchen lighting section.")
pdf.bullet("FOS Lighting (online but Mumbai-based) - request samples of decorative pieces; their service handles all-India.")
pdf.bullet("Local high-end interior store (Sadashivanagar / Whitefield) - often has bespoke brass fixtures from Klove / Sage Living; ask for the lighting consultant.")

pdf.h2("Offline (Chitradurga - day-to-day fittings)")
pdf.bullet("Local Schneider / Legrand authorised dealer - modular switch plates + a few branded LEDs.")
pdf.bullet("Local Asian Paints colour studio - they often carry a basic decorative-pendant catalogue too (limited but useful for emergency).")
pdf.bullet("Get the magnetic track + premium decorative pendants delivered from Bengaluru / online - Chitradurga retail won't carry it.")

pdf.callout("Negotiation tip",
    "When buying through a Bengaluru showroom, ask for 'project price' (not retail). On a "
    "Rs 2-3 lakh whole-house lighting order you should see 15-25% off MRP, especially if you "
    "buy bulbs + cove + magnetic in one go. They will also throw in basic installation guidance.")

# ---------- 9. WATTAGE / CIRCUIT SUMMARY ----------
pdf.add_page()
pdf.h1("9. Wattage + Circuit Summary")

pdf.body("This is the engineer's view - total connected lighting load per circuit. "
         "Cross-references electrical/circuits-and-load.md for full circuit IDs.")

pdf.h2("Per-circuit lighting load")
pdf.table(
    ["Circuit", "Zone", "Fixtures", "Total W", "MCB"],
    [
        ["B1", "Foyer lights",                 "2x GU10 7W + shelf strip 11W + screen halo 7W", "39 W", "6A"],
        ["B10", "Foyer cove",                  "Cove LED 4m x 9.6 W/m",                          "38 W", "6A"],
        ["B3", "Living main + magnetic track", "4x COB 12W + magnetic track ~36W (2x12W cyl + 12W linear)", "84 W", "6A"],
        ["B4", "Living cove",                  "Cove LED ~12m x 9.6 W/m",                        "115 W", "6A"],
        ["B6", "Dining lights + pendant",      "2x COB 9W + pendant 30W LED equiv (12W actual)", "30 W", "6A"],
        ["B7", "Dining cove",                  "Cove LED ~10m x 9.6 W/m",                        "96 W", "6A"],
        ["A3", "Kitchen + utility",            "1x panel 24W + utility 12W + store 9W + under-cabinet ~36W", "81 W", "6A"],
        ["B8", "Pooja",                        "1x panel 12W + niche backlight ~10W",            "22 W", "6A"],
        ["C1", "Master bedroom lights",        "1x COB 12W + 2x sconce 6W + wardrobe ~24W",      "48 W", "6A"],
        ["A1", "GF Bath",                      "1x 9W + mirror 12W + niche 10W + exhaust 25W",   "56 W", "6A"],
        ["D5", "BR2 lights + magnetic track",  "1x COB 12W + 2x GU10 5W + track ~36W + shelf ~12W + wardrobe ~24W", "99 W", "6A"],
        ["D11", "BR2 cove",                    "Cove LED ~10m x 9.6 W/m",                        "96 W", "6A"],
        ["D1", "BR1 lights",                   "1x COB 12W + 2x GU10 5W + study 7W + wardrobe ~24W", "53 W", "6A"],
        ["D3", "T1 lights",                    "1x 9W + mirror 12W + niche ~5W + exhaust 25W",   "51 W", "6A"],
        ["D7", "T2 lights",                    "Same as T1",                                     "51 W", "6A"],
        ["D9", "FF Living + corridor",         "2x COB 12W",                                     "24 W", "6A"],
        ["D10", "Balconies",                   "1x 9W + 1x 7W + step lights ~6W",                "22 W", "6A"],
    ],
    [16, 50, 80, 22, 16]
)

pdf.body("Whole-house lighting connected load: ~1.0 - 1.2 kW. Diversified (real-world "
         "concurrent) load: ~600 - 750 W. This is well within the 6A MCB rating per "
         "circuit (1380 W theoretical) and within the GF + FF main DB capacity.")

# ---------- 10. DECORATIVE FIXTURES ----------
pdf.add_page()
pdf.h1("10. Decorative Fixtures -- the hero pieces")

pdf.body("Three pieces will visually carry the house. Get them right and the house has a "
         "soul. Get them wrong and even the magnetic track and travertine wall can't save it.")

pdf.h2("10.1 The void cluster pendant (HERO)")
pdf.image_with_caption("double_height", max_h=85)
pdf.table(
    ["Spec", "Value"],
    [
        ["Style", "Vertical cluster - 10 to 14 cascading slender stems (varying lengths)"],
        ["Width", "24 - 36 inches (610 - 914mm) at the canopy"],
        ["Drop",  "From FF beam (~5500mm above sunken floor) terminating ~2400mm above floor - so total cascade drop ~3100mm"],
        ["Bulbs", "10 - 14 frosted glass tube bulbs OR small spheres, E14 base, 4W LED 2700K CRI95 each"],
        ["Material / finish", "Antique brass OR champagne brass canopy + stems"],
        ["Dimming", "Yes - the chandelier MUST be on its own dimmer (B3 sub-channel)"],
        ["Budget pick (Rs 12-25k)", "Pepperfry / Wooden Street 'Cascade' or 'Rain' style cluster"],
        ["Mid pick (Rs 30-60k)",   "FOS Lighting / Whispering Homes brass cluster"],
        ["Premium pick (Rs 1-2L)", "Klove (Bengaluru), Studio Wood, Articolo (international, via Bengaluru showroom)"],
    ],
    [50, 130]
)

pdf.h2("10.2 The dining pendant")
pdf.image_with_caption("dining_pendant", max_h=70)
pdf.table(
    ["Spec", "Value"],
    [
        ["Style", "Single dome OR 3-globe linear OR drum"],
        ["Diameter", "24 - 30 inches (610 - 760mm) - approximately 50-65% of long table edge"],
        ["Drop", "To 2100mm FFL (table top is at 750mm; pendant base ~900mm above table)"],
        ["Bulbs", "1x E27 LED 12W 2700K CRI90 dimmable OR 3x 4W"],
        ["Material", "Antique brass + frosted glass diffuser"],
        ["Budget (Rs 4-10k)", "Amazon.in / Pepperfry"],
        ["Mid (Rs 12-25k)",   "Anemos, Whispering Homes"],
        ["Premium (Rs 40k+)", "Klove, FOS Lighting"],
    ],
    [50, 130]
)

pdf.h2("10.3 The bedside lamps (master + BR1 + BR2)")
pdf.table(
    ["Spec", "Value"],
    [
        ["Style", "Walnut wood base + brushed brass shade OR cream linen drum"],
        ["Height", "16 - 22 inches"],
        ["Bulb",  "E27 LED 6W 2700K CRI95 dimmable"],
        ["Switch", "Pull-cord OR touch-base (Aqara / Sonoff Zigbee bulb works inside any lamp = makes it smart)"],
        ["Quantity", "5 (2x master, 1-2 BR1, 1-2 BR2)"],
        ["Budget pick", "Pepperfry walnut + brass set ~Rs 2,500/each"],
        ["Mid pick",    "Whispering Homes / Hashtag Decor ~Rs 4,500-7,000/each"],
        ["Premium",    "Custom turning by local carpenter + brass shade ~Rs 8,000-12,000/each"],
    ],
    [50, 130]
)

# ---------- 11. BUY LIST ----------
pdf.add_page()
pdf.h1("11. Buy List (printable)")

pdf.body("This is the master shopping list for the entire house lighting. "
         "Quantities have been totalled across rooms. SKU-level pick is the recommended mid-tier; "
         "swap up or down depending on budget.")

pdf.h2("Recessed downlights / spots / cove (functional)")
pdf.table(
    ["Item", "Spec", "Qty", "Indicative unit price (Rs)", "Subtotal (Rs)"],
    [
        ["Recessed COB downlight 12W", "2700K CRI90 dimmable - 90mm cut-out - Wipro/Havells", "12", "850", "10,200"],
        ["Recessed COB downlight 9W",  "2700K CRI90 - 75mm cut-out - same brand",            "5",  "650", "3,250"],
        ["Recessed GU10 gimbal trim",  "Champagne / matte black trim - same brand",          "10", "350", "3,500"],
        ["GU10 LED bulb",              "5W or 7W 2700K CRI90 dimmable (for gimbals)",        "12", "200", "2,400"],
        ["Recessed IP44 9W",           "3000K-4000K (bathroom ceiling)",                     "3",  "650", "1,950"],
        ["Mirror LED bar 12W",         "4000K CRI95 IP44 - bathroom",                        "3",  "1,200", "3,600"],
        ["LED ceiling panel 24W",      "4000K CRI90 - kitchen",                              "1",  "1,800", "1,800"],
        ["LED batten 12W",             "4000K - utility / store / pooja replacement",        "2",  "550", "1,100"],
        ["LED panel 12W round",        "2700K CRI90 - pooja",                                "1",  "950", "950"],
        ["Wall sconce - master bedroom","Brass + cream linen + E27",                          "2",  "3,500", "7,000"],
        ["Wall light - mid-stair",     "Recessed 5W 2700K",                                  "1",  "1,200", "1,200"],
        ["Step nosing LED",            "3W IP65 each riser",                                 "22", "350", "7,700"],
        ["Outdoor wall light IP65 9W", "Matte black 3000K",                                  "2",  "1,400", "2,800"],
        ["Outdoor canopy IP65 12W",    "Matte black 4000K",                                  "1",  "2,200", "2,200"],
    ],
    [55, 65, 12, 32, 22]
)

pdf.h2("Cove LED strip + drivers")
pdf.table(
    ["Item", "Spec", "Qty", "Indicative unit (Rs)", "Subtotal (Rs)"],
    [
        ["24V LED strip", "2700K CRI90 9.6 W/m IP20 (foyer + living + dining + BR2)", "30 m", "320/m", "9,600"],
        ["24V LED strip", "2700K CRI90 6 W/m (under-shelf foyer + BR2)",              "5 m",  "260/m", "1,300"],
        ["24V LED strip IP65", "3000K (bathroom niches)",                              "3 m",  "420/m", "1,260"],
        ["24V LED strip", "2200K (pooja niche)",                                       "1 m",  "380/m", "380"],
        ["Mean Well 24V driver 60W",  "Per zone",                                       "5",   "1,800", "9,000"],
        ["Mean Well 24V driver 100W", "Living + BR2",                                   "2",   "2,800", "5,600"],
        ["Aluminium cove channel",    "Diffuser + clip + end caps",                     "30 m","180/m", "5,400"],
        ["Smart Zigbee dimmer (Sonoff/Aqara) for cove zones", "Per zone",               "5",   "1,300", "6,500"],
    ],
    [60, 75, 14, 25, 22]
)

pdf.h2("Magnetic COB track system")
pdf.table(
    ["Item", "Spec", "Qty", "Indicative unit (Rs)", "Subtotal (Rs)"],
    [
        ["Magnetic track 20mm recessed", "Matte black 1m sections - Arihant Star or JSL", "5 m total (2.5m living + 1.5m BR2 + 1m foyer optional)", "850/m", "4,250"],
        ["Magnetic cylindrical COB spot 12W", "2700K CRI90 24deg - matte black",        "5",  "1,400", "7,000"],
        ["Magnetic linear COB grazer 12W (300mm)", "2700K CRI90",                       "2",  "1,800", "3,600"],
        ["Magnetic small pendant module 6W", "2700K CRI90 frosted glass",                "1",  "1,600", "1,600"],
        ["Mean Well 48V 100W driver",     "For living track",                            "1",  "3,200", "3,200"],
        ["Mean Well 48V 60W driver",      "For BR2 track",                               "1",  "2,400", "2,400"],
        ["Mean Well 48V 60W driver",      "For foyer track (optional)",                  "1",  "2,400", "2,400"],
        ["Track end caps + connectors",   "Per run",                                     "6",  "200",  "1,200"],
    ],
    [55, 65, 32, 25, 22]
)

pdf.h2("Decorative (the eye candy)")
pdf.table(
    ["Item", "Spec", "Qty", "Indicative unit (Rs)", "Subtotal (Rs)"],
    [
        ["Vertical cluster pendant - void", "Brass, 30in cluster, 12 frosted tubes - mid tier", "1", "45,000", "45,000"],
        ["Decorative pendant - dining",     "Brass + frosted dome, 24in",                       "1", "12,000", "12,000"],
        ["Floor lamp - living (brass arc)", "5-6ft arc with brass shade",                       "1", "8,500", "8,500"],
        ["Floor lamp - master BR nook",     "Brass arc, 5ft",                                   "1", "7,500", "7,500"],
        ["Bedside lamp - walnut + brass",   "Pair (master)",                                    "2", "3,500", "7,000"],
        ["Bedside lamp - BR1",              "Single",                                           "1", "3,500", "3,500"],
        ["Bedside lamp - BR2",              "Single",                                           "1", "3,500", "3,500"],
        ["Brass desk lamp - BR2",           "Articulated arm, brass shade",                     "1", "4,500", "4,500"],
    ],
    [60, 70, 14, 25, 22]
)

pdf.h2("Smart relays + accessories (already partially in the electrical brief)")
pdf.table(
    ["Item", "Spec", "Qty", "Indicative unit (Rs)", "Subtotal (Rs)"],
    [
        ["Sonoff ZBMINI R2 Zigbee relay", "1-channel - behind every smart switch",        "20", "750", "15,000"],
        ["Aqara Hub M3 / equivalent",     "Zigbee gateway",                                "1",  "5,500", "5,500"],
        ["Door-actuated reed switch + relay", "For each wardrobe LED strip",               "5",  "350", "1,750"],
        ["PIR motion sensor (bathrooms)",  "10-min timer auto-off",                        "3",  "850", "2,550"],
    ],
    [55, 70, 12, 25, 22]
)

pdf.callout("Indicative whole-house lighting budget",
    "Functional fittings (downlights / spots / cove / panels + drivers + step lights + outdoor): "
    "Rs ~70,000 - 90,000.\n"
    "Magnetic COB track full set (3 zones, mid-tier): Rs ~25,000 - 30,000.\n"
    "Decorative (chandelier + pendants + lamps): Rs ~85,000 - 1,15,000 (mid tier; halve for "
    "budget, double for premium).\n"
    "Smart relays + sensors + hub: Rs ~25,000.\n"
    "Total mid-tier budget: Rs ~2,10,000 - 2,60,000 (excluding labour).\n"
    "Add labour / installation: ~Rs 35,000 - 50,000.")

# ---------- 12. INSTALLATION CHECKLIST ----------
pdf.add_page()
pdf.h1("12. Installation Checklist")

pdf.body("In sequence. Tick as each is signed off.")

pdf.h2("Before plastering (electrician phase)")
checklist_pre = [
    "All ceiling boxes for recessed COB cut at exact positions per Section 6 - confirmed against floor plan",
    "Magnetic-track conduit chase + driver-box position marked above false ceiling at all 3 magnetic-track zones (Living TV wall, BR2 desk, optional Foyer)",
    "Cove channel chase prepared at all cove perimeter positions - foyer / living / dining / BR2",
    "Cove LED driver boxes positioned in inspection-hatch reach - one per cove zone",
    "Wall sconce boxes (master bedroom E wall) at 1400mm FFL, 600mm N + S of bed centreline",
    "Stair step-nosing channel cut into the L wall of staircase, 22 risers in GF flight",
    "Door-actuated reed switch position drilled into all wardrobe carcasses (wardrobe-strip control)",
    "Bathroom IP44 ceiling boxes + IP44 mirror-bar position marked + niche LED strip channel cut",
    "All switch-board boxes confirmed as 65mm depth (NOT 50mm) for Sonoff relay compatibility",
    "Neutral wire pulled to every smart-switch box (no exceptions)",
]
for item in checklist_pre:
    pdf.bullet("[ ] " + item, size=10)
pdf.ln(1)

pdf.h2("After plastering / before false ceiling close-up")
checklist_mid = [
    "Cove LED + driver wired and tested - every zone working before gypsum boards close the cove",
    "Magnetic track driver wired and tested (with one module attached) before false ceiling closes",
    "Recessed downlight cut-outs aligned to plan - verify after gypsum board is up but before painting",
    "Wardrobe LED strip + reed switch tested with the wardrobe shutter - door open = on, door closed = off",
    "Step-nosing LED + 24V driver in staircase niche tested",
    "Bathroom PIR motion sensor + 10-min auto-off tested",
    "Smart relays installed in every smart-switch box; relays configured into hub; switch labelled in app",
]
for item in checklist_mid:
    pdf.bullet("[ ] " + item, size=10)
pdf.ln(1)

pdf.h2("Decorative + commissioning")
checklist_post = [
    "Vertical cluster pendant in void - install AFTER painting + cleaning, NOT before",
    "Dining pendant - install after dining table is on site (so drop is correct)",
    "Wall sconces in master bedroom - install after bed is positioned (so flanking distance is correct)",
    "Bedside lamps - place after bedside tables in",
    "Brass desk lamp - place after BR2 desk is in",
    "Brass arc floor lamps - place after sofa + reading nook chair are in",
    "All scenes programmed in the smart hub (per Section 5 table)",
    "Walk every room at three times of day - dawn, noon, dusk - and one night session. Tune scene levels.",
    "Hand the homeowner a 1-page 'how to use the lighting' cheat sheet (scenes + voice commands)",
]
for item in checklist_post:
    pdf.bullet("[ ] " + item, size=10)

# ---------- 13. THINGS TO AVOID ----------
pdf.add_page()
pdf.h1("13. Things to AVOID")

pdf.body("Mistakes that look fine on day 1 and look wrong forever. Cheaper to skip than fix.")

pdf.bullet("**Cool white (5000K-6500K) bulbs anywhere except outdoors.** Even the cheapest "
           "Indian electrician will offer 'cool daylight' as default - say no. The whole house "
           "is 2700K. Mixing one cool bulb in a warm room ruins the mood.")
pdf.bullet("**False ceilings with too many recessed downlights.** Looks like an airport. "
           "Use the spacing from Section 6 - typically 1.5m between downlights, not 0.8m.")
pdf.bullet("**Surface-mount tube lights or 'jhumar' chandeliers in the living area.** Either "
           "the recessed downlight + cove + cluster pendant OR fully traditional - never mixed.")
pdf.bullet("**Decorative pendants in places without ceiling height.** A pendant needs 2200mm "
           "minimum below it. Master bedroom (no false ceiling, 11ft slab) is fine; a 9ft "
           "false ceiling room is the bare minimum. NEVER hang a pendant in a 8ft bathroom.")
pdf.bullet("**Mixed kelvin within one zone.** If one bulb in the dining is 2700K and the next "
           "is 3000K, the eye notices instantly. Insist on identical Kelvin from identical "
           "supplier per zone.")
pdf.bullet("**Cheap LED 'panel' lights with a thin plastic diffuser.** They yellow in 18 months "
           "and the colour shifts. Pay 30% more for an aluminium-housing panel.")
pdf.bullet("**Magnetic track from no-name sellers on Amazon.** The bus voltage may be wrong, "
           "the magnets weak, the modules wobble. Stick to named brands listed in Section 7.")
pdf.bullet("**Skipping CRI on the box.** If the box does not list CRI, the LED is below 80. "
           "Skin and food look wrong under it.")
pdf.bullet("**Forgetting that LED drivers fail.** They live above the false ceiling - design "
           "an inspection hatch from day 1 (300x300mm minimum) at every driver location. "
           "Without it, replacing a Rs 1,800 driver in 3 years means tearing out gypsum "
           "(Rs 8,000 of damage to fix Rs 1,800 of part).")
pdf.bullet("**Forgetting outdoor IP rating.** A 'normal' indoor wall light on the balcony "
           "lasts ~6 months in monsoon. Use IP65 minimum, always.")
pdf.bullet("**Switching everything off the same scene.** Every layer must be independently "
           "controllable. If you can't dim the cove without dimming the pendant, you have "
           "wasted half the value of the layered scheme.")

pdf.callout("If you only remember three things",
    "(1) 2700K everywhere except kitchen + bathrooms.\n"
    "(2) CRI 90+ on every fitting that is visible.\n"
    "(3) Every layer on its own dimmer.\n"
    "Get those three right and the rest can be average without anyone noticing.")

# ---------- BACK ----------
pdf.add_page()
pdf.set_y(60)
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(80, 50, 20)
pdf.cell(0, 10, "End of Whole-House Lighting Brief", ln=1, align="C")
pdf.ln(3)
pdf.set_font("Helvetica", "I", 11)
pdf.set_text_color(120, 90, 50)
pdf.multi_cell(0, 6,
    "v1.0 - 2026-05-10. This document is intended to be read together with:",
    align="C")
pdf.ln(2)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(40, 40, 40)
for line in [
    "interior-design/master-interior-spec.md  (whole-house style + finishes)",
    "electrical/conduits-and-cavities.md  (PART 3 - exact lighting positions)",
    "electrical/db-layout.md  (DB + circuits)",
    "electrical/circuits-and-load.md  (load calc)",
    "materials-finishes/master-color-palette.md  (paint + tile palette)",
]:
    pdf.set_x(40)
    pdf.cell(0, 6, "- " + line, ln=1)

pdf.ln(8)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(120, 100, 70)
pdf.multi_cell(0, 5,
    "All AI-generated reference photographs in this document are for mood + fitting-type "
    "communication only. They are not site photos. Final fittings must be verified physically "
    "in showroom samples before bulk order.", align="C")

pdf.output(str(OUT))
print(f"WROTE: {OUT}  (pages: {pdf.page_no()})")
