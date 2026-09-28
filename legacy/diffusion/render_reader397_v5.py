"""Reference-derived 39 s reader397 + LTE HAT concept animation.
Conceptual only: no electrical/fit/bench validation is implied. Blender 5.2 + EEVEE.
Render at 8 fps 524x360; composition script supplies data-driven cards/chrome and upscales 2x.
"""
import bpy, math, pathlib, sys, os
from mathutils import Vector
OUT=pathlib.Path(__file__).resolve().parent; FRAMES=OUT/'frames'; FRAMES.mkdir(parents=True,exist_ok=True)
# Native 24 fps source. Extended holds are intentional: seated parts and cards
# remain readable rather than forcing this factual assembly study into 13.875 s.
FPS=24; END=546
bpy.context.preferences.filepaths.save_version=0

def mat(name,color,metal=0,rough=.5):
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
shell=mat('Charcoal shell',(.07,.085,.08,1),0,.48);green=mat('Main PCB',(.025,.25,.16,1),0,.48);red=mat('LTE PCB',(.46,.06,.035,1),0,.44);silver=mat('Satin metal',(.48,.52,.52,1),.75,.3);black=mat('Screen glass',(.018,.027,.029,1),.05,.18);paper=mat('E-paper',(.70,.73,.67,1),0,.72);orange=mat('PTT orange',(.78,.23,.06,1),0,.4);battery=mat('Battery pouch',(.28,.31,.32,1),.55,.3);blue=mat('Power board',(.02,.18,.30,1),0,.42);gold=mat('Connector gold',(.72,.46,.10,1),.7,.22);pocket=mat('Tray pocket',(.13,.16,.17,1),0,.52);ledge=mat('Seat ledge',(.30,.34,.33,1),.35,.32)
def box(name,dims,loc,ma,bevel=.5):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
 if bevel:
  q=o.modifiers.new('Soft edge','BEVEL');q.width=bevel;q.segments=2
 return o
def cyl(name,r,d,loc,ma):
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=d,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(ma);return o
def add_group(name,objs):
 e=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(e)
 for x in objs:x.parent=e
 e['group_id']=name;return e
def kf(o,prop,frame,value):
 setattr(o,prop,value);o.keyframe_insert(data_path=prop,frame=frame)
def loc(o,f,v):kf(o,'location',f,v)
def rot(o,f,v):kf(o,'rotation_euler',f,v)
def smooth(o):
 # Blender 5.2's Action channel API no longer exposes .fcurves directly.
 # Keyframes inserted above default to Bezier, which is the intended settle.
 return None
# scene
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
# Conceptual rear tray has the exact same X/Y footprint as the front fascia.
# The LTE HAT is rotated on the rear stack; depth, not width/length, grows.
case=[]
case += [box('rear_tray_base',(5.9,10.4,.45),(0,0,.25),shell,.45),
         box('rear_tray_floor',(5.34,9.84,.09),(0,0,.50),black,.18),
         box('tray_wall_left',(.28,10.4,2.8),(-2.81,0,1.65),shell,.14),
         box('tray_wall_right',(.28,10.4,2.8),(2.81,0,1.65),shell,.14),
         box('tray_wall_top',(5.9,.28,2.8),(0,5.06,1.65),shell,.14),
         box('tray_wall_bottom',(5.9,.28,2.8),(0,-5.06,1.65),shell,.14),
         box('battery_bay_floor',(2.72,5.72,.06),(0,-.5,.58),pocket,.12),
         box('power_locator_left',(2.6,.12,.13),(-1.6,.4,1.12),ledge,.04),
         box('power_locator_right',(2.8,.12,.13),(1.5,.4,1.12),ledge,.04),
         box('hat_locator_left',(.12,5.92,.16),(-1.52,0,1.57),ledge,.04),
         box('hat_locator_right',(.12,5.92,.16),(1.52,0,1.57),ledge,.04),
         box('battery_locator_left',(.10,5.84,.13),(-1.42,-.5,.67),ledge,.04),
         box('battery_locator_right',(.10,5.84,.13),(1.42,-.5,.67),ledge,.04)]
for x in (-2.35,2.35):
 for y in (-4.35,4.35):case.append(cyl('tray_screw_boss',.15,.54,(x,y,.77),silver))
for x in (-2.35,2.35):
 for y in (-4.25,4.25):case.append(cyl('core_standoff',.11,.33,(x,y,2.14),gold))
