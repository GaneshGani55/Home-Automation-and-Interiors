"""
Generate the Dining Hall X-Ray Conduit Map.

A single reference image showing the dining hall room with semi-transparent
walls and ceiling, so the homeowner and electrician can identify what each
conduit is for AFTER plaster/paint hide them physically.

Output: interior-design/generated-images/conduit-maps/dining-xray-conduit-map.png

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_dining_conduit_map.py             # generates if missing
  python3 build_dining_conduit_map.py --regenerate # force regenerate
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "interior-design" / "generated-images" / "conduit-maps"
OUT_PATH = OUT_DIR / "dining-xray-conduit-map.png"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3.1-flash-image-preview"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

PROMPT = """A clean technical isometric X-ray architectural cutaway illustration of a residential dining hall in a modern Indian home.

CRITICAL VIEWING ANGLE - this is the most important geometric constraint:

- The viewer stands in the WEST half of the dining hall, looking EAST.
- This means: the EAST WALL is the BACK WALL of the image (the far wall, in the background).
- The viewer's LEFT hand points NORTH; the viewer's RIGHT hand points SOUTH.
- BEHIND the viewer (out of frame, to the west) is the pooja area and then further west the staircase niche / server cabinet.
- Through the East wall (the back wall of this image) is the kitchen.
- The dining table sits between the viewer and the East wall, in the FOREGROUND-to-MIDDLE of the room.

Room layout reference (plan view from above, for your understanding only - do NOT draw this layout sketch in the actual image):

                NORTH
                  |
   [Pooja] - [DINING HALL] - [Kitchen]
    WEST     (table center)    EAST
                  |
                SOUTH

   Server niche is far WEST, behind the viewer.

ROOM ELEMENTS TO DRAW with their CORRECT positions:

1. DINING TABLE - rectangular wooden table with 4 chairs, sitting in the foreground-to-middle of the image (between viewer and east wall). Drawn at normal opacity (solid).

2. CANTILEVER KITCHEN CABINET - mounted FLAT AGAINST the EAST WALL (the BACK wall of the image). It has horizontal floating shelves with a plywood backing board. This is a vertical wall-mounted unit attached to the vertical East wall. Drawn at normal opacity.

3. FUTURE WAVESHARE 10.1 inch TOUCHSCREEN - this is a SMALL FLAT RECTANGULAR OUTLINE mounted on the PLYWOOD BACKING of the cantilever cabinet, embedded into the EAST WALL surface. ABSOLUTELY CRITICAL: this is a WALL-MOUNTED screen on the EAST WALL (a VERTICAL surface). IT IS NOT ON THE CEILING. IT IS NOT HORIZONTAL. IT IS NOT FLOATING IN MID-AIR. The screen is at standing eye height (about 1500mm above floor), vertical orientation, behind the plywood mount of the cantilever cabinet. Label this with a thin leader line: "Future Waveshare 10.1 inch touchscreen (WALL-MOUNTED on East wall behind cantilever plywood)".

4. FUTURE CEILING SPEAKER - a SMALL ROUND or RECTANGULAR junction box embedded FLUSH in the FALSE CEILING, directly above the center of the dining table. ABSOLUTELY CRITICAL: this is a HORIZONTAL element on the CEILING surface, facing downward. THIS IS A DIFFERENT THING FROM THE WAVESHARE TOUCHSCREEN. The speaker location is overhead, on the ceiling, NOT on any wall. Label with leader line: "Future ceiling speaker location (CEILING-MOUNTED, centered above dining table on false ceiling)".

5. SIMPLE LIGHT WOOD FLOOR visible at the bottom edge.

X-RAY EFFECT - the core visual technique:

- The walls AND the false ceiling are rendered SEMI-TRANSPARENT at about 30 percent opacity (you can see through them).
- This reveals the electrical conduits embedded INSIDE the walls and ceiling, drawn as SOLID GREY PVC CYLINDRICAL TUBES.
- The furniture, cantilever cabinet, screen position outline, and ceiling speaker junction box are drawn at NORMAL OPACITY (solid, fully visible).

X-RAY CONDUITS - this is the most important visual content:

Both conduits originate to the WEST (behind the viewer, out of frame to the LEFT edge of the image where the server niche lives).

