(function(){
const W=ms=>new Promise(r=>setTimeout(r,ms));
const fire=el=>{for(const t of ['pointerdown','mousedown','pointerup','mouseup','click']) el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window}));};
return {
 title: function(p){ const t=document.querySelector('input[placeholder="Add a catchy title"]'); const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; t.focus(); set.call(t,p.h); t.dispatchEvent(new Event('input',{bubbles:true})); t.dispatchEvent(new Event('change',{bubbles:true})); const d=document.querySelector('[contenteditable=true]'); d.focus(); const r=document.createRange(); r.selectNodeContents(d); r.collapse(false); const s=getSelection(); s.removeAllRanges(); s.addRange(r); return t.value.length; },
 desc: function(){ const d=document.querySelector('[contenteditable=true]'); d.focus(); const r=document.createRange(); r.selectNodeContents(d); const s=getSelection(); s.removeAllRanges(); s.addRange(r); return d.innerText; },
 sched: async function(i,p){ const [hh,mm]=p.t.split(':');
  document.querySelector('input[type=radio][value=schedule]').click(); await W(1200);
  const tins=[...document.querySelectorAll('input')].filter(x=>x.type=='text'); const timeIn=tins.find(x=>/^\d\d:\d\d$/.test(x.value)), dateIn=tins.find(x=>/^\d{4}-\d\d-\d\d$/.test(x.value));
  fire(timeIn); await W(700);
  const L=[...document.querySelectorAll('.tiktok-timepicker-option-text.tiktok-timepicker-left')], R=[...document.querySelectorAll('.tiktok-timepicker-option-text.tiktok-timepicker-right')];
  const h=L.find(e=>e.textContent.trim()===hh), m=R.find(e=>e.textContent.trim()===mm); if(h) fire(h); await W(300); if(m) fire(m); await W(500);
  fire(dateIn); await W(700);
  const hdrTxt=()=>{const w=document.querySelector('.month-header-wrapper'); return w? w.querySelector('.month-title').textContent.trim()+' / '+w.querySelector('.year-title').textContent.trim() : '';};
  for(let k=0;k<3 && hdrTxt()!==p.hdr;k++){ const ar=document.querySelectorAll('.month-header-wrapper .arrow'); fire(ar[ar.length-1]); await W(500);}
  const hdr=hdrTxt();
  const day=[...document.querySelectorAll('.day.valid')].find(e=>e.textContent.trim()===String(p.day)); if(day) fire(day); await W(600);
  const desc=document.querySelector('[contenteditable=true]').innerText; const tEl=document.querySelector('input[placeholder="Add a catchy title"]'); const title=tEl?tEl.value:'(video post, no title field)';
  const imgs=(document.body.innerText.match(/\d+\/\d+/)||[''])[0];
  const ok = timeIn.value===p.t && dateIn.value===p.d && title.length>5 && desc.includes('SnapAndLearn');
  if(ok){ const b=[...document.querySelectorAll('button')].filter(e=>e.innerText.trim()==='Schedule'); b[b.length-1].click(); await W(7000);}
  return JSON.stringify({i, ok, time:timeIn.value, date:dateIn.value, hdr, imgs, cap30: document.body.innerText.includes('only schedule up to 30'), done: location.pathname.includes('/content')});
 }
};})()
