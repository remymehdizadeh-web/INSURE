(function(){var d=document,h=d.documentElement,R=matchMedia('(prefers-reduced-motion: reduce)').matches;
var hd=d.querySelector('header.site'),mb=d.querySelector('.menu-btn');
if(mb)mb.addEventListener('click',function(){var o=d.body.classList.toggle('nav-open');mb.setAttribute('aria-expanded',o);var r=hd.getBoundingClientRect();h.style.setProperty('--sheet-top',r.bottom+'px')});
addEventListener('scroll',function(){hd&&hd.classList.toggle('scrolled',scrollY>40)},{passive:true});
// auto-tag common blocks for reveal
d.querySelectorAll('main section h2, main section .card, main .icard, main .st, main .stat, main .reg, main .faq details, main .lp .cov > div, main .creds .it').forEach(function(e,i){if(!e.hasAttribute('data-rv'))e.setAttribute('data-rv','')});
var groups=new Map();d.querySelectorAll('[data-rv]').forEach(function(e){var p=e.parentElement,n=groups.get(p)||0;groups.set(p,n+1);if(!e.style.getPropertyValue('--d'))e.style.setProperty('--d',Math.min(n,5)*0.08+'s')});
function count(e){var t=+e.dataset.count;if(R){e.textContent=t;return}var s=null,D=1400;function f(ts){if(!s)s=ts;var k=Math.min(1,(ts-s)/D),v=1-Math.pow(1-k,3);e.textContent=Math.round(t*v);if(k<1)requestAnimationFrame(f)}e.textContent='0';requestAnimationFrame(f)}
if(R||!('IntersectionObserver' in window)){return}
var vh=innerHeight;d.querySelectorAll('[data-rv]').forEach(function(e){if(e.getBoundingClientRect().top<vh*0.92)e.classList.add('in')});
h.classList.add('motion');
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
d.querySelectorAll('[data-rv]:not(.in)').forEach(function(e){io.observe(e)});
var co=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){count(x.target);co.unobserve(x.target)}})},{threshold:.6});
d.querySelectorAll('[data-count]').forEach(function(e){co.observe(e)});
var px=[].slice.call(d.querySelectorAll('[data-px]')),st=d.querySelector('.steps2'),tick=false;
function upd(){tick=false;var H=innerHeight;px.forEach(function(e){var r=e.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>H)return;var c=(r.top+r.height/2-H/2);e.style.transform='translate3d(0,'+(c*-(+e.dataset.px)).toFixed(1)+'px,0)'});
if(st){var r=st.getBoundingClientRect(),p=(H*0.8-r.top)/(r.height+H*0.3);st.style.setProperty('--p',Math.max(0,Math.min(1,p)).toFixed(3))}}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});upd();
})();
