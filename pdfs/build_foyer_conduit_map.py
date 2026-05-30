"""
Generate the Foyer X-Ray Conduit Maps (3 variants).

Three reference images at different detail levels:
1. comprehensive - ALL conduits including lighting (~15-18 conduits, busy)
2. focused      - Data + water automation + cavity + doorbell + ceiling speaker
                 (~10-12 conduits, balanced - RECOMMENDED for on-site reference)
3. minimal      - Just data/signal conduits, no water automation (~4-6 conduits, cleanest)

Each shows the same foyer room with same geometry, just different conduit subsets.

Output:
  interior-design/generated-images/conduit-maps/foyer-xray-comprehensive.png
  interior-design/generated-images/conduit-maps/foyer-xray-focused.png
  interior-design/generated-images/conduit-maps/foyer-xray-minimal.png

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_foyer_conduit_map.py                  # generate all missing
  python3 build_foyer_conduit_map.py --regenerate     # force regen all 3
  python3 build_foyer_conduit_map.py --variant focused  # generate just one
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "interior-design" / "generated-images" / "conduit-maps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3.1-flash-image-preview"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

# Shared geometric and stylistic base — keeps all 3 variants visually consistent
SHARED_BASE = """A clean technical isometric X-ray architectural cutaway illustration of the FOYER (entrance hall) of a modern Indian residential home.

CRITICAL VIEWING ANGLE - this is the most important geometric constraint:

- The viewer stands in the WEST side of the foyer, just inside the Living hall, looking EAST INTO the foyer.
- This means: the EAST WALL is the BACK WALL of the image (the far wall, in the background).
- The viewer's LEFT hand points NORTH; the viewer's RIGHT hand points SOUTH.
- BEHIND the viewer (out of frame, to the west) is the Living/Dining/Staircase area; further west is the staircase server niche.

Room layout reference (plan view from above, for understanding only - do NOT draw this sketch in the actual image):

                  NORTH (main door on N wall)
                       |
       [Living] - [FOYER ENTRANCE] - [East exterior wall - DB+Starter]
        WEST     (5 ft N-S deep)         EAST
                       |
                  SOUTH (stone feature wall with screen cavity)

Server niche is far WEST behind the viewer.

ROOM ELEMENTS TO DRAW with their CORRECT positions:

1. EAST WALL (the back wall of the image, a 9-inch / 230 mm thick exterior masonry wall):
   - DB (Distribution Board) RECESSED FLUSH INTO THE EAST WALL on the TOP - a rectangular metallic outline approximately 400 mm wide x 600 mm tall, top edge at about 2100 mm above floor. Labeled "DB - Schneider Acti9 48-way".
   - STARTER CUPBOARD RECESSED FLUSH INTO THE EAST WALL DIRECTLY BELOW THE DB - a rectangular wooden cabinet outline approximately 600 mm wide x 400 mm tall, BELOW the DB (the two stacked vertically). Labeled "Starter Cupboard - P1+P2 motor starters + Sonoff DUALR3".
   - CRITICAL: DB is ABOVE Starter. Both are WALL-FLUSHED (flush mounted, not protruding). Both sit on the LEFT side of the East wall (north portion), behind where the open door rests against the wall.

2. SOUTH WALL (the right wall of the image, a 9-inch thick stone-clad feature wall on its East portion):
   - SCREEN CAVITY: a large rectangular opening cut into the south wall at standing eye height, approximately 580 mm wide x 380 mm tall x 100 mm deep. Labeled "Screen cavity (Samsung 21.5 inch monitor)".
   - Inside the cavity: a small black rectangular outline marks the Samsung monitor position.
   - Below or beside the monitor: a small SOCKET PANEL outline labeled "8M cavity socket - 2 sockets + Cat6 keystone jack (Cat6 from server terminates HERE)".
   - The cavity has a halo LED strip outline around its edges (subtle).
   - The South wall is shown with a textured stone-cladding pattern (light beige natural stone effect).

