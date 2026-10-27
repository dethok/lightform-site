/* Light + Form Concepts - vanilla, no libraries. Loaded in <head>: `motion` is set before first paint. */
document.documentElement.classList.add('motion');
document.addEventListener('DOMContentLoaded', () => {
  const d = document, root = d.documentElement, $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const hdr = $('.site-header'), hasHero = d.body.classList.contains('has-hero');
  let megaOpen = false, drawerOpen = false;

  // header: transparent over the hero, solid after 40px (always solid without a hero, or while a menu is open)
  const upd = () => hdr.classList.toggle('is-solid', !hasHero || scrollY > 40 || megaOpen || drawerOpen);
  addEventListener('scroll', upd, { passive: true }); upd();

  // mega menu: hover-intent 120ms on fine pointers, click on touch, Escape / click-outside closes
  const mega = $('.has-mega'), trigger = $('.mega-trigger'), fine = matchMedia('(hover:hover) and (pointer:fine)');
  let timer;
  const setMega = o => { megaOpen = o; trigger.setAttribute('aria-expanded', o); root.classList.toggle('mega-open', o); upd(); };
  mega.addEventListener('mouseenter', () => { if (fine.matches) { clearTimeout(timer); timer = setTimeout(() => setMega(true), 120); } });
  mega.addEventListener('mouseleave', () => { if (fine.matches) { clearTimeout(timer); timer = setTimeout(() => setMega(false), 120); } });
  trigger.addEventListener('click', e => { if (!fine.matches || e.detail === 0) setMega(!megaOpen); });
  d.addEventListener('click', e => { if (megaOpen && !mega.contains(e.target)) setMega(false); });

  // mobile drawer: focus trap + body scroll lock
  const drawer = $('.drawer'), openBtn = $('.menu-btn'), closeBtn = $('.drawer-close');
  drawer.inert = true;
  const setDrawer = o => {
    drawerOpen = o; drawer.classList.toggle('is-open', o); drawer.inert = !o;
    d.body.classList.toggle('no-scroll', o); openBtn.setAttribute('aria-expanded', o);
    (o ? closeBtn : openBtn).focus(); upd();
  };
  openBtn.addEventListener('click', () => setDrawer(true));
  closeBtn.addEventListener('click', () => setDrawer(false));
  $$('a', drawer).forEach(a => a.addEventListener('click', () => setDrawer(false)));
  matchMedia('(min-width:900px)').addEventListener('change', e => { if (e.matches && drawerOpen) setDrawer(false); });
  d.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (megaOpen) { setMega(false); trigger.focus(); }
      if (drawerOpen) setDrawer(false);
    }
    if (e.key === 'Tab' && drawerOpen) {
      const f = $$('a,button', drawer), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // lamps: tap toggles on touch (first tap lights a linked tile, second tap follows the link)
  if (matchMedia('(pointer:coarse)').matches) {
    $$('.lamp').forEach(l => l.addEventListener('click', e => {
      if (l.classList.toggle('is-on') && l.closest('a')) e.preventDefault();
    }));
  }

  // scroll reveal, once
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
  }), { threshold: .15 });
  $$('.reveal').forEach(el => io.observe(el));

  // hero Ken Burns
  const kb = $('.hero-bg'); if (kb) kb.classList.add('kb');

  // product gallery + explicit Lights on / off toggle
  const slides = $$('.g-slide'), thumbs = $$('[data-thumb]'), lt = $('[data-lights]');
  if (slides.length && lt) {
    let on = false, cur = 0;
    const show = i => {
      cur = i;
      slides.forEach((s, k) => { s.classList.toggle('is-active', k === i); s.classList.toggle('is-on', on && k === i); });
      thumbs.forEach((t, k) => t.setAttribute('aria-current', k === i));
    };
    thumbs.forEach((t, k) => t.addEventListener('click', () => show(k)));
    lt.addEventListener('click', () => { on = !on; lt.setAttribute('aria-pressed', on); lt.textContent = on ? 'Lights off' : 'Lights on'; show(cur); });
    show(0);
  }
});
