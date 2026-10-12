(() => {
  const html = document.documentElement;
  const isHome = document.body.dataset.page === 'home';
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, min, max) => Math.min(Math.max(v, min), max);

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  // a #section in the URL is honoured only when arriving from another page of the site;
  // a plain open or reload always starts from the first screen
  const navEntry = performance.getEntriesByType('navigation')[0];
  let cameFromSite = false;
  try {
    cameFromSite = !!document.referrer && (!navEntry || navEntry.type === 'navigate')
      && new URL(document.referrer).origin === location.origin
      && new URL(document.referrer).pathname !== location.pathname;
  } catch (e) { /* malformed referrer */ }
  const startHash = cameFromSite ? location.hash : '';
  if (location.hash) history.replaceState(null, '', location.pathname + location.search);
  window.scrollTo(0, 0);

  /* ---------- Text splitting ---------- */
  const wrap = (text, i) => {
    const outer = document.createElement('span');
    const inner = document.createElement('span');
    outer.className = 'w';
    inner.className = 'w__i';
    inner.style.setProperty('--i', i);
    inner.textContent = text;
    outer.append(inner);
    return outer;
  };

  document.querySelectorAll('[data-split]').forEach((el) => {
    const byChars = el.dataset.split === 'chars';
    let i = 0;
    const walk = (node) => {
      [...node.childNodes].forEach((child) => {
        if (child.nodeType === Node.TEXT_NODE) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) frag.append(' ');
            else if (byChars) [...part].forEach((ch) => frag.append(wrap(ch, i++)));
            else frag.append(wrap(part, i++));
          });
          child.replaceWith(frag);
        } else if (child.nodeType === Node.ELEMENT_NODE && child.tagName !== 'BR') {
          walk(child);
        }
      });
    };
    walk(el);
  });

  /* ---------- Reveal on scroll (starts after the loader) ---------- */
  const startReveals = () => {
    const targets = document.querySelectorAll('[data-split], [data-reveal]');
    if (!('IntersectionObserver' in window)) {
      targets.forEach((el) => el.classList.add('is-in'));
      return;
    }
    // a fully clipped element never counts as intersecting, so "draw" reveals follow their parent
    const proxied = new Map();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        (proxied.get(entry.target) || [entry.target]).forEach((el) => el.classList.add('is-in'));
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    targets.forEach((el) => {
      if (el.dataset.reveal !== 'draw') return io.observe(el);
      const parent = el.parentElement;
      proxied.set(parent, [...(proxied.get(parent) || []), el]);
      io.observe(parent);
    });
  };

  /* ---------- Loader: 1 → 100% ---------- */
  const loaderNum = document.getElementById('loader-num');
  const DURATION = 1900;
  let finished = false;
  let pageLoaded = document.readyState === 'complete';
  window.addEventListener('load', () => { pageLoaded = true; });

  const finish = () => {
    if (finished) return;
    finished = true;
    if (loaderNum) loaderNum.textContent = '100';
    setTimeout(() => {
      html.classList.remove('is-loading');
      html.classList.add('is-loaded');
      const target = startHash && startHash !== '#home' && document.querySelector(startHash);
      if (target) target.scrollIntoView();
      else window.scrollTo(0, 0);
      startReveals();
    }, 300);
  };

  const startedAt = performance.now();
  const tick = (now) => {
    if (finished) return;
    const t = clamp((now - startedAt) / DURATION, 0, 1);
    const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    // hold at 92% until the page assets are really in
    const value = Math.round(1 + 99 * eased);
    const shown = pageLoaded ? value : Math.min(value, 92);
    loaderNum.textContent = shown;
    if (shown >= 100) finish();
    else requestAnimationFrame(tick);
  };
  if (loaderNum) requestAnimationFrame(tick);
  setTimeout(finish, loaderNum ? 6000 : 0);

  /* ---------- Header ---------- */
  const header = document.getElementById('header');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // logo replays the whole site from the loading screen
  document.querySelectorAll('[data-logo]').forEach((logo) => {
    logo.addEventListener('click', (e) => {
      e.preventDefault();
      if (isHome) {
        history.replaceState(null, '', location.pathname);
        window.scrollTo(0, 0);
        location.reload();
      } else {
        location.href = logo.getAttribute('href');
      }
    });
  });

  /* ---------- Menu ---------- */
  const menu = document.getElementById('menu');
  const openBtn = document.querySelector('[data-menu-open]');
  const closeBtn = document.querySelector('[data-menu-close]');
  menu.querySelectorAll('.menu__item').forEach((item, i) => item.style.setProperty('--i', i));

  const setMenu = (open) => {
    html.classList.toggle('menu-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    openBtn.setAttribute('aria-expanded', String(open));
  };
  openBtn.addEventListener('click', () => setMenu(true));
  closeBtn.addEventListener('click', () => setMenu(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  // in-page anchors: close the menu and scroll smoothly instead of reloading
  document.querySelectorAll('a[href*="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const url = new URL(link.href, location.href);
      if (url.pathname !== location.pathname || !url.hash) return;
      const target = document.querySelector(url.hash);
      if (!target) return;
      e.preventDefault();
      setMenu(false);
      const top = url.hash === '#home' ? 0 : target.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
  menu.querySelectorAll('a.menu__link:not([href*="#"])').forEach((link) => {
    link.addEventListener('click', () => setMenu(false));
  });

  /* ---------- Case page: accordion + screenshot zoom ---------- */
  document.querySelectorAll('.acc__head').forEach((head) => {
    head.addEventListener('click', () => {
      const open = head.parentElement.classList.toggle('is-open');
      head.setAttribute('aria-expanded', String(open));
    });
  });

  const lightbox = document.getElementById('lightbox');
  if (lightbox) {
    const big = lightbox.querySelector('img');
    const setLightbox = (open) => {
      lightbox.classList.toggle('is-open', open);
      lightbox.setAttribute('aria-hidden', String(!open));
    };
    document.addEventListener('click', (e) => {
      const img = e.target.closest('img[data-zoom]');
      if (img) {
        big.src = img.currentSrc || img.src;
        big.alt = img.alt;
        lightbox.scrollTop = 0;
        setLightbox(true);
      } else if (e.target.closest('#lightbox')) {
        setLightbox(false);
      }
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setLightbox(false); });
  }

  /* ---------- Cursor + head parallax ---------- */
  const cursor = document.getElementById('cursor');
  const head = document.getElementById('head');
  const pointer = { x: innerWidth / 2, y: innerHeight / 2, moved: false };
  const cur = { x: pointer.x, y: pointer.y };
  const look = { x: 0, y: 0, tx: 0, ty: 0, ex: 0, ey: 0 };

  if (finePointer && cursor) {
    html.classList.add('has-cursor');
    const interactive = 'a[href], button, .card__btn, .menu__link, img[data-zoom]';
    document.addEventListener('pointerover', (e) => {
      cursor.classList.toggle('is-hover', !!e.target.closest(interactive));
    });
    document.addEventListener('pointerdown', () => cursor.classList.add('is-down'));
    document.addEventListener('pointerup', () => cursor.classList.remove('is-down'));
    document.addEventListener('pointerleave', () => cursor.classList.remove('is-visible'));
  }

  window.addEventListener('pointermove', (e) => {
    pointer.x = e.clientX;
    pointer.y = e.clientY;
    if (!pointer.moved) {
      pointer.moved = true;
      cur.x = pointer.x;
      cur.y = pointer.y;
    }
    if (cursor) cursor.classList.add('is-visible');
    if (head) {
      const r = head.getBoundingClientRect();
      look.tx = clamp((pointer.x - (r.left + r.width / 2)) / (innerWidth / 2), -1, 1);
      look.ty = clamp((pointer.y - (r.top + r.height * 0.53)) / (innerHeight / 2), -1, 1);
    }
  }, { passive: true });

  const frame = () => {
    if (finePointer && cursor) {
      cur.x += (pointer.x - cur.x) * 0.22;
      cur.y += (pointer.y - cur.y) * 0.22;
      cursor.style.transform = `translate3d(${cur.x}px, ${cur.y}px, 0)`;
    }
    if (head) {
      look.x += (look.tx - look.x) * 0.06;
      look.y += (look.ty - look.y) * 0.06;
      // eyes react quicker than the head turns
      look.ex += (look.tx - look.ex) * 0.16;
      look.ey += (look.ty - look.ey) * 0.16;
      head.style.setProperty('--mx', look.x.toFixed(4));
      head.style.setProperty('--my', look.y.toFixed(4));
      head.style.setProperty('--ex', look.ex.toFixed(4));
      head.style.setProperty('--ey', look.ey.toFixed(4));
    }
    requestAnimationFrame(frame);
  };
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) requestAnimationFrame(frame);
})();
