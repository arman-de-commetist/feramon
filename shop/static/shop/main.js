// falling petals
const petals = document.getElementById('petals');
for (let i = 0; petals && i < 18; i++) {
  const p = document.createElement('i');
  p.className = 'petal';
  p.style.left = Math.random() * 100 + '%';
  p.style.animationDuration = 9 + Math.random() * 10 + 's';
  p.style.animationDelay = -Math.random() * 15 + 's';
  const s = .6 + Math.random() * .9;
  p.style.width = 22 * s + 'px'; p.style.height = 18 * s + 'px';
  petals.appendChild(p);
}

// lock the page behind the phone menu / managers sheet (iOS ignores overflow:hidden on <body>)
let lockedY = 0, locks = 0;
window.lockScroll = on => {
  if (on) {
    if (locks++ === 0) {
      lockedY = window.scrollY;
      document.body.style.top = -lockedY + 'px';
      document.body.classList.add('scroll-locked');
    }
  } else if (locks > 0 && --locks === 0) {
    document.body.classList.remove('scroll-locked');
    document.body.style.top = '';
    const html = document.documentElement, prev = html.style.scrollBehavior;
    html.style.scrollBehavior = 'auto';  // jump back instantly, no smooth scroll from the top
    window.scrollTo(0, lockedY);
    html.style.scrollBehavior = prev;
  }
};

// mobile menu
const setMenu = open => {
  if (open === document.body.classList.contains('menu-open')) return;
  document.body.classList.toggle('menu-open', open);
  window.lockScroll(open);
};
document.getElementById('burger')?.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
document.querySelectorAll('#menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
matchMedia('(min-width: 981px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

// reveal on scroll
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: .15 });
document.querySelectorAll('.reveal').forEach((el, i) => {
  el.style.transitionDelay = (i % 4) * 0.08 + 's';
  io.observe(el);
});

// order picker -> hidden variant field, animated price and poster
const price = document.getElementById('price');
const variantInput = document.getElementById('id_variant');
const qtyInput = document.getElementById('id_quantity');
const buyImg = document.getElementById('buyImg');
const buyVisual = document.getElementById('buyVisual');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fmt = n => n.toLocaleString('ru-RU').replace(/\u00a0/g, ' ') + ' ₸';
const replay = (el, cls) => { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); };

let shownPrice = 0;
const updatePrice = (animate = false) => {
  const active = document.querySelector('.volumes:not([hidden]) .vol-btn.active');
  if (!active || !price) return;
  const target = Number(active.dataset.price) * Math.max(1, Number(qtyInput?.value) || 1);
  const from = shownPrice;
  shownPrice = target;
  if (!animate || reduceMotion || from === target) { price.textContent = fmt(target); return; }
  replay(price, 'bump');
  const t0 = performance.now(), dur = 500;
  const step = now => {
    const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
    price.textContent = fmt(Math.round((from + (target - from) * e) / 10) * 10);
    if (k < 1 && shownPrice === target) requestAnimationFrame(step);
    else if (shownPrice === target) price.textContent = fmt(target);
  };
  requestAnimationFrame(step);
};

const swapPoster = src => {
  if (!buyImg || !src || buyImg.getAttribute('src') === src) return;
  if (reduceMotion || !buyImg.animate) { buyImg.src = src; return; }
  buyImg.getAnimations().forEach(a => a.cancel());
  buyImg.animate(
    [{ transform: 'none', opacity: 1, filter: 'blur(0)' },
     { transform: 'perspective(800px) rotateY(80deg) scale(.85)', opacity: 0, filter: 'blur(6px)' }],
    { duration: 260, easing: 'ease-in', fill: 'forwards' }
  ).onfinish = () => {
    buyImg.src = src;
    const show = () => buyImg.animate(
      [{ transform: 'perspective(800px) rotateY(-80deg) scale(.85)', opacity: 0, filter: 'blur(6px)' },
       { transform: 'perspective(800px) rotateY(8deg) scale(1.04)', opacity: 1, filter: 'blur(0)', offset: .7 },
       { transform: 'none', opacity: 1, filter: 'blur(0)' }],
      { duration: 520, easing: 'cubic-bezier(.2,.8,.3,1)', fill: 'forwards' }
    );
    buyImg.decode ? buyImg.decode().then(show, show) : show();
  };
};

