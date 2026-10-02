/* simonmonu.at · Seitenskript, Fassung 15. Nichts hiervon ist nötig, damit die Seite funktioniert. */
(function(){
'use strict';
var d=document,root=d.documentElement,body=d.body;
window.SM_LAEUFT=true;
var EN=root.lang==='en';
/* Wurzel der Website, abgeleitet vom Ort dieses Skripts: funktioniert auf dem Server und per Doppelklick im Ordner */
var BASIS=(function(){var s=d.currentScript&&d.currentScript.src;return s?s.replace(/js\/seite\.js.*$/,''):'/'})();
var DATEI=location.protocol==='file:';
function ort(p){var u=BASIS+p;return DATEI?u.replace(/\/(\?|#|$)/,'/index.html$1'):u}
var red=matchMedia('(prefers-reduced-motion: reduce)').matches;
var fein=matchMedia('(pointer: fine)').matches;
function tick(n){try{if(!red&&navigator.vibrate&&matchMedia('(pointer: coarse)').matches)navigator.vibrate(n||8)}catch(e){}}
function $(s,c){return (c||d).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
function ss(k,v){try{v==null?sessionStorage.removeItem(k):sessionStorage.setItem(k,v)}catch(e){}}
function zahl(n,st){var s=n.toFixed(st).split('.');s[0]=s[0].replace(/\B(?=(\d{3})+(?!\d))/g,EN?',':'.');return s.join(EN?'.':',')}
var BUEHNE='.sek-werke,.sek-kontakt,.sek-schaufenster,.sek-case-bild,.sek-demo,.sek-anfrage,.fuss';

/* Start: wartet auf das Ende der Startansicht (falls sie läuft) und auf die Schriften, damit die Zeilen stimmen */
var START=(function(){var fs=[],ok=false;return{warte:function(f){ok?f():fs.push(f)},los:function(){if(ok)return;ok=true;
  var w=d.fonts&&d.fonts.ready?Promise.race([d.fonts.ready,new Promise(function(r){setTimeout(r,500)})]):Promise.resolve();w.then(function(){fs.forEach(function(f){f()})})}}})();

/* Per Doppelklick geöffnet (file://): Links auf Ordner zeigen sonst eine Dateiliste statt der Seite */
if(DATEI)$$('a[href]').forEach(function(a){var h=a.getAttribute('href');if(/^(https?:|mailto:|tel:|#)/.test(h))return;a.setAttribute('href',h.replace(/(^|\/)(\?|#|$)/,function(m,s,r){return (s||'')+'index.html'+r}).replace(/^\.\/index\.html/,'index.html'))});

/* Theme: System, Hell, Dunkel */
(function(){
  var b=$('[data-thema]');if(!b)return;
  var txt=$('[data-thema-text]',b),folge={system:'hell',hell:'dunkel',dunkel:'system'},namen=EN?{system:'System',hell:'Light',dunkel:'Dark'}:{system:'System',hell:'Hell',dunkel:'Dunkel'};
  function jetzt(){var a=root.getAttribute('data-theme');return a==='light'?'hell':a==='dark'?'dunkel':'system'}
  function zeige(){txt.textContent=(EN?'Appearance: ':'Darstellung: ')+namen[jetzt()]}
  b.addEventListener('click',function(){
    root.classList.add('umschalten');setTimeout(function(){root.classList.remove('umschalten')},60);
    var n=folge[jetzt()];
    if(n==='system'){root.removeAttribute('data-theme');try{localStorage.removeItem('sm-theme')}catch(e){}}
    else{root.setAttribute('data-theme',n==='hell'?'light':'dark');try{localStorage.setItem('sm-theme',n)}catch(e){}}
    zeige();
  });
  zeige();
})();

/* Messung der eigenen Seite (nur auf diesem Gerät, nichts wird gesendet) */
function messung(){
  var r=performance.getEntriesByType('resource').filter(function(e){return e.name.indexOf(location.origin)===0});
  var nav=performance.getEntriesByType('navigation')[0];
  var liste=[];
  /* Gewicht = komprimierte Dateigröße (encodedBodySize), damit Cache-Treffer nicht als 0 KB zählen; c = kam aus dem Cache */
  function gr(e){return e.encodedBodySize||e.transferSize||0}
  if(nav)liste.push({n:location.pathname==='/'?'index.html':location.pathname.replace(/^\//,''),b:gr(nav),c:!nav.transferSize&&nav.encodedBodySize>0});
  var schon={};
  r.forEach(function(e){var n=e.name.replace(location.origin+'/','').replace(/\?.*/,'');if(schon[n])return;schon[n]=1;liste.push({n:n,b:gr(e),c:!e.transferSize&&e.encodedBodySize>0})});
  var summe=liste.reduce(function(a,e){return a+e.b},0);
  return {liste:liste,n:liste.length,kb:summe/1000};
}

/* Startansicht „Stückliste“: die echten Dateien dieser Seite, während sie ankommen. Danach hebt sie sich wie ein Vorhang. */
(function(){
  var el=$('[data-stueckliste]');
  if(!root.classList.contains('intro')||!el){if(el)el.remove();START.los();return}
  var ul=$('[data-st-liste]',el),bal=$('[data-st-balken]',el),sum=$('[data-st-summe]',el);
  var t0=performance.now(),min=700,max=1800,fertig=false,gezeigt=0,p=0;
  var ziel={loading:.3,interactive:.7,complete:1};
  function zeile(e){
    var li=d.createElement('li');
    [e.n,e.c?(EN?'from cache':'aus dem Cache'):zahl(e.b/1000,1)+' KB'].forEach(function(t){var s=d.createElement('span');s.textContent=t;li.appendChild(s)});
    ul.appendChild(li);
  }
  function schritt(){
    if(fertig)return;
    var m=messung();
    while(gezeigt<m.liste.length&&gezeigt<8){zeile(m.liste[gezeigt]);gezeigt++}
    var t=performance.now()-t0,z=ziel[d.readyState]||.3;
    p+=(Math.min(z,Math.max(t/min,.1))-p)*.18;bal.style.transform='scaleX('+p.toFixed(3)+')';
    if(t>=max||(t>=min&&d.readyState==='complete'))ende(m);else requestAnimationFrame(schritt);
  }
  function ende(m){
    if(fertig)return;fertig=true;ss('sm-intro','1');
    ['keydown','pointerdown','wheel','touchstart'].forEach(function(n){removeEventListener(n,abbruch)});
    m=m||messung();bal.style.transform='scaleX(1)';
    sum.textContent=m.n+(EN?' files, ':' Dateien, ')+zahl(m.kb,0)+' KB';
    setTimeout(function(){
      root.classList.add('intro-aus');el.classList.add('weg');START.los();
      setTimeout(function(){root.classList.remove('intro');el.remove()},800);
    },red?0:260);
  }
  function abbruch(){ende()}
  ['keydown','pointerdown'].forEach(function(n){addEventListener(n,abbruch)});
  ['wheel','touchstart'].forEach(function(n){addEventListener(n,abbruch,{passive:true})});
  requestAnimationFrame(schritt);
})();

/* Kopfbereich der Startseite: die Überschrift steht sofort, Text und Knöpfe folgen. Darunter die Maßlinie. */
(function(){
  var kopf=$('.hero-innen');if(!kopf)return;
  var h1=$('.hero-titel',kopf);
  /* Maßlinie: misst die tatsächliche Breite der Überschrift (längste Zeile) */
  function masslinie(){
    var el=d.createElement('div');el.className='masslinie';el.setAttribute('aria-hidden','true');
    var s=d.createElement('span');el.appendChild(s);kopf.appendChild(el);
    function mess(){
      var rs=[],tw=d.createTreeWalker(h1,NodeFilter.SHOW_TEXT),n;
      while((n=tw.nextNode())){if(!n.textContent.trim())continue;var r=d.createRange();r.selectNodeContents(n);Array.prototype.push.apply(rs,Array.prototype.slice.call(r.getClientRects()).filter(function(x){return x.width>2}))}
      if(!rs.length)return;
      var l=Math.min.apply(null,rs.map(function(x){return x.left})),re=Math.max.apply(null,rs.map(function(x){return x.right})),un=Math.max.apply(null,rs.map(function(x){return x.bottom}));
      var b=kopf.getBoundingClientRect();
      el.style.left=(l-b.left)+'px';el.style.width=(re-l)+'px';el.style.top=(un-b.top+12)+'px';
      s.textContent=zahl(re-l,0)+' px';
    }
    mess();var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(mess,120)});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(mess);
    return el;
  }
  var ml=h1&&fein?masslinie():null;
  START.warte(function(){
    $$(':scope > .hero-ort, :scope > .hero-text',kopf).forEach(function(e,i){e.style.setProperty('--v',(120+i*110)+'ms');requestAnimationFrame(function(){requestAnimationFrame(function(){e.classList.add('an')})})});
    if(ml)setTimeout(function(){ml.classList.add('an')},red?0:420);
  });
})();

/* Beim Hinscrollen: Inhalte unterhalb des ersten Bildschirms erscheinen einmal. Was schon zu sehen ist, bleibt unberührt. */
(function(){
  if(red||!('IntersectionObserver' in window))return;
  var SEL=['main h2.t-l','main h2.t-xl','main .statement','.werk-bild','.werk-info','.werke-mehr',
    '.sek:not(.sek-hero):not(.sek-kopfseite) .lead','.datenblatt tbody tr','.pakete-fuss','.schiene li','.karte','.faq-liste','.betreuung-liste li',
    '.prinzipien li','.text-spalte > p','.ueber-text','.kontakt-direkt','.kontakt-rechts','.tab-wrap','.farbreihe li','.vorher-nachher','.werte',
    '.fenster','.drin-liste li','.code','.hilft-liste','.direkt','.zahlung','.einfuehrung','.schieber-schritte li'].join(',');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var t=e.target;
    requestAnimationFrame(function(){t.classList.add('da')})})},{rootMargin:'0px 0px -8% 0px',threshold:0});
  START.warte(function(){
    var h=innerHeight;
    $$(SEL).forEach(function(e){
      if(e.closest('.sek-hero,.sek-kopfseite'))return;
      if(e.getBoundingClientRect().top<h*.98)return;
      var p=e.parentNode,geschw=Array.prototype.filter.call(p.children,function(k){return k.matches(SEL)}),i=geschw.indexOf(e);
      e.style.setProperty('--v',Math.min(i,5)*70+'ms');
      e.classList.add('auf');io.observe(e);
    });
  });
})();

/* Derselbe Text: Vorher/Nachher-Schieber. Ziehen mit Maus oder Finger (senkrecht scrollt die Seite weiter),
   Pfeiltasten über den Regler. Beim ersten Hinsehen zeigt die Fläche kurz nur die Rohfassung, dann gleitet die Linie zur Mitte. */
(function(){
  var s=$('[data-schieber]');if(!s)return;
  var f=$('.sch-flaeche',s),r=$('.sch-regler',s),zieht=false,beruehrt=false;
  function setze(p){p=Math.max(0,Math.min(100,p));s.style.setProperty('--x',p+'%');r.value=Math.round(p)}
  function von(e){var b=f.getBoundingClientRect();return (e.clientX-b.left)/b.width*100}
  function halt(){beruehrt=true;s.classList.remove('gleitet')}
  f.addEventListener('pointerdown',function(e){
    if(e.button>0)return;halt();zieht=true;s.classList.add('zieht');
    if(e.pointerType==='mouse'){setze(von(e));e.preventDefault()}
    try{f.setPointerCapture(e.pointerId)}catch(_){}
  });
  f.addEventListener('pointermove',function(e){if(zieht)setze(von(e))});
  function los(){zieht=false;s.classList.remove('zieht')}
  f.addEventListener('pointerup',los);f.addEventListener('pointercancel',los);f.addEventListener('lostpointercapture',los);
  r.addEventListener('input',function(){halt();setze(+r.value)});
  if(red||!('IntersectionObserver' in window)||!(window.CSS&&'registerProperty' in CSS))return;
  START.warte(function(){
    var b=f.getBoundingClientRect();if(b.top<innerHeight*.9)return;
    setze(100);
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting)return;io.disconnect();if(beruehrt)return;
      setTimeout(function(){if(beruehrt)return;s.classList.add('gleitet');requestAnimationFrame(function(){setze(50)});
        setTimeout(function(){s.classList.remove('gleitet')},1600)},250);
    })},{threshold:.45});
    io.observe(f);
  });
})();

/* Schaufenster: die Arbeiten laufen live in einem Fenster. Am Desktop wird die Seite in voller Breite (1440 px)
   gerendert und verkleinert, damit man die Desktop-Fassung sieht; schmaler als 700 px zeigt das Fenster die Handy-Fassung. */
(function(){
  $$('[data-fenster]').forEach(function(fe){
    var reiter=$$('[data-reiter]',fe),tafeln=$$('[data-tafel]',fe);
    function frame(tf){return $('iframe',tf)}
    function passe(tf){
      var box=$('[data-fenster-bild]',tf),f=frame(tf);if(!box||!f)return;var w=box.clientWidth;
      if(w>=700){var s=w/1440;f.style.width='1440px';f.style.height=Math.ceil(box.clientHeight/s)+'px';f.style.transform='scale('+s+')'}
      else{f.style.width='100%';f.style.height='100%';f.style.transform='none'}
    }
    function lade(tf){var f=frame(tf);if(!f)return;if(!f.getAttribute('src')){var s=f.getAttribute('data-src');f.addEventListener('load',function(){f.classList.add('da')},{once:true});f.setAttribute('src',/^https?:/.test(s)?s:ort(s.replace(/^\//,'')))}passe(tf)}
    var sichtbar=false;
    function waehle(i,fokus){
      reiter.forEach(function(r,j){r.setAttribute('aria-selected',j===i?'true':'false');r.tabIndex=j===i?0:-1});
      tafeln.forEach(function(tf,j){tf.hidden=j!==i});
      if(sichtbar)lade(tafeln[i]);if(fokus)reiter[i].focus();
    }
    reiter.forEach(function(r,i){
      r.addEventListener('click',function(){waehle(i)});
      r.addEventListener('keydown',function(e){var n=null,l=reiter.length;
        if(e.key==='ArrowRight'||e.key==='ArrowDown')n=(i+1)%l;else if(e.key==='ArrowLeft'||e.key==='ArrowUp')n=(i-1+l)%l;else if(e.key==='Home')n=0;else if(e.key==='End')n=l-1;
        if(n!==null){e.preventDefault();waehle(n,true)}});
    });
    function aktiv(){for(var i=0;i<tafeln.length;i++)if(!tafeln[i].hidden)return tafeln[i];return tafeln[0]}
    /* erst laden, wenn das Fenster in die Nähe kommt: die Seite bleibt leicht */
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();sichtbar=true;lade(aktiv())}},{rootMargin:'500px 0px'});io.observe(fe)}
    else{sichtbar=true;lade(aktiv())}
    var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){passe(aktiv())},100)});
    /* Handy: im Fenster seitlich wischen wechselt die Arbeit; senkrechtes Scrollen bleibt der Seite */
    (function(){var x0=0,y0=0,ok=false;
      function cur(){for(var i=0;i<tafeln.length;i++)if(!tafeln[i].hidden)return i;return 0}
      fe.addEventListener('touchstart',function(e){var b=e.target.closest&&e.target.closest('[data-fenster-bild]');ok=!!b&&!b.classList.contains('aktiv');if(ok){x0=e.touches[0].clientX;y0=e.touches[0].clientY}},{passive:true});
      fe.addEventListener('touchend',function(e){if(!ok)return;ok=false;var t=e.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;
        if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5){var i=cur(),n=dx<0?i+1:i-1;if(n>=0&&n<tafeln.length){waehle(n);tick(10);var r=reiter[n];if(r&&r.scrollIntoView&&!red)r.scrollIntoView({block:'nearest',behavior:'smooth'})}}},{passive:true});
    })();
    /* Erst nach Tippen bedienbar, sonst hält das Fenster beim Scrollen der Seite den Finger fest */
    $$('[data-tippen]',fe).forEach(function(b){b.addEventListener('click',function(){b.closest('[data-fenster-bild]').classList.add('aktiv');b.hidden=true})});
  });
})();

