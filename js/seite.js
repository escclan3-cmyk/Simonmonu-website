/* simonmonu.at · Seitenskript. Nichts hiervon ist nötig, damit die Seite funktioniert. */
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
function $(s,c){return (c||d).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
function sg(k){try{return sessionStorage.getItem(k)}catch(e){return null}}
function ss(k,v){try{v==null?sessionStorage.removeItem(k):sessionStorage.setItem(k,v)}catch(e){}}
function zahl(n,st){var s=n.toFixed(st).split('.');s[0]=s[0].replace(/\B(?=(\d{3})+(?!\d))/g,EN?',':'.');return s.join(EN?'.':',')}
/* Zählt eine Zahl in einem Text hoch (0 bis Zielwert), ohne Einheit oder Format zu verändern */
function tween(dauer,f){var t0=performance.now();(function s(n){var k=Math.min(1,(n-t0)/dauer),e=1-Math.pow(1-k,4);f(e);if(k<1)requestAnimationFrame(s)})(t0)}
/* Start: wartet auf das Ende der Stückliste (falls sie läuft) und auf die Schriften, damit die Zeilen stimmen */
var START=(function(){var fs=[],ok=false;return{warte:function(f){ok?f():fs.push(f)},los:function(){if(ok)return;ok=true;var w=d.fonts&&d.fonts.ready?Promise.race([d.fonts.ready,new Promise(function(r){setTimeout(r,500)})]):Promise.resolve();w.then(function(){fs.forEach(function(f){f()})})}}})();

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

/* Messung der eigenen Seite (nur auf diesem Gerät) */
function messung(){
  var r=performance.getEntriesByType('resource').filter(function(e){return e.name.indexOf(location.origin)===0});
  var nav=performance.getEntriesByType('navigation')[0];
  var liste=[];
  /* Gewicht = komprimierte Dateigröße (encodedBodySize), damit Cache-Treffer nicht als 0 KB zählen; c = kam aus dem Cache */
  function gr(e){return e.encodedBodySize||e.transferSize||0}
  if(nav)liste.push({n:location.pathname==='/'?'index.html':location.pathname.replace(/^\//,''),b:gr(nav),t:nav.responseEnd,c:!nav.transferSize&&nav.encodedBodySize>0});
  r.forEach(function(e){liste.push({n:e.name.replace(location.origin+'/','').replace(/\?.*/,''),b:gr(e),t:e.responseEnd,c:!e.transferSize&&e.encodedBodySize>0})});
  var summe=liste.reduce(function(a,e){return a+e.b},0);
  var ende=nav?(nav.loadEventEnd||nav.domContentLoadedEventEnd||performance.now()):performance.now();
  return {liste:liste,n:liste.length,kb:summe/1000,s:ende/1000};
}

/* Spur-Zeile: echte Werte, live gemessen */
function spur(){
  if(DATEI)return;   /* file:// liefert keine Messdaten: die beim Bauen berechneten Werte bleiben stehen */
  var m=messung();
  var sp=$('[data-spur]');
  function text(k){return EN?'This page: '+Math.round(m.n*k)+(m.n===1?' file, ':' files, ')+zahl(m.kb*k,0)+'\u00a0KB, loaded on your device in '+zahl(m.s*k,2)+'\u00a0s':'Diese Seite: '+Math.round(m.n*k)+(m.n===1?' Datei, ':' Dateien, ')+zahl(m.kb*k,0)+'\u00a0KB, bei Ihnen in '+zahl(m.s*k,2)+'\u00a0s geladen'}
  if(sp&&m.n>0){if(red)sp.textContent=text(1);else START.warte(function(){tween(900,function(k){sp.textContent=text(k)})})}
  var f=$('[data-spur-fuss]');
  if(f&&m.n>0)f.textContent=(EN?'This page: '+m.n+' files, ':'Diese Seite: '+m.n+' Dateien, ')+zahl(m.kb,0)+' KB';
  if(m.n>0){$$('[data-live-n]').forEach(function(e){e.textContent=m.n});$$('[data-live-kb]').forEach(function(e){e.textContent=zahl(m.kb,0)})}
}
if(d.readyState==='complete')setTimeout(spur,0);else addEventListener('load',function(){setTimeout(spur,0)});

/* Startansicht "Stückliste": zeigt die echten Dateien dieser Seite, während sie ankommen */
(function(){
  var el=$('[data-stueckliste]');
  if(!root.classList.contains('intro')||!el){if(el)el.remove();START.los();return}
  var ul=$('[data-st-liste]',el),sum=$('[data-st-summe]',el);
  var start=performance.now(),min=900,max=2400,fertig=false,gezeigt=0;
  function zeile(e){
    var li=d.createElement('li');li.className='mono';
    [e.n,e.c?(EN?'from cache':'aus dem Cache'):zahl(e.b/1000,1)+' KB',zahl(e.t/1000,2)+' s'].forEach(function(t){var s=d.createElement('span');s.textContent=t;li.appendChild(s)});
    ul.appendChild(li);
  }
  function tick(){
    if(fertig)return;
    var m=messung();
    while(gezeigt<m.liste.length&&gezeigt<9){zeile(m.liste[gezeigt]);gezeigt++}
    sum.textContent=m.n+(EN?' files, ':' Dateien, ')+zahl(m.kb,0)+'\u00a0KB';
    var t=performance.now()-start;
    if(t>=max||(t>=min&&d.readyState==='complete'))ende();else requestAnimationFrame(tick);
  }
  function ende(){
    if(fertig)return;fertig=true;ss('sm-intro','1');
    removeEventListener('keydown',ende);removeEventListener('pointerdown',ende);removeEventListener('wheel',ende);removeEventListener('touchstart',ende);
    el.classList.add('weg');root.classList.add('intro-aus');START.los();
    setTimeout(function(){root.classList.remove('intro');el.remove()},480);
  }
  addEventListener('keydown',ende);addEventListener('pointerdown',ende);addEventListener('wheel',ende,{passive:true});addEventListener('touchstart',ende,{passive:true});
  requestAnimationFrame(tick);
})();

/* Platzhalter -> Bild */
$$('picture.bild[data-bild]').forEach(function(p){
  var i=$('img',p);if(!i)return;
  function ok(){p.classList.add('geladen')}
  if(i.complete&&i.naturalWidth)ok();else{i.addEventListener('load',ok);i.addEventListener('error',ok)}
});

/* Gestaffelte Listen */
(function(){
  var l=$$('[data-stagger]');if(!l.length)return;
  l.forEach(function(x){$$(':scope > *',x).forEach(function(k,i){k.style.setProperty('--i',i)})});
  if(!('IntersectionObserver' in window)){l.forEach(function(x){x.classList.add('ein')});return}
  var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('ein');o.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px'});
  l.forEach(function(x){o.observe(x)});
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
        if(e.key==='ArrowRight')n=(i+1)%l;else if(e.key==='ArrowLeft')n=(i-1+l)%l;else if(e.key==='Home')n=0;else if(e.key==='End')n=l-1;
        if(n!==null){e.preventDefault();waehle(n,true)}});
    });
    function aktiv(){for(var i=0;i<tafeln.length;i++)if(!tafeln[i].hidden)return tafeln[i];return tafeln[0]}
    /* erst laden, wenn das Fenster in die Nähe kommt: die Startseite bleibt leicht */
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();sichtbar=true;lade(aktiv())}},{rootMargin:'500px 0px'});io.observe(fe)}
    else{sichtbar=true;lade(aktiv())}
    var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){passe(aktiv())},100)});
    /* Touch: erst nach Tippen bedienbar, sonst hält das Fenster beim Scrollen der Seite den Finger fest */
    $$('[data-tippen]',fe).forEach(function(b){b.addEventListener('click',function(){b.closest('[data-fenster-bild]').classList.add('aktiv');b.hidden=true})});
  });
})();

