"""
Build the Waveshare Indoor Panel - Visual Install Guide PDF.

Generates 6 step-by-step technical illustrations via Gemini Nano Banana 2
(gemini-3.1-flash-image-preview) and assembles them into a single A4 PDF
site-handout for the carpenter, electrician, and homeowner.

Style: IKEA-assembly-instruction-style isometric line illustrations, consistent
across all 6 frames. Each frame is a numbered install step with a caption.

Requires:
  - fpdf2 (`pip3 install --user fpdf2`)
  - GOOGLE_AI_API_KEY environment variable OR --api-key arg
  - Internet connection to Gemini API

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_waveshare_install_guide_pdf.py
  # OR
  python3 build_waveshare_install_guide_pdf.py --api-key "your-key"
  # Force re-generation of all images even if they exist:
  python3 build_waveshare_install_guide_pdf.py --regenerate
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

from fpdf import FPDF

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).parent.parent
IMG_DIR = ROOT / "interior-design" / "generated-images" / "waveshare-install"
OUT_PDF = Path(__file__).parent / "WAVESHARE_INSTALL_GUIDE.pdf"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Gemini Generation
# --------------------------------------------------------------------------- #
MODEL = "gemini-3.1-flash-image-preview"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

# Shared visual style for all 6 images - consistency anchor
SHARED_STYLE = (
    "Style: Clean technical isometric illustration, in the style of IKEA "
    "assembly instructions or an Apple product setup guide. Flat color palette "
    "with no photographic shading: warm beige walls, light gray cables and "
    "conduit, walnut wood tones for the bezel frame, black thin outlines, "
    "subtle drop shadows only. White background. Text labels in plain English "
    "with thin black leader lines pointing to the labeled parts. Professional "
    "technical-manual layout. NEVER include any photographic or realistic "
    "rendering - keep it as clean diagrammatic illustration."
)

# 6-step install prompt set - each one carefully constructed using the
# 5-component formula (Subject + Action + Location + Composition + Style)
PROMPTS = [
    {
        "step": 1,
        "title": "Wall cross-section - what's behind the wall before install",
        "caption": (
            "A large rectangular masonry cavity (280 x 195 x 80 mm) is chased "
            "into the 9-inch staircase wall, centered at 1500 mm height. "
            "Three cables enter the cavity from the existing 25mm grey "
            "conduit at the bottom: HDMI, USB, and a spare Cat6. They are "
            "coiled into a service loop inside the cavity, ready for the "
            "screen assembly. Below the cavity, vertically aligned, sits the "
            "existing 2-module light switch box for the staircase lights "
            "(2-way switch with another switch at the top of the stairs)."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric cutaway illustration showing the "
            "inside of a residential wall. The wall material is shown in "
            "cutaway with warm beige interior, revealing a large rectangular "
            "recess chased into the masonry. The recess is labeled as a "
            "masonry cavity, 280 mm wide by 195 mm tall by 80 mm deep, "
            "centered at 1500 mm above the floor. A vertical 25mm grey PVC "
            "conduit enters the bottom of this cavity through a small round "
            "hole. Inside the conduit, three cables are visible: a blue Cat6 "
            "ethernet cable labeled SPARE, a flat black HDMI cable, and a "
            "thin white USB cable. The three cable ends are coiled into a "
            "neat service loop inside the masonry cavity, ready to plug into "
            "a future screen. Below the masonry cavity, with about 200 mm "
            "clear gap, sits a smaller existing rectangular 2-module switch "
            "box for the staircase light (a typical Indian modular switch "
            "back box, two switches side by side). Below the switch box on "
            "the wall: visible the first few stairs of the staircase. Labels "
            "with thin black leader lines pointing to each part: 'Custom "
            "masonry cavity 280 x 195 x 80 mm at 1500 mm FFL', '25 mm grey "
            "PVC conduit', 'HDMI cable to Beelink', 'USB cable to Beelink', "
            "'Existing Cat6 (SPARE)', '200 mm gap', 'Existing 2M switch box "
            "for staircase light at 1200 mm FFL'. " + SHARED_STYLE
        ),
    },
    {
        "step": 2,
        "title": "Bench assembly - putting the mount, screen and NFC reader together",
        "caption": (
            "Off-site, the carpenter prepares the walnut bezel with a plywood "
            "sub-frame, four magnetic catches at the corners, and ventilation "
            "slots in the top and bottom bezel. You mount the Waveshare screen "
            "to the sub-frame via four small brass standoffs, and stick the "
            "ACR122U NFC reader to the inside of the lower-right bezel where "
            "it stays hidden but still reads taps through the wood."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric illustration showing components laid "
            "out on a flat workbench surface, ready for assembly. From front "
            "to back: a rectangular walnut wood bezel frame with mitred 45 "
            "degree corners and visible ventilation slots in the top and "
            "bottom edges; a light plywood sub-frame fitted behind the bezel; "
            "a thin black 10.1-inch touchscreen panel positioned to mount "
            "face-down onto the sub-frame via four small brass standoffs at "
            "the corners; a small black NFC reader module (rectangular, about "
            "the size of a credit card) shown attached to the inside lower-"
            "right of the bezel; four small silver neodymium magnets visible "
            "at the four corners of the sub-frame. Two cables coiled to the "
            "side: one HDMI, one USB. Labels with thin black leader lines: "
            "'Walnut bezel (mitred corners)', 'Plywood sub-frame', 'Waveshare "
            "10.1 inch touchscreen', 'NFC reader (hidden behind bezel)', "
            "'Neodymium magnetic catch (x4)', 'M3 brass standoff (x4)', "
            "'Ventilation slots (top + bottom)'. " + SHARED_STYLE
        ),
    },
    {
        "step": 3,
        "title": "Connecting the cables to the back of the screen",
        "caption": (
            "Pull the HDMI and USB cables out of the back box (they have "
            "extra slack - the service loop). Plug them into the matching "
            "ports on the back of the screen. The USB cable carries both the "
            "touch signal and 5V power. Don't tighten anything yet - you'll "
            "push the whole assembly back into the wall next."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric close-up illustration showing the "
            "back of an assembled rectangular walnut-framed touchscreen unit. "
            "Two hands (drawn as simple outlined shapes, no detailed skin) "
            "are connecting two cables: one hand holding an HDMI plug being "
            "inserted into a labelled HDMI port on the back of the screen, "
            "the other hand inserting a micro-USB plug into the screen's USB "
            "port. The cables visibly trail away into a wall back box opening "
            "behind the unit, with some service loop slack visible. Labels "
            "with thin black leader lines: 'HDMI plug into screen', 'USB "
            "plug into screen (carries touch + 5V power)', 'Service loop "
            "leaves slack for later service'. " + SHARED_STYLE
        ),
    },
    {
        "step": 4,
        "title": "Pushing the assembly into the wall cavity - magnets engage",
        "caption": (
            "Hold the walnut bezel flat against the wall, lined up with the "
            "rectangular cavity opening, and push gently. The four neodymium "
            "magnets in the corners catch onto matching steel strike plates "
            "fixed to the cavity walls with a soft click. The bezel sits "
            "flush around the cavity opening, projecting only 3-5mm from the "
            "wall surface - a subtle shadow line, not a tablet bolted on the "
            "wall. Below the new screen, the existing 2M staircase light "
            "switch box is visible, vertically aligned with the cavity."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric front-view illustration of a "
            "rectangular walnut-framed touchscreen panel being pushed into a "
            "matching rectangular cavity in a residential wall. The cavity "
            "is clearly larger than a switch box - it is a custom masonry "
            "rectangular opening sized 280 x 195 mm. The walnut bezel is "
            "wider than the cavity (about 320 x 235 mm), so it overhangs the "
            "cavity edge on all four sides. Two simple outlined hands hold "
            "the bezel and push it gently forward. Around the four corners "
            "of the bezel, small arrows indicate magnetic catches engaging "
            "with strike plates inside the cavity walls, each arrow with a "
            "tiny 'click' indicator. Cables visible behind the panel fold "
            "neatly into the cavity space. The wall is shown as a light "
            "beige flat surface. The bezel finished install position projects "
            "only 3-5mm from the wall (shown in a small inset side view "
            "below the main illustration). Below the new screen assembly on "
            "the wall: an existing smaller 2-module light switch box is "
            "visible, vertically aligned with the screen above, with about "
            "200 mm clear gap between the cavity bottom and the switch top. "
            "Labels with thin black leader lines: 'Push gently - magnets "
            "engage with click (x4)', 'Bezel projects 3-5mm from wall', "
            "'Cables fold into masonry cavity behind panel', 'Walnut bezel "
            "overhangs cavity edge by 20-25 mm each side', 'Existing 2M "
            "staircase light switch below'. " + SHARED_STYLE
        ),
    },
    {
        "step": 5,
        "title": "Finished install - screen showing Home Assistant dashboard",
        "caption": (
            "The completed staircase panel: walnut bezel sitting flush with "
            "the wall at 1500 mm FFL, screen showing the Home Assistant "
            "dashboard (water tank levels, light controls, doorbell tile, "
            "music, weather). The small brass 'tap here' dot in the lower-"
            "right corner of the bezel marks where to tap a phone or NFC "
            "sticker to trigger a scene. Vertically aligned below the "
            "screen with about 200 mm gap is the existing 2-module switch "
            "for the staircase light (a 2-way switch - same control point "
            "as the top of the stairs), creating a clean vertical control "
            "stack near the bottom of the staircase."
        ),
        "aspect_ratio": "3:4",
        "prompt": (
            "A clean technical isometric front-view illustration of a "
            "finished installed touchscreen panel on a residential staircase "
            "wall, near the bottom of the stairs. The walnut wood bezel "
            "(approximately 320 mm wide by 235 mm tall) is flush against a "
            "light beige wall, with subtle shadow at the edges. The screen "
            "inside the bezel shows a smart home dashboard interface with "
            "clean rectangular tiles: two vertical cylindrical gauges "
            "labelled 'Overhead tank' and 'Sump' showing water levels; a "
            "small camera-view tile labelled 'Doorbell'; a grid of toggle "
            "buttons labelled 'Lights'; a music player tile; a small weather "
            "tile. The dashboard tiles use cool blue and warm orange accent "
            "colors on a dark background. In the lower-right corner of the "
            "walnut bezel, a small brass-colored dot marks the NFC tap "
            "location. Below the screen on the wall, with about 200 mm "
            "vertical gap, is the existing rectangular 2-module wall switch "
            "box (a typical Indian modular switch plate with two rocker "
            "switches for the staircase light, mounted at about 1200 mm "
            "above the floor). The first one or two steps of the staircase "
            "are visible at the bottom of the image. Labels at the side, "
            "with thin leader lines: 'Walnut bezel flush with wall (1500 mm "
            "FFL)', 'Home Assistant dashboard', 'Brass NFC tap dot - tap "
            "phone here', '200 mm clear gap', 'Existing 2M staircase light "
            "switch (2-way, ~1200 mm FFL)'. " + SHARED_STYLE
        ),
    },
    {
        "step": 6,
        "title": "Service mode - pulling the panel forward for maintenance",
        "caption": (
            "If anything inside needs service - screen replacement, cable "
            "swap, NFC reader change - grip the bezel and pull straight out. "
            "Magnets release with a soft pop, and the whole assembly slides "
            "forward about 150mm on the cable service loop. No need to "
            "unplug anything. When done, push back in - magnets catch, click "
            "into place, flush again. No wall damage, no tools."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric three-quarter view illustration of "
            "a walnut-framed touchscreen panel pulled forward from a wall by "
            "about 150mm. The assembly is partially out of the wall opening, "
            "with cables visibly stretched but still connected - they trail "
            "from inside the wall back box to ports on the back of the unit. "
            "Around the four corners, the magnetic catches are shown "
            "disengaged with small motion arrows indicating they have just "
            "released. A simple outlined hand grips the bottom of the bezel, "
            "pulling it forward. The back of the panel is partly visible, "
            "revealing the small NFC reader module attached to the inside of "
            "the bezel, and the back-of-screen connectors. Labels with thin "
            "black leader lines: 'Grip bezel, pull straight forward', "
            "'Magnets release (x4) - soft pop', 'Service loop on cables - "
            "no need to unplug', 'Slide unit out for screen, NFC reader, or "
            "cable replacement', 'Push back in when done - magnets re-engage'."
            " " + SHARED_STYLE
        ),
    },
]


def gemini_generate(prompt: str, aspect_ratio: str, api_key: str,
                    out_path: Path, max_retries: int = 5) -> bool:
    """Call Gemini API to generate one image. Saves PNG to out_path."""
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": "1K",  # 1K = ~145 DPI at 180mm PDF width - plenty
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
                  f"(may take 30-120s for 2K image)...")
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            print(f"  → received response in {dt:.1f}s")

            # Walk response → find first inline image
            for cand in data.get("candidates", []):
                content = cand.get("content", {})
                for part in content.get("parts", []):
                    inline = part.get("inlineData") or part.get("inline_data")
                    if inline and "data" in inline:
                        png_bytes = base64.b64decode(inline["data"])
                        out_path.write_bytes(png_bytes)
                        print(f"  ✓ saved {out_path.name} "
                              f"({len(png_bytes)/1024:.0f} KB)")
                        return True
                # If we got here without an image, check finishReason
                fr = cand.get("finishReason", "?")
                print(f"  ✗ no image in response (finishReason={fr})")
                if fr in ("IMAGE_SAFETY", "PROHIBITED_CONTENT", "SAFETY"):
                    return False  # don't retry safety blocks
            # No candidates at all
            print(f"  ✗ empty response: {str(data)[:300]}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  ✗ HTTPError {e.code}: {err_body}")
            if e.code in (429, 500, 502, 503, 504):
                wait = 10 * attempt
                print(f"    transient {e.code} - waiting {wait}s and retrying")
                time.sleep(wait)
                continue
            return False
        except (TimeoutError, urllib.error.URLError) as e:
            print(f"  ✗ network/timeout error: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            return False
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ unexpected error: {type(e).__name__}: {e}")
            return False

    return False


# --------------------------------------------------------------------------- #
# PDF Assembly
# --------------------------------------------------------------------------- #
class InstallGuidePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(14, 14, 14)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(80, 50, 20)
        self.cell(0, 6,
                  "Waveshare Staircase Panel - Visual Install Guide", ln=0,
                  align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", ln=1)
        self.set_draw_color(180, 140, 70)
        self.line(14, 23, 196, 23)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6,
                  "v1.0 - 2026-05-28 - hand to carpenter + electrician + "
                  "homeowner",
                  align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(80, 50, 20)
        self.cell(0, 14, text, ln=1)
        self.ln(2)

    def h2(self, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(80, 60, 30)
        self.set_fill_color(248, 240, 220)
        self.cell(0, 10, text, ln=1, fill=True)
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)


def build_pdf(api_key: str | None, regenerate: bool) -> int:
    print(f"\nBuilding Waveshare Install Guide PDF → {OUT_PDF}\n")

    # Step 1: Ensure all 6 images exist
    missing_images = []
    for spec in PROMPTS:
        img_path = IMG_DIR / f"install-step-{spec['step']}.png"
        if regenerate or not img_path.exists():
            missing_images.append(spec)

    if missing_images:
        if not api_key:
            print(f"✗ {len(missing_images)} image(s) need generation but no "
                  "API key provided.")
            print("  Set GOOGLE_AI_API_KEY env var or use --api-key flag.")
            print("  Free key: https://aistudio.google.com/apikey\n")
            return 1
        print(f"Generating {len(missing_images)} image(s) via Gemini "
              "(this can take 5-15 min total at 2K)...\n")
        for spec in missing_images:
            print(f"Step {spec['step']}/6: {spec['title']}")
            img_path = IMG_DIR / f"install-step-{spec['step']}.png"
            ok = gemini_generate(
                spec["prompt"], spec["aspect_ratio"], api_key, img_path
            )
            if not ok:
                print(f"\n✗ Failed to generate step {spec['step']}. "
                      "Aborting PDF build.")
                return 2
    else:
        print("All 6 images already exist; skipping regeneration "
              "(use --regenerate to force).")

    # Step 2: Assemble PDF
    print("\nAssembling PDF...")
    pdf = InstallGuidePDF()

    # ---- Cover page ----
    pdf.add_page()
    pdf.set_y(50)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(80, 50, 20)
    pdf.cell(0, 16, "Waveshare Staircase Panel", ln=1, align="C")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(140, 100, 50)
    pdf.cell(0, 10, "Visual Install Guide - 6 steps", ln=1, align="C")
    pdf.ln(14)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    intro = (
        "This guide walks the carpenter, electrician, and homeowner through "
        "installing the staircase-wall Waveshare 10.1\" smart display panel. "
        "Six numbered steps with technical diagrams take you from the "
        "pre-plaster wall state through to a finished, serviceable "
        "installation.\n\n"
        "Architecture: the screen is driven directly by the Beelink mini-PC "
        "in the server niche below, via HDMI + USB cables through the "
        "existing 25mm conduit (no Pi at the panel). NFC reader hidden "
        "behind the lower-right bezel allows tap-to-scene from a phone or "
        "sticker tag. The walnut mount uses 4 magnetic catches so the entire "
        "assembly can be pulled forward for service without wall damage."
    )
    pdf.multi_cell(0, 6, intro)
    pdf.ln(8)

    pdf.set_fill_color(248, 240, 220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(80, 50, 20)
    pdf.cell(0, 9, "  Quick reference", ln=1, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    qref = (
        "  Location:   Staircase South wall, 1500mm FFL\n"
        "  Conduit:    C-Niche-Waveshare (25mm grey PVC, ~2m)\n"
        "  Cables:     Cat6 (spare) + HDMI + USB-A inside conduit\n"
        "  Brain:      Beelink mini-PC in server niche below\n"
        "  Mount:      Recessed walnut bezel + 4-magnet service hatch\n"
        "  Reference:  electrical/WAVESHARE_INDOOR_PANEL.md (full spec)\n"
    )
    pdf.multi_cell(0, 6, qref)
    pdf.ln(4)

    # ---- Step pages - 1 per page, image + caption ----
    for spec in PROMPTS:
        img_path = IMG_DIR / f"install-step-{spec['step']}.png"
        pdf.add_page()
        pdf.h2(f"Step {spec['step']} - {spec['title']}")
        # Image: max width 180mm, scaled to fit
        if img_path.exists():
            try:
                # Place image, fpdf2 will preserve aspect ratio if h omitted
                pdf.image(str(img_path), x=14, y=pdf.get_y(), w=180)
                # Move cursor down - estimate image height from aspect ratio
                ar_w, ar_h = spec["aspect_ratio"].split(":")
                img_height = 180 * (int(ar_h) / int(ar_w))
                pdf.set_y(pdf.get_y() + img_height + 4)
            except Exception as e:
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(150, 50, 50)
                pdf.cell(0, 8, f"[image error: {e}]", ln=1)
        else:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(150, 50, 50)
            pdf.cell(0, 8, "[image missing - re-run with --regenerate]", ln=1)

        pdf.body(spec["caption"])

    # ---- Final page - credits + cross-refs ----
    pdf.add_page()
    pdf.h2("Reference and next steps")
    refs = (
        "Full hardware + mount spec:\n"
        "  electrical/WAVESHARE_INDOOR_PANEL.md (15-section site handout)\n\n"
        "Related conduit documentation:\n"
        "  electrical/conduits-and-cavities.md (C-Niche-Waveshare row)\n\n"
        "Decision history:\n"
        "  decisions/decision-log.md (2026-05-25 v3.0 entry)\n\n"
        "Next session - once panel is installed:\n"
        "  Home Assistant dashboard layout (separate session, live editing "
        "on the actual panel)\n\n"
        "Dining hall companion panel (future):\n"
        "  Cat6 stub already provisioned via C-Niche-Dining conduit. "
        "Architecture: Pi-at-screen wired, matching the foyer welcome system "
        "pattern. Install when interior designer's cantilever shelf design "
        "is finalised."
    )
    pdf.body(refs)

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT_PDF))
    print(f"\n✓ PDF written to {OUT_PDF}")
    print(f"  Size: {OUT_PDF.stat().st_size / 1024:.1f} KB")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api-key", help="Google AI API key (or set "
                                      "GOOGLE_AI_API_KEY env)")
    ap.add_argument("--regenerate", action="store_true",
                    help="Force re-generation of all 6 images")
    args = ap.parse_args()
    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY")
    return build_pdf(api_key, args.regenerate)


if __name__ == "__main__":
    sys.exit(main())
