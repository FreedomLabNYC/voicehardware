"""Render actual Blender source. preview / stills / animation [start end]."""
import bpy,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
(R/'frames').mkdir(exist_ok=True)
(R/'assets').mkdir(exist_ok=True)
a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['preview']
bpy.ops.wm.open_mainfile(filepath=str(R/'voice397-wifi.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.refresh_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
s.cycles.samples=16 if a[0]=='animation' else 32
if a[0]=='animation':
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_percentage=75 if a[0]=='animation' else (60 if a[0]=='preview' else 100)
frames=range(int(a[1]) if len(a)>1 else 1,(int(a[2]) if len(a)>2 else 480)+1) if a[0]=='animation' else [150,440]
for f in frames:
 s.frame_set(f)
 out=R/'frames'/f'frame-{f:04d}.png' if a[0]=='animation' else (R/(('preview-')+('exploded.png' if f==150 else 'finished.png')) if a[0]=='preview' else R/'assets'/('exploded-raw.png' if f==150 else 'finished-raw.png'))
 s.render.filepath=str(out);st=time.monotonic();bpy.ops.render.render(write_still=True);print('FRAME_DONE',f,round(time.monotonic()-st,2),flush=True)
print('RENDER_COMPLETE',a[0],flush=True)