/* Bewegung: Start, Überschriften Zeile für Zeile, Bilder, Linien, Zahlen. Alles einmal, nichts bei reduzierter Bewegung. */
(function(){
  if(red)return;
  if(!('IntersectionObserver' in window)){root.classList.add('frei');return}
  function teile(h){
    if(h.classList.contains('geteilt'))return !!h.__orig;
    var kinder=Array.prototype.slice.call(h.childNodes);
    if(kinder.some(function(n){return n.nodeType===1&&n.tagName!=='BR'})){h.classList.add('geteilt');return false}
    h.__orig=h.innerHTML;h.innerHTML='';
    var w=[];
    kinder.forEach(function(n){
      if(n.nodeType===3)n.textContent.split(/\s+/).forEach(function(x){if(!x)return;var s=d.createElement('span');s.textContent=x;h.appendChild(s);h.appendChild(d.createTextNode(' '));w.push(s)});
      else h.appendChild(d.createElement('br'));
    });
    var reihen=[],top=null;
    w.forEach(function(s){var o=s.offsetTop;if(top===null||o>top+2){reihen.push([]);top=o}reihen[reihen.length-1].push(s.textContent)});
    h.innerHTML='';
    reihen.forEach(function(r,i){var a=d.createElement('span');a.className='zeile';var b=d.createElement('span');b.className='zeile-in';b.style.setProperty('--z',i);b.textContent=r.join(' ');a.appendChild(b);h.appendChild(a)});
    h.__n=reihen.length;h.classList.add('geteilt');return true;
  }
  function zeige(h,v){
    var geteilt=teile(h);
    if(v)h.style.setProperty('--v',v+'ms');
    requestAnimationFrame(function(){requestAnimationFrame(function(){h.classList.add('an')})});
    if(geteilt)offen.push(h);
  }
  /* Nach dem Auftritt bleiben die Zeilen stehen (ein Austausch des Texts würde als neuer größter Inhalt zählen und das
     gemessene LCP verschlechtern). Erst wenn sich die Fensterbreite ändert, kommt der ursprüngliche Text zurück. */
  var offen=[],rt;
  addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){offen.forEach(function(h){if(h.__orig!=null&&h.classList.contains('an')){h.innerHTML=h.__orig;h.__orig=null}});offen=offen.filter(function(h){return h.__orig!=null})},150)});
  function auf(e,v){if(v!=null)e.style.setProperty('--v',v+'ms');requestAnimationFrame(function(){requestAnimationFrame(function(){e.classList.add('an')})})}
  function zaehle(dd){
    var m=/^(\d+)(?:[,.](\d+))?(.*)$/.exec(dd.textContent.trim());if(!m)return;
    var ziel=parseFloat(m[1]+'.'+(m[2]||'0')),st=m[2]?m[2].length:0,rest=m[3];
    tween(1200,function(k){dd.textContent=zahl(ziel*k,st)+rest});
  }
  /* Maßlinie unter der Startüberschrift: misst die tatsächliche Zeilenbreite und Schriftgröße */
  function masslinie(h1){
    var box=h1.parentElement,el=d.createElement('div');el.className='masslinie';el.setAttribute('aria-hidden','true');
    var s=d.createElement('span');el.appendChild(s);box.appendChild(el);
    function mess(){
      var rs=[],tw=d.createTreeWalker(h1,NodeFilter.SHOW_TEXT),n;
      while((n=tw.nextNode())){if(!n.textContent.trim())continue;var r=d.createRange();r.selectNodeContents(n);Array.prototype.push.apply(rs,Array.prototype.slice.call(r.getClientRects()).filter(function(x){return x.width>2}))}
      if(!rs.length)return;var l=Math.min.apply(null,rs.map(function(x){return x.left})),re=Math.max.apply(null,rs.map(function(x){return x.right}));
      var b=box.getBoundingClientRect(),hb=h1.getBoundingClientRect();
      el.style.left=(l-b.left)+'px';el.style.width=(re-l)+'px';el.style.top=(hb.bottom-b.top+5)+'px';
      s.textContent=zahl(re-l,0)+(EN?' px wide, type ':' px breit, Schrift ')+zahl(parseFloat(getComputedStyle(h1).fontSize),0)+' px';
    }
    mess();var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(mess,120)});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(mess);
    return el;
  }
  /* Start: Kopfbereich der Seite */
  START.warte(function(){
    var kopf=$('.hero-innen')||$('.sek-kopfseite .wrap');if(!kopf)return;
    var h1=$('h1',kopf),rest=$$(':scope > :not(h1):not(.lead)',kopf);
    if(h1)zeige(h1,0);
    rest.forEach(function(e,i){e.classList.add('bw-auf');auf(e,e.classList.contains('spur')?0:80+i*100)});
    if(h1&&kopf.classList.contains('hero-innen')){var ml=masslinie(h1);setTimeout(function(){ml.classList.add('an')},900)}
  });
  /* Beim Scrollen */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;io.unobserve(e.target);var t=e.target,art=t.__art;
    if(art==='zeilen')zeige(t,0);
    else if(art==='linie')t.classList.add('linie-an');
    else{auf(t);if(t.classList.contains('werte'))$$('dd.mono',t).forEach(zaehle)}
  })},{rootMargin:'0px 0px -12% 0px',threshold:0});
  /* Fließtext, der schon beim Laden im Bild ist, steht sofort da: sonst misst der Browser den größten Inhalt erst nach der Einblendung */
  function beob(sel,art,kl,v){$$(sel).forEach(function(e,i){if(e.__art||e.classList.contains('geteilt'))return;
    if(art==='text'&&e.getBoundingClientRect().top<innerHeight){e.__art=art;e.style.transition='none';e.classList.add('an');return}
    e.__art=art;if(kl)e.classList.add(kl);if(v!=null)e.style.setProperty('--v',(typeof v==='function'?v(e,i):v)+'ms');io.observe(e)})}
  START.warte(function(){
    beob('main :is(h1,h2):is(.t-display,.t-xl,.t-l)','zeilen');
    beob('.sek+.sek','linie');
    beob('.fenster-rahmen,.vorher-nachher figure','bild','bw-bild');
    beob('.arbeit-zeile,.reiter-liste,.fenster-info','auf','bw-auf',120);
    beob('.sek:not(.sek-hero):not(.sek-kopfseite):not(.rechtstext) .lead,.text-spalte > p,.zahlung,.einfuehrung,.preis-hinweis,.ueber-text,.problem-text > p,.beleg-text','text','bw-text',180);
    beob('.alle,.sek:not(.sek-hero):not(.sek-kopfseite) .knoepfe,.tab-wrap,.farbreihe li,.formular,.direkt,.faq-liste,.betreuung-liste li,.prinzipien li,.code,.hilft-liste,.werte,.ueber-link','auf','bw-auf',function(e,i){return 120+(e.matches('li')?Array.prototype.indexOf.call(e.parentNode.children,e)*80:0)});
  });
})();

