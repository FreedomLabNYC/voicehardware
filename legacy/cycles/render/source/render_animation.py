"""Render Luxobench-style preview frames or the full conceptual product film.

Usage:
  blender -b --python render/source/render_animation.py -- preview
  blender -b --python render/source/render_animation.py -- animation [start [end]]

The scene is illustrative, not mechanical/electrical fit validation.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[2]
RENDER = ROOT / "render"
SCENE_PATH = RENDER / "reader397-flush-footprint-assembly.blend"
FPS, END = 24, 546
PREVIEW_FRAMES = (78, 192, 336, 528)


def args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=("preview", "animation"))
    p.add_argument("start", type=int, nargs="?", default=1)
    p.add_argument("end", type=int, nargs="?", default=END)
    p.add_argument("--cpu", action="store_true")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--samples", type=int, default=24)
    out = p.parse_args(argv)
    if not 1 <= out.start <= out.end <= END:
        p.error(f"range must be within 1-{END}")
    return out


def device(scene, force_cpu: bool) -> dict:
    scene.cycles.device = "CPU"
    if force_cpu:
        return {"backend": "CPU", "devices": ["CPU"]}
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for backend in ("METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            prefs.compute_device_type = backend
            prefs.refresh_devices()
            devices = [d for d in prefs.devices if d.type == backend]
            if not devices:
                continue
            for d in prefs.devices:
                d.use = d.type == backend
            scene.cycles.device = "GPU"
            return {"backend": backend, "devices": [d.name for d in devices]}
        except (RuntimeError, TypeError, ValueError):
            continue
    return {"backend": "CPU", "devices": ["CPU"]}


def main() -> None:
    a = args()
    if not SCENE_PATH.exists():
        raise FileNotFoundError(f"Build first: {SCENE_PATH}")
    bpy.ops.wm.open_mainfile(filepath=str(SCENE_PATH))
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.render.resolution_x, s.render.resolution_y = 720, 1080
    s.render.resolution_percentage = 50 if a.mode == "preview" else 100
    s.render.image_settings.file_format = "PNG"
    s.render.image_settings.color_mode = "RGB"
    s.render.fps, s.render.fps_base = FPS, 1.0
    s.cycles.samples = a.samples
    s.cycles.use_adaptive_sampling = True
    s.cycles.adaptive_threshold = 0.03
    s.cycles.use_denoising = True
    s.cycles.seed = 7
    s.render.use_persistent_data = True
    selected = PREVIEW_FRAMES if a.mode == "preview" else range(a.start, a.end + 1)
    out = RENDER / ("previews" if a.mode == "preview" else "frames")
    out.mkdir(parents=True, exist_ok=True)
    report = {"mode": a.mode, "scene": SCENE_PATH.name, "blender": bpy.app.version_string,
              "fps": FPS, "samples": a.samples, "size": [s.render.resolution_x * s.render.resolution_percentage // 100, s.render.resolution_y * s.render.resolution_percentage // 100],
              "device": device(s, a.cpu), "frames": []}
    for frame in selected:
        target = out / (f"preview-{frame:04d}.png" if a.mode == "preview" else f"frame-{frame:04d}.png")
        if a.resume and target.exists() and target.stat().st_size > 1000:
            report["frames"].append({"frame": frame, "file": target.name, "skipped": True})
            continue
        s.frame_set(frame)
        s.render.filepath = str(target)
        started = time.monotonic()
        try:
            bpy.ops.render.render(write_still=True)
        except RuntimeError:
            if s.cycles.device != "GPU":
                raise
            s.cycles.device = "CPU"
            report["device"] = {"backend": "CPU", "devices": ["CPU"], "gpu_fallback": True}
            bpy.ops.render.render(write_still=True)
        report["frames"].append({"frame": frame, "file": target.name, "seconds": round(time.monotonic() - started, 3)})
        (out / f"render-report-{a.mode}.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report["frames"][-1]), flush=True)
    print("RENDER_OK", json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
