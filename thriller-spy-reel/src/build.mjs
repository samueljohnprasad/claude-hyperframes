/* Build editable HTML from the measured voice timings. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const root=path.resolve(import.meta.dirname,'..');
const req=createRequire(import.meta.url);
const ot=req(path.join(root,'assets/vendor/opentype.cjs'));
const font=ot.loadSync(path.join(root,'assets/fonts/LeagueGothic.ttf'));
const meta=JSON.parse(await fs.readFile(path.join(root,'timing.json'),'utf8'));
const art=await fs.readFile(path.join(root,'assets/art.js'),'utf8');
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const config={
 intro:{title:['HOLLYWOOD','THRILLERS'],tag:'FIVE HOLLYWOOD THRILLERS YOU SHOULD KNOW',bg:'#d23a22',fg:'#efe4c9'},
 silence:{rank:5,year:1991,title:['THE SILENCE','OF THE LAMBS'],tag:'THE HUNTER ENTERS THE MIND',bg:'#efe4c9',fg:'#1b1714',poster:'assets/posters/silence.jpg'},
 se7en:{rank:4,year:1995,title:['SE7EN'],tag:'SEVEN SINS. ONE NIGHTMARE.',bg:'#efe4c9',fg:'#1b1714',poster:'assets/posters/se7en.jpg'},
 psycho:{rank:3,year:1960,title:['PSYCHO'],tag:'CHECK IN. NEVER CHECK OUT.',bg:'#1b1714',fg:'#efe4c9',poster:'assets/posters/psycho.jpg'},
 prestige:{rank:2,year:2006,title:['THE','PRESTIGE'],tag:'EVERY DETAIL IS AN ILLUSION',bg:'#d23a22',fg:'#efe4c9',poster:'assets/posters/prestige.jpg'},
 darkknight:{rank:1,year:2008,title:['THE DARK','KNIGHT'],tag:'CHAOS BECOMES A WEAPON',bg:'#efe4c9',fg:'#1b1714',poster:'assets/posters/darkknight.jpg'},
 outro:{title:['SAVE THE','WATCHLIST'],tag:'WHICH THRILLER IS YOUR #1?',bg:'#e2a52a',fg:'#1b1714'}
};
const artKinds={silence:'jury',se7en:'jury',psycho:'forrest',prestige:'shawshank',darkknight:'godfather'};
const hash=n=>{let x=Math.sin(n*51.2+99)*28317;return x-Math.floor(x)};
function flatten(commands){const contours=[];let p=[],px=0,py=0;for(const c of commands){if(c.type==='M'){p=[];contours.push(p);p.push([c.x,c.y]);px=c.x;py=c.y;}else if(c.type==='L'){p.push([c.x,c.y]);px=c.x;py=c.y;}else if(c.type==='Q'||c.type==='C'){for(let j=1;j<=10;j++){const t=j/10,u=1-t;if(c.type==='Q')p.push([u*u*px+2*u*t*c.x1+t*t*c.x,u*u*py+2*u*t*c.y1+t*t*c.y]);else p.push([u**3*px+3*u*u*t*c.x1+3*u*t*t*c.x2+t**3*c.x,u**3*py+3*u*u*t*c.y1+3*u*t*t*c.y2+t**3*c.y]);}px=c.x;py=c.y;}}return contours;}
function recut(points,seed){let s=0,out=[];for(let i=0;i<points.length;i++){let a=points[i],b=points[(i+1)%points.length],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1,n=Math.max(1,Math.ceil(l/9));for(let j=0;j<n;j++){let u=j/n,d=j?(Math.sin((s+u*l)*.09+seed)*.9+Math.sin((s+u*l)*.23+seed)*.35):0;out.push([a[0]+u*dx-dy/l*d,a[1]+u*dy+dx/l*d]);}s+=l;}return 'M'+out.map(p=>p.map(n=>n.toFixed(2)).join(',')).join('L')+'Z';}
function titleSVG(lines,color){
 let groups=[];lines.forEach((text,row)=>{const size=155;const advance=font.getAdvanceWidth(text,size);const sx=Math.min(1,775/advance);let x=0;for(let i=0;i<text.length;i++){const glyph=font.charToGlyph(text[i]);const cmd=glyph.getPath(x,145+row*140,size).commands;const d=flatten(cmd).map(p=>recut(p,i+row*17)).join('');groups.push(`<g transform="translate(0 ${((hash(i+row*31)-.5)*2).toFixed(2)}) scale(${sx} 1)"><path fill="${color}" fill-rule="evenodd" d="${d}"/></g>`);x+=glyph.advanceWidth*size/font.unitsPerEm;}});
 return `<svg class="cut-title" viewBox="0 0 800 300" role="img" aria-label="${esc(lines.join(' '))}">${groups.join('')}</svg>`;
}
function captions(scene){
  const raw=scene.text.split(/\s+/);const words=scene.words.slice(0,raw.length);let groups=[];
  // ASR supplies acoustic anchors; the script supplies spelling and punctuation.
  for(let i=0;i<raw.length;){let end=Math.min(raw.length,i+5);if(end<raw.length&&/[.!?]$/.test(raw[end-2]||''))end--;
    const index=Math.min(words.length-1,i);
    const start=scene.voiceStart-scene.start+(words[index]?.start||0);
    groups.push({text:raw.slice(i,end).join(' '),start});i=end;
  }
  return groups.map((p,i)=>({...p,duration:Math.max(.1,(groups[i+1]?.start??Math.min(scene.duration-.05,scene.voiceStart-scene.start+scene.speechDuration+.3))-p.start)}));
}
await fs.mkdir(path.join(root,'compositions'),{recursive:true});
const hosts=[];const cueSheet=[];const allCaptions=[];
for(const scene of meta.scenes){
 const c=config[scene.id],id='drama-'+scene.id;const titleAt=scene.id==='intro'||scene.id==='outro'||scene.id==='silence'?0:scene.voiceStart-scene.start+(scene.words[2]?.start??.65);
 const caps=captions(scene);const bottom=scene.id==='outro'?1133:1118;
 for(let i=0;i<caps.length;i++){const p=caps[i];allCaptions.push({...p,id:`drama-${scene.id}-cap-${i}`,start:scene.start+p.start,light:c.bg==='#d23a22'||c.bg==='#1b1714'});}
 const tagAt=scene.id==='godfather'?7.0:Math.min(scene.duration-2.8,Math.max(2.4,scene.duration*.52));
 const list=scene.id==='outro'?['5   THE SILENCE OF THE LAMBS','4   SE7EN','3   PSYCHO','2   THE PRESTIGE','1   THE DARK KNIGHT'].map((x,i)=>`<div id="drama-outro-list-${i}" class="list-row" style="top:${566+i*112}px;color:${i%2?'#efe4c9':'#1b1714'}">${x}</div>`).join(''):'';
 const markup=`<!doctype html><html><head><meta charset="UTF-8"><title>${esc(c.title.join(' '))}</title></head><body><template>
<style>
@font-face{font-family:'League Gothic';src:url('assets/fonts/LeagueGothic.ttf')}@font-face{font-family:'League Spartan';src:url('assets/fonts/LeagueSpartan.ttf');font-weight:100 900}
#root{position:absolute;inset:0;overflow:hidden;background:${c.bg};color:${c.fg};font-family:'League Spartan';}
.paper-art{position:absolute;inset:0;width:1080px;height:1920px}
.poster-frame{position:absolute;left:150px;top:600px;width:780px;height:610px;padding:18px;background:#efe4c9;box-shadow:8px 10px 0 rgba(27,23,20,.35);transform:rotate(-1.2deg);object-fit:cover}
.poster-frame img{display:block;width:100%;height:100%;object-fit:contain;background:#1b1714}
.kicker{position:absolute;left:110px;top:196px;font-size:29px;font-weight:700;letter-spacing:3px}
.movie-title{position:absolute;left:110px;top:${scene.id==='outro'?230:270}px;width:800px;height:300px}.cut-title{width:800px;height:300px;overflow:visible}
.rank{position:absolute;left:790px;top:188px;width:120px;height:105px;font-family:'League Gothic';font-size:106px;line-height:1;text-align:center}
.year{position:absolute;left:112px;top:260px;font-size:32px;font-weight:600;letter-spacing:2px}
.tag-clip{position:absolute;inset:0}.tagline{position:absolute;left:110px;top:${bottom}px;font-size:37px;font-weight:800;letter-spacing:1px;max-width:804px;line-height:1.12}
.caption-clip{position:absolute;inset:0}.caption-strip{position:absolute;left:108px;top:1220px;width:810px;min-height:116px;background:${c.bg==='#efe4c9'||c.bg==='#e2a52a'?'#1b1714':'#efe4c9'};color:${c.bg==='#efe4c9'||c.bg==='#e2a52a'?'#efe4c9':'#1b1714'};padding:17px 24px 18px 36px;font-size:44px;font-weight:600;line-height:1.15;clip-path:polygon(1% 1%,98% 0,100% 10%,99% 95%,2% 100%,0 84%,1% 44%,0 8%);}
.caption-strip:before{content:'';position:absolute;left:14px;top:28px;width:9px;height:12px;background:${c.bg==='#d23a22'?'#d23a22':'#e2a52a'}}
.list-row{position:absolute;left:190px;width:670px;font-size:41px;line-height:70px;font-weight:700;letter-spacing:.2px}
.intro-number{position:absolute;left:350px;top:535px;width:370px;height:370px;border-radius:50%;background:#1b1714;color:#efe4c9;font-family:'League Gothic';font-size:330px;line-height:390px;text-align:center;transform:rotate(-5deg)}
.intro-ribbon{position:absolute;left:120px;top:1015px;width:820px;min-height:82px;padding:18px 30px;background:#efe4c9;color:#1b1714;font-size:34px;font-weight:800;line-height:1.05;transform:rotate(-1.5deg);clip-path:polygon(1% 4%,98% 0,100% 12%,99% 92%,3% 100%,0 82%,1% 42%,0 12%)}
</style>
<div id="root" data-composition-id="${id}" data-width="1080" data-height="1920" data-duration="${scene.duration}">
 <canvas id="${id}-canvas" class="paper-art" width="1080" height="1920" data-layout-allow-overflow aria-hidden="true"></canvas>
 ${c.poster?`<div id="poster-${scene.id}" class="poster-frame clip" data-start="0" data-duration="${scene.duration}" data-layout-allow-overlap><img src="${c.poster}" alt="${esc(c.title.join(' '))} theatrical poster"></div>`:''}
 <div class="kicker">${scene.id==='intro'?'A PERSONAL TOP FIVE':scene.id==='outro'?'YOUR NEXT MOVIE NIGHT':'HOLLYWOOD THRILLERS / MY TOP FIVE'}</div>
 ${c.rank?`<div class="rank">0${c.rank}</div><div class="year">${c.year} / DRAMA</div>`:''}
 <div id="${id}-title" class="movie-title">${titleSVG(c.title,c.fg)}</div>
 ${scene.id==='intro'?'<div class="intro-number">5</div><div class="intro-ribbon">FIVE HOLLYWOOD THRILLERS YOU SHOULD KNOW</div>':''}
 ${list}
 <div id="${id}-tag" class="clip tag-clip" data-start="${tagAt.toFixed(4)}" data-duration="${(scene.duration-tagAt).toFixed(4)}"><div class="tagline">${c.tag}</div></div>
</div>
<script>${art}</script>
<script>
(function(){
 const state={t:0};
 const paint=DramaPaper.create(document.getElementById('${id}-canvas'),'${artKinds[scene.id]||scene.id}',${scene.duration});
 const tl=gsap.timeline({paused:true});
 tl.fromTo(state,{t:0},{t:${scene.duration},duration:${scene.duration},ease:'none',onUpdate:()=>paint(state.t)},0);
 ${scene.id==='intro'?'':`tl.fromTo('#${id}-title',{x:1100},{x:0,duration:.25,ease:'power3.out'},${titleAt.toFixed(4)});`}
 ${scene.id==='outro'?Array.from({length:5},(_,i)=>`tl.fromTo('#drama-outro-list-${i}',{opacity:0},{opacity:1,duration:.05},${.35+i*.10});`).join('\n'):''}
 tl.fromTo('#${id}-tag .tagline',{x:-1000},{x:0,duration:.22,ease:'power3.out'},${tagAt.toFixed(4)});
 paint(0);
 window.__timelines=window.__timelines||{};
 window.__timelines['${id}']=tl;
})();
</script></template></body></html>`;
 await fs.writeFile(path.join(root,'compositions',`${scene.id}.html`),markup);
 hosts.push(`<div id="${id}" class="clip" data-composition-id="${id}" data-composition-src="compositions/${scene.id}.html" data-start="${scene.start}" data-duration="${scene.duration}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>`);
 cueSheet.push({id:scene.id,cut:scene.start,title:scene.start+titleAt,speech:scene.voiceStart,end:scene.voiceStart+scene.speechDuration});
}
const capHtml=`<!doctype html><html><body><template><style>
@font-face{font-family:'League Spartan';src:url('assets/fonts/LeagueSpartan.ttf');font-weight:100 900}
#root{position:absolute;inset:0;overflow:hidden;font-family:'League Spartan'}
.caption-clip{position:absolute;inset:0}.caption-strip{position:absolute;left:108px;top:1210px;width:810px;min-height:116px;padding:17px 24px 18px 36px;font-size:44px;font-weight:600;line-height:1.15;color:#efe4c9}.light{color:#1b1714}.caption-stock{position:absolute;inset:0;width:100%;height:100%;z-index:0}.caption-words{position:relative;z-index:1}
.caption-strip:before{content:'';position:absolute;left:14px;top:28px;width:9px;height:12px;background:#d23a22}
</style><div id="root" data-composition-id="drama-captions" data-track-kind="captions" data-duration="${meta.duration}" data-width="1080" data-height="1920">
${allCaptions.map(p=>`<div id="${p.id}" class="clip caption-clip" data-start="${p.start.toFixed(4)}" data-duration="${p.duration.toFixed(4)}" data-track-index="4"><div class="caption-strip ${p.light?'light':''}"><svg class="caption-stock" viewBox="0 0 810 116" preserveAspectRatio="none" aria-hidden="true" data-layout-ignore><path fill="${p.light?'#efe4c9':'#1b1714'}" d="M8,2 L170,0 L295,2 L478,0 L654,2 L793,0 L810,12 L802,40 L806,72 L800,110 L611,112 L418,113 L203,114 L16,116 L0,98 L8,51 L0,10 Z"/></svg><span class="caption-words">${esc(p.text)}</span></div></div>`).join('\n')}
</div><script>(function(){const tl=gsap.timeline({paused:true});${allCaptions.map(p=>`tl.fromTo('#${p.id} .caption-strip',{x:-75},{x:0,duration:.18,ease:'power3.out'},${p.start.toFixed(4)});`).join('\n')}tl.to({t:0},{t:1,duration:${meta.duration},ease:'none'},0);window.__timelines=window.__timelines||{};window.__timelines['drama-captions']=tl;})();</script></template></body></html>`;
await fs.writeFile(path.join(root,'compositions/captions.html'),capHtml);
hosts.push(`<div id="drama-captions" class="clip" data-composition-id="drama-captions" data-composition-src="compositions/captions.html" data-track-kind="captions" data-start="0" data-duration="${meta.duration}" data-track-index="4" data-width="1080" data-height="1920"></div>`);
const index=`<!doctype html><html lang="en" data-composition-variables='[{"id":"voiceLevel","type":"number","label":"Voice level","default":1,"min":0,"max":1}]'><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"><title>Five Hollywood Dramas</title><script src="assets/vendor/gsap.min.js"></script><style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:#d23a22}.clip{position:absolute;inset:0;width:1080px;height:1920px}</style></head><body><main id="main" data-composition-id="main" data-width="1080" data-height="1920" data-fps="24" data-duration="${meta.duration}">${hosts.join('\n')}<audio id="drama-voice" class="clip" src="assets/audio/voice-master.wav" data-start="0" data-duration="${meta.duration}" data-volume="1" data-track-index="5" data-audio-group="voiceover"></audio><audio id="drama-music" class="clip" src="assets/audio/music-ducked.wav" data-start="0" data-duration="${meta.duration}" data-volume="1" data-track-index="6" data-audio-group="music"></audio><audio id="drama-sfx" class="clip" src="assets/audio/sfx-ducked.wav" data-start="0" data-duration="${meta.duration}" data-volume="1" data-track-index="7" data-audio-group="sfx"></audio></main><script>const tl=gsap.timeline({paused:true});tl.to({t:0},{t:1,duration:${meta.duration},ease:'none'});window.__timelines=window.__timelines||{};window.__timelines['main']=tl;</script></body></html>`;
await fs.writeFile(path.join(root,'index.html'),index.replaceAll('voice-master.wav','voice-master-delivery.wav').replaceAll('music-ducked.wav','music-ducked-delivery.wav').replaceAll('sfx-ducked.wav','sfx-ducked-delivery.wav'));
await fs.writeFile(path.join(root,'cues.json'),JSON.stringify(cueSheet,null,2));
await fs.writeFile(path.join(root,'SCRIPT.md'),meta.scenes.map(s=>`## ${s.id} (${s.start.toFixed(2)} s)\n\n${s.text}\n`).join('\n'));
const timecode=t=>{const ms=Math.round(t*1000);return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')},${String(ms%1000).padStart(3,'0')}`;};
await fs.writeFile(path.join(root,'captions.srt'),allCaptions.map((c,i)=>`${i+1}\n${timecode(c.start)} --> ${timecode(c.start+c.duration)}\n${c.text}\n`).join('\n'));
console.log(`Built ${meta.scenes.length} scenes, ${meta.duration.toFixed(3)} seconds.`);