const burst = emoji => {
  if (!buyVisual || reduceMotion || !document.body.animate) return;
  const w = buyVisual.clientWidth, h = buyVisual.clientHeight;
  const items = [emoji, '✨', '🌸', emoji, '✨', '💖', emoji, '✨', '🌸', emoji];
  items.forEach((e, i) => {
    const s = document.createElement('span');
    s.className = 'burst';
    s.textContent = e;
    buyVisual.appendChild(s);
    const a = (i / items.length) * Math.PI * 2 + Math.random() * .5;
    const r = 120 + Math.random() * 110;
    const x = w / 2, y = h / 2;
    s.animate(
      [{ transform: `translate(${x}px,${y}px) scale(.2)`, opacity: 0 },
       { transform: `translate(${x + Math.cos(a) * r * .6}px,${y + Math.sin(a) * r * .6}px) scale(1.2)`, opacity: 1, offset: .35 },
       { transform: `translate(${x + Math.cos(a) * r}px,${y + Math.sin(a) * r + 40}px) scale(.6) rotate(${Math.random() * 180 - 90}deg)`, opacity: 0 }],
      { duration: 1100 + Math.random() * 400, easing: 'cubic-bezier(.2,.7,.3,1)' }
    ).onfinish = () => s.remove();
  });
};

const ripple = (b, ev) => {
  if (reduceMotion) return;
  const r = b.getBoundingClientRect(), size = Math.max(r.width, r.height) * 2;
  const x = ev && ev.clientX ? ev.clientX - r.left : r.width / 2;
  const y = ev && ev.clientY ? ev.clientY - r.top : r.height / 2;
  const span = document.createElement('span');
  span.className = 'ripple';
  Object.assign(span.style, { width: size + 'px', height: size + 'px', left: x - size / 2 + 'px', top: y - size / 2 + 'px' });
  b.appendChild(span);
  span.addEventListener('animationend', () => span.remove());
};

const giftBox = document.getElementById('giftBox');          // 100 ml: Dyson
const giftPerfumes = document.getElementById('giftPerfumes'); // 30 / 50 ml: French perfumes
const priceOld = document.getElementById('priceOld');
const priceOff = document.getElementById('priceOff');
let giftNeed = 0;

const giftChecks = () => [...document.querySelectorAll('#giftPerfumes input[type=checkbox]')];
const updateGiftCount = () => {
  const got = giftChecks().filter(c => c.checked).length;
  const el = document.getElementById('giftGot');
  if (el) el.textContent = got;
  giftPerfumes?.classList.toggle('full', giftNeed > 0 && got >= giftNeed);
};
// never more perfumes than the volume allows: the oldest choice gives way to the newest
let checkOrder = giftChecks().filter(c => c.checked);
giftChecks().forEach(c => c.addEventListener('change', () => {
  checkOrder = checkOrder.filter(x => x !== c);
  if (c.checked) checkOrder.push(c);
  while (checkOrder.length > giftNeed && giftNeed > 0) checkOrder.shift().checked = false;
  updateGiftCount();
}));

