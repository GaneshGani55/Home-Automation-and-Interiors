"""
Generate the Staircase-Wall Conduit Spine X-Ray Map (UNIFIED).

A 2-floor sectional cutaway viewed from the GF living hall looking at the
staircase. The 9-inch staircase W wall is the vertical CONDUIT SPINE: the
server niche sits at its base and FOUR conduits rise through it and branch
to their endpoints.

Geometry locked from user's description + floor-plans-decoded.md +
conduits-and-cavities.md:
  - LEFT of image  = NORTH side = open areas (GF dining/living, FF Living)
                     -> both ceiling APs hang here
  - RIGHT of image = SOUTH side = staircase + spine wall + Bedroom 2
                     (the "balcony room") + server niche at base
  - The staircase W wall (GF) == Bedroom 2's N wall (FF) == the spine

FOUR conduits (each exactly ONE grey tube, all starting at the niche):
  1. C-Niche-Waveshare -> staircase touchscreen on the spine wall (GF, 1500mm)
  2. R-GF-1            -> GF ceiling AP over dining/living (LEFT)
  3. R-FF-1            -> FF ceiling AP over FF Living (LEFT)
  4. R-FF-2            -> Bedroom 2 (balcony room) study desk, far face of
                         spine wall (FF, 700mm desk height)

Output: interior-design/generated-images/conduit-maps/staircase-wall-conduit-spine.png

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_staircase_spine_conduit_map.py              # generates if missing
  python3 build_staircase_spine_conduit_map.py --regenerate # backup existing, regen
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
OUT_PATH = OUT_DIR / "staircase-wall-conduit-spine.png"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3.1-flash-image-preview"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

PROMPT = """A clean technical isometric X-ray architectural cutaway illustration of a modern Indian home staircase, showing TWO FLOORS (Ground Floor below, First Floor above) in a single vertical cross-section. The purpose is a PERMANENT POST-PLASTER REFERENCE so the homeowner and electrician can identify every conduit that rises through the staircase wall.

THE CORE IDEA: there is ONE thick masonry wall - the STAIRCASE WALL - that runs vertically through both floors. It is the "conduit spine". The server niche sits at the BASE of this wall, and FOUR grey conduits rise up inside this single wall and branch out to four endpoints. Make this wall the visual backbone of the whole image.

CRITICAL VIEWING GEOMETRY (read carefully, follow exactly):

- The viewer is standing in the Ground Floor living hall, looking AT the staircase.
- Landscape orientation, wider than tall. GF on the bottom half, FF on the top half, a concrete floor slab between them.
- LEFT side of image = NORTH side of house = the OPEN areas (GF dining/living below; FF Living above). BOTH ceiling Wi-Fi APs hang here on the LEFT.
- RIGHT side of image = SOUTH side = the STAIRCASE, the thick SPINE WALL, and (on FF) BEDROOM 2 (the "balcony bedroom"). The SERVER NICHE is at the base of the spine wall on the RIGHT.
- The SPINE WALL is a single thick (9 inch) masonry wall positioned in the RIGHT-CENTER of the image, running vertically from the GF floor up through the slab to the FF ceiling. On the GF it is the staircase wall; on the FF the SAME wall is Bedroom 2's north wall.

SOLID ELEMENTS (drawn at NORMAL opacity, fully visible):

GROUND FLOOR (bottom half):
- A1. SERVER NICHE: a rectangular recess at the BASE of the spine wall (bottom-right area, below the staircase). Inside, small stacked components: a black mini-PC labeled "Beelink (HA + Frigate)", a router labeled "TP-Link AX55", a small switch labeled "TL-SG1210P PoE switch", a patch panel, and a "UPS". Overall label: "SERVER NICHE (below staircase)".
- A2. STAIRCASE: a flight of stairs ascending from the GF floor along the RIGHT side, against the spine wall, with a half-landing where it turns (dog-leg) and continues up to the FF. Draw it solid, light wood/stone treads. Small label "Staircase (up to FF)".
- A3. GF OPEN AREA on the LEFT: a simple dining table and a sofa, outlined. Label "GF Dining / Living".
- A4. GF FALSE CEILING: a thin horizontal layer across the top of the GF half, drawn semi-transparent (30 percent). Above it the concrete slab.

