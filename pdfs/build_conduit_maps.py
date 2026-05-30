"""
Build CONDUIT_MAPS.pdf - visual conduit overlays on floor plans for the electrician.

Why this file exists:
  Earlier text-heavy electrician PDFs (ELECTRICIAN_REFERENCE, FOYER_ELECTRICIAN_MASTER_PLAN)
  were ignored on site - too much reading. This is the visual replacement: each conduit
  drawn as a coloured line directly on the AutoCAD floor plan, with a numbered legend.

Layout:
  A3 landscape, one sheet per service per floor.
  Left ~55% of sheet = AutoCAD floor plan + coloured conduit overlay + numbered callouts
  Right ~45%        = title block, colour-code legend, conduit cheat sheet, critical notes

Sheets:
  GF-01  Ground Floor   Light Power (RED 25mm)
  GF-02  Ground Floor   Heavy Power (BLUE 25mm) - sockets, AC, geyser, hob
  GF-03  Ground Floor   Data / Cat6 (ORANGE = real PVC grey, schematic orange for visibility)
  GF-04  Ground Floor   Low-Voltage 16mm (PURPLE) - cove/halo/shelf LED, sensors
  GF-05  Ground Floor   Water Automation (GREEN)
  FF-01  First Floor    Power + Data combined
  RISER  Vertical X-section through staircase wall (GF -> FF -> terrace)

Source-of-truth markdown:
  electrical/conduits-and-cavities.md
  electrical/FOYER_MASTER_ELECTRICIAN_PLAN.md
  electrical/water-automation-conduits.md (or PART 0.7 of conduits-and-cavities.md)

Run: python3 build_conduit_maps.py
"""
from fpdf import FPDF
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT  = Path(__file__).parent / "CONDUIT_MAPS.pdf"
GF_IMG = ROOT / "floor-plans" / "ground-floor-autocad.png"
FF_IMG = ROOT / "floor-plans" / "first-floor-autocad.png"

# ---------- Editorial palette (matches existing PDFs) ----------
INK        = ( 28,  28,  30)
INK_SOFT   = ( 90,  90,  95)
INK_FAINT  = (140, 140, 145)
PAPER      = (255, 255, 255)
RULE       = (220, 215, 205)

# Conduit colour code
C_POWER_LIGHT = (220,  30,  30)   # RED    - 25mm light power
C_POWER_HEAVY = ( 30,  90, 220)   # BLUE   - 25mm heavy power (sockets/AC/geyser)
C_DATA        = (235, 110,  20)   # ORANGE - 25mm LV-25 Cat6 (real PVC grey; orange for visibility)
C_LV16        = (140,  90, 200)   # PURPLE - 16mm LV-16 (speaker, halo, doorbell)
C_WATER       = ( 30, 140, 100)   # GREEN  - water automation

# ---------- Page geometry ----------
PAGE_W, PAGE_H = 420, 297   # A3 landscape, mm

GF_PLAN_X, GF_PLAN_Y = 10, 25
GF_PLAN_W, GF_PLAN_H = 220, 260
GF_IMG_W,  GF_IMG_H  = 1022, 1304

FF_PLAN_X, FF_PLAN_Y = 10, 25
FF_PLAN_W, FF_PLAN_H = 220, 258
FF_IMG_W,  FF_IMG_H  = 1176, 1382


def gf_px_to_mm(px_x, px_y):
    return (GF_PLAN_X + px_x * (GF_PLAN_W / GF_IMG_W),
            GF_PLAN_Y + px_y * (GF_PLAN_H / GF_IMG_H))


def ff_px_to_mm(px_x, px_y):
    return (FF_PLAN_X + px_x * (FF_PLAN_W / FF_IMG_W),
            FF_PLAN_Y + px_y * (FF_PLAN_H / FF_IMG_H))


# ---------- Landmarks (pixel coords on the AutoCAD raster) ----------
# Orientation: TOP=S, BOTTOM=N (main door), LEFT=E, RIGHT=W

GF = {
    # Foyer + entry
    "db":               (115, 1090),
    "foyer_switch_pnl": (260, 1160),
    "cavity":           (245,  955),
    "main_door_out":    (160, 1200),
    "porch_ceiling":    (105, 1255),
    "porch_wall":       (105, 1150),

    # Staircase + data hub
    "niche":            (370, 1010),
    "ws_staircase":     (560,  945),
    "riser_to_ff":      (780,  720),

    # Dining
    "ws_dining":        (240,  550),
    "dining_speaker":   (215,  610),
    "dining_pendant":   (240,  580),

    # Kitchen / utility
    "cam4_kitchen_e":   ( 95,  240),
    "kitchen_ceiling":  (270,  220),
    "kitchen_counter":  (250,  170),    # counter sockets (~1100mm FFL on N wall)
    "kitchen_hob":      (140,  165),
    "kitchen_chimney":  (180,  150),
    "kitchen_sink":     ( 95,  280),
    "utility_socket":   ( 95,  160),
    "fridge_niche":     ( 95,  445),
    "utility_light":    (150,  130),

    # Living
    "tv_wall":          (950, 1000),
    "living_ceil_1":    (820,  960),
    "living_ceil_2":    (820, 1140),
    "living_ceil_3":    (700,  960),
    "living_ceil_4":    (700, 1140),
    "living_socket_1":  (950, 1180),
    "living_socket_2":  (820, 1240),
    "chandelier_void":  (660,  450),     # roughly above GF Living's centre, hanging into FF void
    "living_cove":      (810, 1100),

    # Master bedroom
    "mbr_ceiling":      (700,  290),
    "mbr_bedside_n":    (790,  240),
    "mbr_bedside_s":    (790,  340),
    "mbr_ac":           (650,  395),     # N wall above door
    "mbr_wardrobe_s":   (730,  170),     # S wall wardrobe driver
    "mbr_wardrobe_w":   (840,  290),     # W wall wardrobe tail
    "mbr_dressing":     (840,  370),

    # Common bathroom + geyser
    "gf_bath_ceiling":  (520,  470),
    "gf_bath_geyser":   (520,  390),
    "gf_bath_pir":      (450,  470),     # PIR switch outside door

    # Pooja
    "pooja_ceiling":    (190,  830),

    # Staircase landing + niche light
    "staircase_ceil":   (660,  650),
    "niche_light":      (340,  960),     # niche internal light

    # Water automation
    "terrace_sintex":   (820,  120),     # rough projection of terrace SW parapet
    "sump_jb":          ( 95,  720),     # E external wall above manhole
    "db_cupboard":      (155, 1080),     # adjacent to DB (E wall foyer)
    "borewell_head":    ( 95,  900),     # outside east wall
    "p2_cage":          ( 95,  640),     # east outside wall P2 cage
}

FF = {
    "riser_from_gf":    (655,  790),
    "ff_living_ap":     (520,  610),
    "br1_study":        (775,  450),
    "br2_study":        (340,  450),
    "br1_ceil":         (770,  340),
    "br2_ceil":         (390,  340),
    "br1_bedside_l":    (700,  300),
    "br1_bedside_r":    (840,  300),
    "br2_bedside_l":    (320,  300),
    "br2_bedside_r":    (460,  300),
    "br1_ac":           (820,  240),
    "br2_ac":           (370,  240),
    "t1_ceil":          (790,  170),     # toilet 1 ceiling
    "t1_geyser":        (840,  200),
    "t2_ceil":          (380,  170),     # toilet 2 ceiling
    "t2_geyser":        (320,  200),
    "ff_living_ceil":   (550,  760),
    "ff_balcony":       (250,  900),     # FF balcony lower left
    "front_balcony_nw": (210, 1110),     # CAM-3 outside
    "ff_riser_terrace": (700,  300),     # bundle continuing up to terrace
}


