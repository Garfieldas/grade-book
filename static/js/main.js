document.addEventListener("DOMContentLoaded", function () {
  try {
    if (window.lucide && typeof lucide.createIcons === "function") {
      lucide.createIcons();
    }
  } catch (e) {
    console.warn("lucide init failed", e);
  }
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
});
document.body.addEventListener("htmx:afterSwap", () => {
  lucide.createIcons();
});
htmx.onLoad(function (target) {
  const handleAlert = (alert) => {
    setTimeout(() => {
      alert.classList.add("opacity-0", "transition", "duration-700");
      setTimeout(() => alert.remove(), 700);
    }, 3000);
  };
  if (target.classList.contains("autoremove")) {
    handleAlert(target);
  }
  const alerts = target.querySelectorAll(".autoremove");
  alerts.forEach(handleAlert);
});

(function applyStoredTheme() {
  try {
    const stored = localStorage.getItem('theme');
    const theme = stored || document.documentElement.getAttribute('data-theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
  } catch (_) {}
})();
const openBtn = document.getElementById('open-theme-settings');
const modal = document.getElementById('theme-modal');
const select = document.getElementById('theme-select');
const closeBtn = document.getElementById('close-theme-modal');

if (openBtn && modal && select) {
  openBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    select.value = current;
    if (typeof modal.showModal === 'function') {
      modal.showModal();
    } else {
      modal.setAttribute('open', '');
    }
  });

  select.addEventListener('change', () => {
    const value = select.value;
    document.documentElement.setAttribute('data-theme', value);
    try {
      localStorage.setItem('theme', value);
    } catch (_) {}
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      if (typeof modal.close === 'function') {
        modal.close();
      } else {
        modal.removeAttribute('open');
      }
    });
  }
}