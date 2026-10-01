/* Läuft synchron im Kopf: Klassen und Theme setzen, bevor etwas gemalt wird. */
(function(){
  var d=document.documentElement,t;
  d.classList.add('js');
  try{t=localStorage.getItem('sm-theme');if(t==='hell')d.setAttribute('data-theme','light');else if(t==='dunkel')d.setAttribute('data-theme','dark')}catch(e){}
  var red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(red)d.classList.add('ruhig');
  var erzwingen=/[?&]intro\b/.test(location.search),gesehen=false;
  try{gesehen=sessionStorage.getItem('sm-intro')==='1'}catch(e){}
  /* Startansicht nur auf dem Server: per Doppelklick (file://) misst der Browser keine Dateien */
  if(d.hasAttribute('data-start')&&!red&&location.protocol!=='file:'&&(erzwingen||!gesehen))d.classList.add('intro');
  /* Notbremse: Läuft seite.js nicht an (Fehler, blockiert), ist nach 4 s alles sichtbar */
  setTimeout(function(){if(!window.SM_LAEUFT)d.classList.add('frei')},4000);
  /* Seitenwechsel in Chrome/Edge: magenta Haarlinie zieht einmal über die Seite */
  addEventListener('pagereveal',function(ev){
    if(!ev.viewTransition||red)return;
    var w=document.querySelector('[data-wechsel]');
    if(w&&w.animate)w.animate([{opacity:1,transform:'scaleX(0)'},{opacity:1,transform:'scaleX(1)',offset:.7},{opacity:0,transform:'scaleX(1)'}],{duration:520,easing:'cubic-bezier(.65,0,.35,1)'});
  });
})();