# ---------- Hub markers (rectangles drawn ON the floor plan as origin/destination cues) ----------

NICHE_BOX  = (340, 985, 60, 50)         # px (x, y, w, h)
DB_BOX     = ( 88, 1065, 60, 50)
DB_CUP_BOX = ( 90, 1130, 60, 35)        # DB cupboard adjacent to DB (water automation)
RISER_BOX_FF = (635, 770, 50, 40)       # Riser arrival hub on FF


# ---------- Niche exit ports (already used by GF-03) ----------

PORT = {
    "to_cavity":   (340, 992),
    "to_doorbell":  (340, 1010),
    "to_cam1":     (340, 1020),
    "to_cam2":     (350, 1035),
    "to_stair":    (400, 998),
    "to_ff_riser": (400, 1015),
    "to_dining":   (385, 985),
    "to_speaker":  (370, 985),
    "to_cam4":     (355, 985),
}

# DB exit ports (for power conduits)
DB_PORT = {
    "to_foyer_switch": (148, 1075),  # E edge of DB, upper - goes up to false ceiling then to switch panel
    "to_cavity":       (148, 1085),  # E edge of DB, middle - to cavity power
    "to_living":       (148, 1095),  # E edge, lower - to living wall
    "to_living_sock":  (148, 1105),
    "to_kitchen":      (118, 1065),  # N edge - up to kitchen
    "to_dining":       (105, 1075),
    "to_mbr":          (148, 1075),  # going up E wall to MBR (combined with foyer_switch routing)
    "to_bath":         (140, 1065),  # up to bath
    "to_riser":        (148, 1115),  # to FF riser (right of DB)
    "to_cupboard":     (115, 1115),  # to DB cupboard for water automation
}


# ============================================================================
# CONDUIT DEFINITIONS (one list per sheet)
# ============================================================================
#
# Each conduit dict has:
#   ref         : prefixed callout (e.g. "D3", "P1", "H5", "L2", "W1", "F1") - electrician says "P-three"
#   id          : full ID from conduits-and-cavities.md (for cross-reference)
#   colour      : line colour (one of the C_* constants)
#   size        : "25mm" / "16mm" / "20mm" etc.
#   status      : "live" (pull cable now) or "provision" (pull string only, capped)
#   route       : list of (px_x, px_y) waypoints in image pixel coords
#   contents    : what cables go inside (1-line)
#   from_to     : short human summary for the cheat sheet
#   dest_label  : short label drawn next to the destination circle on the floor plan
#   note        : optional gotcha for the electrician

# ----- GF-01: LIGHT POWER (RED 25mm) -----
# Lighting circuits originating at DB. Switch panels are intermediate stops.

GF_LIGHT_CONDUITS = [
    {
        "ref": "P1", "id": "C-DB-Foyer-Switch",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_foyer_switch"], (148, 1075), (148, 1160), GF["foyer_switch_pnl"]],
        "contents": "1.5sqmm L + N + E (feeds 6-gang foyer panel; powers all foyer + porch lighting)",
        "from_to": "DB -> foyer switch panel (N wall, 18M Schneider Unica, 1200mm FFL)",
        "dest_label": "FOYER SW PANEL",
        "note": "65mm-deep GI MS box. NEUTRAL must reach the panel - no exceptions.",
    },
    {
        "ref": "P2", "id": "C-SW-Spots",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (260, 1100), (260, 1050), (300, 1050)],
        "contents": "Switched live from Gang 1 + N + E",
        "from_to": "Switch panel -> 2x foyer ceiling GU10 spotlights",
        "dest_label": "FOYER SPOTS",
        "note": "GU10 7W 2700K, adjustable gimbals to angle 30deg toward stone wall.",
    },
    {
        "ref": "P3", "id": "C-SW-Cove-Halo",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (260, 1100), (260, 1010), (260, 970), (280, 970)],
        "contents": "Switched live Gang 2 + N + E (powers cove driver + halo driver)",
        "from_to": "Switch panel -> false ceiling cove driver + halo driver above cavity",
        "dest_label": "COVE + HALO",
        "note": "Both drivers above false ceiling. Halo wraps cavity top, cove wraps foyer perimeter.",
    },
    {
        "ref": "P4", "id": "C-SW-Shelf",
        "colour": C_POWER_LIGHT, "size": "16mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (260, 1120), (300, 1120), (300, 980)],
        "contents": "Switched live Gang 3 + N + E (powers walnut shelf 24V driver)",
        "from_to": "Switch panel -> walnut shelf underneath, S wall of foyer",
        "dest_label": "SHELF LED",
        "note": "Floor route preferred for the wire (avoids extra ceiling penetration).",
    },
    {
        "ref": "P5", "id": "C-SW-Porch-Ceiling",
        "colour": C_POWER_LIGHT, "size": "16mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (260, 1180), (180, 1220), (130, 1240)],
        "contents": "Switched live Gang 5 + N + E",
        "from_to": "Switch panel -> outside porch ceiling light",
        "dest_label": "PORCH CEILING",
        "note": "Through N wall to porch. Outdoor IP44 fitting required.",
    },
    {
        "ref": "P6", "id": "B3-Living-Main",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living"], (148, 1050), (700, 1050), (700, 960)],
        "contents": "1.5sqmm L + N + E (4-way splits at false ceiling JB)",
        "from_to": "DB -> Living false ceiling, 4x recessed COB ceiling boxes (12W 2700K)",
        "dest_label": "LIVING 4x CEIL",
        "note": "Avoid the FF cut-out void area. Stay in solid-slab zone (left/west).",
    },
    {
        "ref": "P7", "id": "B-Chandelier",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living"], (148, 800), (300, 600), (500, 500), GF["chandelier_void"]],
        "contents": "1.5sqmm L + N + E (single drop for chandelier)",
        "from_to": "DB -> vertical up W wall -> FF beam -> ceiling rose box at void centre",
        "dest_label": "CHANDELIER",
        "note": "Terminate at ceiling rose box on FF beam level. Chandelier hangs into double-height void.",
    },
    {
        "ref": "P8", "id": "A3-Kitchen-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_kitchen"], (118, 800), (240, 600), (240, 240), GF["kitchen_ceiling"]],
        "contents": "1.5sqmm L + N + E (kitchen ceiling + utility light branch)",
        "from_to": "DB -> kitchen ceiling box + utility light",
        "dest_label": "KITCHEN CEIL",
        "note": "Cool/neutral 4000K panel for task area. Utility light branched from this run.",
    },
    {
        "ref": "P9", "id": "Dining-Pendant",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_dining"], (105, 800), (200, 580), GF["dining_pendant"]],
        "contents": "1.5sqmm L + N + E (pendant + 2x downlights via JB)",
        "from_to": "DB -> dining pendant centre + 2x supplementary downlights",
        "dest_label": "DINING PENDANT",
        "note": "Pendant drop to 2100mm FFL above dining table. Confirm table position first.",
    },
    {
        "ref": "P10", "id": "C1-MBR-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_mbr"], (148, 800), (550, 500), (700, 350), GF["mbr_ceiling"]],
        "contents": "1.5sqmm L + N + E (ceiling + bedside L + bedside R + wardrobe driver)",
        "from_to": "DB -> MBR ceiling + 2x bedside (E wall) + S/W wardrobe LED driver",
        "dest_label": "MBR LIGHTS",
        "note": "Centre on bed once headboard line is marked. Bedside sconces flank headboard.",
    },
    {
        "ref": "P11", "id": "A1-GFBath-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_bath"], (148, 700), (400, 500), GF["gf_bath_ceiling"]],
        "contents": "1.5sqmm L + N + E (ceiling + mirror + exhaust + PIR switch)",
        "from_to": "DB -> bathroom ceiling + mirror light + exhaust + PIR outside door",
        "dest_label": "BATH LIGHTS",
        "note": "PIR switch outside door, W side, 1200mm FFL. Geyser switch BELOW PIR at 1050mm.",
    },
    {
        "ref": "P12", "id": "Pooja-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living"], (148, 900), (190, 900), GF["pooja_ceiling"]],
        "contents": "1.5sqmm L + N + E (Pooja spotlights + strip)",
        "from_to": "DB -> Pooja ceiling (spots + decorative strip)",
        "dest_label": "POOJA",
        "note": "Spot lights + strip lights as per the markup on AutoCAD. Confirm fixture spec on-site.",
    },
    {
        "ref": "P13", "id": "Staircase-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living"], (148, 950), (500, 950), GF["staircase_ceil"]],
        "contents": "1.5sqmm L + N + E (step lights + mid-flight wall light + landing)",
        "from_to": "DB -> step lights + mid-flight wall light + niche light + landing",
        "dest_label": "STAIRS",
        "note": "Step lights (3W each) on each riser left side. 2-way switch at top + bottom.",
    },
]

