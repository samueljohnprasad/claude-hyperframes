/* Original deterministic cut-paper sets, inspired by the supplied style grammar. */
window.DramaPaper = (() => {
  const C={ink:'#1b1714',paper:'#efe4c9',red:'#d23a22',gold:'#e2a52a'};
  const hash=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v)};
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const ease=x=>1-(1-clamp(x))**3;
  const paths=new Map();
  function cut(points,seed=1){
    const key=JSON.stringify(points)+seed;if(paths.has(key))return paths.get(key);
    const p=new Path2D();let travel=0;
    points.forEach((a,i)=>{const b=points[(i+1)%points.length],dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy)||1,n=Math.max(1,Math.ceil(len/9));
      for(let j=0;j<n;j++){const u=j/n,s=travel+len*u;const d=(Math.sin(s*.053+seed*4)*1.15+Math.sin(s*.17+seed)*.55)*(j?1:.2);const x=a[0]+dx*u-dy/len*d,y=a[1]+dy*u+dx/len*d;if(i===0&&j===0)p.moveTo(x,y);else p.lineTo(x,y);}travel+=len;});
    p.closePath();paths.set(key,p);return p;
  }
  const rect=(x,y,w,h)=>[[x,y],[x+w,y],[x+w,y+h],[x,y+h]];
  const ellipse=(x,y,rx,ry)=>Array.from({length:48},(_,i)=>{const a=i/48*Math.PI*2;return[x+Math.cos(a)*rx,y+Math.sin(a)*ry]});
  function shape(g,points,col,seed=1,shadow=true){g.save();if(shadow){g.shadowColor='rgba(20,12,6,.28)';g.shadowBlur=5;g.shadowOffsetX=3;g.shadowOffsetY=4;}g.fillStyle=col;g.fill(cut(points,seed));g.restore();}
  function disk(g,x,y,r,col,seed){shape(g,ellipse(x,y,r,r),col,seed)}
  function bar(g,x,y,w,h,col,rotation=0,seed=1){g.save();g.translate(x,y);g.rotate(rotation);shape(g,rect(0,0,w,h),col,seed);g.restore()}
  function line(g,points,col,width=4){g.save();g.strokeStyle=col;g.lineWidth=width;g.lineJoin='round';g.lineCap='round';g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.stroke();g.restore()}
  let texture;
  function finish(g){
    if(!texture){texture=document.createElement('canvas');texture.width=540;texture.height=960;const t=texture.getContext('2d'),im=t.createImageData(540,960);for(let y=0;y<960;y++)for(let x=0;x<540;x++){const n=hash(y*540+x);const i=(y*540+x)*4,v=246+Math.round(n*9);im.data[i]=v;im.data[i+1]=v;im.data[i+2]=v-2;im.data[i+3]=255;}t.putImageData(im,0,0);t.strokeStyle='rgba(60,40,20,.12)';t.lineWidth=.5;for(let i=0;i<2200;i++){const x=hash(i+3)*540,y=hash(i+789)*960;t.beginPath();t.moveTo(x,y);t.lineTo(x+hash(i+99)*8,y+hash(i+456)*3);t.stroke();}}
    g.save();g.globalCompositeOperation='multiply';g.drawImage(texture,0,0,1080,1920);g.restore();
  }
  function figure(g,x,y,scale=1,{color=C.ink,bg=C.paper,pose='stand',accent=true,flip=false}={}){
    g.save();g.translate(x,y);g.scale(flip?-scale:scale,scale);
    const p=new Path2D();const add=(pts,s=1)=>p.addPath(cut(pts,s));
    add([[-23,-332],[-29,-317],[-28,-292],[-18,-281],[6,-280],[20,-294],[31,-299],[18,-308],[17,-328],[1,-341]],2);
    add([[-21,-284],[-48,-263],[-42,-160],[-29,-145],[32,-147],[39,-221],[28,-268],[2,-284]],3);
    if(pose==='sit'){
      add([[-37,-168],[29,-165],[92,-119],[89,-90],[10,-119],[-34,-125]],4);
      add([[73,-115],[98,-111],[81,-28],[111,-20],[108,-7],[49,-9],[52,-28]],5);
      add([[-17,-137],[3,-113],[-2,-38],[28,-24],[26,-11],[-29,-12],[-29,-38]],6);
    }else{
      add([[-35,-158],[-1,-151],[-7,-72],[-9,-22],[16,-11],[14,0],[-39,0],[-36,-23],[-40,-82]],4);
      add([[-2,-155],[30,-150],[41,-76],[55,-21],[80,-8],[78,3],[29,3],[17,-21],[3,-77]],5);
    }
    if(pose==='hope'){
      add([[-36,-260],[-64,-243],[-108,-305],[-123,-354],[-135,-352],[-131,-302],[-83,-210],[-42,-211]],7);
      add([[22,-265],[52,-258],[100,-315],[113,-362],[126,-359],[126,-309],[70,-214],[34,-214]],8);
    }else if(pose==='vote'){
      add([[19,-262],[48,-249],[65,-299],[69,-346],[82,-350],[91,-310],[69,-215],[35,-213]],8);
      add([[-35,-259],[-60,-247],[-70,-164],[-55,-136],[-44,-139],[-48,-167],[-31,-217]],7);
    }else{
      add([[-35,-261],[-59,-246],[-67,-173],[-58,-149],[-44,-150],[-45,-177],[-30,-221]],7);
      add([[24,-266],[48,-252],[72,-198],[pose==='sit'?107:58,-171],[pose==='sit'?100:44,-157],[47,-182],[20,-216]],8);
    }
    g.strokeStyle=bg;g.lineWidth=6;g.lineJoin='round';g.stroke(p);g.save();g.shadowColor='rgba(0,0,0,.3)';g.shadowBlur=5;g.shadowOffsetY=4;g.fillStyle=color;g.fill(p);g.restore();
    if(accent){shape(g,[[-6,-277],[6,-276],[14,-245],[8,-227],[-2,-246]],C.red,13,false)}
    g.restore();
  }
  function ticket(g,x,y,scale=1,rotation=0,col=C.gold){
    g.save();g.translate(x,y);g.rotate(rotation);g.scale(scale,scale);shape(g,[[0,0],[90,0],[90,17],[80,24],[90,32],[90,80],[0,80],[0,55],[10,47],[0,39]],C.ink,60);shape(g,[[6,5],[84,5],[84,19],[75,25],[84,34],[84,74],[6,74],[6,57],[16,47],[6,36]],col,61);for(let i=0;i<4;i++)bar(g,25,15+i*13,42,4,C.ink,0,80+i);g.restore();
  }
  function feather(g,x,y,r){g.save();g.translate(x,y);g.rotate(r);shape(g,[[-5,68],[-35,12],[-29,-38],[9,-80],[20,-23],[13,26]],C.paper,91);line(g,[[0,75],[2,-55]],C.ink,2);for(let k=0;k<5;k++)line(g,[[0,34-k*17],[-22,13-k*17]],C.ink,1.4);g.restore()}
  function print(g,text,x,y,size,col,rotation=0){g.save();g.translate(x,y);g.rotate(rotation);g.font=`${size}px 'League Gothic'`;g.fillStyle=col;g.fillText(text,0,0);g.restore()}
  function create(canvas,kind,duration){
    const g=canvas.getContext('2d');
    const grounds={intro:C.red,forrest:C.gold,jury:C.paper,schindler:C.ink,shawshank:C.red,godfather:C.paper,outro:C.gold};
    const bg=grounds[kind]||C.paper;
    return function paint(t){
      g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.fillStyle=bg;g.fillRect(0,0,1080,1920);
      // One quiet diagonal continues below Instagram's interface area.
      const dark=bg===C.ink?'#302923':bg===C.red?'#b8321e':bg===C.gold?'#cc9223':'#d9ccae';
      shape(g,[[0,1460],[1080,1160],[1080,1600],[0,1920]],dark,22,false);
      for(let k=0;k<5;k++)bar(g,-60+k*240,1570-k*55,155,320,bg,.28,150+k);
      const a=ease((t-1.9)/1.0),b=ease((t-4)/1.2),tw=Math.floor(t*12)/12;
      if(kind==='intro'){
        disk(g,545,814,290,C.ink,10);
        print(g,'5',366,1050,640,C.paper,-.07);
        for(let k=0;k<5;k++){const step=ease((t-.25-k*.14)/.35);ticket(g,160+k*153,1040+Math.abs(k-2)*16-step*55,.9,(k-2)*.09);}
        shape(g,[[50,535],[210,475],[248,500],[90,565]],C.gold,11);
      }else if(kind==='forrest'){
        disk(g,560,787,285,C.paper,14);
        print(g,'LIFE',184,1040,390,'#cc9223',-.07);
        g.save();g.translate(-24*a,0);
        for(let k=0;k<3;k++)bar(g,238,752+k*35,520,22,C.ink,-.025,20+k);
        bar(g,232,873,565,32,C.ink,-.025,25);bar(g,281,897,22,127,C.ink,0,26);bar(g,699,887,22,137,C.ink,0,27);
        figure(g,483,938,1.12,{pose:'sit',bg:C.paper});ticket(g,710,934,.66,.09);g.restore();
        feather(g,758-120*clamp(t/duration),576+152*clamp(t/duration),-.45+tw*.1);
      }else if(kind==='jury'){
        print(g,'DOUBT',144,989,330,'#d9ccae',-.09);
        for(let k=0;k<6;k++)figure(g,238+k*112,780,.55,{pose:k===0&&a>.5?'vote':'sit',accent:k===0,bg,color:k===0?C.red:C.ink});
        shape(g,[[175,818],[811,766],[926,904],[292,985]],C.gold,37);
        bar(g,310,977,25,100,C.ink,-.06,38);bar(g,812,919,25,140,C.ink,.03,39);
        for(let k=0;k<6;k++)figure(g,268+k*108,1100,.59,{pose:'sit',accent:false,bg,flip:true});
        if(a>0){g.save();g.globalAlpha=a;disk(g,197,626,57,C.red,40);print(g,'1',181,661,100,C.paper);g.restore();}
      }else if(kind==='schindler'){
        g.save();g.translate(20*a,-10*a);g.rotate(-.025);
        shape(g,[[239,574],[790,586],[821,1052],[225,1038]],C.paper,51);
        bar(g,276,626,465,15,C.ink,0,52);
        for(let k=0;k<11;k++){const width=270+hash(k+8)*150;bar(g,278,682+k*28,width,4,C.ink,0,70+k);}
        // Red coat is an abstract story motif, never a copied still.
        disk(g,711,867,22,C.ink,84);shape(g,[[694,890],[728,890],[754,976],[673,976]],C.red,85);bar(g,694,976,11,51,C.ink,0,86);bar(g,721,976,11,51,C.ink,0,87);
        g.restore();ticket(g,196+95*b,998,.85,-.10);
      }else if(kind==='shawshank'){
        disk(g,546,798,278,C.paper,90);
        for(let k=0;k<6;k++){const move=(k<3?-1:1)*105*a;bar(g,238+k*116+move,590,33,500,C.ink,-.035,100+k)}
        bar(g,205,596,693,34,C.ink,-.035,99);
        print(g,'HOPE',233,1053,330,C.gold,-.03);
        figure(g,533,1003,1.06,{pose:a>.5?'hope':'stand',bg:C.paper,accent:false});
        ticket(g,793,1023,.65,.15);
      }else if(kind==='godfather'){
        g.save();g.translate(0,25);
        disk(g,548,791,288,C.gold,111);
        print(g,'FAMILY',179,1058,290,'#d9ccae',-.04);
        for(let k=0;k<3;k++)figure(g,360+k*179,1064,k===1?1.18:.91,{bg:C.gold,accent:k===1});
        bar(g,338,562,441,25,C.ink,-.035,113);bar(g,488,514,186,22,C.ink,.12,114);
        const drop=18*a;
        for(let k=0;k<4;k++){const x=379+k*104;line(g,[[x,575],[x+(k<2?38:-20),703+drop]],C.red,5)}
        ticket(g,765,701,.65,-.12);g.restore();
      }else if(kind==='outro'){
        for(let k=0;k<5;k++){const land=ease((t-k*.10)/.35);bar(g,155+(1-land)*(k%2?1050:-1050),555+k*112,748,96,k%2?C.ink:C.paper,-.025+k*.008,130+k);}
        ticket(g,813,1128,1.1,-.2);
      }
      finish(g);
    }
  }
  return {create};
})();
