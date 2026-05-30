"""
Generate the Wi-Fi AP X-Ray Conduit Map.

A 2-floor sectional cutaway showing the Cat6 conduit runs from the staircase
server niche to:
  - GF false ceiling AP (above dining/living junction)
  - FF false ceiling AP (FF Living central)
  - FF bedroom study desk drops (R-FF-2 + R-FF-3)

Output: interior-design/generated-images/conduit-maps/wifi-ap-conduit-map.png

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_wifi_ap_conduit_map.py              # generates if missing
  python3 build_wifi_ap_conduit_map.py --regenerate # backup existing, regen
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
OUT_PATH = OUT_DIR / "wifi-ap-conduit-map.png"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3.1-flash-image-preview"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

PROMPT = """A clean technical isometric X-ray architectural cutaway illustration showing TWO FLOORS of a modern Indian residential home (Ground Floor and First Floor) in a single image, viewed in vertical CROSS-SECTION from the South side looking NORTH. The image must clearly show the vertical relationship between the staircase server niche on the WEST side and three ceiling/wall AP termination points distributed across both floors.

CRITICAL VIEWING GEOMETRY (read carefully):

- This is a VERTICAL CROSS-SECTION view of the house, looking from the SOUTH toward the NORTH.
- The image is wider than tall (landscape orientation).
- LEFT side of image = WEST side of house (where the staircase + server niche live).
- RIGHT side of image = EAST side of house (kitchen / bedrooms).
- BOTTOM of image = Ground Floor (GF).
- TOP of image = First Floor (FF) with false ceiling above.
- The image shows a 2-floor cutaway: GF on bottom half, FF on top half, with floor slab between them.

ROOM ELEMENTS (drawn at NORMAL OPACITY, solid):

A. GROUND FLOOR (bottom half of image):

A1. SERVER NICHE - a small rectangular recess in the LEFT side of the GF (west side, on the staircase wall). Inside the niche, visible: a small black mini-PC labeled "Beelink (HA + Frigate)", a TP-Link router labeled "TP-Link AX55 router", a small PoE network switch labeled "TL-SG1210P PoE switch", a 12-port patch panel, and a UPS - drawn as small stacked components. Labeled overall: "SERVER NICHE (GF, west side, on staircase wall)".

A2. GF FLOOR with tiled finish (bottom edge of GF half).

A3. GF OPEN AREA - the central area of the GF half showing the open dining/living junction: a rectangular dining table on the right portion, a sofa or living seating on the left portion. Simple outlined furniture. Label: "GF Open Dining/Living junction".

A4. GF FALSE CEILING - a horizontal layer across the top of the GF half, drawn semi-transparent (30 percent opacity). Above this false ceiling is the GF concrete slab (the floor of FF above).

A5. GF CEILING AP - a small round disc mounted FLUSH on the GF false ceiling, CENTERED above the dining/living junction. Round white disc with a subtle status LED. Label: "GF Ceiling AP (Ubiquiti UniFi U6-Lite or equivalent, PoE-powered)".

B. FIRST FLOOR (top half of image):

B1. GF-TO-FF FLOOR SLAB - horizontal concrete layer separating the two floors.

B2. FF FLOOR with finished tile.

B3. FF LIVING + BEDROOM AREA - on the right side of the FF half, draw an outlined STUDY DESK with a chair against the FF bedroom wall. On the left side of the FF half, draw a small balcony silhouette. Between them, the central FF Living area. Labels: "FF Bedroom (with study desk)", "FF Living (central)", "FF Balcony" (small).

B4. FF FALSE CEILING - a horizontal layer across the top of the FF half, drawn semi-transparent (30 percent opacity).

B5. FF CEILING AP - a small round disc mounted FLUSH on the FF false ceiling, CENTERED above the FF Living area. Round white disc. Label: "FF Ceiling AP (Ubiquiti UniFi U6-Lite or equivalent, PoE-powered)".

B6. FF STUDY DESK WALL JACK - a small Cat6 keystone wall plate on the wall above the study desk at desk height (700 mm above FF floor). Label: "Study desk Cat6 jack (R-FF-2 or R-FF-3 termination)".

C. ROOF / TERRACE (very top edge of image): light beige horizontal line indicating roof, no detail needed.

X-RAY EFFECT (the core visual technique):

- All WALLS, FLOORS (the GF-to-FF slab), and FALSE CEILINGS are rendered SEMI-TRANSPARENT at about 30 percent opacity (you can see THROUGH them).
- This reveals the Cat6 conduit runs embedded INSIDE walls and ceilings as SOLID GREY PVC CYLINDRICAL TUBES.
- The server niche components, furniture, AP discs, wall jacks, doors, and floor tiles are drawn at NORMAL OPACITY (solid, fully visible).

