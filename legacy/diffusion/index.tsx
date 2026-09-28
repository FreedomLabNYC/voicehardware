type Card = { id:string; start:number; end:number; n:string; title:string; line1:string; line2:string; source:string; x:number; y:number };

const cards: Card[] = [
  {id:'power-card', start:3.7, end:6.45, n:'01 / POWER BAYS', title:'Shared 1S power path', line1:'Protected pack: selection pending', line2:'Power wiring: unbench-tested', source:'Conceptual carrier stack · no shipping claim', x:480, y:470},
  {id:'hat-card', start:7.35, end:10.35, n:'02 / CELLULAR SHELF', title:'SIM7080G LTE-M / NB-IoT HAT', line1:'Cheapest quote: ship $11.20', line2:'ETD: 12–28 days to 10014', source:'Waveshare SKU17693 · quote Sep 13', x:538, y:272},
  {id:'audio-card', start:10.75, end:13.45, n:'03 / I/O LAYER', title:'PTT + audio carrier', line1:'Physical PTT + speaker interface', line2:'Fit and wiring: unbench-tested', source:'Illustrative internal geometry', x:519, y:425},
  {id:'core-card', start:13.85, end:16.55, n:'04 / CORE SEAT', title:'3.97-inch reader core', line1:'SKU33552 revision pending', line2:'Fit: not bench-verified', source:'Board outline: 99.5 × 60 mm · research Sep 12', x:510, y:432},
  {id:'display-card', start:16.95, end:19.85, n:'05 / FRONT ASSEMBLY', title:'Display + fascia close', line1:'Components remain seated below', line2:'Case stack-up: not fit-tested', source:'Conceptual tray model', x:500, y:350},
];

function OverlayCard(p: Card) {
  const cardX=730, cardY=103, cardW=276, cardH=205;
  return <html id={p.id} x={0} y={0} width={1048} height={720} start={p.start} end={p.end}>
    <div style="position:relative;width:1048px;height:720px;font-family:Inter,Arial,sans-serif;color:#202523;">
      <svg style="position:absolute;inset:0;width:1048px;height:720px;overflow:visible" aria-hidden="true">
        <path d={`M730 286 L710 286 L${p.x} ${p.y}`} fill="none" stroke="#3477a2" stroke-width="1.25"/>
        <circle cx={p.x} cy={p.y} r="3.5" fill="#f3f4ef" stroke="#3477a2" stroke-width="1.25"/>
      </svg>
      <div style={`position:absolute;left:${cardX}px;top:${cardY}px;width:${cardW}px;height:${cardH}px;box-sizing:border-box;background:#f8f8f3;border:1px solid #c7cbc4;padding:12px;`}>
        <div style="font:10px/1.2 'SF Mono',Menlo,monospace;letter-spacing:.4px;color:#2d6f9d">{p.n}</div>
        <div style="margin-top:10px;font-size:18px;line-height:1.1;letter-spacing:-.3px">{p.title}</div>
        <div style="margin-top:13px;font-size:13px;line-height:1.45">{p.line1}<br/>{p.line2}</div>
        <div style="position:absolute;left:12px;right:12px;bottom:10px;border-top:1px solid #d4d7d1;padding-top:6px;font:7px/1.2 'SF Mono',Menlo,monospace;color:#626863">{p.source}</div>
      </div>
    </div>
  </html>;
}

function Summary() {
 return <html id="summary" x={0} y={0} width={1048} height={720} start={20.25} end={22.75}>
  <div style="position:relative;width:1048px;height:720px;font-family:Inter,Arial,sans-serif;color:#202523;">
   <div style="position:absolute;left:443px;top:119px;width:526px;height:164px;box-sizing:border-box;background:#f8f8f3;border:1px solid #c7cbc4;padding:16px;">
    <div style="font:10px/1.2 'SF Mono',Menlo,monospace;letter-spacing:.4px;color:#2d6f9d">READER + LTE HAT / FLUSH-FOOTPRINT CONCEPT</div>
    <div style="margin-top:11px;font-size:19px;letter-spacing:-.35px">LTE HAT cheapest live shipping: $11.20</div>
    <div style="margin-top:8px;font-size:13px">Registered Post Air Mail · ETD 12–28 days · ZIP 10014</div>
    <div style="margin-top:10px;font:9px/1.2 'SF Mono',Menlo,monospace;color:#626863">Proposed enclosure stack · electrical, RF and fit validation pending</div>
   </div>
  </div>
 </html>
}

export default function Project() {
 return <stage background="#f3f4ef" camera={[0.62,0,0,0.62,75,85]}>
  <scene id="reader-v5-scene" name="Reader 3.97 flush-footprint assembly" width={1048} height={720} fill="#f3f4ef" active workarea={[0,22.75]}>
   <video id="blender-plates" src="assets/reader397-v5-plates.mp4" x={0} y={0} width={1048} height={720} start={0} end={22.75} muted />
   <html id="page-chrome" x={0} y={0} width={1048} height={720} end={22.75}>
    <div style="position:relative;width:1048px;height:720px;font-family:Inter,Arial,sans-serif;color:#202523;pointer-events:none;">
     <div style="position:absolute;left:42px;top:63px;font:11px/1 'SF Mono',Menlo,monospace;letter-spacing:.3px">VOICE HARDWARE / CONCEPT STUDY</div>
     <div style="position:absolute;left:789px;top:69px;font:9px/1 'SF Mono',Menlo,monospace;color:#626863">ASSEMBLY / 02</div>
     <div style="position:absolute;left:42px;right:42px;top:82px;border-top:1px solid #d5d7d1"></div>
     <div style="position:absolute;left:42px;top:600px;font-size:13px">3.97 READER + OPTIONAL LTE-M HAT</div>
     <div style="position:absolute;left:42px;top:620px;font:8px/1.2 'SF Mono',Menlo,monospace;color:#626863">Flush X/Y footprint · rear stack grows in depth · clearances and wiring unbench-tested</div>
     <div style="position:absolute;left:42px;right:42px;top:708px;border-top:1px solid #d5d7d1"></div>
     <div style="position:absolute;left:42px;top:708px;width:964px;border-top:2px solid #3477a2"></div>
    </div>
   </html>
   <OverlayCard {...cards[0]} /><OverlayCard {...cards[1]} /><OverlayCard {...cards[2]} /><OverlayCard {...cards[3]} /><OverlayCard {...cards[4]} /><Summary />
  </scene>
 </stage>
}
