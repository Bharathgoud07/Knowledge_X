/**
 * KnowledgeX — main.js
 * Global interactive enhancements
 */

document.addEventListener('DOMContentLoaded', function () {

  // ============================================================
  // 1. 3D Tilt Card Effect
  // ============================================================
  const TILT_MAX = 8; // max tilt degrees

  document.querySelectorAll('.tilt-card').forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -TILT_MAX;
      const rotateY = ((x - centerX) / centerX) * TILT_MAX;

      card.style.transform = `perspective(600px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(4px)`;
    });

    card.addEventListener('mouseleave', function () {
      card.style.transform = '';
    });
  });

  // ============================================================
  // 2. Auto-dismiss flash messages after 4s
  // ============================================================
  document.querySelectorAll('.toast').forEach(function (toast) {
    setTimeout(function () {
      const instance = bootstrap.Toast.getInstance(toast);
      if (instance) instance.hide();
    }, 4200);
  });

  // ============================================================
  // 3. Smooth scroll for anchor links
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ============================================================
  // 4. Table row hover highlight
  // ============================================================
  document.querySelectorAll('table tbody tr').forEach(function (row) {
    row.addEventListener('mouseenter', function () {
      this.style.background = 'var(--bg-hover)';
      this.style.transition = 'background 0.15s';
    });
    row.addEventListener('mouseleave', function () {
      this.style.background = '';
    });
  });

  // ============================================================
  // 5. Animate stat cards on load
  // ============================================================
  document.querySelectorAll('.stat-card, .glass-card').forEach(function (card, i) {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    setTimeout(function () {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, i * 40);
  });

});