X-RAY CONDUITS (this is the main visual content):

All four conduits ORIGINATE at the SERVER NICHE (left side, GF). Each is drawn as a solid grey 25mm PVC tube.

C1. "R-GF-1" (NEW, locked 2026-05-29):
- Exits the top of the server niche
- Goes UP through the staircase wall to GF false ceiling level
- Then turns HORIZONTAL and runs EAST through the GF false ceiling void
- DROPS DOWN slightly and terminates at the GF CEILING AP junction box (centered above dining/living)
- Label with leader line: "R-GF-1 (25mm grey, ~6-8m) - PoE Cat6 to GF ceiling AP - NEW conduit locked 2026-05-29"

C2. "R-FF-1" (UPDATED, locked 2026-05-29):
- Also exits the top of the server niche
- Travels UP THROUGH the staircase wall, PASSING THROUGH the GF false ceiling, PASSING THROUGH the GF-to-FF floor slab, continuing UP into the FF level
- Then turns HORIZONTAL at FF false ceiling level and runs EAST through the FF false ceiling void
- Terminates at the FF CEILING AP junction box (centered above FF Living)
- Label with leader line: "R-FF-1 (25mm grey, 2x Cat6 + pull-string) - PoE Cat6 to FF ceiling AP (UPDATED 2026-05-29: terminates at CEILING, no longer wall plate at 2400mm)"

C3. "R-FF-2":
- Also exits the top of the server niche
- Travels UP through the staircase wall alongside R-FF-1
- At FF level branches off horizontally toward the FF bedroom
- DROPS DOWN through the FF bedroom wall to desk height (700 mm above FF floor)
- Terminates at the study desk Cat6 jack
- Label with leader line: "R-FF-2 (25mm grey, 1x Cat6) - wired Cat6 drop to bedroom study desk"

C4. "R-FF-3" (optional, draw as a thin dotted parallel line to R-FF-2 to indicate a similar drop for the other bedroom):
- Same routing pattern as R-FF-2 but to the OTHER bedroom (mirror)
- Label group: "R-FF-3 (25mm grey, 1x Cat6) - mirror drop to other bedroom study desk"

All four conduits should be drawn as SOLID GREY and clearly distinguishable. Each terminates with a small round PVC fitting symbol at its endpoint.

DIRECTIONAL ANCHOR: A bold label near the server niche reading "Source: Beelink + TL-SG1210P PoE switch in server niche" with a small arrow pointing into the niche components.

LEGEND BOX in lower-right corner (small clean text):
Line 1: "All conduits: 25mm grey PVC"
Line 2: "Inside each: 1x or 2x Cat6 + pull-string"
Line 3: "Powered by PoE on TL-SG1210P switch"
Line 4: "AP model placeholder: Ubiquiti UniFi U6-Lite (or equivalent: TP-Link EAP670, Aruba AP22)"

STRICT GEOMETRY RULES that you MUST FOLLOW:

- This MUST be a vertical 2-floor cross-section. GF below, FF above. Floor slab between them.
- All conduits ORIGINATE on the LEFT side (server niche). They never appear from the right or top.
- The GF AP MUST be on the GF false ceiling (top of GF half, below the floor slab). NEVER on a wall, NEVER on the FF ceiling.
- The FF AP MUST be on the FF false ceiling (top of FF half). NEVER on a wall, NEVER on the GF ceiling.
- The study desk wall jack MUST be on the FF bedroom wall at desk height (not on the floor, not on the ceiling).
- The server niche is on the LEFT (west). All conduits exit it going RIGHT (east) or UP.

STYLE REQUIREMENTS:

- Clean technical isometric architectural blueprint illustration
- IKEA assembly manual aesthetic (similar to Apple "How to set up your Mac" or building cross-section diagrams)
- Flat color palette only - NO photographic shading or realism
- Warm beige semi-transparent walls, floors, and ceilings (30 percent opacity)
- Light wood tones for furniture (solid normal opacity)
- White solid discs for the APs with a small status LED indicator
- Solid prominent grey for all conduits
- Thin black outlines on all elements
- White background outside the building boundary
- Sans-serif font for all labels
- NEVER include any people, decorative items, or extra elements
- The image must function as a PERMANENT POST-PLASTER REFERENCE so the homeowner and electrician can identify the Wi-Fi AP cabling network at a glance"""


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

    print(f"\nWi-Fi AP X-ray conduit map -> {OUT_PATH}\n")
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