/* Zeiger: ein Zeichenkreuz. Über Links und Knöpfen ein Auswahlrahmen, über den Arbeiten ein Etikett, auf der Bühne hell.
   Der eigene Zeiger ersetzt den Pfeil erst, wenn er sich bewegt hat; über Eingabefeldern und Demos bleibt der normale. */
(function(){
  if(!fein||red)return;
  var z=d.createElement('div');z.className='zeiger-el aus';z.setAttribute('aria-hidden','true');
  var k=d.createElement('span');k.className='zeiger-kreuz';var r=d.createElement('span');r.className='zeiger-rahmen';var t=d.createElement('span');t.className='zeiger-text';
  z.appendChild(r);z.appendChild(k);z.appendChild(t);body.appendChild(z);
  var x=-80,y=-80,frame=0,an=false;
  function pos(){frame=0;z.style.transform='translate('+x+'px,'+y+'px)'}
  addEventListener('pointermove',function(e){
    if(e.pointerType&&e.pointerType!=='mouse')return;
    x=e.clientX;y=e.clientY;if(!an){an=true;root.classList.add('zeiger')}if(!frame)frame=requestAnimationFrame(pos);
  },{passive:true});
  d.addEventListener('pointerover',function(e){
    var el=e.target;if(!el.closest)return;
    if(el.closest('iframe,input,textarea,select')){z.classList.add('aus');return}
    z.classList.toggle('aus',!an);
    z.classList.toggle('dunkel',!!el.closest(BUEHNE));
    var a=el.closest('a,button,summary,label,.schritt');
    var etikett=el.closest('.werk-bild')?(EN?'View':'Ansehen'):el.closest('.sch-flaeche')?(EN?'Drag':'Ziehen'):(a&&a.getAttribute('data-zeiger'))||'';
    z.classList.toggle('griff',!!a);
    t.textContent=etikett;z.classList.toggle('mit-text',!!etikett);
  });
  d.documentElement.addEventListener('mouseleave',function(){z.classList.add('aus')});
  d.documentElement.addEventListener('mouseenter',function(){if(an)z.classList.remove('aus')});
})();

