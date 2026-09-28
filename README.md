# Voice hardware

[Live comparison](https://freedomlab.nyc/voicehardware/) · [Hardware sources](REFERENCES.md) · [Agent instructions](AGENTS.md)

Four source-grounded **interactive assembly studies**: M5StickS3 K150, ZECTRIX NOTE4 Developer Kit, Waveshare 3.97 SKU33552 and Waveshare 1.54 V2 SKU32298. These are **not fit-tested hardware or manufacturing designs**. Manufacturer dimensions are separated from approximate internal envelopes. The 3.97 viewer retains the existing EEVEE geometry and proposed graphite/orange case. No invented battery geometry, mandatory LTE stack or unverified working voice roundtrip.

See [interactive viewer editing, sources, limitations and QA](docs/INTERACTIVE_VIEWERS.md) and the [change manifest](docs/CHANGE_MANIFEST.md).

## Contents
- `site/`: the complete public comparison, three actual MP4s, poster images and linked hardware details. No login needed.
- `blender/voice397-wifi.blend`: editable current animated scene (finished hero at frame 440; exploded pose at 150).
- `blender/source/`: deterministic scene build, render, geometry validation, still captions and video encoding.
- `blender/finished.png`, `exploded.png`: rendered stills. Existing delivered media retain their original “private concept” captions; publication does not turn a concept into validated hardware.
- `legacy/cycles/`: earlier Cycles film's build/render/encode scripts.
- `legacy/diffusion/`: earlier JSX overlay composition, source EEVEE plate renderer and actual plate MP4. Historical shipping quotes are not current.
- `scripts/`: media refresh and real-browser website checks.

## Website editing
```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m http.server 8000 --bind 127.0.0.1 --directory site
```
Open http://127.0.0.1:8000 and edit `site/index.html`, `site/viewer.css` and `site/js/{assembly-viewer,hardware-models}.js`. Run `python scripts/verify_site.py` (it starts its own byte-range-capable temporary server). Tests exercise all four real WebGL viewers on desktop/mobile, deterministic scrubbing, orbit, selection, occlusion, pause/resume, the GitHub link and all three preserved films. New screenshots and results are saved under `qa/interactive/`; the earlier film-only QA files are left intact.

## Current Blender rebuild
Needs Blender 5.x (original scene produced in 5.2.0), Python 3.11+, Pillow and FFmpeg/ffprobe on PATH. Blender uses its bundled Python; do not pip-install bpy. CPU Cycles is available when Metal is absent; EEVEE still requires a supported graphics context. Set `VOICE_FONT` to a local TTF if automatic Arial/DejaVu lookup fails.

From repository root (on macOS set BLENDER to `/Applications/Blender.app/Contents/MacOS/Blender`; elsewhere use your installed executable):
```sh
export BLENDER=blender
"$BLENDER" -b --python-exit-code 1 --python blender/source/build_scene.py
"$BLENDER" -b --python-exit-code 1 --python blender/source/validate_scene.py
"$BLENDER" -b --python-exit-code 1 --python blender/source/render.py -- animation 440 440
# Inspect the smoke frame; then render the full 480-frame sequence:
"$BLENDER" -b --python-exit-code 1 --python blender/source/render.py -- animation
"$BLENDER" -b --python-exit-code 1 --python blender/source/render.py -- stills
python blender/source/label_stills.py
python blender/source/encode.py
python scripts/sync_media.py
python scripts/verify_site.py
```
Film: EEVEE, 20 seconds, 24 fps, 960×720. Stills: Cycles, 1280×960. Rendering time depends on hardware. Geometry validation checks camera framing, sourced extents and aperture ray tests, not physical feasibility. `encode.py` requires every rendered frame, encodes H.264, checks 480 frames/duration and fully decodes the MP4. Rebuilds need not be byte-identical across Blender/GPU versions.

## Historical pipelines
Cycles:
```sh
"$BLENDER" -b --python-exit-code 1 --python legacy/cycles/render/source/build_scene.py
"$BLENDER" -b --python-exit-code 1 --python legacy/cycles/render/source/render_animation.py -- animation --samples 16
python legacy/cycles/render/source/encode_animation.py
```
Its geometry is illustrative and predates the corrected current scene. Diffusion Studio uses `legacy/diffusion/index.tsx` over `assets/reader397-v5-plates.mp4`. Open that folder in a compatible Diffusion Studio editor (`npm install`, then `npm run open` if its `dapi` CLI is installed). The service/editor is an optional external dependency; its availability is not guaranteed by this repository. `render_reader397_v5.py` rebuilds and renders source plates; use FFmpeg at 24 fps to encode `frames/reader-v5-%04d.png` into the plate MP4. Original service project identifiers and generated duplicate JSX IDs are removed. A new service-side export of the sanitized legacy project has not been verified.

## Publishing
This source repository is public, but it does not automatically deploy to Freedom Lab. With owner authorization, copy **only `site/` contents** into `voicehardware/` in [the website repository](https://github.com/FreedomLabNYC/freedomlabnyc-website). Stage that directory, run its shared-style audit, build-site and built-site audit; commit/push and verify GitHub Pages plus the exact public route and video playback. Do not upload render frames, private research, credentials or service logs.

Dependencies retain their own licenses. No blanket license to third-party designs, trademarks or media is implied. No purchases are required for the current local Blender/HTML workflow.
