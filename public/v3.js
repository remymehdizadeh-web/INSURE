(function(){var d=document,R=matchMedia('(prefers-reduced-motion: reduce)').matches;if(R)return;
var pb=d.querySelector('.prog-bar'),t=false;function u(){t=false;var m=d.documentElement.scrollHeight-innerHeight;pb&&pb.style.setProperty('--sp',m>0?(scrollY/m).toFixed(4):0)}
addEventListener('scroll',function(){if(!t){t=true;requestAnimationFrame(u)}},{passive:true});u();
d.querySelectorAll('.pband,.about-photo').forEach(function(e){e.setAttribute('data-rv','')});
var L=d.querySelectorAll('[data-lic]');if(!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);var e=x.target,v=e.dataset.lic,s=null,D=1300;
function f(ts){if(!s)s=ts;var k=(ts-s)/D,o='';for(var i=0;i<v.length;i++){var c=v[i];o+=(/\d/.test(c)&&k<(i+1)/v.length)?Math.floor(Math.random()*10):c}e.textContent=o;if(k<1)requestAnimationFrame(f);else e.textContent=v}requestAnimationFrame(f)})},{threshold:.6});
L.forEach(function(e){io.observe(e)})})();
(function(){var f=function(){document.body.classList.toggle('past-hero',scrollY>innerHeight*.7)};addEventListener('scroll',f,{passive:true});f()})();
(function(){if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;var d=document,r=d.querySelector('.cs-r');if(!r)return;r.setAttribute('data-rv','');
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(r);r.classList.add('in');r.querySelectorAll('[data-money]').forEach(function(e){var t=+e.dataset.money,s=null;function f(ts){if(!s)s=ts;var k=Math.min(1,(ts-s)/1600),v=1-Math.pow(1-k,3);e.textContent='$'+Math.round(t*v).toLocaleString('en-US');if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)})})},{threshold:.4});io.observe(r)})();