/* Seitenwechsel dort, wo der Browser keine View Transitions kann (Firefox, Safari, per Doppelklick): kurz ausblenden, dann weiter */
(function(){
  if(red||(!DATEI&&('PageRevealEvent' in window)))return;
  d.addEventListener('click',function(e){
    if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    var a=e.target.closest&&e.target.closest('a[href]');if(!a||a.target||a.hasAttribute('download'))return;
    var h=a.getAttribute('href');if(/^(#|mailto:|tel:|javascript:)/.test(h))return;
    var u=new URL(a.href,location.href);
    if(DATEI?u.protocol!=='file:':u.origin!==location.origin)return;
    if(u.pathname===location.pathname&&u.hash)return;
    e.preventDefault();root.classList.add('geht');setTimeout(function(){location.href=a.href},190);
  });
  addEventListener('pageshow',function(){root.classList.remove('geht')});
})();

/* Zeiger: ein Kreuz, daneben die Position in Pixeln. Auf den dunklen Flächen hell. */
(function(){
  if(!fein||red)return;
  var z=d.createElement('div');z.className='zeiger-el';z.setAttribute('aria-hidden','true');
  var t=d.createElement('span');t.className='zeiger-text';var m=d.createElement('span');m.className='zeiger-mass mono';
  z.appendChild(t);z.appendChild(m);body.appendChild(z);root.classList.add('zeiger');
  var x=-50,y=-50,frame=0,BUEHNE='.sek-arbeiten,.sek-kontakt,.sek-schaufenster,.sek-case-bild,.sek-demo,.sek-anfrage';
  function pos(){frame=0;z.style.transform='translate('+x+'px,'+y+'px)';m.textContent=Math.round(x)+' \u00b7 '+Math.round(y)}
  addEventListener('pointermove',function(e){x=e.clientX;y=e.clientY;if(!frame)frame=requestAnimationFrame(pos)},{passive:true});
  d.addEventListener('pointerover',function(e){
    if(e.target.tagName==='IFRAME'){z.classList.add('aus');return}z.classList.remove('aus');
    z.classList.toggle('dunkel',!!(e.target.closest&&e.target.closest(BUEHNE)));
    var a=e.target.closest&&e.target.closest('a,button,summary,label,select');
    if(a){z.classList.add('griff');t.textContent=a.getAttribute('data-zeiger')||''}else{z.classList.remove('griff');t.textContent=''}
    z.classList.toggle('mit-text',!!t.textContent);
  });
  d.addEventListener('mouseleave',function(){z.style.transform='translate(-50px,-50px)'});
})();

/* Menü schließen bei Klick auf Link */
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
      if(r.ok)location.href=ort(EN?'en/thanks/':'danke/');else throw 0;
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
