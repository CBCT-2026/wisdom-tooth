// Render the labelled model pictures for the 2D information sheet (images/sheet-whole-<lang>.jpg, sheet-closeup-<lang>.jpg)
// from the AR web page, so the sheet labels match the web labels (including Japanese furigana).
// Serve the repo first: python3 -m http.server 8765
// Usage: DPR=2.55 [FOV=18deg] node tools/sheet_images.js <lang> "<orbit>" "<target>|-" <width> <height> <out.png>
//   whole:    DPR=2.55 FOV=18deg node tools/sheet_images.js ja "90deg 80deg auto" - 600 424 whole.png
//   close-up: DPR=2.55 node tools/sheet_images.js ja "100deg 80deg 0.13m" "-0.036m -0.016m -0.058m" 541 425 closeup.png
const {chromium}=require('playwright');
(async()=>{const [lang,orbit,target,w,h,out]=process.argv.slice(2);
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+(process.env.DPR||2)});
await p.goto(`http://localhost:8765/${lang}/index.html`);
await p.waitForFunction(()=>document.querySelector('#mv').loaded,{timeout:60000});
await p.evaluate(([o,t,fov])=>{const mv=document.querySelector('#mv');
 document.body.innerHTML='';document.body.appendChild(mv);document.body.style.margin=0;document.body.style.background='#fff';
 mv.style.cssText='width:100vw;height:100vh;max-height:none;background:#fff;border:0;border-radius:0;box-shadow:none;--poster-color:#fff';
 mv.removeAttribute('camera-controls');if(t)mv.classList.add('zoomed');mv.interactionPrompt='none';
 mv.minCameraOrbit='auto auto 0.01m';mv.cameraOrbit=o;if(t)mv.cameraTarget=t;if(fov)mv.fieldOfView=fov;mv.jumpCameraToGoal();
 document.querySelectorAll('.ar-btn,.progress').forEach(e=>e.remove());},[orbit,target==='-'?null:target,process.env.FOV]);
await p.waitForTimeout(2500);
await p.screenshot({path:out,clip:{x:0,y:6,width:+w,height:+h-6}});await b.close();})();