# ----- GF-02: HEAVY POWER (BLUE 25mm) -----

GF_HEAVY_CONDUITS = [
    {
        "ref": "H1", "id": "C-DB-Cavity-Power",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_cavity"], (148, 1050), (200, 1010), (245, 1010), (245, 980)],
        "contents": "2.5sqmm L + N + E (230V to cavity 2x 5A sockets; Sonoff Mini R2 switches Monitor)",
        "from_to": "DB -> foyer screen cavity (back wall, bottom-LEFT)",
        "dest_label": "CAVITY POWER",
        "note": "Cavity socket panel = 2-module on cavity BACK wall, centre 53in / 1346mm FFL.",
    },
    {
        "ref": "H2", "id": "B5-Living-TV",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living_sock"], (148, 1180), (700, 1180), GF["tv_wall"]],
        "contents": "2.5sqmm L + N + E - 3 boxes: 16A socket + double 5A + Cat6 keystone",
        "from_to": "DB -> TV wall (W wall of Living) - 3 boxes at 300mm FFL",
        "dest_label": "TV CLUSTER",
        "note": "All 3 boxes at same height. Keep Cat6 keystone box 150mm from power boxes (interference).",
    },
    {
        "ref": "H3", "id": "B5-Living-Perimeter",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_living_sock"], (148, 1240), (820, 1240)],
        "contents": "2.5sqmm L + N + E - skirting-level run to perimeter sockets at 300mm FFL",
        "from_to": "DB -> Living perimeter sockets (multiple boxes around the room)",
        "dest_label": "LIVING SOCKETS",
        "note": "Min 150mm from corners. Skirting-level chase.",
    },
    {
        "ref": "H4", "id": "A4-Kitchen-Counter",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_kitchen"], (118, 800), (200, 250), (200, 170), GF["kitchen_counter"]],
        "contents": "2.5sqmm L + N + E - 4x counter sockets (5A + 16A combo)",
        "from_to": "DB -> kitchen counter wall - 4x boxes at 1100mm FFL",
        "dest_label": "KITCHEN SOCKETS",
        "note": "Above counter level, behind backsplash position. Confirm with kitchen designer for tile cutout.",
    },
    {
        "ref": "H5", "id": "A5-Chimney",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_kitchen"], (118, 700), (180, 300), GF["kitchen_chimney"]],
        "contents": "2.5sqmm L + N + E (chimney 16A socket)",
        "from_to": "DB -> chimney socket above hob at 1900mm FFL",
        "dest_label": "CHIMNEY",
        "note": "Centre over hob position. 16A socket.",
    },
    {
        "ref": "H6", "id": "A6-Hob",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_kitchen"], (118, 900), (140, 300), GF["kitchen_hob"]],
        "contents": "4sqmm L + N + E (25A hob direct hardwire)",
        "from_to": "DB -> hob position at 150mm FFL (floor screed route)",
        "dest_label": "HOB",
        "note": "DIRECT hardwire (no socket). 25A MCB. Conduit emerges from floor at hob centreline.",
    },
    {
        "ref": "H7", "id": "A8-Fridge",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_kitchen"], (118, 600), (100, 460), GF["fridge_niche"]],
        "contents": "2.5sqmm L + N + E (16A fridge socket)",
        "from_to": "DB -> fridge niche socket at 300mm FFL",
        "dest_label": "FRIDGE",
        "note": "Inside fridge niche - confirm height after fridge model is picked.",
    },
    {
        "ref": "H8", "id": "C2-MBR-Sockets",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_mbr"], (148, 700), (550, 500), (700, 350), GF["mbr_bedside_n"]],
        "contents": "2.5sqmm L + N + E (2x bedside double 5A + utility sockets)",
        "from_to": "DB -> MBR bedside boxes (E wall) at 600mm FFL + utility",
        "dest_label": "MBR SOCKETS",
        "note": "Bedside sockets at 600mm FFL on E wall, flanking the headboard.",
    },
    {
        "ref": "H9", "id": "E3-MBR-AC",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_mbr"], (148, 600), (400, 450), GF["mbr_ac"]],
        "contents": "4sqmm L + N + E (20A AC socket)",
        "from_to": "DB -> MBR AC socket at 1850mm FFL on N wall above door",
        "dest_label": "MBR AC",
        "note": "RCBO protection. Confirm AC manual for socket position above outdoor unit side.",
    },
    {
        "ref": "H10", "id": "A2-GFBath-Geyser",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [DB_PORT["to_bath"], (148, 700), (400, 500), GF["gf_bath_geyser"]],
        "contents": "2.5sqmm L + N + E (20A geyser circuit)",
        "from_to": "DB -> geyser outlet at 1850mm FFL inside bathroom",
        "dest_label": "BATH GEYSER",
        "note": "20A RCBO. Geyser SWITCH (DP) outside door at 1050mm FFL (below PIR).",
    },
]

# ----- GF-03: DATA / CAT6 (ORANGE) -----  (already defined in earlier draft, kept compatible)