const showGift = vb => {
  const type = vb ? vb.dataset.giftType : '';
  if (giftBox) {
    const wasHidden = giftBox.hidden;
    giftBox.hidden = type !== 'dyson';
    if (!giftBox.hidden && wasHidden) replay(giftBox, 'gift-in');
  }
  if (giftPerfumes) {
    const wasHidden = giftPerfumes.hidden;
    giftPerfumes.hidden = type !== 'perfume';
    giftNeed = type === 'perfume' ? Number(vb.dataset.giftCount) || 1 : 0;
    document.getElementById('giftNeed').textContent = giftNeed;
    document.getElementById('giftPerfumeTitle').textContent = vb ? vb.dataset.gift : '';
    while (checkOrder.length > giftNeed) checkOrder.shift().checked = false;
    if (!giftPerfumes.hidden && wasHidden) replay(giftPerfumes, 'gift-in');
    updateGiftCount();
  }
  if (priceOld && vb) {
    const old = Number(vb.dataset.old) || 0, now = Number(vb.dataset.price);
    priceOld.textContent = old > now ? fmt(old) : '';
    if (priceOff) {
      priceOff.hidden = !(old > now);
      priceOff.textContent = old > now ? '−' + Math.floor((1 - now / old) * 100) + '%' : '';
    }
  }
};
showGift(document.querySelector('.volumes:not([hidden]) .vol-btn.active'));

// step 2: volume
const pickVolume = (vb, ev, animate = true) => {
  if (ev) ripple(vb, ev);
  vb.parentElement.querySelectorAll('.vol-btn').forEach(x => x.classList.remove('active'));
  vb.classList.add('active');
  if (animate) replay(vb, 'pop');
  if (variantInput) variantInput.value = vb.dataset.id;
  if (animate && vb.dataset.giftType && buyVisual) burst(vb.dataset.giftType === 'dyson' ? '💇‍♀️' : '🎁');
  showGift(vb);
  if (animate) updatePrice(true); // pickAroma animates the price itself
};

// step 1: perfume — keeps the chosen volume (e.g. 100 мл stays 100 мл)
const pickAroma = (b, ev) => {
  if (ev) ripple(b, ev);
  if (b.classList.contains('active')) return;
  const prevLabel = document.querySelector('.volumes:not([hidden]) .vol-btn.active')?.dataset.label;
  document.querySelectorAll('#aroma button').forEach(x => x.classList.remove('active'));
  b.classList.add('active');
  replay(b, 'pop');
  if (buyVisual && b.dataset.theme) {
    buyVisual.className = buyVisual.className.replace(/theme-\S+/, 'theme-' + b.dataset.theme);
    replay(buyVisual, 'flash');
  }
  swapPoster(b.dataset.img);
  burst(b.dataset.emoji || '🌸');
  let group = null;
  document.querySelectorAll('.volumes').forEach(g => {
    const mine = g.dataset.product === b.dataset.product;
    g.hidden = !mine;
    if (mine) group = g;
  });
  if (group) {
    replay(group, 'gift-in');
    const vb = [...group.querySelectorAll('.vol-btn')].find(x => x.dataset.label === prevLabel) || group.querySelector('.vol-btn');
    if (vb) pickVolume(vb, null, false);
    updatePrice(true);
  }
};
document.querySelectorAll('#aroma button').forEach(b => b.addEventListener('click', ev => pickAroma(b, ev)));
document.querySelectorAll('.vol-btn').forEach(b => b.addEventListener('click', ev => pickVolume(b, ev)));

// "Заказать" on a perfume section preselects that perfume + volume in the order form
const selectVariant = id => {
  const vb = document.querySelector(`.vol-btn[data-id="${id}"]`);
  if (!vb) return;
  const ab = document.querySelector(`#aroma button[data-product="${vb.parentElement.dataset.product}"]`);
  if (ab) pickAroma(ab);
  pickVolume(vb);
};
document.querySelectorAll('[data-pick]').forEach(a => a.addEventListener('click', () => {
  setTimeout(() => selectVariant(a.dataset.pick), 450); // after the smooth scroll lands
}));
qtyInput?.addEventListener('input', () => updatePrice(true));
updatePrice();


// gifts page: filter by women / men / unisex
document.querySelectorAll('#giftFilter button').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('#giftFilter button').forEach(x => x.classList.toggle('on', x === b));
  document.querySelectorAll('.gift-big').forEach(card => {
    card.hidden = b.dataset.g !== 'all' && card.dataset.g !== b.dataset.g;
  });
}));

