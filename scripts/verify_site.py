"""Exercise real website media and layout locally or at an explicit public URL."""
from pathlib import Path
import functools,http.server,threading,json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];Q=R/'qa';Q.mkdir(exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def do_GET(self):
  path=Path(self.translate_path(self.path))
  if path.suffix=='.mp4' and path.is_file():
   data=path.read_bytes();n=len(data);a,b=0,n-1
   request=self.headers.get('Range','')
   if request.startswith('bytes='):
    left,right=request[6:].split('-',1);a=int(left or 0);b=min(int(right) if right else n-1,n-1)
   self.send_response(206 if request else 200)
   self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes')
   if request:self.send_header('Content-Range',f'bytes {a}-{b}/{n}')
   self.send_header('Content-Length',str(b-a+1));self.end_headers()
   try:self.wfile.write(data[a:b+1])
   except (BrokenPipeError,ConnectionResetError):pass
  else:super().do_GET()
server=None
if len(sys.argv)>1:url=sys.argv[1]
else:
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R/'site')))
 threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/'
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True);page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  response=page.goto(url);assert response.status==200
  page.wait_for_function('Array.from(document.querySelectorAll("video")).length===3 && Array.from(document.querySelectorAll("video")).every(v=>v.readyState>=1)',timeout=60000)
  assert page.locator('.hardware').count()==3
  assert page.locator('.hardware a').count()>=8
  link=page.locator('.project-nav a');assert link.get_attribute('href')=='https://github.com/FreedomLabNYC/voicehardware'
  assert link.get_attribute('target')=='_blank'
  for v in page.locator('video').all():
   v.evaluate('(v)=>{v.muted=true;return v.play()}');v.evaluate('v=>v.pause()');v.evaluate('v=>v.currentTime=2')
   v.evaluate('(v)=>v.seeking ? new Promise(resolve=>v.addEventListener("seeked",resolve,{once:true})) : Promise.resolve()')
   assert abs(v.evaluate('v=>v.currentTime')-2)<.2
  for w,h in [(1440,1000),(390,844)]:
   page.set_viewport_size({'width':w,'height':h});page.evaluate('scrollTo(0,0)')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   box=link.bounding_box();assert box['x']>w/2 and box['y']<100
   page.screenshot(path=str(Q/f'page-{w}.png'),full_page=True)
  assert not errors,errors
  result={'url':url,'status':'PASS','videos':3,'hardware_sections':3,'hardware_links':page.locator('.hardware a').count(),'play_seek_pause':'pass','desktop_mobile_overflow':False,'page_errors':errors}
  (Q/'site-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));b.close()
finally:
 if server:server.shutdown();server.server_close()