GF_DATA_CONDUITS = [
    {
        "ref": "D1", "id": "C-Niche-Cavity-Data",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_cavity"], (245, 992), GF["cavity"]],
        "contents": "1x indoor Cat6 (UTP)",
        "from_to": "Niche -> foyer screen cavity (back wall, bottom-RIGHT)",
        "dest_label": "CAVITY (Cat6)",
        "note": "FLOOR route under screed (NOT ceiling). ~12m. Drops Cat6 to RPi behind the foyer monitor.",
    },
    {
        "ref": "D2", "id": "C-Niche-Doorbell",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_doorbell"], (260, 1010), (260, 1180), GF["main_door_out"]],
        "contents": "1x outdoor LSZH UV-rated Cat6 (PoE)",
        "from_to": "Niche -> main-door outside face (Hikvision DS-KV6113-WPE1(C) Video Doorbell PoE)",
        "dest_label": "DOORBELL",
        "note": "Floor route preferred. Doorbell at 1450mm FFL, latch side.",
    },
    {
        "ref": "D3", "id": "C-Niche-CAM1",
        "colour": C_DATA, "size": "25mm", "status": "provision",
        "route": [PORT["to_cam1"], (220, 1020), (220, 1100), GF["porch_wall"]],
        "contents": "PULL STRING ONLY - capped IP67 back-box at porch W wall, 1650mm FFL",
        "from_to": "Niche -> porch W wall (future face-detection camera)",
        "dest_label": "CAM-1 (future)",
        "note": "DROPPED from base install (2026-05-20) - Hikvision doorbell handles face capture.",
    },
    {
        "ref": "D4", "id": "C-Niche-CAM2",
        "colour": C_DATA, "size": "25mm", "status": "provision",
        "route": [PORT["to_cam2"], (200, 1035), (200, 1255), GF["porch_ceiling"]],
        "contents": "PULL STRING ONLY - capped IP67 back-box at porch ceiling NE corner",
        "from_to": "Niche -> porch ceiling (future overview camera, 2700mm FFL)",
        "dest_label": "CAM-2 (future)",
        "note": "False-ceiling route only - soffit not reachable via floor.",
    },
    {
        "ref": "D5", "id": "C-Niche-Waveshare-Stair",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_stair"], (560, 998), GF["ws_staircase"]],
        "contents": "1x HDMI 2.0 (3m) + 1x USB-A->micro-USB (3m) + existing Cat6 spare",
        "from_to": "Niche -> staircase S wall, 1500mm FFL (Waveshare 10.1in panel)",
        "dest_label": "STAIR SCREEN",
        "note": "CUSTOM 280x195x80mm masonry cavity (not modular box). ~200mm above existing 2M switch.",
    },
    {
        "ref": "D6", "id": "C-Niche-Dining",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_dining"], (385, 700), (240, 700), GF["ws_dining"]],
        "contents": "1x indoor Cat6 + 1x pull string",
        "from_to": "Niche -> dining E wall (Waveshare dining panel)",
        "dest_label": "DINING SCREEN",
        "note": "~12m / 35-40ft. Pi-at-screen pattern (foyer-style). Position TBD by interior designer.",
    },
    {
        "ref": "D7", "id": "C-Niche-DiningSpeaker",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_speaker"], (370, 750), (215, 750), GF["dining_speaker"]],
        "contents": "1x indoor Cat6 (PoE-capable) + 1x pull string",
        "from_to": "Niche -> ceiling JB above future dining table (mono speaker)",
        "dest_label": "DINING SPKR",
        "note": "Ceiling JB centred over future dining table. Foyer-pattern Pi + PAM8403 + 3in ceiling speaker.",
    },
    {
        "ref": "D8", "id": "C-Niche-CAM4",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [PORT["to_cam4"], (355, 400), (95, 400), GF["cam4_kitchen_e"]],
        "contents": "1x outdoor LSZH UV Cat6 (PoE) + draw wire",
        "from_to": "Niche -> E-wall exterior at kitchen-utility junction, 2400-2600mm FFL",
        "dest_label": "CAM-4 (E ext)",
        "note": "Horizontal run 150mm below GF slab soffit. Confirm whether utility has external door.",
    },
    {
        "ref": "D9", "id": "C-Niche -> FF riser",
        "colour": C_DATA, "size": "25mm x 3", "status": "live",
        "route": [PORT["to_ff_riser"], (780, 1015), GF["riser_to_ff"]],
        "contents": "3x LV-25 conduits up staircase W wall: (a) R-FF-1 2x Cat6, (b) R-FF-2 1x Cat6, (c) R-FF-3 1x Cat6. CAM-3+CAM-5 continue further up.",
        "from_to": "Niche -> vertical rise in staircase W wall -> FF (see FF-01 sheet)",
        "dest_label": "FF RISER (3x)",
        "note": "Dedicated 150mm-wide chase channel. See FF-01 sheet for terminations above.",
    },
]

# ----- GF-04: LOW-VOLTAGE 16mm (PURPLE) -----

GF_LV16_CONDUITS = [
    {
        "ref": "L1", "id": "FSP -> Cove Driver",
        "colour": C_LV16, "size": "16mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (260, 1100), (260, 1020), (300, 1010)],
        "contents": "24V DC 2-core to cove driver (driver inside false ceiling perimeter)",
        "from_to": "Switch panel -> cove LED driver in false ceiling",
        "dest_label": "COVE DRIVER",
        "note": "Driver sits in false ceiling perimeter. Accessible via inspection hatch.",
    },
    {
        "ref": "L2", "id": "FSP -> Halo Driver",
        "colour": C_LV16, "size": "16mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (270, 1080), (270, 960), GF["cavity"]],
        "contents": "24V DC 2-core to halo driver above cavity",
        "from_to": "Switch panel -> halo driver above false ceiling, near cavity top",
        "dest_label": "HALO DRIVER",
        "note": "Halo strip wraps cavity reveal. Amber 2200K. Driver in false ceiling above cavity.",
    },
    {
        "ref": "L3", "id": "FSP -> Shelf Driver",
        "colour": C_LV16, "size": "16mm", "status": "live",
        "route": [GF["foyer_switch_pnl"], (280, 1130), (340, 970), (310, 970)],
        "contents": "24V DC 2-core to walnut shelf 24V driver",
        "from_to": "Switch panel -> shelf LED driver under walnut shelf",
        "dest_label": "SHELF DRIVER",
        "note": "Shelf strip 6W/m, warm white. Driver under shelf carcass.",
    },
    {
        "ref": "L4", "id": "Cavity-Top -> FC speaker provision",
        "colour": C_LV16, "size": "16mm", "status": "provision",
        "route": [(280, 970), (280, 900), (280, 800)],
        "contents": "PULL STRING ONLY - future ceiling speaker in foyer false ceiling",
        "from_to": "Cavity TOP wall -> false ceiling above (future ceiling speaker)",
        "dest_label": "FC SPKR (future)",
        "note": "Conduit exits cavity TOP inner wall going up into false ceiling. Pull string only.",
    },
    {
        "ref": "L5", "id": "Door contact sensor",
        "colour": C_LV16, "size": "16mm", "status": "provision",
        "route": [PORT["to_doorbell"], (220, 1010), (220, 1170), (160, 1180)],
        "contents": "PULL STRING ONLY - future concealed door contact sensor at top of frame",
        "from_to": "Niche -> main door frame TOP (door contact sensor)",
        "dest_label": "DOOR CONTACT",
        "note": "Concealed sensor at top of main door frame. Future provision, no cable now.",
    },
    {
        "ref": "L6", "id": "MBR Wardrobe S driver",
        "colour": C_LV16, "size": "16mm", "status": "live",
        "route": [GF["mbr_ceiling"], (700, 230), GF["mbr_wardrobe_s"]],
        "contents": "24V DC 2-core to wardrobe S-wall LED strip driver",
        "from_to": "MBR ceiling JB -> S-wall wardrobe top rail LED driver",
        "dest_label": "MBR WARDROBE S",
        "note": "Door-activated sensor on each wardrobe leaf.",
    },
    {
        "ref": "L7", "id": "MBR Wardrobe W tail driver",
        "colour": C_LV16, "size": "16mm", "status": "live",
        "route": [GF["mbr_ceiling"], (770, 290), GF["mbr_wardrobe_w"]],
        "contents": "24V DC 2-core to wardrobe W-wall tail LED driver",
        "from_to": "MBR ceiling JB -> W-wall wardrobe tail LED driver",
        "dest_label": "MBR WARDROBE W",
        "note": "Tail of L-shaped wardrobe; door-activated sensor.",
    },
]

# ----- GF-05: WATER AUTOMATION (GREEN) -----