/* Lesefortschritt (nur schmale Bildschirme, per CSS) */
(function(){
  var l=d.createElement('div');l.className='fortschritt';l.setAttribute('aria-hidden','true');body.appendChild(l);
  var w=false;function z(){w=false;var h=root.scrollHeight-innerHeight,p=h>0?Math.min(1,Math.max(0,(window.pageYOffset||root.scrollTop)/h)):0;l.style.transform='scaleX('+p+')'}
  function q(){if(!w){w=true;requestAnimationFrame(z)}}
  addEventListener('scroll',q,{passive:true});addEventListener('resize',q);z();
})();

/* Menü */
$$('[data-menue]').forEach(function(m){m.addEventListener('toggle',function(){tick(8)})});
$$('[data-menue] a').forEach(function(a){a.addEventListener('click',function(){var m=a.closest('details');if(m)m.open=false})});
addEventListener('keydown',function(e){if(e.key==='Escape'){var m=$('[data-menue][open]');if(m)m.open=false}});

/* Formular: Fehler stehen am Feld (aria-describedby), geprüft beim Absenden und danach beim Verlassen des Felds */
$$('[data-formular]').forEach(function(f){
  var meld=$('[data-meldung]',f),ep=f.getAttribute('data-endpoint'),versucht=false;
  var pre=/[?&]paket=(\w+)/.exec(location.search);var sel=$('select',f);if(pre&&sel)sel.value=pre[1];
  function pruefe(i){
    var v=i.value.trim(),txt='';
    if(!v)txt=EN?'Please fill this in.':'Bitte ausfüllen.';else if(i.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v))txt=EN?'Please enter a valid email address, for example name@company.com.':'Bitte eine gültige E-Mail-Adresse eingeben, zum Beispiel name@betrieb.at.';
    var id=i.id+'-fehler',p=d.getElementById(id);
    if(txt){if(!p){p=d.createElement('p');p.className='feld-fehler';p.id=id;i.parentNode.appendChild(p)}p.textContent=txt;i.setAttribute('aria-invalid','true');i.setAttribute('aria-describedby',id)}
    else{if(p)p.remove();i.removeAttribute('aria-invalid');i.removeAttribute('aria-describedby')}
    return !txt;
  }
  $$('[required]',f).forEach(function(i){i.addEventListener('blur',function(){if(versucht)pruefe(i)});i.addEventListener('input',function(){if(i.getAttribute('aria-invalid'))pruefe(i)})});
  f.addEventListener('submit',function(e){
    versucht=true;var fehl=null;
    $$('[required]',f).forEach(function(i){if(!pruefe(i)&&!fehl)fehl=i});
    if(fehl){e.preventDefault();meld.textContent=EN?'Please check the marked fields.':'Bitte prüfen Sie die markierten Felder.';fehl.focus();return}
    meld.textContent='';
    if(!ep){e.preventDefault();meld.textContent=EN?'Your email program opens with a prepared message.':'Ihr E-Mail-Programm öffnet sich mit einer vorbereiteten Nachricht.';
      var v=new FormData(f),txt='';v.forEach(function(w,k){if(k!=='_gotcha'&&w)txt+=k+': '+w+'\n'});
      location.href='mailto:'+f.getAttribute('action').replace('mailto:','')+'?subject='+encodeURIComponent(EN?'Enquiry via simonmonu.at':'Anfrage über simonmonu.at')+'&body='+encodeURIComponent(txt);return}
    e.preventDefault();var k=$('button[type=submit]',f);if(k.disabled)return;k.disabled=true;meld.textContent=EN?'Sending …':'Wird gesendet …';
    fetch(ep,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}}).then(function(r){
      if(r.ok){tick([12,60,12]);location.href=ort(EN?'en/thanks/':'danke/')}else throw 0;
    }).catch(function(){k.disabled=false;meld.textContent=(EN?'That did not work, sorry. Please write directly to ':'Das hat leider nicht geklappt. Bitte schreiben Sie direkt an ')+((($('a[href^="mailto:"]')||{}).textContent)||(EN?'my email address':'meine E-Mail-Adresse'))+'.'});
  });
});

/* Danke: Wochentag, bis zu dem ich mich melde (zwei Werktage) */
(function(){
  var e=$('[data-danke]');if(!e)return;
  var t=new Date(),n=0,w=EN?['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],mo=['January','February','March','April','May','June','July','August','September','October','November','December'];
  while(n<2){t.setDate(t.getDate()+1);if(t.getDay()!==0&&t.getDay()!==6)n++}
  e.textContent=EN?'I will get back to you by '+w[t.getDay()]+', '+mo[t.getMonth()]+' '+t.getDate()+'.':'Ich melde mich spätestens bis '+w[t.getDay()]+', '+t.getDate()+'.'+(t.getMonth()+1)+'. bei Ihnen.';
})();

})();
