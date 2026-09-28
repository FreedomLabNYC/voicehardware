"""Real Chromium WebGL QA. Local ephemeral server; never touches existing qa/page-* files."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading, json, sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa/interactive';OUT.mkdir(exist_ok=True,parents=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,format,*args):pass
    def do_GET(self):
        path=Path(self.translate_path(self.path))
        if path.suffix!='.mp4' or not path.is_file():return super().do_GET()
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
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'site')))
threading.Thread(target=server.serve_forever,daemon=True).start()
report={'devices':[], 'errors':[], 'network_errors':[], 'screenshots':[]}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width in (1440,390):
   page=browser.new_page(viewport={'width':width,'height':1000 if width==1440 else 844},device_scale_factor=1,is_mobile=width==390,has_touch=width==390)
   page.on('pageerror',lambda e:report['errors'].append(str(e)))
   page.on('response',lambda r:report['network_errors'].append([r.status,r.url]) if r.status>=400 else None)
   page.goto(sys.argv[1] if len(sys.argv)>1 else f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('document.querySelectorAll("[data-ready=true]").length===4')
   assert page.locator('[data-device]').evaluate_all('(es)=>es.map(e=>e.dataset.device)')==['stick','note4','397','154']
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   for i,kind in enumerate(['stick','note4','397','154']):
    section=page.locator(f'[data-device="{kind}"]');stage=section.locator('.stage');stage.scroll_into_view_if_needed();page.wait_for_timeout(250)
    def state():return page.evaluate('(i)=>hardwareViewers[i].snapshot()',i)
    def scrub(v):
     section.locator('input').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}));}',v);page.wait_for_timeout(150)
    def labels():
     s=state();rs=[x['rect'] for x in s['labels']]
     for j,a in enumerate(rs):
      for b in rs[j+1:]:assert not(a['left']<b['right'] and a['right']>b['left'] and a['top']<b['bottom'] and a['bottom']>b['top']),s
     assert all(x['id']==x['hitPart'] for x in s['labels'])
     return len(rs)
    def shot(name):
     path=OUT/f'{kind}-{width}-{name}.png';stage.screenshot(path=str(path));report['screenshots'].append(str(path.relative_to(ROOT)))
    shot('assembled');scrub(0);initial=state()['parts'];count=labels();shot('exploded')
    for v in [25,70,100,70,25,0]:scrub(v);labels()
    assert state()['parts']==initial,'Backward scrub changed the absolute geometry'
    # Callout click actually selects + material highlight (not only DOM styling).
    callouts=section.locator('.callout:visible');assert callouts.count()>0
    chosen=callouts.first.get_attribute('data-part');callouts.first.click();assert state()['selected']==chosen
    assert page.evaluate('([i,id])=>hardwareViewers[i].meshes.some(o=>o.userData.part===id&&o.material.emissive?.getHex()>0)',[i,chosen])
    # Parts list remains usable when the matching geometry is occluded.
    section.locator('.parts [data-part="board"]').click();assert state()['selected']=='board'
    stage.scroll_into_view_if_needed();page.wait_for_timeout(200)
    before=state()['camera'];r=stage.bounding_box();page.mouse.move(r['x']+r['width']*.48,r['y']+r['height']*.65);page.mouse.down();page.mouse.move(r['x']+r['width']*.73,r['y']+r['height']*.56,steps=12);page.mouse.up();page.wait_for_timeout(150)
    assert state()['camera']!=before,'Orbit drag failed';labels();shot('orbited')
    # Mobile additionally exercises a real touch gesture, not just mouse emulation.
    if width==390:
     cdp=page.context.new_cdp_session(page);before_touch=state()['camera'];x=r['x']+r['width']*.5;y=r['y']+r['height']*.6
     cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
     for step in range(1,9):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+step*9,'y':y-step*2}]})
     cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_timeout(100);assert state()['camera']!=before_touch
     cdp.detach()
    # Keyboard orbit and zoom, usable without pointer precision.
    canvas=stage.locator('canvas');canvas.focus();before=state()['camera'];canvas.press('ArrowLeft');canvas.press('+');assert state()['camera']!=before
    section.locator('.play').click();stage.scroll_into_view_if_needed();page.wait_for_timeout(400);section.locator('.play').click();paused=state()['progress'];assert paused>0;page.wait_for_timeout(220);assert state()['progress']==paused
    section.locator('.play').click();stage.scroll_into_view_if_needed();page.wait_for_timeout(300);section.locator('.play').click();assert state()['progress']>paused
    section.locator('.reset').click();assert state()['progress']==1 and not state()['playing'];assert state()['selected'] is None
    # Occluded internal callouts are absent in closed state, regardless of selection.
    stage.scroll_into_view_if_needed();page.wait_for_timeout(150);assert not any(x['id']=='board' for x in state()['labels'])
    canvas.focus()
    for _ in range(26):canvas.press('ArrowRight')
    page.wait_for_timeout(180);labels();assert not any(x['id']=='display' for x in state()['labels']),'Display callout showed through opaque back'
    shot('back');section.locator('.reset').click()
    report['devices'].append({'kind':kind,'width':width,'meshes':state()['meshes'],'exploded_labels':count,'deterministic_scrub':True,'orbit':True,'click_highlight':True,'pause_resume':True,'reset':True,'no_label_overlap':True})
   page.locator('.films summary').click()
   for video in page.locator('video').all():
    video.evaluate('(v)=>v.load()');video.evaluate('(v)=>new Promise((resolve,reject)=>{if(v.readyState>=1)return resolve();v.onloadedmetadata=()=>resolve();v.onerror=()=>reject("video load");})');video.evaluate('(v)=>{v.currentTime=2;return v.play()}');page.wait_for_timeout(150);video.evaluate('(v)=>v.pause()');assert video.evaluate('(v)=>v.currentTime>=2 && v.paused')
   assert page.locator('.project-nav a').get_attribute('href')=='https://github.com/FreedomLabNYC/voicehardware'
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   page.screenshot(path=str(OUT/f'page-{width}.png'),full_page=True)
   page.close()
  browser.close()
 assert not report['errors'],report['errors']
 assert not report['network_errors'],report['network_errors']
 report['passed']=True
finally:
 server.shutdown();server.server_close();(OUT/'results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