GF_WATER_CONDUITS = [
    {
        "ref": "W1", "id": "C-Sintex-1",
        "colour": C_WATER, "size": "20mm", "status": "live",
        "route": [GF["niche"], (450, 950), (650, 850), (780, 720), (820, 200), GF["terrace_sintex"]],
        "contents": "1x outdoor LSZH Cat6 (PoE for Sintex water-level sensor)",
        "from_to": "Niche -> staircase shaft -> terrace SW parapet Sintex JB (~42ft)",
        "dest_label": "SINTEX JB",
        "note": "Embedded under terrace screed BEFORE tiling. IP65 JB 200x200x100mm at SW parapet.",
    },
    {
        "ref": "W2", "id": "C-Sintex-2",
        "colour": C_WATER, "size": "16mm", "status": "live",
        "route": [GF["niche"], (440, 940), (640, 840), (770, 710), (810, 190), (810, 130)],
        "contents": "2-core 1.5mm2 double-insulated (Sintex float failsafe to DB cupboard)",
        "from_to": "Niche -> terrace Sintex float -> DB cupboard (~45ft)",
        "dest_label": "SINTEX FLOAT",
        "note": "Parallel to W1, MIN 50mm separation. Terminates at float terminal block in DB cupboard.",
    },
    {
        "ref": "W3", "id": "C-Sump-1",
        "colour": C_WATER, "size": "20mm", "status": "live",
        "route": [GF["niche"], (350, 950), (200, 900), (130, 800), GF["sump_jb"]],
        "contents": "1x outdoor LSZH Cat6 (PoE for sump water-level sensor)",
        "from_to": "Niche -> E external wall above manhole, sump JB (~25ft)",
        "dest_label": "SUMP JB",
        "note": "Sleeve through E wall, slope outward to prevent water ingress.",
    },
    {
        "ref": "W4", "id": "C-Sump-2",
        "colour": C_WATER, "size": "16mm", "status": "live",
        "route": [GF["niche"], (350, 940), (200, 890), (130, 790), (115, 720)],
        "contents": "2-core 1.5mm2 (sump float failsafe to DB cupboard)",
        "from_to": "Niche -> sump float -> DB cupboard (~25ft)",
        "dest_label": "SUMP FLOAT",
        "note": "Parallel to W3, MIN 50mm separation.",
    },
    {
        "ref": "W5", "id": "C-DB-Backup",
        "colour": C_WATER, "size": "20mm", "status": "provision",
        "route": [GF["niche"], (300, 1050), (200, 1090), GF["db_cupboard"]],
        "contents": "PULL STRING ONLY - future Cat6 backup link (water automation)",
        "from_to": "Niche -> DB cupboard (~12ft)",
        "dest_label": "BACKUP LINK",
        "note": "Both ends capped + labelled WATER AUTOMATION - FUTURE Cat6.",
    },
    {
        "ref": "W6", "id": "C-Motor-P1",
        "colour": C_WATER, "size": "25mm", "status": "live",
        "route": [GF["db_cupboard"], (130, 1000), (100, 900), GF["borewell_head"]],
        "contents": "4sqmm armoured (P1 borewell motor power, 16A Type C)",
        "from_to": "DB cupboard -> borewell head outside (confirm existing run can be repurposed)",
        "dest_label": "P1 BOREWELL",
        "note": "P1 starter sits in DB cupboard. CONFIRM existing conduit can carry new 4sqmm.",
    },
    {
        "ref": "W7", "id": "C-Motor-P2",
        "colour": C_WATER, "size": "25mm", "status": "live",
        "route": [GF["db_cupboard"], (130, 900), (100, 700), GF["p2_cage"]],
        "contents": "2.5sqmm PVC (P2 booster pump power, 16A Type C)",
        "from_to": "DB cupboard -> P2 cage east outside wall (~5ft)",
        "dest_label": "P2 BOOSTER",
        "note": "P2 starter inside DB cupboard. Cage = lockable outdoor enclosure on east wall.",
    },
]

# ----- FF-01: First Floor Combined (Power + Data) -----

FF_CONDUITS = [
    # Power circuits arrive from GF riser (FF["riser_from_gf"]) and fan out:
    {
        "ref": "F1", "id": "D5-BR2-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (550, 600), (400, 400), FF["br2_ceil"]],
        "contents": "1.5sqmm L + N + E (BR2 ceiling + cove + bedside spots + wardrobe driver)",
        "from_to": "Riser -> BR2 ceiling (centred) + cove + bedsides + wardrobe driver",
        "dest_label": "BR2 LIGHTS",
        "note": "Centre on bed once headboard line is marked.",
    },
    {
        "ref": "F2", "id": "D6-BR2-Sockets",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (500, 700), (350, 450), FF["br2_bedside_l"]],
        "contents": "2.5sqmm L + N + E (bedside L + bedside R + study sockets)",
        "from_to": "Riser -> BR2 bedside + study sockets at 600mm FFL",
        "dest_label": "BR2 SOCKETS",
    },
    {
        "ref": "F3", "id": "E5-BR2-AC",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (500, 600), (380, 350), FF["br2_ac"]],
        "contents": "4sqmm L + N + E (20A AC socket)",
        "from_to": "Riser -> BR2 AC socket at 1850mm FFL",
        "dest_label": "BR2 AC",
    },
    {
        "ref": "F4", "id": "D8-T2-Geyser",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (480, 500), (350, 300), FF["t2_geyser"]],
        "contents": "2.5sqmm L + N + E (20A geyser; switch outside door 1200mm FFL)",
        "from_to": "Riser -> T2 geyser outlet 1850mm FFL + DP switch outside door",
        "dest_label": "T2 GEYSER",
    },
    {
        "ref": "F5", "id": "D1-BR1-Lights",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (700, 600), (770, 450), FF["br1_ceil"]],
        "contents": "1.5sqmm L + N + E (BR1 ceiling + bedsides + wardrobe driver)",
        "from_to": "Riser -> BR1 ceiling (centred) + bedsides + wardrobe driver",
        "dest_label": "BR1 LIGHTS",
    },
    {
        "ref": "F6", "id": "D2-BR1-Sockets",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (720, 700), (820, 450), FF["br1_bedside_r"]],
        "contents": "2.5sqmm L + N + E (bedside L + R + study)",
        "from_to": "Riser -> BR1 bedside + study sockets at 600mm FFL",
        "dest_label": "BR1 SOCKETS",
    },
    {
        "ref": "F7", "id": "E4-BR1-AC",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (740, 600), (820, 300), FF["br1_ac"]],
        "contents": "4sqmm L + N + E (20A AC socket)",
        "from_to": "Riser -> BR1 AC socket at 1850mm FFL",
        "dest_label": "BR1 AC",
    },
    {
        "ref": "F8", "id": "D3+D4-T1",
        "colour": C_POWER_HEAVY, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (720, 500), (830, 250), FF["t1_geyser"]],
        "contents": "2.5sqmm L + N + E (T1 geyser 20A + lights)",
        "from_to": "Riser -> T1 geyser + lights bundle",
        "dest_label": "T1 GEYSER+LT",
    },
    {
        "ref": "F9", "id": "D9-FF-Living",
        "colour": C_POWER_LIGHT, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (600, 750), FF["ff_living_ceil"]],
        "contents": "1.5sqmm L + N + E (FF Living lights + balcony + corridor)",
        "from_to": "Riser -> FF Living ceiling + front balcony + corridor lights",
        "dest_label": "FF LIVING LT",
    },

    # Data conduits (orange, from FF["riser_from_gf"]):
    {
        "ref": "F10", "id": "R-FF-1",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (600, 700), (520, 650), FF["ff_living_ap"]],
        "contents": "2x Cat6 UTP (router + spare) + draw wire",
        "from_to": "Riser -> FF Living central wall (router/AP mount) at 2400mm FFL",
        "dest_label": "FF AP (R-FF-1)",
        "note": "Wall plate Cat6 keystone x2 + 5A power socket 300mm beside (on D9 lighting circuit). Equidistant between BR1 and BR2.",
    },
    {
        "ref": "F11", "id": "R-FF-2",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (500, 650), (340, 470), FF["br2_study"]],
        "contents": "1x Cat6 UTP + draw wire",
        "from_to": "Riser -> BR2 study wall, 700mm FFL",
        "dest_label": "BR2 STUDY Cat6",
    },
    {
        "ref": "F12", "id": "R-FF-3",
        "colour": C_DATA, "size": "25mm", "status": "live",
        "route": [FF["riser_from_gf"], (740, 650), (775, 470), FF["br1_study"]],
        "contents": "1x Cat6 UTP + draw wire",
        "from_to": "Riser -> BR1 study wall, 700mm FFL",
        "dest_label": "BR1 STUDY Cat6",
    },
    {
        "ref": "F13", "id": "R-FF-4",
        "colour": C_DATA, "size": "16mm", "status": "provision",
        "route": [FF["ff_living_ap"], (450, 700), (300, 900), FF["ff_balcony"]],
        "contents": "PULL STRING ONLY - outdoor Cat6 future (balcony AP)",
        "from_to": "FF AP -> FF balcony soffit (future outdoor mesh AP)",
        "dest_label": "BALCONY AP",
        "note": "Pull draw wire only. Cap at IP67 keystone box at balcony soffit corner.",
    },
    {
        "ref": "F14", "id": "CAM-3-Front-Balcony",
        "colour": C_DATA, "size": "25mm", "status": "provision",
        "route": [FF["riser_from_gf"], (500, 900), (300, 1050), FF["front_balcony_nw"]],
        "contents": "PULL STRING + 1x outdoor Cat6 - IP67 back-box for ColorVu 4MP",
        "from_to": "Riser -> front balcony NW corner soffit/parapet (CAM-3)",
        "dest_label": "CAM-3",
        "note": "Elevated overview of compound, gate, driveway. 5500mm ground level.",
    },
    {
        "ref": "F15", "id": "CAM-5-Terrace",
        "colour": C_DATA, "size": "25mm", "status": "provision",
        "route": [FF["riser_from_gf"], (700, 600), FF["ff_riser_terrace"]],
        "contents": "PULL STRING + 1x outdoor UV-resistant Cat6 - IP67 back-box at terrace parapet",
        "from_to": "Riser -> continue UP to terrace level (CAM-5)",
        "dest_label": "CAM-5 (terrace)",
        "note": "Use UV-rated conduit for last 500mm above roof. Mount on parapet beside terrace door.",
    },
]