FIRST FLOOR (top half):
- B1. GF-to-FF concrete SLAB: horizontal band separating the floors.
- B2. FF LIVING on the LEFT: an open area with a railing edge (overlooking the void). Label "FF Living".
- B3. BEDROOM 2 on the RIGHT, on the far side of the spine wall: a STUDY DESK with a chair pushed against the spine wall (the desk is on the BEDROOM side / far face of the wall). Label "Bedroom 2 (balcony bedroom) - study desk".
- B4. FF FALSE CEILING: a thin horizontal layer across the top of the FF half, semi-transparent (30 percent).

X-RAY EFFECT:
- All WALLS (especially the spine wall), the floor SLAB, and both FALSE CEILINGS are SEMI-TRANSPARENT at about 30 percent opacity, so the grey conduits embedded inside are clearly visible.
- The server-niche components, staircase, furniture, AP discs, the touchscreen, and the desk wall-jack are SOLID (normal opacity).

THE FOUR CONDUITS (this is the main content). Each is exactly ONE solid grey 25mm PVC tube. ALL FOUR start at the SERVER NICHE and rise inside the single spine wall. NEVER draw two parallel tubes to the same endpoint - one tube per endpoint only.

1. "C-Niche-Waveshare" - the SHORTEST run:
   - From the niche, goes UP the spine wall only a short distance to about 1500mm height (eye level).
   - Terminates at a small WAVESHARE TOUCHSCREEN PANEL mounted flat ON the spine wall (a small rectangular tablet-like screen), positioned just ABOVE a small existing 2-module light switch.
   - Label with leader line: "C-Niche-Waveshare (HDMI + USB) -> staircase touchscreen".

2. "R-GF-1" - to the GF ceiling AP:
   - From the niche, UP the spine wall to GF false-ceiling level, then turns LEFT (north) and runs horizontally through the GF false ceiling void toward the LEFT, dropping slightly to terminate at the GF CEILING AP.
   - The GF CEILING AP is a round white disc mounted FLUSH on the GF false ceiling, on the LEFT, centered above the dining/living area.
   - Label the AP: "GF Ceiling AP (Ubiquiti UniFi U6-Lite or equiv, PoE)".
   - Label the conduit: "R-GF-1 (1x Cat6, PoE)".

3. "R-FF-1" - to the FF ceiling AP:
   - From the niche, UP the spine wall, PASSING THROUGH the GF false ceiling and THROUGH the GF-to-FF concrete slab, continuing up into the FF, to FF false-ceiling level, then turns LEFT (north) and runs through the FF false ceiling void to terminate at the FF CEILING AP.
   - The FF CEILING AP is a round white disc mounted FLUSH on the FF false ceiling, on the LEFT, centered above FF Living.
   - Label the AP: "FF Ceiling AP (Ubiquiti UniFi U6-Lite or equiv, PoE)".
   - Label the conduit: "R-FF-1 (2x Cat6, PoE)".

4. "R-FF-2" - to the Bedroom 2 study desk:
   - From the niche, UP the spine wall to FF level, then crosses to the BEDROOM 2 side (the FAR / right face of the spine wall) and DROPS DOWN to a small Cat6 wall jack at desk height (700mm) right behind the STUDY DESK.
   - Label the conduit: "R-FF-2 (1x Cat6) -> Bedroom 2 study desk".

DIRECTIONAL ANCHOR: a bold label with an arrow pointing into the niche reading "Source: Beelink + PoE switch in server niche (below staircase)".

A small compass hint in a corner: "LEFT = NORTH (open hall side)  /  RIGHT = SOUTH (staircase + Bedroom 2)".