3. NORTH WALL (the left wall of the image):
   - MAIN DOOR opening on the North wall (3.2 ft wide door, hinges on East side, swings against East wall when open). Drawn as a hinged door outline, partially open against the East wall.
   - On the OUTSIDE FACE of the North wall (visible through the X-ray effect), near the door: a small rectangular back box labeled "Hikvision doorbell (outside face, ~1450 mm FFL)".
   - On the INSIDE FACE of the North wall, near the door jamb: a small "Foyer Switch Panel" outline labeled "Foyer light switches (smart, Sonoff hidden)".

4. CEILING (false ceiling, visible across the top of the image):
   - Small round disc labeled "Ceiling speaker (foyer ambient audio)" - centered on the ceiling.
   - 2 small downlight circles labeled "Spotlights" (symbolic).

5. FLOOR (light tile pattern at the bottom edge).

X-RAY EFFECT - the core visual technique:

- The WALLS (North, South, East) and the FALSE CEILING are rendered SEMI-TRANSPARENT at about 30% opacity (you can see THROUGH them).
- This reveals the electrical conduits embedded inside them as SOLID GREY (data conduits) or RED (power conduits) or BLUE (motor conduits) PVC CYLINDRICAL TUBES.
- The DB, Starter cupboard, screen cavity, monitor, socket panel, door, doorbell back box, switch panel, ceiling speaker, spotlights, and floor are drawn at NORMAL OPACITY (solid, fully visible).

STRICT GEOMETRY RULES that you MUST FOLLOW:

- DB MUST be on the East wall (BACK wall of image), positioned ABOVE the Starter cupboard. NEVER on the South wall or North wall.
- Starter cupboard MUST be on the East wall, DIRECTLY BELOW the DB. NEVER beside the DB.
- Screen cavity MUST be on the South wall (RIGHT wall of image), NEVER on the East or North wall.
- Door MUST be on the North wall (LEFT wall of image), NEVER on East or South.
- Both DB and Starter are FLUSH-mounted (recessed into the wall surface), NOT protruding boxes.
- The East wall is the BACK wall of the image, the South wall is on the RIGHT, the North wall is on the LEFT.

STYLE REQUIREMENTS:

- Clean technical isometric architectural blueprint illustration
- IKEA assembly manual aesthetic
- Flat color palette only - NO photographic shading or realism
- Warm beige semi-transparent walls and ceiling (30 percent opacity)
- Stone texture on South feature wall (light beige natural stone pattern, still 30 percent opacity)
- Light wood tones for door panel and starter cupboard facade (solid normal opacity)
- Metallic grey for DB (solid normal opacity)
- Conduits drawn as SOLID, PROMINENT cylindrical tubes in their proper color codes
- Thin black outlines on all elements
- White background outside the room boundary
- Sans-serif font for all labels
- NEVER include any people, decorative items, or extra elements
- The image must function as a PERMANENT POST-PLASTER REFERENCE so the homeowner and electrician can identify which conduit is for what purpose at a glance

"""

# Variant-specific conduit content
VARIANTS = {
    "comprehensive": {
        "filename": "foyer-xray-comprehensive.png",
        "title": "Comprehensive — all conduits including lighting",
        "conduits": """X-RAY CONDUITS (Comprehensive — ALL conduit categories visible):

A. DATA / SIGNAL CONDUITS (drawn as solid GREY tubes - colour: medium grey):

A1. "C-Niche-Cavity-Data" - enters from LEFT edge (west, from server niche), travels at FLOOR level (underfloor route, beneath the foyer tile), then ROTATES UP into the South feature wall, terminates at the Cat6 keystone jack inside the 8M cavity socket panel on the cavity back wall. Label: "C-Niche-Cavity-Data (25mm grey, ~12m, underfloor route) - Cat6 to cavity keystone".

A2. "C-Niche-Doorbell" - enters from LEFT edge, also at FLOOR level alongside A1, then ROTATES UP into the North wall, EXITS through the outside face of the North wall, terminates at the Hikvision doorbell back box. Label: "C-Niche-Doorbell (25mm grey, ~9m) - Cat6 PoE for Hikvision doorbell".

B. POWER CONDUITS (drawn as solid RED tubes - colour: red/orange):