# ============================================================================
# PDF BUILDER
# ============================================================================

class ConduitPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A3")
        self.set_auto_page_break(False)

    # ---------- Page-level chrome ----------

    def header_block(self, sheet_id, floor, service, revision_date):
        self.set_xy(0, 0)
        self.set_fill_color(*INK)
        self.rect(0, 0, PAGE_W, 18, "F")
        self.set_text_color(*PAPER)
        self.set_font("Helvetica", "B", 16)
        self.set_xy(10, 4)
        self.cell(0, 6, f"  {sheet_id}   {floor}   {service}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_xy(10, 11)
        self.cell(0, 4, f"  Conduit map for electrician   Rev {revision_date}   Drawn on AutoCAD reference (handwritten plan is canonical)")

        self.set_font("Helvetica", "B", 9)
        self.set_xy(PAGE_W - 110, 5)
        self.cell(100, 4, "SCHEMATIC - verify dimensions against handwritten plan", align="R")
        self.set_font("Helvetica", "", 8)
        self.set_xy(PAGE_W - 110, 11)
        self.cell(100, 4, "TOP=S   BOTTOM=N (main door)   LEFT=E   RIGHT=W", align="R")

    # ---------- Floor plan + overlay drawing ----------

    def draw_floor_plan_base(self, img_path, x, y, w, h):
        self.image(str(img_path), x=x, y=y, w=w, h=h)

    def draw_hub(self, hub_box_px, px_to_mm_fn, label_top, label_bottom="",
                 fill=(255, 230, 80), border=INK):
        x_px, y_px, w_px, h_px = hub_box_px
        x_mm, y_mm = px_to_mm_fn(x_px, y_px)
        x2_mm, y2_mm = px_to_mm_fn(x_px + w_px, y_px + h_px)
        w_mm, h_mm = x2_mm - x_mm, y2_mm - y_mm

        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.6)
        self.rect(x_mm, y_mm, w_mm, h_mm, "FD")

        self.set_text_color(*INK)
        self.set_font("Helvetica", "B", 6)
        self.set_xy(x_mm, y_mm + h_mm / 2 - 2)
        self.cell(w_mm, 2.5, label_top, align="C", new_x="LMARGIN", new_y="NEXT")
        if label_bottom:
            self.set_font("Helvetica", "", 5)
            self.set_xy(x_mm, y_mm + h_mm / 2 + 0.5)
            self.cell(w_mm, 2.5, label_bottom, align="C")

    def draw_conduit(self, conduit, px_to_mm_fn, line_w=2.2):
        colour = conduit["colour"]
        status = conduit["status"]
        route_mm = [px_to_mm_fn(*p) for p in conduit["route"]]

        self.set_draw_color(*colour)
        self.set_line_width(line_w if status == "live" else line_w * 0.75)
        if status == "provision":
            self.set_dash_pattern(dash=2.0, gap=1.5)
        else:
            self.set_dash_pattern()

        for i in range(len(route_mm) - 1):
            x1, y1 = route_mm[i]
            x2, y2 = route_mm[i + 1]
            self.line(x1, y1, x2, y2)

        self.set_dash_pattern()
        ex, ey = route_mm[-1]
        self._numbered_callout(ex, ey, conduit["ref"], colour, status,
                              label=conduit.get("dest_label", ""))

    def _numbered_callout(self, x, y, ref, colour, status, label=""):
        r = 3.6
        self.set_draw_color(*colour)
        self.set_line_width(0.5)
        if status == "live":
            self.set_fill_color(*colour)
            self.ellipse(x - r, y - r, r * 2, r * 2, "FD")
            self.set_text_color(*PAPER)
        else:
            self.set_fill_color(*PAPER)
            self.ellipse(x - r, y - r, r * 2, r * 2, "FD")
            self.set_text_color(*colour)

        # Font sizing depends on ref length (2 chars = D1, 3 chars = D10)
        font_size = 7.5 if len(str(ref)) <= 2 else 6.5
        self.set_font("Helvetica", "B", font_size)
        self.set_xy(x - r, y - r + 0.5)
        self.cell(r * 2, r * 2, str(ref), align="C")

        if label:
            self.set_text_color(*INK)
            self.set_font("Helvetica", "B", 6.5)
            self.set_xy(x + r + 0.8, y - 1.5)
            self.cell(40, 3, label)

    # ---------- Right column: legend + cheat sheet ----------

    def colour_legend(self, x, y):
        self.set_xy(x, y)
        self.set_text_color(*INK)
        self.set_font("Helvetica", "B", 9)
        self.cell(80, 5, "Conduit colour code", new_x="LMARGIN", new_y="NEXT")
        y += 6
        items = [
            (C_POWER_LIGHT, "RED",    "25mm light power (1.5mm2 L/N/E)"),
            (C_POWER_HEAVY, "BLUE",   "25mm heavy power (2.5 / 4mm2)"),
            (C_DATA,        "ORANGE", "25mm Cat6 / network (LV-25 grey PVC)"),
            (C_LV16,        "PURPLE", "16mm low-voltage (LV-16)"),
            (C_WATER,       "GREEN",  "Water automation (20/16mm)"),
        ]
        self.set_font("Helvetica", "", 8)
        for colour, name, desc in items:
            self.set_xy(x, y)
            self.set_fill_color(*colour)
            self.rect(x, y + 1, 5, 3, "F")
            self.set_text_color(*INK)
            self.set_xy(x + 7, y)
            self.cell(80, 4.5, f"{name}  -  {desc}")
            y += 5

        y += 1
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(80, 4, "Line style:")
        y += 4
        self.set_font("Helvetica", "", 8)
        self.set_xy(x, y)
        self.cell(80, 4, "Solid    = pull cable NOW")
        y += 4
        self.set_xy(x, y)
        self.cell(80, 4, "Dashed   = pull STRING only (future)")
        y += 5

        # Ref scheme note
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(80, 4, "Ref scheme:")
        y += 4
        self.set_font("Helvetica", "", 7.5)
        self.set_xy(x, y)
        self.cell(80, 3.5, "P = light power   H = heavy power")
        y += 3.5
        self.set_xy(x, y)
        self.cell(80, 3.5, "D = data Cat6    L = LV-16  W = water")
        y += 3.5
        self.set_xy(x, y)
        self.cell(80, 3.5, "F = first-floor combined")
        return y

    def cheat_sheet(self, x, y, w, conduits, title):
        self.set_xy(x, y)
        self.set_text_color(*INK)
        self.set_font("Helvetica", "B", 10.5)
        self.cell(w, 6, title, new_x="LMARGIN", new_y="NEXT")
        y += 7

        self.set_xy(x, y)
        self.set_fill_color(*INK)
        self.set_text_color(*PAPER)
        self.set_font("Helvetica", "B", 8)
        self.rect(x, y, w, 5, "F")
        self.set_xy(x + 1, y + 0.6)
        self.cell(10, 4, "Ref")
        self.cell(20, 4, "Size")
        self.cell(w - 32, 4, "From -> To  /  What's inside  /  Note")
        y += 6

        self.set_text_color(*INK)
        for c in conduits:
            row_h = self._cheat_row(x, y, w, c)
            y += row_h
            # If we'd overflow, break early
            if y > PAGE_H - 10:
                break
        return y

    def _cheat_row(self, x, y, w, c):
        # Ref circle
        self.set_fill_color(*c["colour"])
        self.set_draw_color(*c["colour"])
        self.set_line_width(0.5)
        if c["status"] == "live":
            self.ellipse(x + 0.5, y + 0.6, 6, 6, "FD")
            self.set_text_color(*PAPER)
        else:
            self.set_fill_color(*PAPER)
            self.ellipse(x + 0.5, y + 0.6, 6, 6, "FD")
            self.set_text_color(*c["colour"])
        font_size = 7.5 if len(str(c["ref"])) <= 2 else 6.5
        self.set_font("Helvetica", "B", font_size)
        self.set_xy(x + 0.5, y + 1.3)
        self.cell(6, 4.5, str(c["ref"]), align="C")

        # Size column
        self.set_text_color(*INK)
        self.set_font("Helvetica", "B", 7.5)
        self.set_xy(x + 10, y + 0.5)
        self.cell(20, 4, c["size"])

        if c["status"] == "provision":
            self.set_text_color(*INK_SOFT)
            self.set_font("Helvetica", "B", 6.5)
            self.set_xy(x + 10, y + 4)
            self.cell(20, 3, "(provision)")

        # Main column
        col_x = x + 30
        col_w = w - 32
        self.set_text_color(*INK)
        self.set_font("Helvetica", "B", 7.8)
        self.set_xy(col_x, y + 0.3)
        self.multi_cell(col_w, 3.4, c["from_to"], new_x="LMARGIN", new_y="NEXT")
        used = self.get_y() - y

        self.set_font("Helvetica", "", 7.2)
        self.set_text_color(*INK_SOFT)
        self.set_xy(col_x, y + used)
        self.multi_cell(col_w, 3.1, f"Inside: {c['contents']}", new_x="LMARGIN", new_y="NEXT")
        used = self.get_y() - y

        if c.get("note"):
            self.set_font("Helvetica", "I", 6.8)
            self.set_text_color(*INK_FAINT)
            self.set_xy(col_x, y + used)
            self.multi_cell(col_w, 3.0, c["note"], new_x="LMARGIN", new_y="NEXT")
            used = self.get_y() - y

        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(x, y + used + 0.4, x + w, y + used + 0.4)
        return used + 1.4

    # ---------- Footer ----------

    def footer_note(self, x, y, w, text):
        self.set_xy(x, y)
        self.set_text_color(*INK_SOFT)
        self.set_font("Helvetica", "I", 7.5)
        self.cell(w, 3, text)


