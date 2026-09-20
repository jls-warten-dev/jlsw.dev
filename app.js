/* jlsw.dev — vanilla JS. i18n + theme + terminal typing. No dependencies. */
(() => {
  'use strict';

  const $ = (sel, ctx = document) => ctx.querySelector(sel);

  /* ── i18n dictionary ─────────────────────────── */
  const I18N = {
    es: {
      nav: { proyectos: 'Proyectos', stack: 'Stack', sobre: 'Sobre mí', contacto: 'Contacto' },
      heroSub: 'Programador <strong>Python / Frappe / ERPNext</strong>. Construyo apps web, automatizaciones, Business Intelligence (Bold BI) y la infraestructura que las sostiene — del código al despliegue.',
      heroH1: 'José Luis Sánchez Warten — Programador Python y Frappe',
      ctaProjects: 'Ver proyectos',
      ctaCv: 'Descargar CV',
      terminal: [
        { p: '$', c: 'whoami' },
        { o: 'jose — python & frappe developer' },
        { p: '$', c: 'ls proyectos/' },
        { o: 'todomal.es  tfv  dinodieta  homelab', hl: true }
      ],
      badges: { prod: 'en producción', alt: '24/7' },
      slotTitle: 'tu-proyecto',
      slotText: 'Espacio reservado. Los detalles de cada proyecto se ampliarán con estudios de caso completos.',
      footerNote: 'hecha a mano',
      kofiHint: '— invítame a uno si te sirvió de algo',
      skip: 'Saltar al contenido',
      'p.dino': 'Generador de dietas personalizadas sobre ERPNext: motor de reglas nutricionales, planificador semanal y seguimiento de síntomas para consulta profesional.',
      'p.todomal': 'Blog con backend propio en Frappe — sin WordPress: DocTypes a medida, API REST y cero plugins de terceros. Gestionado por una IA sarcástica y brutalista.',
      'p.tfv': 'Web de una fotógrafa y veterinaria de Monforte de Lemos: portfolio, blog, exposiciones y área de clientes — SPA sobre Frappe con Vue, instalable como PWA.',
      'p.homelab': 'Dos servidores con Docker: backups automatizados, media server, automatización de flujos con n8n y un asistente de IA autoalojado. Todo documentado.',
      'p.alixeira': 'Conversor de imágenes por lotes a WebP/JPEG que ajusta cada archivo a un tamaño exacto en KB. Sin conexión, con marca de agua, redimensionado, ZIPs e informes.',
      'foot.visit': 'Visitar sitio',
      'foot.download': 'Descargar',
      'foot.repo': 'Repositorio',
      'foot.story': 'La historia',
      shots: { open: 'Ver captura', close: 'Cerrar', todomalHome: 'todomal.es — portada', todomalPost: 'todomal.es — artículo con comentarios', tfvHome: 'tamarafotoveterinaria.es — portada con portfolio', tfvPortfolio: 'tamarafotoveterinaria.es — galería del portfolio', dinoCalendar: 'DinoDieta — planificador semanal en modo oscuro', dinoRecipes: 'DinoDieta — buscador de recetas en modo claro', alixeiraRun: 'Alixeira — proceso completado con estadísticas', alixeiraConfig: 'Alixeira — opciones de configuración' },
      st: { lang: 'Lenguajes', framework: 'Framework', data: 'Datos', infra: 'Infraestructura', backups: 'Backups automatizados', ai: 'IA' },
      about: {
        p1: 'Llevo 4 años programando en producción con Python y el framework Frappe/ERPNext: desde motores de negocio hasta paneles de control con Vue. Durante ese tiempo he administrado también Bold BI (la solución de Business Intelligence de Syncfusion): dashboards corporativos, conexiones a datos y automatización de informes. Antes de eso, casi una década resolviendo problemas de clientes cara a cara — algo que se nota en cómo escribo software: para personas, no solo para máquinas. Cuento con la certificación oficial de Frappe Framework.',
        p2: 'Mantengo mi propio homelab con dos servidores, lo que me ha obligado a aprender Docker, redes, backups y monitorización de forma práctica. Aprendo sistemáticamente: ahora profundizando en Django/DRF y cloud (AWS).',
      p3: 'La IA forma parte de mi día a día: programo asistido por OpenCode y mantengo un agente personal sobre Hermes que ejecuta despliegues, monitoriza servicios y administra mis servidores; los conecto entre sí mediante MCP. Sé cuándo la IA acelera el trabajo — y cuándo toca apagarla y pensar.'
      },
      foot: { static: 'build estática', analytics: 'analítica propia sin cookies' }
    },
    en: {
      nav: { proyectos: 'Projects', stack: 'Stack', sobre: 'About me', contacto: 'Contact' },
      heroSub: '<strong>Python / Frappe / ERPNext</strong> developer. I build web apps, automations, Business Intelligence (Bold BI) and the infrastructure behind them — from code to deployment.',
      heroH1: 'José Luis Sánchez Warten — Python & Frappe Developer',
      ctaProjects: 'View projects',
      ctaCv: 'Download CV',
      terminal: [
        { p: '$', c: 'whoami' },
        { o: 'jose — python & frappe developer' },
        { p: '$', c: 'ls projects/' },
        { o: 'todomal.es  tfv  dinodieta  homelab', hl: true }
      ],
      badges: { prod: 'in production', alt: '24/7' },
      footerNote: 'handcrafted',
      kofiHint: '— buy me one if this was useful',
      skip: 'Skip to content',
      'p.dino': 'Personalized diet generator built on ERPNext: nutritional rules engine, weekly planner and symptom tracking for professional practice.',
      'p.todomal': 'Blog running on its own Frappe backend — no WordPress: custom DocTypes, REST API and zero third-party plugins. Run by a sarcastic, brutalist AI.',
      'p.tfv': 'Website for a photographer & veterinarian: portfolio, blog, exhibitions and a client area — a Frappe + Vue SPA, installable as a PWA.',
      'p.homelab': 'Two Docker-powered servers: automated backups, media server, n8n workflow automation and a self-hosted AI assistant. Fully documented.',
      'p.alixeira': 'Batch image converter to WebP/JPEG that hits an exact target size in KB. Offline, with watermark, resizing, ZIPs and reports.',
      'foot.visit': 'Visit site',
      'foot.download': 'Download',
      'foot.repo': 'Repository',
      'foot.story': 'The story',
      shots: { open: 'View screenshot', close: 'Close', todomalHome: 'todomal.es — homepage', todomalPost: 'todomal.es — article with comments', tfvHome: 'tamarafotoveterinaria.es — homepage with portfolio', tfvPortfolio: 'tamarafotoveterinaria.es — portfolio gallery', dinoCalendar: 'DinoDieta — weekly planner in dark mode', dinoRecipes: 'DinoDieta — recipe search in light mode', alixeiraRun: 'Alixeira — completed run with stats', alixeiraConfig: 'Alixeira — configuration options' },
      st: { lang: 'Languages', framework: 'Framework', data: 'Data', infra: 'Infrastructure', backups: 'Automated backups', ai: 'AI' },
      about: {
        p1: 'I have 4 years of production experience programming with Python and the Frappe/ERPNext framework: from business logic engines to Vue dashboards. During that time I have also administered Bold BI (Syncfusion\u2019s Business Intelligence suite): corporate dashboards, data connections and report automation. Before that, nearly a decade solving customer problems face to face — something that shows in how I write software: for people, not just machines. I hold the official Frappe Framework certification.',
        p2: 'I run my own homelab with two servers, which has forced me to learn Docker, networking, backups and monitoring hands-on. I learn systematically: currently deepening Django/DRF and cloud (AWS).',
      p3: 'AI is part of my daily workflow: I code assisted by OpenCode and run a personal agent built on Hermes that handles deployments, monitors services and administers my servers, all wired together via MCP. I know when AI speeds things up — and when it\'s time to switch it off and think.'
      },
      foot: { static: 'static build', analytics: 'own cookie-free analytics' }
    }
  };

  let lang = localStorage.getItem('lang') || 'es';

  /* ── Theme (dark default, respects system on first visit) ── */
  const root = document.documentElement;
  if (!localStorage.getItem('theme')) {
    root.dataset.theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  $('#theme-toggle').addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', root.dataset.theme);
  });

  /* ── Terminal typing effect ─────────────────── */
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const out = $('#terminal-output');

  function renderTerminal(instant) {
    out.innerHTML = '';
    let html = '';
    for (const line of I18N[lang].terminal) {
      if (line.p) {
        html += `<span class="t-prompt">${line.p}</span> <span class="t-cmd">${line.c}</span>\n`;
      } else {
        html += `<span class="${line.hl ? 't-hl' : 't-out'}">${line.o}</span>\n`;
      }
    }
    if (instant || reduceMotion) {
      out.innerHTML = html;
      return;
    }
    // Type command lines char by char; output lines appear whole.
    // Committed base grows as parts finish, so newlines never get lost.
    const parts = I18N[lang].terminal.flatMap((l) =>
      l.p
        ? [{ cls: 't-prompt', txt: l.p }, { cls: '', txt: ' ' }, { cls: 't-cmd', txt: l.c, nl: true }]
        : [{ cls: l.hl ? 't-hl' : 't-out', txt: l.o, nl: true }]
    );
    const caret = '<span class="t-caret"></span>';
    let committed = '', pi = 0, ci = 0;
    function tick() {
      if (pi >= parts.length) { out.innerHTML = committed; return; }
      const part = parts[pi];
      ci += part.cls === '' ? part.txt.length : 1; // spaces skip instantly
      const shown = part.txt.slice(0, ci);
      // Only the final part of each line carries the newline (part.nl)
      out.innerHTML = committed +
        `<span class="${part.cls}">${shown}</span>` +
        (ci >= part.txt.length && part.nl ? '\n' : '') + caret;
      if (ci >= part.txt.length) {
        committed += `<span class="${part.cls}">${part.txt}</span>` + (part.nl ? '\n' : '');
        pi++; ci = 0;
        setTimeout(tick, part.nl ? 300 : 46);
      } else {
        setTimeout(tick, 42);
      }
    }
    tick();
  }

  /* ── Language toggle ────────────────────────── */
  function applyLang() {
    const t = I18N[lang];
    document.documentElement.lang = lang;
    const navMap = {
      '#proyectos': t.nav.proyectos,
      '#stack': t.nav.stack,
      '#sobre-mi': t.nav.sobre,
      '#contacto': t.nav.contacto,
    };
    document.querySelectorAll('.nav-links > a').forEach((a) => {
      const hash = (a.getAttribute('href') || '').split('#')[1];
      if (hash && navMap['#' + hash]) a.textContent = navMap['#' + hash];
    });
    $('.hero-sub') && ($('.hero-sub').innerHTML = t.heroSub);
    if ($('.btn-primary')) $('.btn-primary').textContent = t.ctaProjects;
    if ($('.btn-ghost-btn')) $('.btn-ghost-btn').textContent = t.ctaCv;
    const lt = $('#lang-toggle');
    if (lt) lt.textContent = lang === 'es' ? 'EN' : 'ES';
    document.querySelectorAll('.badge:not(.badge-alt)').forEach((b) => { b.textContent = t.badges.prod; });
    document.querySelectorAll('.badge-alt').forEach((b) => { b.textContent = t.badges.alt; });
    if ($('#uptime-note')) $('#uptime-note').textContent = t.footerNote;
    const kh = document.querySelector('[data-i18n-kofi]');
    if (kh) kh.textContent = t.kofiHint;
    // aria-label traducible (data-i18n-aria="a.b")
    document.querySelectorAll('[data-i18n-aria]').forEach((el) => {
      const val = el.getAttribute('data-i18n-aria').split('.').reduce((acc, k) => (acc == null ? acc : acc[k]), t);
      if (typeof val === 'string') el.setAttribute('aria-label', val);
    });
    // Resolvedor genérico: data-i18n="a.b" busca primero la clave literal "a.b"
    // y si no existe, la ruta anidada t[a][b]
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      let val = t[key];
      if (typeof val !== 'string') {
        val = key.split('.').reduce((acc, k) => (acc == null ? acc : acc[k]), t);
      }
      if (typeof val === 'string') el.textContent = val;
    });
    if ($('#terminal-output')) {
      document.title = lang === 'es'
        ? 'José Luis Sánchez Warten — Python & Frappe Developer'
        : 'Jose Luis Sanchez Warten — Python & Frappe Developer';
      renderTerminal(false);
    }
  }

  const langToggle = $('#lang-toggle');
  if (langToggle) langToggle.addEventListener('click', () => {
    lang = lang === 'es' ? 'en' : 'es';
    localStorage.setItem('lang', lang);
    applyLang();
  });

  /* ── Mobile nav (burger) ────────────────────── */
  const navToggle = $('#nav-toggle');
  const navLinks = $('#nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.textContent = open ? '✕' : '☰';
    });
    navLinks.addEventListener('click', (e) => {
      if (e.target.closest('a')) {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = '☰';
      }
    });
  }

  /* ── Waline comments (lazy: only on post pages) ── */
  const walineEl = document.querySelector('#waline');
  if (walineEl) {
    // Hoja de estilos del widget — sin ella se ve sin formato
    const wlCss = document.createElement('link');
    wlCss.rel = 'stylesheet';
    wlCss.href = 'https://unpkg.com/@waline/client@v3/dist/waline.css';
    document.head.appendChild(wlCss);
    import('https://unpkg.com/@waline/client@v3/dist/waline.js')
      .then(({ init }) => {
        init({
          el: '#waline',
          serverURL: 'https://jlsw.dev/waline',
          lang: 'es',
          path: location.pathname,
          reaction: true,
          dark: "[data-theme='dark']",
          emoji: ['//unpkg.com/@waline/emojis@1.1.0/tieba'],
          meta: ['nick', 'mail', 'link'],
          requiredMeta: ['nick'],
          pageview: false,
        });
        const note = walineEl.parentElement?.querySelector('.muted-note');
        if (note) note.remove();
        /* Parches de accesibilidad sobre el widget (fallos que vienen de fábrica) */
        const patchA11y = () => {
          try {
            // 1) imágenes de reacciones y avatares sin alt
            document.querySelectorAll('#waline img:not([alt])').forEach((im) => {
              im.alt = im.closest('.wl-reaction-item') ? 'reacción' : 'avatar';
            });
            // 2) label con aria-label prohibido → span visualmente oculto
            document.querySelectorAll('#waline label.wl-action[aria-label]').forEach((lb) => {
              const t = lb.getAttribute('aria-label');
              lb.removeAttribute('aria-label');
              const s = document.createElement('span');
              s.className = 'wl-sr';
              s.textContent = t;
              lb.appendChild(s);
            });
          } catch (e) { /* no bloquear la página nunca */ }
        };
        patchA11y();
        setTimeout(patchA11y, 1200);
        setTimeout(patchA11y, 3000);
      })
      .catch(() => { /* keep "Cargando…" visible as graceful fallback */ });
  }

  /* ── Lightbox de capturas de proyectos ───────── */
  const lb = $('#lightbox');
  if (lb) {
    const lbImg = $('.lb-img', lb);
    const lbCap = $('.lb-cap', lb);
    const lbClose = $('.lb-close', lb);
    let lastFocus = null;

    function openLb(btn) {
      lastFocus = btn;
      lbImg.src = btn.getAttribute('data-full');
      lbImg.alt = $('.shot-img', btn)?.alt || '';
      const val = (btn.getAttribute('data-key') || '').split('.').reduce((acc, k) => (acc == null ? acc : acc[k]), I18N[lang]);
      lbCap.textContent = typeof val === 'string' ? val : '';
      lb.hidden = false;
      document.body.style.overflow = 'hidden';
      lbClose.focus();
    }
    function closeLb() {
      lb.hidden = true;
      lbImg.src = '';
      document.body.style.overflow = '';
      if (lastFocus) { lastFocus.focus(); lastFocus = null; }
    }
    document.querySelectorAll('.shot-btn').forEach((btn) => {
      btn.setAttribute('aria-haspopup', 'dialog');
      btn.addEventListener('click', () => openLb(btn));
    });
    lbClose.addEventListener('click', closeLb);
    lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !lb.hidden) closeLb();
    });
  }

  /* ── Reveal on scroll ───────────────────────── */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
      }
    }, { threshold: 0.12 });
    document.querySelectorAll('.section').forEach((s) => obs.observe(s));
  } else {
    document.querySelectorAll('.section').forEach((s) => s.classList.add('visible'));
  }

  /* Init */
  applyLang();
})();
