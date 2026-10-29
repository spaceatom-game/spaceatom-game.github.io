/* Progressive enhancement for approved, first-party game assets; no external requests. */
(() => {
 "use strict";
 const allowed=/^\.\/assets\/official\/[a-z0-9][a-z0-9._/-]*\.(?:png|jpe?g|webp|svg)$/i;
 const isLocal=(p)=>typeof p==="string"&&allowed.test(p)&&!p.split("/").includes("..");
 const exists=(p)=>new Promise((resolve)=>{
   if(!isLocal(p))return resolve(false);
   const image=new Image();
   image.onload=()=>resolve(true);
   image.onerror=()=>resolve(false);
   image.src=p;
 });
 async function swap(key,path){
   if(!(await exists(path)))return;
   document.querySelectorAll('[data-official-art="'+key+'"]').forEach((img)=>{
     img.src=path;
     if(key==="logo"){img.hidden=false;img.parentElement.classList.add("official-ready");}
     else img.alt="Official SpaceAtom "+(key==="hero"?"key":key+" outpost")+" artwork";
   });
   const label=document.querySelector('[data-art-caption="'+key+'"]');
   if(label)label.textContent=key==="hero"?"OFFICIAL SPACEATOM GAME ART":"OFFICIAL GAME ART / "+key.toUpperCase();
 }
 async function gallery(items,id,sectionId,kind){
   if(!Array.isArray(items))return;
   const selected=items.slice(0,kind==="character"?12:8).filter((x)=>x&&isLocal(x.image));
   const validated=(await Promise.all(selected.map(async(x)=>(await exists(x.image))?x:null))).filter(Boolean);
   if(!validated.length)return;
   const root=document.getElementById(id);
   validated.forEach((item,index)=>{
     const card=document.createElement(kind==="character"?"article":"figure");
     card.className=kind==="character"?"character-card":"screenshot-card";
     const wrap=document.createElement("div");wrap.className="character-art-wrap";
     const img=document.createElement("img");
     img.src=item.image;img.loading="lazy";
     img.alt=typeof item.alt==="string"&&item.alt.trim()?item.alt:
       kind==="character"?"SpaceAtom character: "+(item.name||"unknown"):"SpaceAtom game screenshot "+(index+1);
     if(kind==="character"){img.className="character-art";wrap.appendChild(img);}
     const caption=document.createElement(kind==="character"?"div":"figcaption");
     caption.className=kind==="character"?"character-label":"";
     const title=document.createElement(kind==="character"?"h3":"span");
     title.textContent=kind==="character"?(item.name||"Character "+(index+1)):(item.caption||"GAME CAPTURE // "+String(index+1).padStart(2,"0"));
     caption.appendChild(title);
     if(kind==="character"){const role=document.createElement("span");role.textContent=item.role||"FILE // "+String(index+1).padStart(2,"0");caption.appendChild(role);}
     if(kind==="character")card.append(wrap,caption);else card.append(img,caption);
     root.appendChild(card);
   });
   document.getElementById(sectionId).hidden=false;
   if(kind==="character")document.querySelectorAll("[data-characters-link]").forEach((a)=>{a.hidden=false;});
 }
 async function start(){
   try{
     const response=await fetch("./assets/official/media.json",{cache:"no-store"});
     if(!response.ok)return;
     const m=await response.json();
     if(!m||m.version!==1)return;
     await Promise.all(["logo","hero","ally","enemy"].map((type)=>swap(type,m[type])));
     await Promise.all([gallery(m.characters,"character-gallery","characters","character"),
                        gallery(m.screenshots,"screenshots-gallery","screenshots","screenshot")]);
   }catch(_error){/* Preserve existing concept artwork if optional files are unavailable. */}
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);
 else start();
})();