lower=add_group('lower_housing',case)
# Core reader PCB
core=[box('reader_core_pcb',(5.25,9.35,.18),(0,0,6.4),green,.15),box('esp_module',(2.0,1.5,.19),(0,-2.6,6.59),silver,.1),box('audio_codec',(1.0,.7,.16),(-1.5,1.9,6.58),black,.08)]
for x in (-2,2):core.append(box('board_connector',(.42,.72,.23),(x,3.25,6.6),gold,.05))
coreg=add_group('reader_core_pcb',core)
# HAT a rectangular designed board / 65x30.2 envelope relative
hat=[box('sim7080_hat_pcb',(5.7,2.65,.22),(0,.55,10.8),red,.15),box('sim7080_module',(2.2,1.45,.18),(-.9,.55,11.0),silver,.08),box('sim_slot',(1.05,.75,.18),(1.75,.55,11.0),black,.06),box('main_antenna_ipex',(.35,.35,.2),(2.45,1.5,11.0),gold,.04)]
hatg=add_group('sim7080_hat',hat)
# shared cell/pack is transparent pending protected pack selection
bat=[box('replacement_cell_envelope',(2.3,5.3,.55),(0,-.5,8.6),battery,.35),box('pack_protection_placeholder',(1.4,.5,.15),(0,2.25,8.95),blue,.07)]
batg=add_group('replacement_1s_pack',bat)
# Power charger and boost
power=[box('bq24074_powerpath',(2.25,1.45,.19),(-1.6,.4,9.45),blue,.12),box('boost_5v_sys',(2.5,.95,.18),(1.5,.4,9.72),blue,.12),box('usb_c_charge_port',(1.0,.30,.38),(0,-5.05,9.45),silver,.14)]
powerg=add_group('shared_power_path',power)
# audio / PTT / speaker carrier
audio=[box('audio_control_carrier',(4.7,2.4,.16),(0,-.2,13.1),green,.14),box('mic_module',(.7,.7,.16),(-1.55,-.2,13.3),silver,.12),box('speaker_module',(1.2,1.2,.18),(1.45,-.2,13.3),black,.12),box('ptt_module',(1.3,.65,.19),(0,-1.2,13.3),orange,.18)]
audiog=add_group('io_audio_ptt',audio)
# display + front cover
display=[box('display_backing',(5.15,8.85,.18),(0,.45,16.1),black,.26),box('397_epaper_display',(4.55,7.65,.1),(0,.45,16.26),paper,.18)]
dispg=add_group('display_397',display)
front=[box('front_cover',(5.9,10.4,.36),(0,0,20.5),shell,.6),box('display_aperture',(4.68,7.78,.08),(0,.45,20.71),black,.2),box('physical_ptt',(2.35,.5,.18),(0,-3.85,20.75),orange,.19)]
for x in [-.9,-.45,0,.45,.9]:front.append(cyl('speaker_hole',.09,.07,(x,-4.5,20.73),black))
frontg=add_group('front_cover',front)
trim=add_group('top_trim',[box('top_trim',(1.45,.5,.18),(0,4.55,22),silver,.16)])
# Start positions. Group origins matter children placed world then parents move from 0
for g in (coreg,hatg,batg,powerg,audiog,dispg,frontg,trim):g.location=(0,0,0)
# 65 × 30.2 mm HAT: rotate its 5.7 × 2.65 scene envelope so its 2.65 side
# occupies the flush enclosure width. This is a visual layout, not fit proof.
hatg.rotation_euler=(0,0,math.pi/2)
# Continuous conceptual-tray sequence at 24fps. Every part enters a visible
# seat, stays opaque, and remains where it was seated until final closure.
loc(lower,1,(0,0,.25));rot(lower,1,(0,0,0));loc(lower,54,(-4.0,.6,4.5));rot(lower,54,(1.25,.30,-.85));loc(lower,78,(0,0,.25));rot(lower,78,(0,0,0));smooth(lower)
def stage(g, enter, shown_z, exit, seated_z):
 loc(g,1,(0,0,4));loc(g,enter,(0,0,4));loc(g,enter+17,(0,0,shown_z));loc(g,exit,(0,0,shown_z));loc(g,exit+18,(0,0,seated_z));smooth(g)
stage(batg,90,-3.8,174,-7.85)
stage(powerg,90,-3.6,174,-8.10)
stage(hatg,174,-3.4,258,-9.10)
stage(audiog,258,-3.0,336,-11.10)
stage(coreg,336,-3.3,402,-4.20)
stage(dispg,402,-3.0,456,-13.60)
# Components do not exist visually before their entry beat. They never fade or hide after entry.
def reveal(g, enter):
 # Empty visibility does not propagate to child meshes in Blender; key every child.
 for o in g.children:
  o.hide_render=True;o.keyframe_insert(data_path='hide_render',frame=1)
  o.hide_render=False;o.keyframe_insert(data_path='hide_render',frame=enter)
reveal(batg,90);reveal(powerg,90);reveal(hatg,174);reveal(audiog,258)
reveal(coreg,336);reveal(dispg,402);reveal(frontg,456);reveal(trim,510)
# Closure comes after all retained layers are visible.
# Front fascia must remain above the seated layers; never sink below the lower shell.
loc(frontg,1,(0,0,4));rot(frontg,1,(0,0,0));loc(frontg,456,(0,0,4));rot(frontg,456,(1.45,.2,-.7));loc(frontg,510,(0,0,-17.65));rot(frontg,510,(0,0,0));smooth(frontg)
loc(trim,1,(0,0,4));loc(trim,510,(0,0,4));loc(trim,528,(0,0,-19.0));smooth(trim)
# floor and camera
# High-key neutral studio matching the reference visual language.
floor=mat('Studio pale gray',(.95,.95,.91,1),0,.86);box('seamless_ground',(100,100,.2),(0,0,-.18),floor,0)
def point(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(18,-24,28));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=25;point(cam,(0,0,5));bpy.context.scene.camera=cam
for locl,power,size in [((-18,-18,34),5100,17),((15,-6,20),2700,11),((0,18,24),1800,12)]:
 bpy.ops.object.light_add(type='AREA',location=locl);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;point(l,(0,0,5))
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=1048;scene.render.resolution_y=720;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(FRAMES/'reader-v5-');scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=END
scene.world.color=(.98,.98,.95);scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=3.0;scene.render.threads_mode='FIXED';scene.render.threads=6
scene.frame_start=int(os.environ.get('RENDER_START_FRAME','1'));scene.frame_end=int(os.environ.get('RENDER_END_FRAME',str(END)))
scene['architecture_status']='QUALIFIED FOR CONCEPTUAL FLUSH-FOOTPRINT MODEL / NOT YET BENCH QUALIFIED';scene['disclosure']='Illustrative flush-footprint enclosure. Board outlines sourced; stack-up, clearances, shared-power wiring and fit remain unbench-tested.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'reader397-flush-footprint-assembly.blend'))
print('RENDER_ANIMATION',END,FPS,flush=True);bpy.ops.render.render(animation=True);print('RENDER_OK',flush=True)
