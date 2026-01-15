document.addEventListener('DOMContentLoaded', () => {
  // -----------------------------
  // Auto-hide flash messages
  // -----------------------------
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(t => {
    setTimeout(() => {
      t.style.opacity = '0';
      setTimeout(() => t.remove(), 400);
    }, 3000);
  });

  // -----------------------------
  // Confirm deletion safety
  // -----------------------------
  document.body.addEventListener('click', (e) => {
    const el = e.target.closest('.btn-delete');
    if (!el) return;
    const ok = confirm('Are you sure? This action cannot be undone.');
    if (!ok) e.preventDefault();
  });

  // -----------------------------
  // Allow Enter to submit forms
  // -----------------------------
  const forms = document.querySelectorAll('form');
  forms.forEach(f => f.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      // default form submit allowed; do not block
    }
  }));

  // -----------------------------
  // Hospital slider functionality
  // -----------------------------
  const slider = document.getElementById('hospital-slider');
  const leftBtn = document.querySelector('.slider-arrow.left');
  const rightBtn = document.querySelector('.slider-arrow.right');

  if (slider && leftBtn && rightBtn) {
    const scrollAmount = 300; // pixels to scroll per click

    leftBtn.addEventListener('click', () => {
      slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    rightBtn.addEventListener('click', () => {
      slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });

    // Keyboard navigation for accessibility
    slider.setAttribute('tabindex', '0');
    slider.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight')
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      if (e.key === 'ArrowLeft')
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
  }
});
