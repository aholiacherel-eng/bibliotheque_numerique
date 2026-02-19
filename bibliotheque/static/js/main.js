/* ═══════════════════════════════════════════════════
   BIBLIONUMÉRIQUE — main.js
   ═══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Burger menu (mobile) ───────────────────────────
  const burger     = document.getElementById('burger');
  const mobileMenu = document.getElementById('mobile-menu');

  if (burger && mobileMenu) {
    burger.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      // Animation barres burger
      document.getElementById('b1')?.classList.toggle('rotate-45');
      document.getElementById('b1')?.classList.toggle('translate-y-2');
      document.getElementById('b2')?.classList.toggle('opacity-0');
      document.getElementById('b3')?.classList.toggle('-rotate-45');
      document.getElementById('b3')?.classList.toggle('-translate-y-2');
    });
  }

  // ── Recherche avec suggestions AJAX ───────────────
  const searchInput   = document.getElementById('search-input');
  const suggestionsBox = document.getElementById('search-suggestions');

  if (searchInput && suggestionsBox) {
    let debounceTimer;

    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      const q = searchInput.value.trim();

      if (q.length < 2) {
        suggestionsBox.innerHTML = '';
        suggestionsBox.classList.remove('open');
        return;
      }

      debounceTimer = setTimeout(async () => {
        try {
          const resp = await fetch(`/recherche/ajax/?q=${encodeURIComponent(q)}`);
          const data = await resp.json();

          if (data.suggestions.length === 0) {
            suggestionsBox.classList.remove('open');
            return;
          }

          suggestionsBox.innerHTML = data.suggestions.map(s => `
            <a href="${s.url}" class="suggestion-item">
              <strong>${s.titre}</strong>
              <small>${s.auteurs}</small>
            </a>
          `).join('');
          suggestionsBox.classList.add('open');
        } catch (e) {
          console.error('Erreur suggestions:', e);
        }
      }, 300);
    });

    // Fermer les suggestions en cliquant ailleurs
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-search')) {
        suggestionsBox.classList.remove('open');
      }
    });

    // Navigation clavier dans les suggestions
    searchInput.addEventListener('keydown', (e) => {
      const items = suggestionsBox.querySelectorAll('.suggestion-item');
      const active = suggestionsBox.querySelector('.suggestion-item.focused');
      let idx = Array.from(items).indexOf(active);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (active) active.classList.remove('focused');
        idx = (idx + 1) % items.length;
        items[idx]?.classList.add('focused');
        items[idx]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (active) active.classList.remove('focused');
        idx = (idx - 1 + items.length) % items.length;
        items[idx]?.classList.add('focused');
        items[idx]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && active) {
        e.preventDefault();
        window.location.href = active.href;
      } else if (e.key === 'Escape') {
        suggestionsBox.classList.remove('open');
      }
    });
  }

  // ── Auto-fermeture des messages ────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(2rem)';
      alert.style.transition = 'all .4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ── Lecteur : mise à jour progression (AJAX) ──────
  // Exposé globalement pour être appelé depuis le template lecteur
  window.majProgression = async (slug, page) => {
    try {
      const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
      await fetch(`/lecture/${slug}/progression/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ page }),
      });
    } catch (e) {
      console.error('Erreur progression:', e);
    }
  };

  // ── Highlight lien actif nav ──────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.style.color = 'var(--accent)';
    }
  });

});

// ── CSS dynamique burger ouvert ────────────────────
const style = document.createElement('style');
style.textContent = `
  .nav-links.mobile-open {
    display: flex !important;
    flex-direction: column;
    position: fixed;
    top: 68px; left: 0; right: 0;
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 1.5rem 2rem;
    gap: 1rem;
    box-shadow: var(--shadow-lg);
    z-index: 99;
  }
  .nav-search.mobile-open {
    display: flex !important;
    position: fixed;
    top: calc(68px + 200px); left: 0; right: 0;
    padding: 1rem 2rem;
    background: var(--white);
    z-index: 98;
  }
  .burger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  .burger.open span:nth-child(2) { opacity: 0; }
  .burger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  .suggestion-item.focused { background: var(--warm); }
`;
document.head.appendChild(style);