"""Reopen .blend and validate numeric envelope, camera framing and true apertures."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'voice397-wifi.blend'));s=bpy.context.scene
p=bpy.data.objects['PCB outline EXACT 99.50 x 60.00 R2'];d=bpy.data.objects['Active area EXACT 86.40 x 51.84'];f=bpy.data.objects['Front fascia through-cut solid'];tray=bpy.data.objects['Rear shell / hollow solid']
assert abs(p.dimensions.x-99.5)<.0001 and abs(p.dimensions.y-60)<.0001
assert abs(d.dimensions.x-86.4)<.0001 and abs(d.dimensions.y-51.84)<.0001
s.frame_set(440);dg=bpy.context.evaluated_depsgraph_get()
checks={}
for name,x,y in [('display',3,6),('speaker_slot',13,-36.3),('PTT',-29,-33.5),('mic',-45,-31)]:
 hit,loc,normal,idx,obj,mat=s.ray_cast(dg,Vector((x,y,200)),Vector((0,0,-1)))
 checks[name]={'first_hit':obj.name if obj else None,'height':loc.z if hit else None}
assert checks['display']['first_hit']=='Active area EXACT 86.40 x 51.84'
assert checks['speaker_slot']['height']<20.4
assert checks['PTT']['first_hit'].startswith('Orange PTT')
assert checks['mic']['height']<20.4
bounds=[];stack_gaps=[];rotation_floor=[]
board_meshes=[o for o in bpy.data.objects['02 | SOURCED PCB - exact 99.50 x 60.00 mm'].children if o.type=='MESH']
display_meshes=[o for o in bpy.data.objects['03 | 3.97 E-PAPER - exact active 86.40 x 51.84 mm'].children if o.type=='MESH']
objs=[o for o in s.objects if o.type=='MESH' and o.name!='Infinite studio floor']
for frame in range(1,481):
 s.frame_set(frame)
 board_z=[(o.matrix_world@Vector(v)).z for o in board_meshes for v in o.bound_box]
 display_z=[(o.matrix_world@Vector(v)).z for o in display_meshes for v in o.bound_box]
 stack_gaps.append(min(display_z)-max(board_z))
 if 120<=frame<=144 or 192<=frame<=216:rotation_floor.append(min(board_z)-20.4)
 pts=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for o in objs for v in o.bound_box]
 bound=[min(v.x for v in pts),min(v.y for v in pts),max(v.x for v in pts),max(v.y for v in pts)]
 if bound[0]<.02 or bound[1]<.02 or bound[2]>.98 or bound[3]>.98:bounds.append({'frame':frame,'bounds':bound})
report={'blender':bpy.app.version_string,'reopened_scene':True,'board_mm':list(p.dimensions),'active_display_mm':list(d.dimensions),'case_xy_mm':[tray.dimensions.x,tray.dimensions.y],'screen_and_aperture_raycast':checks,'camera_frames_checked':480,'minimum_board_display_vertical_gap_mm':min(stack_gaps),'minimum_rotating_board_above_rear_rim_mm':min(rotation_floor),'camera_boundary_failures':bounds,'status':'PASS' if not bounds and min(stack_gaps)>0 and min(rotation_floor)>0 else 'NEEDS CORRECTION','not_validated':['Physical fit','Electrical function','Acoustic performance','Thermal behavior','Manufacturability','Battery selection']}
(R/'geometry-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