# ============================================================================
# SHEET BUILDERS
# ============================================================================

def _build_gf_sheet(pdf, sheet_id, service, conduits, *, hub_db=False, hub_niche=False,
                    hub_dbcup=False, title_extra=""):
    """Generic GF sheet builder. Set hub_* flags to draw the matching hub on top."""
    pdf.add_page()
    pdf.header_block(sheet_id=sheet_id, floor="GROUND FLOOR", service=service,
                     revision_date="2026-05-29")
    pdf.draw_floor_plan_base(GF_IMG, GF_PLAN_X, GF_PLAN_Y, GF_PLAN_W, GF_PLAN_H)

    for c in conduits:
        pdf.draw_conduit(c, gf_px_to_mm, line_w=2.2)

    if hub_niche:
        pdf.draw_hub(NICHE_BOX, gf_px_to_mm, "NICHE", "data hub", fill=(255, 230, 80))
    if hub_db:
        pdf.draw_hub(DB_BOX, gf_px_to_mm, "DB", "(power)", fill=(255, 200, 200))
    if hub_dbcup:
        pdf.draw_hub(DB_CUP_BOX, gf_px_to_mm, "DB CUPB.", "(water aut.)", fill=(200, 240, 220))

    right_x = GF_PLAN_X + GF_PLAN_W + 8
    right_w = PAGE_W - right_x - 8
    pdf.colour_legend(right_x, 28)
    pdf.cheat_sheet(right_x, 90, right_w, conduits, title=f"Conduits on this sheet  ({title_extra})")

    pdf.footer_note(GF_PLAN_X, GF_PLAN_Y + GF_PLAN_H + 4, GF_PLAN_W,
                   "Source: electrical/conduits-and-cavities.md PART 2. Handwritten plan is canonical - verify wall positions before chasing.")


def build_sheet_gf_light(pdf):
    _build_gf_sheet(pdf, "GF-01", "LIGHT POWER (RED 25mm)", GF_LIGHT_CONDUITS,
                    hub_db=True, title_extra=f"{len(GF_LIGHT_CONDUITS)} runs")


def build_sheet_gf_heavy(pdf):
    _build_gf_sheet(pdf, "GF-02", "HEAVY POWER (BLUE 25mm)", GF_HEAVY_CONDUITS,
                    hub_db=True, title_extra=f"{len(GF_HEAVY_CONDUITS)} runs")


def build_sheet_gf_data(pdf):
    _build_gf_sheet(pdf, "GF-03", "DATA / CAT6 (ORANGE = LV-25 grey)", GF_DATA_CONDUITS,
                    hub_niche=True, title_extra=f"{len(GF_DATA_CONDUITS)} runs")


def build_sheet_gf_lv16(pdf):
    _build_gf_sheet(pdf, "GF-04", "LOW-VOLTAGE 16mm (PURPLE)", GF_LV16_CONDUITS,
                    title_extra=f"{len(GF_LV16_CONDUITS)} runs")


