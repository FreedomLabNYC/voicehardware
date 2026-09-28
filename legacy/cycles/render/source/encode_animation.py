#!/usr/bin/env python3
"""Encode the Cycles frame sequence and record independently probed metadata."""
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
frames = ROOT / "render" / "frames" / "frame-%04d.png"
out = ROOT / "media" / "reader397-flush-footprint-cycles.mp4"
out.parent.mkdir(parents=True,exist_ok=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "24", "-i", str(frames), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames", "-of", "json", str(out)], check=True, capture_output=True, text=True)
(ROOT / "media" / "video-manifest.json").write_text(json.dumps({"file": out.name, "ffprobe": json.loads(probe.stdout)}, indent=2) + "\n")
print(out)