// quiz: each answer votes for a theme (rose = Нежный, ice = Холодный, caramel = Сладкий)
const quiz = document.getElementById('quiz');
if (quiz) {
  const steps = [...quiz.querySelectorAll('.q-step')];
  const bar = document.getElementById('quizBar');
  const result = document.getElementById('quizResult');
  let votes = {}, at = 0;
  const show = i => {
    steps.forEach((s, k) => s.classList.toggle('on', k === i));
    if (bar) bar.style.width = (i / steps.length) * 100 + '%';
  };
  steps.forEach((step, i) => step.querySelectorAll('[data-vote]').forEach(btn => btn.addEventListener('click', () => {
    votes[btn.dataset.vote] = (votes[btn.dataset.vote] || 0) + 1;
    at = i + 1;
    if (at < steps.length) { show(at); return; }
    steps.forEach(s => s.classList.remove('on'));
    if (bar) bar.style.width = '100%';
    // ties go to the answer given last
    const last = btn.dataset.vote;
    const best = Object.keys(votes).sort((a, b) => votes[b] - votes[a] || (b === last) - (a === last))[0];
    result.hidden = false;
    let shown = false;
    result.querySelectorAll('.qr-item').forEach(it => {
      it.hidden = it.dataset.theme !== best || shown;
      if (!it.hidden) shown = true;
    });
    if (!shown) result.querySelector('.qr-item')?.removeAttribute('hidden');
    replay(result, 'gift-in');
  })));
  document.getElementById('quizRestart')?.addEventListener('click', () => {
    votes = {}; at = 0; result.hidden = true; show(0);
  });
  show(0);
}

// gallery lightbox
const lightbox = document.getElementById('lightbox');
if (lightbox) {
  const img = lightbox.querySelector('img');
  document.querySelectorAll('.m-item').forEach(f => f.addEventListener('click', () => {
    img.src = f.dataset.full; img.alt = f.querySelector('img')?.alt || '';
    lightbox.hidden = false;
  }));
  lightbox.addEventListener('click', e => { if (e.target !== img) lightbox.hidden = true; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') lightbox.hidden = true; });
}

// review form: highlight stars up to the chosen rating
const rates = [...document.querySelectorAll('.rate input')];
const paintStars = () => {
  const v = Number(rates.find(r => r.checked)?.value || 0);
  rates.forEach(r => r.parentElement.classList.toggle('lit', Number(r.value) <= v));
};
rates.forEach(r => r.addEventListener('change', paintStars));
paintStars();


// managers sheet (bottom tab «Связь»)
const sheet = document.getElementById('mgrSheet');
if (sheet) {
  const open = () => {
    if (!sheet.hidden) return;
    sheet.hidden = false; void sheet.offsetWidth; sheet.classList.add('on'); window.lockScroll(true);  // reflow first so the slide-in animates
  };
  const close = () => {
    if (sheet.hidden || !sheet.classList.contains('on')) return;
    sheet.classList.remove('on'); window.lockScroll(false); setTimeout(() => { sheet.hidden = true; }, 300);
  };
  document.getElementById('sheetOpen')?.addEventListener('click', open);
  document.getElementById('sheetClose')?.addEventListener('click', close);
  sheet.addEventListener('click', e => { if (e.target === sheet) close(); });
  sheet.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setTimeout(close, 200)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !sheet.hidden) close(); });
}