B1. "C-DB-Cavity-Power" - originates at the DB on the East wall, runs through a wall chase along the SE corner of the foyer, enters the cavity at the BOTTOM-LEFT corner of the cavity back wall. Label: "C-DB-Cavity-Power (25mm red, ~3m) - 230V for Samsung monitor".

B2. "C-DB-Foyer-Lights" - originates at the DB, runs along the ceiling chase, terminates at the Foyer Switch Panel on the North wall near the door. Label: "C-DB-Foyer-Lights (25mm red, ~3m) - circuit feed".

C. LIGHTING CONDUITS (drawn as thinner SOLID RED tubes branching from the Foyer Switch Panel):

C1, C2, C3 - thin lines branching from the Foyer Switch Panel up into the ceiling and out to 2 spotlights + 1 cove LED. Label group: "Foyer lighting branches (spotlights, cove)".

D. HALO + CEILING SPEAKER CONDUITS at the cavity (drawn as solid GREY thinner tubes):

D1. Halo conduit - 16mm grey, enters cavity through TOP-CENTRE of back wall, comes from a halo LED driver above false ceiling.

D2. Cavity-to-ceiling-speaker conduit - 16mm grey, EXITS the cavity through its TOP inner wall, travels UP through the South wall into the false ceiling void, terminates at the ceiling speaker. Label: "Cavity-top → ceiling speaker (16mm grey, ~1.5m, was pull-string-only, now ACTIVE)".

E. WATER AUTOMATION CONDUITS (drawn as colored tubes per spec):

E1. "C-Sintex-2" - 16mm, enters DB cupboard from OUTSIDE TOP (terrace), through the East wall, terminates at Starter cupboard. Label: "C-Sintex-2 (16mm, ~14m) - Sintex tank float wire from terrace".

E2. "C-Sump-2" - 16mm, enters Starter cupboard from OUTSIDE (sump JB on East exterior wall), through the East wall lower portion. Label: "C-Sump-2 (16mm, ~8m) - Sump float wire".

E3. "C-DB-Backup" - 20mm grey, enters DB from the LEFT (server niche via ceiling chase). Label: "C-DB-Backup (20mm grey, ~4m, EMPTY/pull-string) - future ESP32 motor control".

E4. "C-Motor-P1" - 25mm BLUE, exits Starter cupboard through East wall to outside (borewell). Label: "C-Motor-P1 (25mm blue, armoured) - borewell motor".

E5. "C-Motor-P2" - 25mm BLUE, exits Starter cupboard through East wall lower (P2 pump). Label: "C-Motor-P2 (25mm blue, ~1.5m) - P2 pump motor".

DIRECTIONAL ARROW on LEFT edge: bold arrow "TO SERVER NICHE (staircase wall, west side of house)" pointing leftward out of frame.

LEGEND BOX in lower-right corner (small text, 4 lines):
- "Grey conduits = data (Cat6)"
- "Red conduits = power (220V)"
- "Blue conduits = motor (armoured)"
- "Comprehensive view: ALL conduits"
""",
    },
    "focused": {
        "filename": "foyer-xray-focused.png",
        "title": "Focused — data + water automation + cavity + doorbell + ceiling speaker",
        "conduits": """X-RAY CONDUITS (Focused view - data, water automation, cavity, doorbell, ceiling speaker; lighting branches OMITTED):

A. DATA / SIGNAL CONDUITS (drawn as solid GREY tubes):

A1. "C-Niche-Cavity-Data" - enters from LEFT edge (west, from server niche), travels at FLOOR level (underfloor route beneath foyer tile), rotates UP into the South feature wall, terminates at the Cat6 keystone jack inside the 8M cavity socket panel on the cavity back wall. Label: "C-Niche-Cavity-Data (25mm grey, ~12m, underfloor) - Cat6 to cavity keystone (terminates at keystone in 8M cavity socket panel)".

A2. "C-Niche-Doorbell" - enters from LEFT edge, underfloor alongside A1, rotates UP into the North wall, EXITS through the outside face of the North wall, terminates at the Hikvision doorbell back box on the outside. Label: "C-Niche-Doorbell (25mm grey, ~9m, underfloor) - Cat6 PoE for Hikvision doorbell".

B. POWER CONDUIT (drawn as solid RED tube):

