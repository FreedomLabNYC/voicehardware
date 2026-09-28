"""3.97-inch Wi-Fi product concept. Blender 5.x; all lengths in mm.
Exact sourced outline and display area; all other geometry explicitly conceptual.
Rebuild: Blender -b --python source/build_scene.py
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene
s.unit_settings.system='METRIC'; s.unit_settings.scale_length=.001

def mat(n,c,metal=0,rough=.45):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
 return m
shell=mat('Warm graphite polymer',(.095,.125,.135)); edge=mat('Seam elastomer',(.022,.035,.04)); paper=mat('Reflective e-paper - not emissive',(.79,.83,.74),0,.9); ink=mat('E-paper black',(.024,.039,.038),0,.9)
pcbmat=mat('Source blue PCB',(.012,.095,.15)); silver=mat('Satin shield',(.55,.60,.62),.8,.28); gold=mat('ENIG mounting rings',(.65,.41,.10),.7,.32); chip=mat('IC black',(.026,.030,.034)); cream=mat('Connector nylon',(.83,.80,.68)); orange=mat('PTT burnt orange',(.92,.23,.065)); ribbon=mat('Display FPC amber',(.60,.25,.035),.3); meshmat=mat('Speaker woven black',(.022,.025,.027)); white=mat('Silkscreen',(.75,.84,.84)); floor=mat('Studio midnight',(.024,.038,.049),0,.8)

def group(n):
 o=bpy.data.objects.new(n,None); bpy.context.collection.objects.link(o); return o

def box(n,d,l,m,b=.3,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=l); o=bpy.context.object; o.name=n; o.dimensions=d; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if b:
  mod=o.modifiers.new('Manufactured edge radius','BEVEL'); mod.width=b; mod.segments=3
  bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=mod.name)
 if parent:o.parent=parent
 o['geometry_status']='conceptual envelope; not measured'
 return o

def rr(n,w,h,r,z0,z1,m,parent=None):
 pts=[]
 for cx,cy,a in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(13):
   t=math.radians(a+i*90/12); pts.append((cx+r*math.cos(t),cy+r*math.sin(t)))
 N=len(pts); verts=[(x,y,z) for z in (z0,z1) for x,y in pts]
 faces=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.data.materials.append(m)
 if parent:o.parent=parent
 o['geometry_status']='conceptual envelope; not measured'; return o

def cyl(n,r,d,l,m,parent=None,rot=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=d,location=l);o=bpy.context.object;o.name=n;o.data.materials.append(m)
 if rot:o.rotation_euler=rot
 if parent:o.parent=parent
 return o

def cut(obj,cutter):
 bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('Real through aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)

def text(n,t,size,l,m,parent=None):
 cu=bpy.data.curves.new(n,'FONT');cu.body=t;cu.size=size;cu.extrude=0;cu.align_y='CENTER';o=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(o);o.location=l;cu.materials.append(m)
 if parent:o.parent=parent
 return o

rear=group('01 | REAR SHELL - conceptual 112 x 84 x 23 mm')
tray=rr('Rear shell / hollow solid',112,84,6,0,20,shell,rear)
void=rr('Cavity cutter',108,80,4,2,22,shell);cut(tray,void)
# True USB-C and rotary apertures. Board positions follow manufacturer rear photograph.
cut(tray,box('USB through wall',(12,12,5.5),(-54,6,12),shell,1.8))
cut(tray,box('Rotary access',(18,8,7),(29,40,12),shell,2))
for x in (-51,51):
 for y in (-37,37):
  b=cyl('Concept fastener boss',2.5,15,(x,y,9.5),shell,rear);cut(b,cyl('Pilot hole',1,17,(x,y,9.5),shell))
# Board support ledges do not alter board dimensions.
for x in (-47,47):
 for y in (-21,33):box('Board support seat',(4,4,1.5),(x,y,12.45),shell,.3,rear)
# Distinct gasket ring
seam=rr('Continuous closure gasket',111.4,83.4,5.7,20,20.4,edge,rear);cut(seam,rr('Gasket void',107,79,3.5,19,22,edge))
# No invented battery. Usable lower volume is empty and disclosed in README.
text('Rear interior note','USB / Wi-Fi concept',3,(-33,-8,2.03),white,rear)

board=group('02 | SOURCED PCB - exact 99.50 x 60.00 mm')
board.location=(0,6,14)
p=rr('PCB outline EXACT 99.50 x 60.00 R2',99.5,60,2,-.8,.8,pcbmat,board);p['geometry_status']='99.50 x 60.00 and R2 from official dimension image; thickness 1.6 assumed'
# Manufacturer photograph coordinates, bottom component face. No random chips/traces.
def xy(px,py):return (-(px-480)/650*99.5,(325-py)/390*60)
def part(n,px,py,w,h,d,ma):
 x,y=xy(px,py);return box(n,(w,h,d),(x,y,-.8-d/2),ma,.15,board)
def backlabel(t,px,py,size=1.45,z=-3.3):
 x,y=xy(px,py);o=text('PCB legend '+t,t,size,(x,y,z),white,board);o.rotation_euler=(math.pi,0,math.pi);return o
# Named items explicitly documented in Waveshare Onboard Resources, photo-estimated packages.
part('ESP32-S3-WROOM-1-N16R8 shield',258,324,18,17,2.4,silver)
part('ESP32 antenna keepout substrate',178,324,6,18,1.2,chip)
for n,px,py,w,h,d in [('ES8311 codec',389,302,3.5,3.5,1.2),('NS4150B amplifier',376,386,2.8,3,1.2),('QMI8658 IMU',481,325,2.5,2.5,.8),('TG28 PMIC - revision unresolved',631,325,5,5,1.2),('PCF85063 RTC',230,233,3,2.4,1),('SHTC3 sensor',175,204,2,2,.8)]:part(n,px,py,w,h,d,chip)
part('Microphone',785,235,3,3,1.5,silver)
part('TF socket',745,427,15,15,2,silver)
part('USB-C shell',782,325,8,9,3,silver)
part('USB-C dark mouth',806,325,.5,7,2,chip)
part('Display FPC socket',596,184,6,16,2.2,cream)
part('Display flex tail',646,186,8,16,.3,ribbon)
for name,px in [('SPK',438),('RTC',512),('BAT',589)]:
 part(name+' MX1.25 header',px,491,8,4,3,cream)
 backlabel(name,px-15,470,1.4,-.86)
for name,px in [('PWR',256),('BOOT',324)]:part(name+' switch',px,510,4,2,2,silver)
x,y=xy(288,157);cyl('Source rotary button',6,3,(x,y,-3),chip,board);part('Rotary metal body',288,171,10,8,2.5,silver)
for px,py in [(174,149),(788,148),(173,500),(789,500)]:
 x,y=xy(px,py);cyl('Source mounting annulus',1.7,.15,(x,y,-.88),gold,board);cyl('Mount bore visual',.85,.17,(x,y,-.98),chip,board)
for px in range(631,800,17):
 x,y=xy(px,509);cyl('Source GPIO pad row',.7,.15,(x,y,-.9),gold,board)
backlabel('ESP32-S3',222,315,2.1,-3.25);backlabel('3.97 / WAVESHARE',224,447,2.1,-.84)
# Small detail is attached only to the identified photographed components.
# Pin counts here are illustrative package graphics, not electrical footprints.
pcbmat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.92
pcbmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.12
for label,px,py,w in [('ES8311',389,302,3.5),('NS4150B',376,386,2.8),('QMI8658',481,325,2.5),('TG28*',631,325,5)]:
 x,y=xy(px,py)
 for side in (-1,1):
  for j in (-1,0,1):box('Illustrative pins '+label,(.6,.3,.25),(x+side*(w/2+.22),y+j*.65,-1.05),silver,.02,board)
 backlabel(label,px-8,py+24,1.15,-.85)
backlabel('COMPONENT SIZES / PLACEMENT APPROX.',360,438,1.1,-.85)
# Source-photo based package arrangement, not a PCB fabrication layout.
board['component_layout']='Official details image pixel anchors; package sizes/heights approximate. Component face below display in closed assembly.'

screen=group('03 | 3.97 E-PAPER - exact active 86.40 x 51.84 mm')
back=rr('Concept display carrier',96,57,1,17.2,19,edge,screen);back.location=(1,6,0)
dis=box('Active area EXACT 86.40 x 51.84', (86.4,51.84,.6),(3,6,19.4),paper,0,screen);dis['geometry_status']='86.40 x 51.84 sourced; offset and stack height conceptual'
# Quiet, nonemissive, readable software mockup on the actual screen surface.
text('UI top','HERMES   /   WI-FI',2.3,(-35,26,19.73),ink,screen)
box('UI rule',(73,.22,.02),(3,21.5,19.73),ink,0,screen)
text('UI headline','Ready when you are.',4.4,(-35,12,19.73),ink,screen)
text('UI instruction','Hold the orange key to speak.',2.6,(-35,3,19.73),ink,screen)
text('UI example','A quiet screen. A spoken reply.',2.4,(-35,-5,19.73),ink,screen)
text('UI bottom','VOICE   /   LOCAL CONCEPT',1.85,(-35,-15,19.73),ink,screen)

front=group('04 | FRONT FASCIA - real display and acoustic apertures')
f=rr('Front fascia through-cut solid',112,84,6,20.4,23,shell,front)
c=rr('DISPLAY WINDOW THROUGH CUT',87.2,52.6,1,18,26,shell);c.location=(3,6,0);cut(f,c)
# Fully cut grille slots, not painted black holes.
for row in (-36.3,-33.5,-30.7):
 for x in (13,20,27,34,41):
  c=rr('Speaker slot cutter',4.6,1.35,.65,19,25,shell);c.location=(x,row,0);cut(f,c)
cut(f,box('PTT aperture',(23,9,6),(-29,-33.5,22),shell,2))
cut(f,cyl('Mic vent through fascia',.85,7,(-45,-31,22),shell))
ptt=box('Orange PTT cap - conceptual remote actuator',(21.8,7.8,2.9),(-29,-33.5,22.5),orange,1.6,front)
text('PTT legend','HOLD',1.9,(-33,-33.5,23.98),ink,front)
text('Front identity','03.97',1.5,(41,36.5,23.02),white,front)
for x in (-51,51):
 for y in (-37,37):
  cut(f,cyl('Front screw counterbore',1.7,5,(x,y,22),shell))
  o=cyl('Captive screw',1.5,1,(x,y,21.3),silver,front)
  cut(o,box('Screw driver slot',(2,.4,1),(x,y,21.8),chip,.04))
# Separate actual acoustic volume below grille, illustrative driver dimensions.
audio=group('05 | CONCEPT AUDIO / CONTROL INTEGRATION')
a=box('Concept speaker enclosure',(37,12,7),(27,-33.5,14.5),edge,2,audio)
box('Speaker grille backing',(33,9,.6),(27,-33.5,18.5),meshmat,.5,audio)
for x in range(12,43,2):box('Acoustic mesh horizontal',( .24,8,.1),(x,-33.5,18.86),silver,0,audio)
box('PTT switch reservation',(18,7,3),(-29,-33.5,17),chip,1,audio)
# Planned cable routes shown only as conceptual paired conductors; no fake daughterboard.
def wire(n,coords,ma):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.bevel_depth=.32;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(coords)-1)
 for p,c in zip(sp.bezier_points,coords):p.co=c;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(o);cu.materials.append(ma);o.parent=audio
wire('Concept speaker lead',[(25,-29,14),(23,-25,8),(8,-24,8),(6,-21,10)],orange)
wire('Concept speaker return',[(27,-29,14),(25,-26,7.5),(9,-25,7.5),(7,-21,10)],edge)

# Film: finished hero, honest exploded reveal, retained layers close, final hero.
def key(o,fr,loc=None,rot=None):
 if loc is not None:o.location=loc;o.keyframe_insert(data_path='location',frame=fr)
 if rot is not None:o.rotation_euler=rot;o.keyframe_insert(data_path='rotation_euler',frame=fr)
for fr in (1,48):
 key(board,fr,(0,6,14),(0,0,0));key(screen,fr,(0,0,0));key(front,fr,(0,0,0));key(audio,fr,(0,0,0))
for fr in (120,192):
 key(board,fr,(0,6,55),(0,0,0) if fr==120 else (math.pi,0,math.pi));key(screen,fr,(0,0,83));key(front,fr,(0,0,124));key(audio,fr,(0,-10,18))
# Rotate across the short axis, then yaw: same revealed face, smaller sweep.
key(board,144,(0,6,55),(math.pi,0,math.pi))
key(board,216,(0,6,55),(0,0,0))
# Stagger assembly; board turns back to its honest underside orientation.
key(board,264,(0,6,14),(0,0,0));key(audio,264,(0,0,0));key(screen,264,(0,0,83));key(screen,324,(0,0,0));key(front,324,(0,0,124));key(front,384,(0,0,0))
for g in (board,screen,front,audio):
 key(g,480,tuple(g.location),tuple(g.rotation_euler))

def aim(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(140,-195,225));cam=bpy.context.object;cam.name='Product camera';cam.data.type='ORTHO';s.camera=cam
for fr,l,t,scale in [(1,(130,-190,215),(0,0,10),176),(48,(115,-200,215),(0,0,10),176),(120,(195,-255,165),(0,0,73),280),(192,(205,-255,170),(0,0,73),280),(264,(205,-255,170),(0,0,73),280),(324,(205,-255,170),(0,0,73),280),(384,(120,-195,230),(0,0,11),178),(480,(90,-205,235),(0,0,11),174)]:
 cam.location=l;aim(cam,t);cam.keyframe_insert(data_path='location',frame=fr);cam.keyframe_insert(data_path='rotation_euler',frame=fr);cam.data.ortho_scale=scale;cam.data.keyframe_insert(data_path='ortho_scale',frame=fr)
box('Infinite studio floor',(2000,2000,2),(0,0,-2),floor,0)
for l,power,size in [((-90,-120,260),1800000,190),((150,30,160),1200000,160),((-110,160,150),2100000,140)]:
 bpy.ops.object.light_add(type='AREA',location=l);o=bpy.context.object;o.data.energy=power/6;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,40))
s.world.color=(.18,.18,.18)
s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.use_persistent_data=True
s.render.resolution_x=1280;s.render.resolution_y=960;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.fps=24;s.frame_start=1;s.frame_end=480
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.render.threads_mode='FIXED';s.render.threads=6
s['DISCLOSURE']='CONCEPT STUDY. Exact board 99.50 x 60.00 mm and active area 86.40 x 51.84 mm. Case 112 x 84 x 23 mm proposed. All other geometry, ports, PTT linkage, audio chamber, display thickness, stack and clearances conceptual, not physical fit proof. Wi-Fi only; no LTE/HAT; no invented battery/capacity.'
s.frame_set(440)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'voice397-wifi.blend'))
report={'board_outline_mm':[99.5,60],'board_radius_mm':2,'display_active_mm':[86.4,51.84],'proposed_case_mm':[112,84,23],'cavity_mm':[108,80],'lateral_board_clearance_mm':[4.25,4.0],'frame_count':480,'fps':24,'film_seconds':20,'battery':'not modeled; USB concept; battery selection unresolved','geometry_status':s['DISCLOSURE'],'sources':['https://docs.waveshare.com/ESP32-S3-ePaper-3.97'],'object_count':len(s.objects)}
(ROOT/'design-contract.json').write_text(json.dumps(report,indent=2))
print('BUILD_COMPLETE',json.dumps(report),flush=True)