def build_sheet_gf_water(pdf):
    _build_gf_sheet(pdf, "GF-05", "WATER AUTOMATION (GREEN)", GF_WATER_CONDUITS,
                    hub_niche=True, hub_dbcup=True, title_extra=f"{len(GF_WATER_CONDUITS)} runs")


def build_sheet_ff(pdf):
    pdf.add_page()
    pdf.header_block(sheet_id="FF-01", floor="FIRST FLOOR",
                     service="POWER + DATA COMBINED",
                     revision_date="2026-05-29")
    pdf.draw_floor_plan_base(FF_IMG, FF_PLAN_X, FF_PLAN_Y, FF_PLAN_W, FF_PLAN_H)

    for c in FF_CONDUITS:
        pdf.draw_conduit(c, ff_px_to_mm, line_w=2.2)

    pdf.draw_hub(RISER_BOX_FF, ff_px_to_mm, "RISER", "from GF niche/DB", fill=(255, 230, 80))

    right_x = FF_PLAN_X + FF_PLAN_W + 8
    right_w = PAGE_W - right_x - 8
    pdf.colour_legend(right_x, 28)
    pdf.cheat_sheet(right_x, 90, right_w, FF_CONDUITS,
                   title=f"FF conduits  ({len(FF_CONDUITS)} runs)")

    pdf.footer_note(FF_PLAN_X, FF_PLAN_Y + FF_PLAN_H + 4, FF_PLAN_W,
                   "Source: electrical/conduits-and-cavities.md PART 2 (FF Conduit Runs + R-FF-1/2/3/4). FF balcony projection still pending decision (3ft or expand).")


def build_sheet_riser(pdf):
    """
    Vertical cross-section through the staircase W wall showing the 5 bundles
    going up from GF (DB + niche) to FF, with CAM-3 and CAM-5 continuing to terrace.
    Drawn as a stylized elevation view, NOT a floor plan overlay.
    """
    pdf.add_page()
    pdf.header_block(sheet_id="RISER",
                     floor="STAIRCASE WALL (vertical cross-section)",
                     service="ALL FLOORS - cable risers GF -> FF -> terrace",
                     revision_date="2026-05-29")

    # Draw a stylised vertical column
    col_x = 60        # mm - left edge of column
    col_w = 100       # mm
    col_y_top = 35    # mm - top (terrace level)
    col_y_bot = 250   # mm - bottom (GF DB level)

    # Background column with floor lines
    pdf.set_fill_color(248, 246, 240)
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.4)
    pdf.rect(col_x, col_y_top, col_w, col_y_bot - col_y_top, "FD")

    # Floor markers
    floors = [
        (col_y_bot - 5,   "GROUND FLOOR  (DB + niche level)"),
        (col_y_bot - 75,  "GROUND FLOOR slab (top)"),
        (col_y_top + 80,  "FIRST FLOOR  (FF Living wall + bedrooms)"),
        (col_y_top + 10,  "TERRACE  (CAM-5 + Sintex JB)"),
    ]
    for y, label in floors:
        pdf.set_draw_color(*INK_SOFT)
        pdf.set_line_width(0.3)
        pdf.line(col_x, y, col_x + col_w, y)
        pdf.set_text_color(*INK)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_xy(col_x + col_w + 3, y - 2.5)
        pdf.cell(60, 4, label)

    # Bundles going up the staircase wall - depicted as vertical coloured lines
    bundles = [
        # (x_offset_in_col, y_top, y_bot, colour, label, contents)
        (10, col_y_top + 80, col_y_bot - 5, C_POWER_LIGHT, "B1: D5+D6 (BR2 lights/sockets)", "2x 1.5/2.5sqmm"),
        (22, col_y_top + 80, col_y_bot - 5, C_POWER_LIGHT, "B2: D1+D2 (BR1 lights/sockets)", "2x 1.5/2.5sqmm"),
        (34, col_y_top + 80, col_y_bot - 5, C_POWER_HEAVY, "B3: D3+D4+D7+D8 (T1+T2 geyser/lights)", "2.5sqmm + 1.5sqmm"),
        (46, col_y_top + 80, col_y_bot - 5, C_POWER_LIGHT, "B4: D9 (FF corridor + balconies)", "1.5sqmm"),
        (58, col_y_top + 80, col_y_bot - 5, C_POWER_HEAVY, "B5: E4+E5 (BR1+BR2 AC)", "4sqmm"),
        (72, col_y_top + 80, col_y_bot - 5, C_DATA,        "LV1: R-FF-1 (FF AP, 2x Cat6 + spare)", "Cat6 UTP"),
        (82, col_y_top + 80, col_y_bot - 5, C_DATA,        "LV2: R-FF-2 (BR2 study)", "Cat6 UTP"),
        (92, col_y_top + 80, col_y_bot - 5, C_DATA,        "LV3: R-FF-3 (BR1 study)", "Cat6 UTP"),
        # CAM-3 / CAM-5 continue up to terrace
        (72, col_y_top + 10, col_y_top + 80, C_DATA, "CAM-3 -> FF balcony NW", "Cat6 outdoor"),
        (82, col_y_top + 10, col_y_top + 80, C_DATA, "CAM-5 -> terrace parapet", "Cat6 outdoor UV"),
        # Water automation - C-Sintex-1/2 share the riser shaft up to terrace
        (92, col_y_top + 10, col_y_bot - 5,  C_WATER, "C-Sintex-1/2 (water tank + float)", "Cat6 + 2-core"),
    ]

    pdf.set_line_width(1.6)
    for bx, by_t, by_b, col, label, contents in bundles:
        pdf.set_draw_color(*col)
        pdf.line(col_x + bx, by_t, col_x + bx, by_b)
        # Top arrow
        pdf.line(col_x + bx - 1.5, by_t + 2, col_x + bx, by_t)
        pdf.line(col_x + bx + 1.5, by_t + 2, col_x + bx, by_t)
        # Bottom dot
        pdf.set_fill_color(*col)
        pdf.ellipse(col_x + bx - 1.2, by_b - 1.2, 2.4, 2.4, "F")

    # Bundle legend on the right
    leg_x = 200
    leg_y = 35
    pdf.set_xy(leg_x, leg_y)
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 5, "Riser bundles  (5 power + 3 data + water-auto = 9 conduits up the staircase W wall)", new_x="LMARGIN", new_y="NEXT")

    leg_y += 8
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_xy(leg_x, leg_y)
    pdf.cell(0, 5, "Rule: max 3 circuit wires per 25mm conduit. Use SEPARATE conduits per bundle.")
    leg_y += 8

    for bx, by_t, by_b, col, label, contents in bundles:
        pdf.set_xy(leg_x, leg_y)
        pdf.set_fill_color(*col)
        pdf.rect(leg_x, leg_y + 1, 5, 3, "F")
        pdf.set_text_color(*INK)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_xy(leg_x + 7, leg_y)
        pdf.cell(0, 4, label, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*INK_SOFT)
        pdf.set_xy(leg_x + 7, leg_y + 4)
        pdf.cell(0, 3.5, f"   Wire: {contents}")
        leg_y += 8

    pdf.footer_note(col_x, 275, 300,
                   "Source: electrical/conduits-and-cavities.md PART 2 (Vertical Rise) + R-FF-1/2/3 + CAM-3/4/5. Bundle chase channel ~150mm wide in staircase W wall.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    pdf = ConduitPDF()
    build_sheet_gf_light(pdf)
    build_sheet_gf_heavy(pdf)
    build_sheet_gf_data(pdf)
    build_sheet_gf_lv16(pdf)
    build_sheet_gf_water(pdf)
    build_sheet_ff(pdf)
    build_sheet_riser(pdf)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}  ({pdf.pages_count} pages)")


if __name__ == "__main__":
    main()
