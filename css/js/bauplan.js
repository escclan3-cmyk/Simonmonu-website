/* Bauplan-Ansicht: misst die Seite live im Browser. Nichts wird gesendet. */
(function(){
'use strict';
var d=document,body=d.body,EN=d.documentElement.lang==='en',cols=null,h=null,v=null,koord=null,et=null,aktiv=false,frame=0,px=0,py=0,fokus=null;
function el(t,c){var e=d.createElement(t);e.className=c;return e}
function lum(rgb){var a=rgb.map(function(c){c/=255;return c<=.04045?c/12.92:Math.pow((c+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]}
function rgb(s){var m=/rgba?\(([^)]+)\)/.exec(s);if(!m)return null;var p=m[1].split(/[ ,\/]+/).map(parseFloat);return {c:p.slice(0,3),a:p.length>3?p[3]:1}}
function grund(e){while(e&&e!==d.documentElement){var r=rgb(getComputedStyle(e).backgroundColor);if(r&&r.a>0.95)return r.c;e=e.parentElement}return rgb(getComputedStyle(body).backgroundColor).c}
function kontrast(e){var f=rgb(getComputedStyle(e).color),g=grund(e);if(!f)return '';var a=lum(f.c),b=lum(g),k=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);return k.toFixed(1).replace('.',EN?'.':',')+' : 1'}
function spalten(){var w=innerWidth;return w>=1024?12:w>=768?6:4}
function baueRaster(){
  cols=el('div','bp-raster');cols.setAttribute('aria-hidden','true');var i=el('div','');
  for(var k=0;k<spalten();k++)i.appendChild(d.createElement('i'));cols.appendChild(i);body.appendChild(cols);
}
function beschreibe(e){
  if(!e||e===body||e===d.documentElement)return '';
  var r=e.getBoundingClientRect(),cs=getComputedStyle(e),z=[];
  var name=e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/)[0]:'');
  z.push(name+'  '+Math.round(r.width)+' × '+Math.round(r.height));
  if(/^(H1|H2|H3|H4|P|LI|A|BUTTON|SUMMARY|LABEL|TD|TH|DT|DD|SPAN)$/.test(e.tagName)&&e.textContent.trim()){
    var fs=parseFloat(cs.fontSize),ls=cs.letterSpacing==='normal'?0:parseFloat(cs.letterSpacing);
    z.push(cs.fontFamily.split(',')[0].replace(/"/g,'')+' '+cs.fontWeight+', '+fs.toFixed(1).replace('.',EN?'.':',')+' px, '+(EN?'tracking ':'Spur ')+(ls/fs).toFixed(3).replace('.',EN?'.':',')+' em');
    z.push((EN?'Contrast ':'Kontrast ')+kontrast(e));
  }
  var img=e.tagName==='IMG'?e:(e.querySelector&&e.tagName==='PICTURE'?e.querySelector('img'):null);
  if(img){
    var s=img.currentSrc||img.src,fmt=(s.split('.').pop()||'').toUpperCase().replace(/\?.*/,'');
    var pe=performance.getEntriesByName(s)[0],kb=pe&&pe.transferSize?Math.round(pe.transferSize/100)/10+' KB':(pe?(EN?'from cache':'aus dem Cache'):'');
    z.push(s.replace(location.origin+'/','')+', '+fmt+(kb?', '+(EN?kb:kb.replace('.',',')):''));
  }
  if(e.matches('a,button,summary,input,select,textarea')){
    z.push((EN?'Target size ':'Zielgröße ')+Math.round(r.width)+' × '+Math.round(r.height)+(r.width>=24&&r.height>=24?'  ≥ 24 × 24 ok':(EN?'  under 24 × 24':'  unter 24 × 24')));
  }
  var mt=parseFloat(cs.marginTop),pt=parseFloat(cs.paddingTop);
  if(mt||pt)z.push((EN?'Space above ':'Abstand oben ')+(mt?(EN?'outer ':'außen ')+Math.round(mt):'')+(mt&&pt?', ':'')+(pt?(EN?'inner ':'innen ')+Math.round(pt):'')+' px');
  return z.join('\n');
}
function zeichne(){
  frame=0;if(!aktiv)return;
  h.style.top=py+'px';v.style.left=px+'px';
  koord.textContent=Math.round(px+scrollX)+', '+Math.round(py+scrollY);koord.style.left=(px+8)+'px';koord.style.top=(py+8)+'px';
  var e=d.elementFromPoint(px,py);if(e&&(e===et||e===koord||e===h||e===v))e=null;
  if(fokus&&fokus!==e)fokus.classList.remove('bp-fokus');fokus=e&&e!==body&&e!==d.documentElement?e:null;if(fokus)fokus.classList.add('bp-fokus');
  var t=beschreibe(e);
  if(!t){et.style.display='none';return}
  et.style.display='block';et.textContent=t;et.style.whiteSpace='pre-line';
  var x=Math.min(px+16,innerWidth-et.offsetWidth-8),y=py+36;if(y+et.offsetHeight>innerHeight)y=py-et.offsetHeight-16;
  et.style.left=Math.max(8,x)+'px';et.style.top=Math.max(8,y)+'px';
}
function bewegt(e){px=e.clientX;py=e.clientY;if(!frame)frame=requestAnimationFrame(zeichne)}
function neu(){if(cols){cols.remove();baueRaster()}}
window.SM_BAUPLAN={
  an:function(){
    if(aktiv)return;aktiv=true;baueRaster();
    h=el('div','bp-kreuz-h');v=el('div','bp-kreuz-v');koord=el('div','bp-koord');et=el('div','bp-etikett');et.style.display='none';
    [h,v,koord,et].forEach(function(x){x.setAttribute('aria-hidden','true');body.appendChild(x)});
    addEventListener('pointermove',bewegt,{passive:true});addEventListener('resize',neu);
  },
  aus:function(){
    aktiv=false;if(fokus){fokus.classList.remove('bp-fokus');fokus=null}[cols,h,v,koord,et].forEach(function(x){if(x)x.remove()});cols=h=v=koord=et=null;
    removeEventListener('pointermove',bewegt);removeEventListener('resize',neu);
  }
};
})();
