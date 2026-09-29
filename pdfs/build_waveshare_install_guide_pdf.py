"""
Build the Waveshare Indoor Panel - Visual Install Guide PDF.

Generates step-by-step technical illustrations via Gemini Nano Banana 2
(gemini-3.1-flash-image-preview) and assembles them into a single A4 PDF
site-handout for the carpenter, electrician, and homeowner. Step 3 (the plug
diagram) is drawn in code by waveshare_plug_diagram.py instead - free, exact,
and redrawn on every run.

Style: IKEA-assembly-instruction-style isometric line illustrations, consistent
across all 6 frames. Each frame is a numbered install step with a caption.

v2.0 (2026-09-28) matches electrical/WAVESHARE_INDOOR_PANEL.md v3.3: the
Waveshare 10.1" (G) screen takes its own 12V/2A power (not over the USB), so
there are 3 L-shaped plugs at the screen; it is a tight fit in the cavity; the
server is the MSI Cubi 5. Pictures 1-2 regenerated and 3 drawn 2026-09-29. A
step may carry a "picture_note" - a plain-language correction printed under an
older picture that doesn't match the text yet. Delete the note once that
picture is regenerated from the updated prompt.

Requires:
  - fpdf2 + Pillow (`pip3 install --user fpdf2 pillow`)
  - GOOGLE_AI_API_KEY environment variable OR --api-key arg
  - Internet connection to Gemini API

Usage:
  export GOOGLE_AI_API_KEY="your-key"
  python3 build_waveshare_install_guide_pdf.py
  # OR
  python3 build_waveshare_install_guide_pdf.py --api-key "your-key"
  # Force re-generation of all images even if they exist:
  python3 build_waveshare_install_guide_pdf.py --regenerate
  # Regenerate only some steps: delete their install-step-N.png from IMG_DIR,
  # then run without --regenerate (only missing images are generated).
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

from waveshare_plug_diagram import draw as draw_plug_diagram

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
        "title": "The wall cavity before install - what comes into it",
        "caption": (
            "A 280 x 195 x 80 mm cavity is cut into the 9-inch staircase "
            "wall, centred at 1500 mm FFL, about 200 mm above the existing 2M "
            "staircase light switch. There is no back box - it is a plain "
            "masonry cavity. The 25 mm grey conduit comes in at the bottom "
            "with three cables from the server: HDMI (the picture), USB (the "
            "touch only) and the Cat6 that is already there. Leave a 200 mm "
            "service loop of every cable, including the 12V lead, coiled "
            "inside the cavity - later the screen must pull out 150 mm for "
            "service.\n\n"
            "POWER: the screen needs its own 12V, 2A. Pick one way on site:\n"
            "  (a) PREFERRED - send power up the Cat6 from a PoE port at the "
            "server. A small PoE splitter box in the cavity (it takes power "
            "from the network cable and gives out 12V) feeds the screen.\n"
            "  (b) A small 12V power supply in or next to the staircase "
            "switch box, fed from the switch's 230V, with a short 12V cable "
            "up to the cavity. The 230V stays at the switch box. With (b), "
            "the Cat6 stays spare: fit an RJ45 plug and label it 'SPARE'."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric cutaway illustration of a "
            "residential staircase wall before the screen is installed. The "
            "wall is shown in cutaway with a warm beige interior, revealing "
            "a large rectangular recess chased into the masonry, 280 mm wide "
            "by 195 mm tall by 80 mm deep, centered at 1500 mm above the "
            "floor. The cavity edge is plain plaster: there is NO wooden "
            "frame, NO bezel and NO screen yet. A 25 mm grey PVC conduit is "
            "buried in the wall - draw it as a grey pipe in the cut-away "
            "wall section, rising from below and entering the bottom of the "
            "cavity through a small round hole. Three cables come out of the "
            "conduit into the cavity: a flat black HDMI cable, a thin white "
            "USB cable and a blue Cat6 ethernet cable. The HDMI and USB "
            "cable ends are coiled into a neat service loop. The blue Cat6 "
            "cable plugs into a small black rectangular PoE splitter box, "
            "about the size of a matchbox, resting on the cavity floor; a "
            "short thin black DC power lead with a small round barrel plug "
            "comes out of the splitter box, also coiled with slack. About "
            "200 mm below the cavity is a smaller existing 2-module wall "
            "switch for the staircase light (a typical Indian modular switch "
            "plate, two rocker switches side by side). A thin dashed red "
            "line runs up the wall from the switch to the cavity, showing an "
            "optional short 12V cable route. The first few stairs of the "
            "staircase are visible at the bottom. Use exactly these eight "
            "labels, each with a thin black leader line pointing to its "
            "part, and no other text: 'Masonry cavity 280 x 195 x 80 mm, "
            "1500 mm FFL', '25 mm grey conduit from server', 'HDMI cable to "
            "server', 'USB cable to server - touch only', 'Cat6 into PoE "
            "splitter - 12V for screen (option a)', 'Option b: 12V from a "
            "small supply at the switch', '200 mm gap', 'Existing 2M light "
            "switch'. " + SHARED_STYLE
        ),
    },
    {
        "step": 2,
        "title": "Bench assembly - build the frame around the real screen",
        "caption": (
            "Wait until the screen arrives before the carpenter builds "
            "anything - the fit is tight. The (G) screen in its case is "
            "263.45 x 182.45 x 23.6 mm, so the 280 x 195 mm cavity leaves "
            "only about 6-8 mm spare around it. First re-measure the real "
            "cavity (masonry is never exact), then build the walnut bezel and "
            "plywood sub-frame around the actual screen: 4 magnet catches at "
            "the corners, vent slots top and bottom, and a 220 x 140 mm "
            "window for the picture (the picture itself is 217.91 x 136.50 "
            "mm). The back of the screen has 4 M4 screw holes in a 75 mm "
            "square (VESA 75) - use these to fix it to the sub-frame; the "
            "carpenter decides how once the screen is in hand. Stick the "
            "ACR122U NFC reader inside the lower-right bezel - it reads taps "
            "through the wood."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric illustration showing components laid "
            "out on a flat workbench surface, ready for assembly. From front "
            "to back: a rectangular walnut wood bezel frame with mitred 45 "
            "degree corners and visible ventilation slots in the top and "
            "bottom edges; a light plywood sub-frame fitted behind the bezel; "
            "a thin black 10.1-inch touchscreen in a slim black case, lying "
            "face-down so its back is visible. On the back of the screen, "
            "four small threaded screw holes form a 75 mm square in the "
            "middle, and a recessed port bay runs along one edge. A small "
            "black NFC reader module (rectangular, about the size of a "
            "credit card) is attached to the inside lower-right of the "
            "bezel; four small silver neodymium magnets sit at the four "
            "corners of the sub-frame. Three cables are coiled to the side, "
            "each ending in an L-shaped right-angle plug: a flat black HDMI "
            "cable, a thin white micro-USB cable, and a thin black DC power "
            "lead with a round barrel plug. Labels with thin black leader "
            "lines: 'Walnut bezel (mitred corners)', 'Plywood sub-frame', "
            "'Waveshare 10.1 inch (G) screen - back view', '4x M4 screw "
            "holes (75 mm square)', 'NFC reader (hidden behind bezel)', "
            "'Magnet catch (x4)', 'Vent slots (top + bottom)', '3 cables: "
            "HDMI, touch USB, 12V power'. " + SHARED_STYLE
        ),
    },
    {
        "step": 3,
        "title": "Connecting the 3 cables to the back of the screen",
        "caption": (
            "Pull the cables out of the cavity (the service loop gives you "
            "slack) and plug them into the back of the screen. There are 3 "
            "plugs:\n"
            "  1. HDMI - the picture, from the server.\n"
            "  2. Touch USB (micro-USB) - touch only. It does NOT power the "
            "screen.\n"
            "  3. 12V power (round DC plug) - from the PoE splitter or the "
            "12V supply. 12V, 2A - NOT 5V.\n"
            "The sockets sit in a recess on the back and the plugs go in "
            "sideways, so use L-shaped (90 degree) plugs or adapters on all "
            "3 - straight plugs will not fit in the cavity. Check that the "
            "12V plug fits the screen's power socket (compare it with the "
            "12V adapter in the screen's box). Leave the socket marked "
            "'5V 3A' empty - it gives power OUT (for a Raspberry Pi); it "
            "does not power the screen. Don't fix anything yet - you push the "
            "whole unit into the wall next."
        ),
        # Drawn in code by waveshare_plug_diagram.py, not by Gemini: two AI
        # attempts (2026-09-29) kept drawing straight HDMI/USB plugs, and
        # the L-shaped plugs are the whole point of this step.
        "drawn": True,
        "aspect_ratio": "4:3",
    },
    {
        "step": 4,
        "title": "Pushing the assembly into the wall cavity - magnets engage",
        "caption": (
            "Hold the walnut bezel flat against the wall, lined up with the "
            "cavity opening, and push gently. Feed the cables (and the PoE "
            "splitter box, if you used option a) into the cavity behind the "
            "screen without pinching them - there is only about 6-8 mm spare "
            "around the screen. The four magnets in the corners catch onto "
            "steel strike plates fixed inside the cavity with a soft click. "
            "The bezel sits flush around the cavity opening, projecting only "
            "3-5 mm from the wall - a subtle shadow line, not a tablet bolted "
            "on the wall - and overlaps the wall by 20-25 mm on every side to "
            "hide the cut edge. Below the new screen, the existing 2M "
            "staircase light switch is vertically aligned with the cavity."
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
            "tiny 'click' indicator. Three cables and a small black PoE "
            "splitter box visible behind the panel fold neatly into the "
            "cavity space. The wall is shown as a light "
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
            "the wall at 1500 mm FFL, and the sharp 1920 x 1200 screen "
            "showing the Home Assistant dashboard (water tank levels, light "
            "controls, doorbell tile, music, weather). The small brass 'tap "
            "here' dot in the lower-"
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
            "forward about 150 mm on the cable service loop (HDMI, touch USB "
            "and the 12V lead all need that slack). No need to unplug "
            "anything. This is also how you reach the brightness buttons on "
            "the back of the screen. When done, push back in - magnets catch, "
            "click into place, flush again. No wall damage, no tools."
        ),
        "aspect_ratio": "4:3",
        "prompt": (
            "A clean technical isometric three-quarter view illustration of "
            "a walnut-framed touchscreen panel pulled forward from a wall by "
            "about 150mm. The assembly is partially out of the wall opening, "
            "with three cables (HDMI, USB and a 12V power lead) visibly "
            "stretched but still connected - they trail from inside the wall "
            "cavity to L-shaped plugs on the back of the unit. "
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
                  "v2.1 - 2026-09-29 - (G) screen, 12V power, MSI Cubi 5 - "
                  "hand to carpenter + electrician + homeowner",
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

    def callout(self, title, lines):
        """Amber must-know box. Lines may use **bold** (fpdf2 markdown)."""
        self.set_fill_color(255, 243, 205)
        self.set_draw_color(200, 140, 30)
        self.set_text_color(120, 60, 0)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 9, "  " + title, border="LTR", fill=True,
                  new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, "\n".join(lines), border="LBR", fill=True,
                        markdown=True, padding=(0, 3, 2, 3),
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def picture_note(self, text):
        """Red box under an older picture that doesn't match the text yet."""
        self.set_fill_color(253, 236, 234)
        self.set_draw_color(200, 60, 60)
        self.set_text_color(150, 30, 30)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, "**PICTURE NOTE:** " + text, border=1,
                        fill=True, markdown=True, padding=(1.5, 3),
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def kv(self, key, value):
        """One quick-reference row: bold label column + wrapped value."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 50, 20)
        self.cell(26, 5.5, "  " + key)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, value, new_x="LMARGIN", new_y="NEXT")


def build_pdf(api_key: str | None, regenerate: bool) -> int:
    print(f"\nBuilding Waveshare Install Guide PDF → {OUT_PDF}\n")

    # Step 1: Ensure all 6 images exist. Steps drawn in code are redrawn on
    # every run (free, and keeps the PNG in step with the drawing code).
    missing_images = []
    for spec in PROMPTS:
        img_path = IMG_DIR / f"install-step-{spec['step']}.png"
        if spec.get("drawn"):
            draw_plug_diagram(img_path)
            print(f"Step {spec['step']}: drew {img_path.name} in code")
        elif regenerate or not img_path.exists():
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
        print("All Gemini images already exist; skipping regeneration "
              "(use --regenerate to force).")

    # Step 2: Assemble PDF
    print("\nAssembling PDF...")
    pdf = InstallGuidePDF()

    # ---- Cover page ----
    pdf.add_page()
    pdf.set_y(28)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(80, 50, 20)
    pdf.cell(0, 16, "Waveshare Staircase Panel", ln=1, align="C")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(140, 100, 50)
    pdf.cell(0, 10, "Visual Install Guide - 6 steps", ln=1, align="C")
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    intro = (
        "This guide walks the carpenter, electrician and homeowner through "
        "installing the Waveshare 10.1\" touch screen on the staircase wall. "
        "Six numbered pictures take you from the bare wall to a finished "
        "panel that pulls out for service.\n\n"
        "How it works: the home server (MSI Cubi 5) drives the screen. Two "
        "cables run up the existing 25 mm conduit from the server: HDMI for "
        "the picture (from the server's second screen output) and USB for "
        "the touch. There is no computer at the screen. The screen does NOT "
        "take power from the USB - it has its own 12V power socket, so 12V "
        "is provided at the wall. An NFC reader hidden behind the lower-right "
        "bezel lets you tap a phone or tag to start a scene. The walnut frame "
        "holds on with 4 magnets, so the whole panel pulls out for service "
        "without damaging the wall."
    )
    pdf.multi_cell(0, 6, intro)
    pdf.ln(5)

    pdf.callout("Before you start - 4 things to know", [
        "**1. POWER IS 12V, NOT 5V.** The screen has its own 12V power "
        "socket (12V, 2A). The USB cable carries touch only - it does not "
        "power the screen.",
        "**2. THREE PLUGS at the screen:** HDMI + touch USB + 12V power.",
        "**3. USE L-SHAPED (90 degree) PLUGS.** The sockets sit in a recess "
        "on the back of the screen - straight plugs will not fit.",
        "**4. TIGHT FIT.** Only about 6-8 mm spare around the screen in the "
        "280 x 195 mm cavity. The carpenter builds the frame AFTER the screen "
        "arrives, around the real screen.",
    ])

    pdf.set_fill_color(248, 240, 220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(80, 50, 20)
    pdf.cell(0, 9, "  Quick reference", ln=1, fill=True)
    pdf.ln(1)
    qref = [
        ("Location:", "Staircase South wall, 1500 mm FFL, ~200 mm above the "
                      "existing 2M light switch"),
        ("Cavity:", "280 x 195 x 80 mm masonry cavity (no back box)"),
        ("Screen:", "Waveshare 10.1\" HD touch LCD (G) with case, 1920 x 1200. "
                    "Case 263.45 x 182.45 x 23.6 mm; picture 217.91 x 136.50 "
                    "mm; 4x M4 screw holes on the back (75 mm square, "
                    "VESA 75)"),
        ("Buy from:", "ThinkRobotics (the first order, at ElectroPi, was "
                      "cancelled)"),
        ("Power:", "12V, 2A into the screen's own power socket - NOT 5V, NOT "
                   "over USB. (a) PoE splitter on the Cat6 (preferred) or "
                   "(b) a small 12V supply off the staircase switch 230V"),
        ("Plugs:", "3 at the screen - HDMI + touch micro-USB + 12V - all "
                   "L-shaped (90 degree)"),
        ("Conduit:", "D5 on the map (C-Server-Waveshare, 25 mm grey, ~2 m): "
                     "HDMI + touch USB + Cat6"),
        ("Server:", "MSI Cubi 5 - its second screen output (HDMI) + one USB "
                    "port"),
        ("Mount:", "Walnut bezel + 4-magnet service hatch, built around the "
                   "real screen"),
        ("Full spec:", "electrical/WAVESHARE_INDOOR_PANEL.md (v3.3)"),
    ]
    for key, value in qref:
        pdf.kv(key, value)
    pdf.ln(4)

    # ---- Step pages - 1 per page, image + caption ----
    for spec in PROMPTS:
        img_path = IMG_DIR / f"install-step-{spec['step']}.png"
        pdf.add_page()
        pdf.h2(f"Step {spec['step']} - {spec['title']}")
        # Image: max 180mm wide x 150mm tall (so a portrait picture keeps
        # its caption on the same page), centred
        if img_path.exists():
            try:
                ar_w, ar_h = (int(v) for v in spec["aspect_ratio"].split(":"))
                img_w = min(180, 150 * ar_w / ar_h)
                img_height = img_w * ar_h / ar_w
                # Place image, fpdf2 will preserve aspect ratio if h omitted
                pdf.image(str(img_path), x=14 + (180 - img_w) / 2,
                          y=pdf.get_y(), w=img_w)
                pdf.set_y(pdf.get_y() + img_height + 4)
            except Exception as e:
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(150, 50, 50)
                pdf.cell(0, 8, f"[image error: {e}]", ln=1)
        else:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(150, 50, 50)
            pdf.cell(0, 8, "[image missing - re-run with --regenerate]", ln=1)

        if spec.get("picture_note"):
            pdf.picture_note(spec["picture_note"])
        pdf.body(spec["caption"])

    # ---- Final page - credits + cross-refs ----
    pdf.add_page()
    pdf.h2("Reference and next steps")
    refs = (
        "Full hardware + mount spec:\n"
        "  electrical/WAVESHARE_INDOOR_PANEL.md v3.3 (15-section site "
        "handout). Where it says 'Beelink', read 'the server' - now the "
        "MSI Cubi 5.\n\n"
        "Related conduit documentation:\n"
        "  electrical/conduits-and-cavities.md (C-Niche-Waveshare row) = "
        "D5 / C-Server-Waveshare on the conduit map\n\n"
        "Decision history (decisions/decision-log.md):\n"
        "  2026-05-25 - hybrid panel design (staircase screen driven "
        "straight from the server)\n"
        "  2026-06-02 - server changed to the MSI Cubi 5; screen changed to "
        "the (G) 1920 x 1200\n"
        "  2026-09-28 - ElectroPi cancelled the (G) order; the same (G) "
        "re-chosen, to buy from ThinkRobotics; power corrected to 12V, 2A\n\n"
        "Parts for the power and plugs:\n"
        "  (a) PoE splitter: ask the shop for a 'PoE+ (802.3at) splitter, "
        "12V 2A output' with a DC plug that fits the screen - or (b) a small "
        "12V 2A power supply.\n"
        "  Plus L-shaped (90 degree) HDMI, micro-USB and DC plugs or "
        "adapters for the screen end.\n\n"
        "Homeowner checks before buying:\n"
        "  - Confirm the MSI Cubi 5 model has a second screen output free for "
        "this panel (HDMI, or USB-C with an HDMI adapter).\n"
        "  - WhatsApp ThinkRobotics to confirm the (G) is really in stock "
        "before paying (backup shop: REES52).\n"
        "  - If you choose power option (a), get the bigger PoE switch "
        "(TP-Link Omada ES220GP) - the splitter adds up to ~25 W of load.\n\n"
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
