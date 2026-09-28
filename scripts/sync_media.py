"""Refresh current movie/poster and its HTML hash after a full render."""
from pathlib import Path
import hashlib, re, shutil, subprocess
R=Path(__file__).resolve().parents[1]
p=R/'blender/voice397-wifi.mp4'
assert p.exists(), 'Render and encode the full movie first'
shutil.copy2(p,R/'site/assets/eevee.mp4')
subprocess.run(['ffmpeg','-v','error','-y','-ss','18','-i',str(p),'-frames:v','1','-update','1',str(R/'site/assets/eevee.jpg')],check=True)
f=R/'site/index.html'; s=f.read_text(); marker='aria-labelledby="eevee"'; start=s.index(marker); end=s.index('</section>',start)
chunk=s[start:end]; chunk=re.sub(r'SHA-256<br>[a-f0-9]{64}', 'SHA-256<br>'+hashlib.sha256(p.read_bytes()).hexdigest(),chunk)
f.write_text(s[:start]+chunk+s[end:]);print('Current movie, poster and hash updated; review copy and publish separately.')