// «Задать вопрос менеджеру»: the ready WhatsApp text follows everything chosen in the form
const cfgWa = document.getElementById('cfgWa');
if (cfgWa) {
  const updateWa = () => {
    const vb = document.querySelector('.volumes:not([hidden]) .vol-btn.active');
    if (!vb) return;
    const q = new URLSearchParams({ v: vb.dataset.id });
    if (vb.dataset.giftType === 'dyson') {
      const c = document.querySelector('#giftBox input[name=gift_color]:checked');
      const e = document.querySelector('#giftBox input[name=engraving]');
      if (c) q.set('color', c.value);
      if (e && e.value.trim()) q.set('e', e.value.trim());
    } else if (vb.dataset.giftType === 'perfume') {
      document.querySelectorAll('#giftPerfumes input[type=checkbox]:checked').forEach(g => q.append('g', g.value));
    }
    cfgWa.href = cfgWa.dataset.base.split('?')[0] + '?' + q.toString();
  };
  document.getElementById('cartForm')?.addEventListener('change', updateWa);
  document.getElementById('cartForm')?.addEventListener('input', updateWa);
  document.querySelectorAll('.vol-btn, #aroma button').forEach(b => b.addEventListener('click', () => setTimeout(updateWa, 0)));
  updateWa();
}


// WhatsApp bubble: never sit on top of a button — tuck to the edge while something clickable is underneath
const waFloat = document.querySelector('.float-stack');
if (waFloat) {
  let ticking = false;
  const clickable = 'a, button, input, select, textarea, label, [role="button"]';
  const check = () => {
    ticking = false;
    if (getComputedStyle(waFloat).display === 'none') return;
    if (waFloat.classList.contains('open')) return;  // menu is open — keep it in place
    waFloat.classList.remove('tucked');           // measure the bubble in its normal place
    const r = waFloat.getBoundingClientRect();
    waFloat.style.pointerEvents = 'none';
    let hit = false;
    for (const [x, y] of [[r.left + r.width / 2, r.top + r.height / 2], [r.left + 8, r.top + 8], [r.left + 8, r.bottom - 8],
                          [r.right - 8, r.top + 8], [r.right - 8, r.bottom - 8]]) {
      const el = document.elementFromPoint(x, y);
      if (el && !waFloat.contains(el) && el.closest(clickable) && !el.closest('.tabbar, nav, .m-cta')) { hit = true; break; }
    }
    waFloat.style.pointerEvents = '';
    waFloat.classList.toggle('tucked', hit);
  };
  const schedule = () => { if (!ticking) { ticking = true; requestAnimationFrame(check); } };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule);
  addEventListener('load', schedule);
  setTimeout(schedule, 300);
  setInterval(schedule, 1000);  // content also moves without scrolling (reveal animations, opened panels)
}


// reviews: star text, «Ответить» opens the answer form, emoji picker inserts at the cursor
const rateText = document.getElementById('rateText');
rates.forEach(r => r.addEventListener('change', () => { if (rateText) rateText.textContent = r.value; }));