LEGEND BOX in a lower corner (small clean text):
Line 1: "All 4 conduits: 25mm grey PVC, rise inside the ONE staircase wall"
Line 2: "Each conduit = ONE tube (Cat6 count shown is cables inside it)"
Line 3: "Ceiling APs are PoE only - no socket needed"
Line 4: "(R-FF-3 mirror drop to Bedroom 1 not shown for clarity)"

STRICT GEOMETRY RULES you MUST follow:
- There is ONLY ONE thick spine wall and ALL FOUR conduits rise inside it. Do not invent extra walls full of conduits.
- Exactly FOUR conduits, each a SINGLE grey tube. Never duplicate a tube to the same endpoint.
- All four conduits ORIGINATE at the server niche (right side, base of spine wall). They never appear from the left or the top.
- BOTH ceiling APs are on the LEFT (north). The GF AP on the GF false ceiling, the FF AP on the FF false ceiling. NEVER put an AP on a wall.
- The Waveshare touchscreen is ON the spine wall on the GROUND FLOOR at about 1500mm (eye level), above the light switch. NEVER on a ceiling, never on the FF.
- The Bedroom 2 study-desk wall jack is on the FF, on the FAR (bedroom) face of the spine wall, at desk height. NEVER on the ceiling, never on the GF.
- The server niche is at the BASE of the spine wall on the GF, on the RIGHT.

STYLE:
- Clean technical isometric architectural blueprint illustration; IKEA / Apple setup-guide aesthetic.
- Flat color palette, NO photographic realism.
- Warm beige semi-transparent walls/slab/ceilings (30 percent), light wood furniture and treads (solid), white solid AP discs with a small status LED, prominent solid grey conduits, thin black outlines, white background outside the building.
- Sans-serif labels, kept SHORT and legible. No people, no decorative clutter."""


def gemini_generate(api_key: str, max_retries: int = 5) -> bool:
    body = {
        "contents": [{"parts": [{"text": PROMPT}]}],
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
            print(f"  [attempt {attempt}/{max_retries}] calling Gemini...")
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            print(f"  -> response in {dt:.1f}s")
            for cand in data.get("candidates", []):
                content = cand.get("content", {})
                for part in content.get("parts", []):
                    inline = part.get("inlineData") or part.get("inline_data")
                    if inline and "data" in inline:
                        png_bytes = base64.b64decode(inline["data"])
                        OUT_PATH.write_bytes(png_bytes)
                        print(f"  OK saved {OUT_PATH.name} "
                              f"({len(png_bytes)/1024:.0f} KB)")
                        return True
                fr = cand.get("finishReason", "?")
                print(f"  X no image (finishReason={fr})")
                if fr in ("IMAGE_SAFETY", "PROHIBITED_CONTENT", "SAFETY"):
                    return False
            print(f"  X empty: {str(data)[:200]}")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")[:200]
            print(f"  X HTTP {e.code}: {err}")
            if e.code in (429, 500, 502, 503, 504):
                wait = 10 * attempt
                print(f"    transient - waiting {wait}s")
                time.sleep(wait)
                continue
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print(f"  X timeout: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            return False
        except Exception as e:
            print(f"  X error: {type(e).__name__}: {e}")
            return False
    return False


def backup_existing() -> None:
    if OUT_PATH.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = OUT_PATH.parent / f"{OUT_PATH.stem}_backup-{ts}.png"
        shutil.move(str(OUT_PATH), str(bak))
        print(f"  backed up old image -> {bak.name}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api-key")
    ap.add_argument("--regenerate", action="store_true")
    args = ap.parse_args()
    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY")
    if not api_key:
        print("X No API key.")
        return 1

    print(f"\nStaircase-wall conduit spine X-ray -> {OUT_PATH}\n")
    if OUT_PATH.exists() and not args.regenerate:
        print("Image already exists. Use --regenerate to force.")
        return 0
    if args.regenerate:
        backup_existing()
    if gemini_generate(api_key):
        print(f"\nOK Saved {OUT_PATH}")
        print(f"  Size: {OUT_PATH.stat().st_size / 1024:.1f} KB")
        return 0
    print("\nX Generation failed.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
