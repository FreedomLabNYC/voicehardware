# Agent handoff

Read README.md and REFERENCES.md before editing.

- Current hardware source: `blender/source/build_scene.py`. Preserve millimetres and source board/display dimensions unless a manufacturer source justifies a change.
- Keep concepts labeled. Never claim fit testing, manufacturability, wiring correctness, battery capacity or a working voice roundtrip from a render.
- Current scope is Wi-Fi/USB. LTE appears only in explicitly historical comparisons. Battery, physical PTT and acoustic integration are unresolved.
- Edit `site/index.html` for layout, hardware links and disclosures. Keep three actual video lanes and the top-right public GitHub link. Do not invent output for blocked tools.
- Use free local Blender/Python/FFmpeg for the current workflow. Do not buy tools/credits or perform public writes without owner authorization.
- Test source: compile Python, build Blender scene, reopen and validate. Render a changed frame before a full movie. Full movie: 480 actual frames, 24 fps, 960×720; encode.py probes and fully decodes it.
- After changed movie output, use `python scripts/sync_media.py`, then `python scripts/verify_site.py`. Inspect desktop/mobile screenshots and actual encoded frames; script success alone is not visual approval.
- `legacy/` preserves earlier Cycles and Diffusion Studio sources. It is not the current hardware design; its board proportions/power stack are illustrative. Do not silently promote it.
- Repository has no credentials, private Drive records, service sessions or deployment secrets. Public website deployment is a separate owner-authorized step described in README.