document.querySelectorAll('.reply-btn').forEach(btn => btn.addEventListener('click', () => {
  const form = document.getElementById('reply-' + btn.dataset.root);
  if (!form) return;
  const toSelf = btn.dataset.reply === btn.dataset.root;
  form.querySelector('[name=parent]').value = btn.dataset.reply;
  const text = form.querySelector('textarea');
  if (!toSelf) {  // answering an answer: start with the person's name
    const who = btn.closest('.reply-body')?.querySelector('b')?.textContent.trim();
    if (who && !text.value.startsWith('@' + who)) text.value = '@' + who + ', ' + text.value.replace(/^@[^,]*,\s*/, '');
  }
  form.hidden = toSelf ? !form.hidden : false;
  if (!form.hidden) {
    const name = form.querySelector('[name=name]');
    (name.value ? text : name).focus({ preventScroll: true });
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}));
// the server adds «@name» itself when the answer goes under an answer — avoid writing it twice
document.querySelectorAll('.reply-form').forEach(f => f.addEventListener('submit', () => {
  const parent = f.querySelector('[name=parent]'), text = f.querySelector('textarea');
  if (parent.value !== f.id.replace('reply-', '')) text.value = text.value.replace(/^@[^,]*,\s*/, '');
}));

document.querySelectorAll('.emoji-wrap').forEach(wrap => {
  const field = wrap.querySelector('textarea'), toggle = wrap.querySelector('.emoji-toggle'), panel = wrap.querySelector('.emoji-panel');
  if (!field || !toggle || !panel) return;
  toggle.addEventListener('click', () => {
    panel.hidden = !panel.hidden;
    toggle.setAttribute('aria-expanded', String(!panel.hidden));
  });
  panel.addEventListener('click', e => {
    const b = e.target.closest('.emoji');
    if (!b) return;
    const start = field.selectionStart ?? field.value.length, end = field.selectionEnd ?? field.value.length;
    field.value = field.value.slice(0, start) + b.textContent + field.value.slice(end);
    const pos = start + b.textContent.length;
    field.setSelectionRange(pos, pos);
  });
});
document.addEventListener('click', e => {
  document.querySelectorAll('.emoji-panel:not([hidden])').forEach(p => {
    if (!p.parentElement.contains(e.target)) { p.hidden = true; p.parentElement.querySelector('.emoji-toggle')?.setAttribute('aria-expanded', 'false'); }
  });
});


// Dyson colours: the magnifier opens the photo big; «Выбрать этот цвет» picks it
const dz = document.getElementById('dysonZoom');
if (dz) {
  document.body.appendChild(dz);  // out of the configurator so position:fixed covers the whole screen
  const dzImg = dz.querySelector('img'), dzCap = dz.querySelector('figcaption');
  let dzValue = '';
  const dzClose = () => { if (dz.hidden) return; dz.hidden = true; window.lockScroll(false); };
  document.querySelectorAll('.sw-zoom').forEach(b => b.addEventListener('click', e => {
    e.preventDefault(); e.stopPropagation();  // only zoom — don't change the chosen colour
    dzValue = b.dataset.value;
    dzImg.src = b.dataset.full;
    dzCap.textContent = dzImg.alt = b.closest('.swatch').querySelector('span').textContent;
    dz.hidden = false; window.lockScroll(true);
  }));
  dz.querySelector('.dz-pick').addEventListener('click', () => {
    const input = document.querySelector(`#giftBox input[name=gift_color][value="${dzValue}"]`);
    if (input) { input.checked = true; input.dispatchEvent(new Event('change', { bubbles: true })); }
    dzClose();
  });
  dz.querySelector('.dz-close').addEventListener('click', dzClose);
  dz.addEventListener('click', e => { if (e.target === dz) dzClose(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') dzClose(); });
}


// phones: the round button opens WhatsApp / Instagram / TikTok
const fsStack = document.querySelector('.float-stack');
const fsToggle = fsStack?.querySelector('.fs-toggle');
if (fsToggle) {
  const setOpen = on => {
    fsStack.classList.toggle('open', on);
    fsToggle.setAttribute('aria-expanded', String(on));
    if (on) fsStack.classList.remove('tucked');
  };
  fsToggle.addEventListener('click', e => { e.stopPropagation(); setOpen(!fsStack.classList.contains('open')); });
  document.addEventListener('click', e => { if (!fsStack.contains(e.target)) setOpen(false); });
  fsStack.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setTimeout(() => setOpen(false), 300)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
}


// certificates: open a document full size; tap the document to zoom in/out
const certBox = document.getElementById('certBox');
if (certBox) {
  document.body.appendChild(certBox);
  const img = certBox.querySelector('img'), title = certBox.querySelector('.cb-title');
  const close = () => { if (certBox.hidden) return; certBox.hidden = true; certBox.classList.remove('zoomed'); window.lockScroll(false); };
  document.querySelectorAll('.cert-doc').forEach(b => b.addEventListener('click', () => {
    img.src = b.dataset.full; img.alt = title.textContent = b.dataset.title;
    certBox.classList.remove('zoomed'); certBox.hidden = false; window.lockScroll(true);
    certBox.querySelector('.cb-scroll').scrollTo(0, 0);
  }));
  img.addEventListener('click', () => certBox.classList.toggle('zoomed'));
  certBox.querySelector('.cb-close').addEventListener('click', close);
  certBox.addEventListener('click', e => { if (e.target === certBox || e.target.classList.contains('cb-scroll')) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
}