B1. "C-DB-Cavity-Power" - originates at the DB on the East wall, runs through a SE corner wall chase, enters the cavity at the BOTTOM-LEFT corner of the cavity back wall. Label: "C-DB-Cavity-Power (25mm red, ~3m) - 230V to Samsung monitor".

C. HALO + CEILING SPEAKER CONDUITS at the cavity (drawn as solid GREY thinner tubes):

C1. Halo conduit - 16mm grey, enters cavity through TOP-CENTRE of back wall from a halo LED driver above false ceiling. Label: "Halo LED conduit (16mm grey, 24V) - driver above false ceiling".

C2. Cavity-to-ceiling-speaker conduit - 16mm grey, EXITS the cavity through its TOP inner wall, goes UP through the South wall into the false ceiling void, terminates at the ceiling speaker. Label: "Cavity to ceiling speaker conduit (16mm grey, ~1.5m) - 2-core speaker wire to 3-inch flush-mount ceiling speaker".

D. WATER AUTOMATION CONDUITS (5 visible, drawn in appropriate colors):

D1. "C-Sintex-2" - 16mm tube, enters Starter cupboard from OUTSIDE (terrace, top of East wall). Label: "C-Sintex-2 (16mm, ~14m, from terrace) - Sintex tank float wire".

D2. "C-Sump-2" - 16mm tube, enters Starter cupboard from OUTSIDE (sump JB on East exterior wall, lower portion). Label: "C-Sump-2 (16mm, ~8m, from sump JB) - Sump float wire".

D3. "C-DB-Backup" - 20mm grey tube, enters DB from the LEFT edge (server niche via ceiling-level chase). Label: "C-DB-Backup (20mm grey, ~4m, EMPTY pull-string) - future ESP32 motor control".

D4. "C-Motor-P1" - 25mm BLUE tube, exits Starter cupboard through East wall going outside (to borewell). Label: "C-Motor-P1 (25mm blue armoured) - to borewell motor".

D5. "C-Motor-P2" - 25mm BLUE tube, exits Starter cupboard through East wall lower portion (to P2 pump). Label: "C-Motor-P2 (25mm blue, ~1.5m) - to P2 pump motor".

DIRECTIONAL ARROW on LEFT edge: bold arrow "TO SERVER NICHE (staircase wall, west side of house)" pointing leftward out of frame.

LEGEND BOX in lower-right corner (small text, 4 lines):
- "Grey conduits = data (Cat6)"
- "Red conduits = power (220V)"
- "Blue conduits = motor (armoured)"
- "Focused view: data + water automation + cavity (lighting omitted)"
""",
    },
    "minimal": {
        "filename": "foyer-xray-minimal.png",
        "title": "Minimal — data + signal conduits only (no water automation, no general lighting)",
        "conduits": """X-RAY CONDUITS (Minimal view - data/signal only, no water automation, no general lighting):

A. DATA / SIGNAL CONDUITS (drawn as solid GREY tubes, prominent):

A1. "C-Niche-Cavity-Data" - enters from LEFT edge (west, from server niche), travels at FLOOR level (underfloor route beneath foyer tile), rotates UP into the South feature wall, terminates at the Cat6 keystone jack inside the 8M cavity socket panel on the cavity back wall. Label: "C-Niche-Cavity-Data (25mm grey, ~12m, underfloor) - Cat6 to cavity keystone (terminates here, gives data to RPi Zero inside cavity)".

A2. "C-Niche-Doorbell" - enters from LEFT edge, underfloor alongside A1, rotates UP into the North wall, EXITS through the outside face of the North wall, terminates at the Hikvision doorbell back box. Label: "C-Niche-Doorbell (25mm grey, ~9m) - Cat6 PoE for Hikvision doorbell + camera + intercom".

B. HALO + CEILING SPEAKER CONDUITS at the cavity (drawn as solid GREY thinner tubes):

B1. Halo conduit - 16mm grey, enters cavity through TOP-CENTRE of back wall from a halo LED driver above false ceiling. Label: "Halo LED conduit (16mm grey)".

B2. Cavity-to-ceiling-speaker conduit - 16mm grey, EXITS the cavity through its TOP inner wall, goes UP through the South wall into the false ceiling void, terminates at the ceiling speaker. Label: "Cavity to ceiling speaker (16mm grey, speaker wire active 2026-05-22)".

