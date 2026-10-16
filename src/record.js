const p=require('puppeteer-core');const {execSync}=require('child_process');const fs=require('fs');
const D='/workspace/leadgen/overnight/ready/website_preview_v4/video';fs.mkdirSync(D,{recursive:true});
(async()=>{const b=await p.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
async function rec(name,w,h,m,script){const pg=await b.newPage();await pg.setViewport({width:w,height:h,deviceScaleFactor:1,isMobile:m,hasTouch:m});
await pg.goto('http://127.0.0.1:4176/',{waitUntil:'networkidle0'});await pg.evaluate(()=>document.fonts.ready);await new Promise(r=>setTimeout(r,800));
const client=await pg.createCDPSession();await client.send('Page.startScreencast',{format:'jpeg',quality:70,maxWidth:w,maxHeight:h,everyNthFrame:1});
const frames=[];client.on('Page.screencastFrame',async f=>{frames.push({d:f.data,t:Date.now()});await client.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{})});
await script(pg);await client.send('Page.stopScreencast');await pg.close();
const dir=`/tmp/vid_${name}`;fs.mkdirSync(dir,{recursive:true});frames.forEach((f,i)=>fs.writeFileSync(`${dir}/f${String(i).padStart(5,'0')}.jpg`,Buffer.from(f.d,'base64')));
const dur=(frames.at(-1).t-frames[0].t)/1000;const fps=Math.max(8,Math.min(24,frames.length/Math.max(dur,.1)));
execSync(`ffmpeg -y -framerate ${fps} -i ${dir}/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -movflags +faststart ${D}/${name}.mp4`,{stdio:'inherit'});console.log(name,frames.length,'frames',dur.toFixed(1)+'s')}
await rec('desktop_1440',1440,900,false,async pg=>{await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=28){scrollTo(0,y);await new Promise(r=>setTimeout(r,16))}});await new Promise(r=>setTimeout(r,600));await pg.hover('.lc');await new Promise(r=>setTimeout(r,400));await pg.goto('http://127.0.0.1:4176/quote/',{waitUntil:'domcontentloaded'});await new Promise(r=>setTimeout(r,1200))});
await rec('mobile_390',390,844,true,async pg=>{await new Promise(r=>setTimeout(r,900));await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=22){scrollTo(0,y);await new Promise(r=>setTimeout(r,18))}});await new Promise(r=>setTimeout(r,500));await pg.click('.menu-btn');await new Promise(r=>setTimeout(r,900));await pg.click('.menu-btn');await new Promise(r=>setTimeout(r,300));await pg.goto('http://127.0.0.1:4176/quote/?type=restaurant',{waitUntil:'domcontentloaded'});await new Promise(r=>setTimeout(r,1000))});
await b.close();
execSync(`ffmpeg -y -i ${D}/desktop_1440.mp4 -i ${D}/mobile_390.mp4 -filter_complex "[0:v]setpts=PTS/1.15,scale=1440:900:force_original_aspect_ratio=decrease,pad=1440:900:(ow-iw)/2:(oh-ih)/2,setsar=1[d];[1:v]setpts=PTS/1.15,scale=390:844:force_original_aspect_ratio=decrease,pad=390:844:(ow-iw)/2:(oh-ih)/2,setsar=1,pad=1440:900:(1440-390)/2:(900-844)/2[m];[d][m]concat=n=2:v=1:a=0,fps=24[v]" -map "[v]" -c:v libx264 -pix_fmt yuv420p -movflags +faststart -t 58 ${D}/simpleinsure_v4.mp4`,{stdio:'inherit'});
console.log('combined',fs.statSync(`${D}/simpleinsure_v4.mp4`).size)})();
