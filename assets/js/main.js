// TechWater — interactive helpers
(function () {
  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const list = document.querySelector('.nav ul.primary');
  if (toggle && list) {
    toggle.addEventListener('click', () => {
      list.classList.toggle('open');
      toggle.setAttribute('aria-expanded', list.classList.contains('open'));
    });
  }

  // Highlight active nav item
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(a => {
    const href = (a.getAttribute('href') || '').split('/').pop();
    if (href === path) a.classList.add('active');
  });

  // Countdown to next "Last Friday of the month"
  function nextLastFriday(from = new Date()) {
    const d = new Date(from.getFullYear(), from.getMonth() + 1, 0); // last day of current month
    while (d.getDay() !== 5) d.setDate(d.getDate() - 1);
    d.setHours(9, 0, 0, 0);
    if (d <= from) {
      const n = new Date(from.getFullYear(), from.getMonth() + 2, 0);
      while (n.getDay() !== 5) n.setDate(n.getDate() - 1);
      n.setHours(9, 0, 0, 0);
      return n;
    }
    return d;
  }

  const cd = document.querySelector('[data-countdown]');
  if (cd) {
    const target = nextLastFriday();
    const dateLabel = document.querySelector('[data-cd-date]');
    if (dateLabel) {
      dateLabel.textContent = target.toLocaleDateString('fr-FR', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
      });
    }
    const tick = () => {
      const diff = target - new Date();
      if (diff <= 0) { cd.innerHTML = '<div class="unit"><div class="num">EN COURS</div><div class="lab">White Friday</div></div>'; return; }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff / 3600000) % 24);
      const m = Math.floor((diff / 60000) % 60);
      const s = Math.floor((diff / 1000) % 60);
      cd.innerHTML = `
        <div class="unit"><div class="num">${d}</div><div class="lab">Jours</div></div>
        <div class="unit"><div class="num">${String(h).padStart(2,'0')}</div><div class="lab">Heures</div></div>
        <div class="unit"><div class="num">${String(m).padStart(2,'0')}</div><div class="lab">Minutes</div></div>
        <div class="unit"><div class="num">${String(s).padStart(2,'0')}</div><div class="lab">Secondes</div></div>
      `;
    };
    tick();
    setInterval(tick, 1000);
  }

  // Contact form mock submission
  const form = document.querySelector('form[data-contact]');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Merci ! Votre demande a bien été envoyée. Notre équipe vous recontactera sous 24h.';
        status.style.color = '#14b8a6';
      }
      form.reset();
    });
  }
})();