Conduit 1 (called "C-Niche-Dining"):
- Enters the image from the LEFT edge of the frame (the west side, where the viewer's left would be)
- Travels EAST through the FALSE CEILING VOID (a long horizontal run across the top portion of the image)
- When it reaches the East wall (the back wall of the image), it DROPS DOWN VERTICALLY through the East wall
- Terminates at the WAVESHARE TOUCHSCREEN POSITION (behind the plywood mount of the cantilever cabinet, on the East wall)
- Label with leader line: "C-Niche-Dining conduit (25mm grey PVC, approx 12 metres total) - PoE Cat6 for the Waveshare touchscreen Pi"

Conduit 2 (called "C-Niche-DiningSpeaker"):
- Enters the image from the same LEFT edge of the frame
- Also travels EAST through the FALSE CEILING VOID
- Drops DOWN slightly (or terminates from above) at the CEILING JUNCTION BOX centered above the dining table
- Does NOT continue all the way to the East wall
- Label with leader line: "C-Niche-DiningSpeaker conduit (25mm grey PVC, approx 10 metres total) - PoE Cat6 for future ceiling speaker"

Both conduits are drawn as SOLID GREY, PROMINENT, and clearly distinguishable from the semi-transparent walls and ceiling. Each conduit has a small round PVC fitting symbol at its termination point.

DIRECTIONAL ARROW: Bold arrow on the LEFT edge of the image at the point where the conduits exit westward out of frame, with the text label: "TO SERVER NICHE (staircase wall, west side of house)" with an arrowhead pointing LEFT.

LEGEND BOX in the lower-right corner of the image (small clean text):
Line 1: "Both conduits: 25mm grey PVC"
Line 2: "Inside each: 1x Cat6 + pull-string"
Line 3: "Both terminate at server niche (west)"

STRICT GEOMETRY RULES that you MUST FOLLOW:

- The Waveshare touchscreen MUST be on the East wall (the BACK wall of the image, a VERTICAL surface). NEVER on the ceiling. NEVER floating in mid-air. NEVER on the floor.
- The ceiling speaker junction box MUST be on the ceiling (a HORIZONTAL overhead surface). NEVER on a wall.
- The conduits MUST enter from the LEFT side of the image (representing the west direction) and travel rightward (east) through the false ceiling void.
- The East wall MUST be in the BACK of the image (the far wall, the wall the viewer is facing).
- The dining table MUST be in the foreground/middle, NOT against the East wall.
- The cantilever cabinet MUST be against the East wall (the back wall).

STYLE REQUIREMENTS:

- Clean technical isometric architectural blueprint illustration
- IKEA assembly manual aesthetic (similar to Apple "How to set up your Mac" diagrams)
- Flat color palette only - NO photographic shading or realism
- Warm beige semi-transparent walls and ceiling (30 percent opacity)
- Light wood tones for furniture and cantilever cabinet (solid normal opacity)
- Solid prominent grey for the conduits
- Thin black outlines on all elements
- White background outside the room boundary
- Sans-serif font for all labels
- NEVER include any people, decorative items, or extra elements
- The image must function as a PERMANENT REFERENCE for the homeowner and electrician AFTER plaster and paint are done"""


def gemini_generate(api_key: str, max_retries: int = 5) -> bool:
    """Call Gemini API to generate the image. Saves PNG to OUT_PATH."""
    body = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "3:2",  # architectural landscape ratio
                "imageSize": "2K",  # high-res reference image
            },
        },
    }
    url = f"{API_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            print(f"  [attempt {attempt}/{max_retries}] calling Gemini API "
                  f"(2K image can take 30-180s)...")
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            print(f"  -> received response in {dt:.1f}s")

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
                print(f"  X no image in response (finishReason={fr})")
                if fr in ("IMAGE_SAFETY", "PROHIBITED_CONTENT", "SAFETY"):
                    return False
            print(f"  X empty response: {str(data)[:300]}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  X HTTPError {e.code}: {err_body}")
            if e.code in (429, 500, 502, 503, 504):
                wait = 10 * attempt
                print(f"    transient {e.code} - waiting {wait}s and retrying")
                time.sleep(wait)
                continue
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print(f"  X network/timeout error: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            return False
        except Exception as e:
            print(f"  X unexpected error: {type(e).__name__}: {e}")
            return False

    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api-key", help="Google AI API key (or set GOOGLE_AI_API_KEY env)")
    ap.add_argument("--regenerate", action="store_true",
                    help="Force regeneration even if image exists")
    args = ap.parse_args()
    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY")

    print(f"\nDining hall X-ray conduit map -> {OUT_PATH}\n")

    if OUT_PATH.exists() and not args.regenerate:
        print(f"Image already exists at {OUT_PATH}")
        print("Use --regenerate to force a fresh generation.")
        return 0

    if not api_key:
        print("X No API key. Set GOOGLE_AI_API_KEY env or use --api-key.")
        print("  Get a free key: https://aistudio.google.com/apikey")
        return 1

    print("Generating via Gemini Nano Banana 2...")
    if gemini_generate(api_key):
        print(f"\nOK Saved {OUT_PATH}")
        print(f"  Size: {OUT_PATH.stat().st_size / 1024:.1f} KB")
        return 0
    else:
        print("\nX Generation failed. See errors above.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
