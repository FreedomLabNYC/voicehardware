# Interactive viewer change manifest

- Replaced the film-first page with four interactive assembly studies, ordered M5StickS3, ZECTRIX NOTE4, Waveshare 3.97 and Waveshare 1.54 V2.
- Added editable Three.js geometry, deterministic assembly controls, surface-occlusion-aware labels, selection, orbit, keyboard and touch interactions.
- Bundled Three.js modules and MIT license locally; exported the existing EEVEE assembly as `site/assets/models/voice397.glb` without modifying the Blender source scene.
- Preserved the three existing MP4s and posters in an optional film section. Removed historical private account/status details from the page.
- Added the Blender web exporter, interactive editing/reference documentation and desktop/mobile browser QA under `qa/interactive/`.
- Deployment copies only `site/` into the website's existing `voicehardware/` route. Other website routes and unrelated working changes are outside this release.
- Earlier `qa/page-1440.png`, `qa/page-390.png`, `qa/site-validation.json` and the exploratory `qa/viewer-first.png` are not included in this release's changes.
- Added a Schematik tools section with the web app, Mac desktop download, and the public Hermes voice-satellite guide. Schematik Desktop 0.2.0 is installed locally; generated diagrams are not fit tests of the four assemblies.

See [INTERACTIVE_VIEWERS.md](INTERACTIVE_VIEWERS.md) for model limitations, source references, interaction contracts and verification commands.
