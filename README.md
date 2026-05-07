# Home Interior & Automation — Project Repository

This folder is the **single source of truth** for Ganesh's home interior + home-automation project. Any AI agent (Claude, other models) and any human collaborator should read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) first, then dive into the relevant subfolder.

> **Authoritative drawings:** the **handwritten** floor plans are the latest. AutoCAD screenshots are kept for reference only. Decoded text in [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md) is the canonical room/dimension reference — read that instead of re-processing the images.

## Folder map

| Folder | Purpose |
|---|---|
| [floor-plans/](floor-plans/) | Floor plans (images + decoded markdown). Start here for any spatial question. |
| [electrical/](electrical/) | Electrical layout: switch points, sockets, lighting circuits, DB, conduits. **Hand-out: [pdfs/ELECTRICIAN_REFERENCE.pdf](pdfs/ELECTRICIAN_REFERENCE.pdf).** |
| [furniture/](furniture/) | Furniture layout per room: sizes, placement, built-ins. |
| [automation-iot/](automation-iot/) | Home automation: protocol choice, devices, hubs, scenes, network. |
| [interior-design/](interior-design/) | Style direction, mood, palettes, room-by-room interior decisions. **Master: [master-interior-spec.md](interior-design/master-interior-spec.md).** |
| [interior-design/generated-images/](interior-design/generated-images/) | Output dump for `/banana` skill renders. |
| [materials-finishes/](materials-finishes/) | Tiles, paints, wood, hardware, sanitaryware. **Master palette: [master-color-palette.md](materials-finishes/master-color-palette.md).** |
| [decisions/](decisions/) | Chronological decision log — *what* was chosen and *why*. |
| [pdfs/](pdfs/) | Ready-to-share PDFs: [ELECTRICIAN_REFERENCE.pdf](pdfs/ELECTRICIAN_REFERENCE.pdf) (12 pages, hand to electrician+mason) and [INTERIOR_SUGGESTIONS.pdf](pdfs/INTERIOR_SUGGESTIONS.pdf) (24 pages, hand to interior contractor). |

## Working agreement (for any agent reading this)

1. **Don't re-process the floor-plan images** unless the user asks. Use [floor-plans/floor-plans-decoded.md](floor-plans/floor-plans-decoded.md). It saves tokens and stays consistent.
2. **Update the decision log** ([decisions/decision-log.md](decisions/decision-log.md)) whenever a new decision is locked in. One line per decision with a date.
3. **Update the relevant subfolder README** when scope or content changes — keep each README as that domain's index.
4. **Use `/banana` for any image generation** (interior renders, mood boards). Save outputs into `interior-design/generated-images/` with descriptive filenames (e.g. `master-bedroom-warm-minimal-v1.png`).
5. **Cross-link, don't duplicate.** If the electrical doc needs a room dimension, link to the floor plan instead of copying it — single source of truth.
6. **Flag conflicts.** If something in the handwritten plan disagrees with something the user said in chat, surface it rather than silently picking one.

## Quick links

- [Project context & current status](PROJECT_CONTEXT.md)
- [Decoded floor plans](floor-plans/floor-plans-decoded.md)
- [Decision log](decisions/decision-log.md)
- [Master interior spec (A-Z)](interior-design/master-interior-spec.md)
- [Master colour palette (hex codes)](materials-finishes/master-color-palette.md)
- [Conduits & cavities — electrician cheat sheet](electrical/conduits-and-cavities.md)
- 📄 [Electrician PDF](pdfs/ELECTRICIAN_REFERENCE.pdf) — 12 pages
- 📄 [Interior Suggestions PDF](pdfs/INTERIOR_SUGGESTIONS.pdf) — 24 pages
