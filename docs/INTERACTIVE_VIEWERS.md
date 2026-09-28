# Interactive assembly viewers

## Run and edit

Serve `site/` over HTTP (ES modules cannot reliably run from `file://`):

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory site
python scripts/verify_site.py
# After an authorized deployment, test its exact URL:
python scripts/verify_site.py https://freedomlab.nyc/voicehardware/
```

The QA server implements HTTP byte ranges for real MP4 seeking. A plain Python preview server is fine for the geometry, but may not seek the preserved videos properly. No remote runtime library, paid service, build tool or account is needed. WebGL is required; failure leaves a visible diagnostic and the source links/film previews available. Playback is opt-in, pauses while the viewer is offscreen or the tab is hidden, and lasts 12 seconds of active playback.

- `site/js/hardware-models.js`: editable millimetre geometry, named parts, source/approximation descriptions, screen artwork, assembled transforms and exploded offsets for all four devices.
- `site/js/assembly-viewer.js`: Three.js renderer, controls, deterministic staging, hit-tested labels, selection, resize/visibility handling and keyboard controls.
- `site/viewer.css`: graphite studio, orange controls and responsive layout.
- `site/index.html`: device order, accessible controls, public disclosures and source links. Historical status/account/provenance copy was removed. Existing three MP4s and posters are unchanged, lower on the page in an optional disclosure.
- `site/vendor/three/`: Three.js 0.180.0, required modules and upstream MIT license. GLTFLoader's utility import is rewritten to its local sibling; other upstream source is preserved.

## Source geometry and explicit boundaries

| Viewer | Grounded dimensions | Reconstruction limits |
| --- | --- | --- |
| M5StickS3 K150 | Manufacturer product envelope 48 × 24 × 15 mm; 1.14-inch 135 × 240 TFT; replacement LCD active area 14.864 × 24.912 mm | Existing graphite case and blue front button, not a new housing. Internal carrier, port details and separation are approximate; battery geometry and wiring omitted. Manufacturer lists 250 mAh, microphone and speaker. This is the current documented K150, **not verified as the owner's specific revision**. This screen is LCD, not e-paper. |
| ZECTRIX NOTE4 Developer Kit | 97 × 97 × 8.75 mm including magnetic back; 4.2-inch 400 × 300 e-paper | Existing white product silhouette, landscape display, round lower-right button, lower-left perforations and right-side buttons from manufacturer photo. Screen visible area, shell thicknesses, internal carrier and separation are approximate. No fabricated chip layout, battery geometry, capacity assumption or wiring. The featureless internal envelope explicitly marks the lack of verified mechanical internals. Hearth voice input + screen response does not establish spoken AI output; alarm audio is not TTS proof. |
| Waveshare 3.97 SKU33552 | 99.5 × 60 mm board; 86.4 × 51.84 mm active display | Geometry exported from the existing EEVEE/video-2 `.blend`, retaining named parts, true apertures, speaker/control concept and text meshes. Case 112 × 84 × 23 mm is proposed. Packages, thicknesses, PTT, speaker and leads remain unvalidated concepts. No battery. Web lighting/material color is tuned for the darker viewer; it is not a pixel-identical Blender render. |
| Waveshare 1.54 V2 SKU32298 | Manufacturer enclosure 39.8 × 53 × 16.9 mm, R4.5; visible aperture 27.8 × 27.8 mm; display 200 × 200 | Existing white enclosure. V2 board packages and relative layout are photo-estimated, not fabrication geometry. Source dimensional drawing contains a V1 rear legend; current V2 resource photo/documentation establishes PICO-1-N8R8, 8 MB flash/8 MB PSRAM. Internal dimensions, shell depth split, buttons and connectors approximate; no battery or wiring modeled. |

These are geometric assembly studies, not teardown instructions, collision-free mechanical simulations, print-ready cases, verified RF/acoustic designs, electrical schematics or tested voice products. Uniform conceptual layer separation does not assert a safe real disassembly order. No LTE stack is included. Interior omissions are intentional rather than invented detail.

## First-party references inspected

### M5StickS3
- https://docs.m5stack.com/en/core/StickS3 (documentation endpoint timed out during this build; official shop used as fallback)
- https://shop.m5stack.com/products/m5sticks3-esp32s3-mini-iot-dev-kit
- https://shop.m5stack.com/products/display-1-14-inch-for-sticks3
- Front/product photograph: https://cdn.shopify.com/s/files/1/0056/7689/2250/files/1_f50b328d-f753-4bef-92ec-6f0e8a69e5c0.webp?v=1769049123
- Header face photograph: https://cdn.shopify.com/s/files/1/0056/7689/2250/files/12_9ca84d53-58d8-4d0b-b29d-887832c1affd.webp?v=1770176878

### NOTE4
- https://zectrix.com/en/note4-developer-kit.html
- Manufacturer front photo: https://zectrix.com/public/assets/localized/en/note4-devkit-weather-final.jpg
- Software boundary: https://github.com/shantanugoel/hearth

### Waveshare 3.97
- https://www.waveshare.com/esp32-s3-epaper-3.97.htm?sku=33552
- https://docs.waveshare.com/ESP32-S3-ePaper-3.97
- Existing scene provenance: `REFERENCES.md`, `blender/design-contract.json`, `blender/source/build_scene.py`.

### Waveshare 1.54 V2
- https://www.waveshare.com/wiki/ESP32-S3-ePaper-1.54 (403; migrated official documentation used)
- https://docs.waveshare.com/ESP32-S3-ePaper-1.54
- Dimensions: https://docs.waveshare.com/assets/images/ESP32-S3-ePaper-1.54-ProductSize-3b8bca6e43fd463b41be8cb27bb50a90.webp
- V2 photo: https://docs.waveshare.com/assets/images/ESP32-S3-ePaper-1.54-HW-2a74c41495d6ff743bacc8c742899e7c.webp

Manufacturer images were inspected as reference, not bundled or used as texture substitutes. All viewer surfaces are real Three.js meshes; UI text is a local generated texture (or existing exported Blender text).

## Re-export the current EEVEE assembly

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python-exit-code 1 --python blender/source/export_web.py
```