DO NOT DRAW: any water automation conduits (Sintex, Sump, DB-Backup, Motor cables), any general lighting branches (spotlights, cove, switch panel internal), the DB-to-cavity power conduit. Keep this image clean - data/signal only.

(The DB and Starter cupboard are still visible on the East wall as components, but their internal power-circuit conduits are NOT drawn in this minimal view.)

DIRECTIONAL ARROW on LEFT edge: bold arrow "TO SERVER NICHE (staircase wall, west side of house)" pointing leftward out of frame.

LEGEND BOX in lower-right corner (small text, 3 lines):
- "Grey conduits = data (Cat6) + signal"
- "All 4 data/signal terminations visible"
- "Minimal view: omits water automation + lighting"
""",
    },
}


def gemini_generate(prompt: str, out_path: Path, api_key: str,
                    max_retries: int = 5) -> bool:
    """Call Gemini API to generate a single image. Saves PNG to out_path."""
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "3:2",
                "imageSize": "2K",
            },
        },
    }
    url = f"{API_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                url, data=json.dumps(body).encode("utf-8"),
                headers=headers, method="POST",
            )
            print(f"    [attempt {attempt}/{max_retries}] calling Gemini...")
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            print(f"    -> response in {dt:.1f}s")
            for cand in data.get("candidates", []):
                content = cand.get("content", {})
                for part in content.get("parts", []):
                    inline = part.get("inlineData") or part.get("inline_data")
                    if inline and "data" in inline:
                        png_bytes = base64.b64decode(inline["data"])
                        out_path.write_bytes(png_bytes)
                        print(f"    OK saved {out_path.name} "
                              f"({len(png_bytes)/1024:.0f} KB)")
                        return True
                fr = cand.get("finishReason", "?")
                print(f"    X no image (finishReason={fr})")
                if fr in ("IMAGE_SAFETY", "PROHIBITED_CONTENT", "SAFETY"):
                    return False
            print(f"    X empty: {str(data)[:200]}")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")[:200]
            print(f"    X HTTP {e.code}: {err}")
            if e.code in (429, 500, 502, 503, 504):
                wait = 10 * attempt
                print(f"      transient - waiting {wait}s")
                time.sleep(wait)
                continue
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print(f"    X timeout: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            return False
        except Exception as e:
            print(f"    X error: {type(e).__name__}: {e}")
            return False
    return False


def backup_existing(out_path: Path) -> None:
    """Move existing image to a timestamped backup before overwriting."""
    if out_path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = out_path.parent / f"{out_path.stem}_backup-{ts}.png"
        shutil.move(str(out_path), str(bak))
        print(f"  backed up old image -> {bak.name}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api-key", help="Google AI API key")
    ap.add_argument("--regenerate", action="store_true",
                    help="Force regen all variants (existing images backed up)")
    ap.add_argument("--variant", choices=list(VARIANTS.keys()) + ["all"],
                    default="all", help="Which variant to generate")
    args = ap.parse_args()
    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY")

    if not api_key:
        print("X No API key. Set GOOGLE_AI_API_KEY env or use --api-key.")
        return 1

    to_run = list(VARIANTS.keys()) if args.variant == "all" else [args.variant]
    print(f"\nFoyer X-ray conduit maps - generating {len(to_run)} variant(s)\n")

    failed = []
    for vname in to_run:
        spec = VARIANTS[vname]
        out_path = OUT_DIR / spec["filename"]
        print(f"\n{vname.upper()}: {spec['title']}")
        if out_path.exists() and not args.regenerate:
            print(f"  exists, skipping ({out_path}). Use --regenerate to force.")
            continue
        if args.regenerate:
            backup_existing(out_path)
        full_prompt = SHARED_BASE + spec["conduits"]
        if not gemini_generate(full_prompt, out_path, api_key):
            failed.append(vname)
            print(f"  FAILED: {vname}")

    print()
    if failed:
        print(f"X {len(failed)} variant(s) failed: {failed}")
        return 2
    print(f"OK all variants generated. Files in: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
