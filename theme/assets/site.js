/* Light + Form Concepts - vanilla, no libraries. Loaded in <head>: `motion` is set before first paint. */
document.documentElement.classList.add('motion');
document.addEventListener('DOMContentLoaded', () => {
  const d = document, root = d.documentElement, $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const hdr = $('.site-header'), hasHero = d.body.classList.contains('has-hero');
  let megaOpen = false, drawerOpen = false;

  // header: transparent over the hero, solid after 40px (always solid without a hero, or while a menu is open)
  const upd = () => hdr.classList.toggle('is-solid', !hasHero || scrollY > 40 || megaOpen || drawerOpen);
  addEventListener('scroll', upd, { passive: true }); upd();

  // header search: an empty submit just opens/focuses the field
  const hs = $('.hsearch'); if (hs) { hs.addEventListener('submit', e => { const i = $('.hsearch-in', hs); if (!i.value.trim()) { e.preventDefault(); i.focus(); } }); }

  // mega menus (Shop + Services): hover-intent 120ms on fine pointers, click on touch, Escape / click-outside closes; one open at a time
  const megas = $$('.has-mega'), fine = matchMedia('(hover:hover) and (pointer:fine)');
  const setMega = (m, o) => {
    if (o) megas.forEach(x => x !== m && setMega(x, false));
    m.classList.toggle('is-open', o); $('.mega-trigger', m).setAttribute('aria-expanded', o);
    megaOpen = megas.some(x => x.classList.contains('is-open')); root.classList.toggle('mega-open', megaOpen); upd();
  };
  megas.forEach(m => {
    let timer;
    m.addEventListener('mouseenter', () => { if (fine.matches) { clearTimeout(timer); timer = setTimeout(() => setMega(m, true), 120); } });
    m.addEventListener('mouseleave', () => { if (fine.matches) { clearTimeout(timer); timer = setTimeout(() => setMega(m, false), 120); } });
    $('.mega-trigger', m).addEventListener('click', e => { if (!fine.matches || e.detail === 0) setMega(m, !m.classList.contains('is-open')); });
  });
  d.addEventListener('click', e => megas.forEach(m => { if (m.classList.contains('is-open') && !m.contains(e.target)) setMega(m, false); }));

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
      megas.forEach(m => { if (m.classList.contains('is-open')) { setMega(m, false); $('.mega-trigger', m).focus(); } });
      if (drawerOpen) setDrawer(false);
    }
    if (e.key === 'Tab' && drawerOpen) {
      const f = $$('a,button', drawer), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  if (matchMedia('(pointer:coarse)').matches) {
    // flip tiles: first tap shows the description, second tap follows the link
    $$('.tile-flip').forEach(t => t.addEventListener('click', e => {
      if (t.classList.toggle('is-flipped')) e.preventDefault();
    }));
  }

  // scroll reveal, once
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
  }), { threshold: .15 });
  $$('.reveal').forEach(el => io.observe(el));

  // hero Ken Burns
  const kb = $('.hero-bg'); if (kb) kb.classList.add('kb');

  // product gallery
  const slides = $$('.g-slide'), thumbs = $$('[data-thumb]');
  if (slides.length) {
    const show = i => {
      slides.forEach((s, k) => s.classList.toggle('is-active', k === i));
      thumbs.forEach((t, k) => t.setAttribute('aria-current', k === i));
    };
    thumbs.forEach((t, k) => t.addEventListener('click', () => show(k)));
    show(0);
  }
});
