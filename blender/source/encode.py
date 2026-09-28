"""Encode actual rendered frames with Pillow type, probe, fully decode, extract QA."""
import subprocess,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
frames=list((R/'frames').glob('frame-*.png'))
assert len(frames)==480, f'Need 480 actual frames; got {len(frames)}'
for f in range(1,481):assert (R/'frames'/f'frame-{f:04d}.png').stat().st_size>1000
import os
font=os.environ.get('VOICE_FONT') or next((f for f in ['/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf'] if Path(f).exists()), 'DejaVuSans.ttf')
fonts={s:ImageFont.truetype(font,s) for s in (12,17,20)}
copy=[('A quiet screen. A spoken reply.',0,2),('Built around the 99.50 x 60.00 mm source board.',2,8),('Controller and audio return to the enclosure.',8,11),('The e-paper display seats behind a real aperture.',11,13.5),('One complete device.',13.5,16),('Hold to speak. Release to listen.',16,20)]
out=R/'voice397-wifi.mp4'
cmd=['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','960x720','-framerate','24','-i','pipe:0','-frames:v','480','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for f in range(1,481):
 im=Image.open(R/'frames'/f'frame-{f:04d}.png').convert('RGB');assert im.size==(960,720)
 d=ImageDraw.Draw(im);d.text((28,22),'03.97  /  WI-FI',font=fonts[20],fill='#e4e7e4');d.text((932,25),'CONCEPT STUDY',anchor='ra',font=fonts[12],fill='#adb8b8')
 d.text((28,694),'Concept geometry except sourced board outline + display area. Not fit-tested.',font=fonts[12],fill='#b3bebe')
 t=(f-1)/24
 for message,lo,hi in copy:
  if lo<=t<hi:d.text((28,668),message,font=fonts[17],fill='#e4e7e4')
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]))
v=probe['streams'][0]
assert v['codec_name']=='h264' and (v['width'],v['height'])==(960,720)
assert v['nb_read_frames']=='480' and v['r_frame_rate']=='24/1'
assert abs(float(probe['format']['duration'])-20)<.01
p=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],capture_output=True,text=True);assert p.returncode==0,p.stderr
subprocess.run(['ffmpeg','-y','-i',str(out),'-vf','fps=1/2,scale=480:360,tile=5x2','-frames:v','1','-update','1',str(R/'encoded-contact-sheet.jpg')],check=True)
probe['validation']={'expected_frames':480,'actual_frames':int(v['nb_read_frames']),'full_decode_exit_code':p.returncode,'full_decode_stderr':p.stderr,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'file_bytes':out.stat().st_size,'audio':'intentionally silent','native_render_dimensions':[960,720],'film_engine':'Blender EEVEE 32 samples','stills_engine':'Blender Cycles 32 samples'}
(R/'video-validation.json').write_text(json.dumps(probe,indent=2))
print(json.dumps(probe['validation'],indent=2))
