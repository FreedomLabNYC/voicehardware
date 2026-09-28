"""Export existing EEVEE geometry without altering the .blend. Blender 5.x."""
import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'blender/voice397-wifi.blend'))
bpy.context.scene.frame_set(440)
bpy.ops.object.select_all(action='DESELECT')
for o in list(bpy.context.scene.objects):
    if o.parent or o.name[:2] in ('01','02','03','04','05'):
        o.select_set(True)
# Convert text and wires so no exported visible details depend on Blender fonts.
for o in list(bpy.context.selected_objects):
    if o.type in ('FONT','CURVE'):
        bpy.context.view_layer.objects.active=o
        others=list(bpy.context.selected_objects)
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
        bpy.ops.object.convert(target='MESH')
        for x in others:
            try:x.select_set(True)
            except ReferenceError:pass
out=ROOT/'site/assets/models';out.mkdir(parents=True,exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(out/'voice397.glb'),use_selection=True,export_format='GLB',export_animations=False,export_extras=True,export_yup=False)
print('WEB_EXPORT_COMPLETE',out/'voice397.glb')