The exporter opens the existing `.blend`, evaluates frame 440, selects the five named hardware groups, converts text/curves into meshes, and exports `site/assets/models/voice397.glb`. It never saves over the `.blend`. No Blender animations, camera, light or studio floor are exported. Three.js normalizes the imported source extent to 112 mm, preserving proportions; each part's absolute assembled transform is retained. The current export was exercised in Blender 5.2.0.

## Interaction contracts

- The scrubber is 0% exploded → 100% assembled. Every part pose is computed from the absolute scrub value, with staged smoothstep closure; backward scrubbing has no integration drift.
- Orbit works through mouse, touch and keyboard arrows. `+`/`-` zoom; Reset returns to the assembled home pose and clears selection. The geometry fits its bounding sphere on scrub/resize, preserving viewing direction; manual zoom is reframed when the assembly value changes.
- Each callout tests rays against actual scene meshes. A callout exists only if the nearest ray hit belongs to its part. Its leader endpoint is that actual surface hit, reprojected every rendered frame. There are no X-ray labels. Board/audio labels are additionally gated after their assembly stages.
- Label rectangles are placed deterministically with collision checks; labels without free space or a visible surface are suppressed. The component list remains available independently of label visibility. Selecting a hidden component does not make geometry transparent or fabricate an on-screen anchor.
- Mesh clicks, callout clicks and component-list clicks share selection. Standard materials get an orange emissive highlight; textured basic display materials get a warm tint. Selection descriptions remain outside the canvas.
- Near/far clipping planes scale with the millimetre model to avoid the visible coplanar flicker that a 0.1 mm near plane caused on NOTE4 during initial QA.

## Verification

`python scripts/verify_site.py` runs the current `scripts/verify_interactive.py` suite. It writes only `qa/interactive/`; pre-existing `qa/page-1440.png`, `qa/page-390.png` and `qa/site-validation.json` are not overwritten.

Checks cover all four devices at 1440px and 390px: ready state, device order, real mesh counts, forward/backward scrub pose equality, callout hit ownership, no label-rectangle overlap, click/material selection, mouse orbit, keyboard orbit/zoom, mobile touch orbit, pause/resume, reset, rear-view screen occlusion, page overflow, source link and all three real films' playback/seek/pause. No JavaScript or HTTP errors are accepted. Assembled, exploded, orbited and rear screenshots are saved per device and viewport; visual inspection is still required in addition to assertions.

This implementation is locally verified in Chromium, including mobile emulation—not tested on physical iOS/Android hardware or Safari/Firefox. Publishing is a separate authorized step: copy only `site/` to the website repository's `voicehardware/` route, build/audit the website, wait for Pages deployment and run the same suite against the exact live URL.
