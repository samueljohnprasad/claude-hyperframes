import fs from 'node:fs/promises';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
const put = async (file,url) => {
  const dest=path.join(root,file); await fs.mkdir(path.dirname(dest),{recursive:true});
  try {if((await fs.stat(dest)).size>100)return;}catch{}
  const response=await fetch(url); if(!response.ok) throw Error(`${response.status}: ${url}`);
  await fs.writeFile(dest,Buffer.from(await response.arrayBuffer())); console.log(file);
};
const gf='https://raw.githubusercontent.com/google/fonts/86aced91de05cd4f96a06838124cca45be337b2b/ofl';
await put('assets/fonts/LeagueGothic.ttf',`${gf}/leaguegothic/LeagueGothic%5Bwdth%5D.ttf`);
await put('assets/fonts/LeagueSpartan.ttf',`${gf}/leaguespartan/LeagueSpartan%5Bwght%5D.ttf`);
await put('assets/audio/spy-glass.mp3','https://incompetech.com/music/royalty-free/mp3-royaltyfree/Spy%20Glass.mp3');
const copies=[
 ['assets/vendor/gsap.min.js','C:/Users/NISHNATH/AppData/Roaming/npm/node_modules/hyperframes/dist/vendor/npm/gsap@3.15.0/dist/gsap.min.js'],
 ['assets/vendor/opentype.cjs','C:/Users/NISHNATH/lemo-opuscar/styles/spy-titles/demo/vendor/opentype.min.js'],
 ['assets/audio/paper-wipe.mp3',path.resolve(root,'../audio/openverse/openverse_wipe.mp3')],
 ['assets/fonts/LeagueGothic-OFL.txt','C:/Users/NISHNATH/lemo-opuscar/styles/spy-titles/demo/fonts/LeagueGothic-OFL.txt'],
 ['assets/fonts/LeagueSpartan-OFL.txt','C:/Users/NISHNATH/lemo-opuscar/styles/spy-titles/demo/fonts/LeagueSpartan-OFL.txt']
];
for(const [file,source] of copies){const dest=path.join(root,file);await fs.mkdir(path.dirname(dest),{recursive:true});await fs.copyFile(source,dest);}
console.log('Media and vendor files ready.');
