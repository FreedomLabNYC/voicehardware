"""Apply concept labels to actual Blender still renders. Pillow avoids FFmpeg font-filter dependencies."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
import os
font=os.environ.get('VOICE_FONT') or next((f for f in ['/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf'] if Path(f).exists()), 'DejaVuSans.ttf')
for n in ('finished','exploded'):
 im=Image.open(R/'assets'/(n+'-raw.png')).convert('RGB');d=ImageDraw.Draw(im)
 d.text((36,28),'03.97  /  WI-FI',font=ImageFont.truetype(font,27),fill='#d7dfdf')
 d.text((1244,32),'CONCEPT STUDY',anchor='ra',font=ImageFont.truetype(font,15),fill='#d7dfdf')
 d.text((36,926),'Source board 99.50 x 60.00 mm. Enclosure + other geometry conceptual; not fit-tested.',font=ImageFont.truetype(font,16),fill='#d7dfdf')
 im.save(R/(n+'.png'))
 print(n,im.size)
