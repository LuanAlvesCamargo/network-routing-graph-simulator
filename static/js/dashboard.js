// NetAdmin Dashboard JS

// Animate KPI numbers counting up
function animateValue(el, end, duration = 600) {
  if (!el) return;
  const start = parseInt(el.textContent) || 0;
  const range = end - start;
  if (range === 0) return;
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(start + range * ease);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// Update live clock in header
function updateClock() {
  const el = document.getElementById('live-label');
  if (el) {
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    const s = String(now.getSeconds()).padStart(2, '0');
    el.textContent = `${h}:${m}:${s}`;
  }
}

setInterval(updateClock, 1000);
updateClock();

// Animate all KPI values on load
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.kpi-value').forEach(el => {
    const v = parseInt(el.textContent);
    if (!isNaN(v)) {
      el.textContent = '0';
      animateValue(el, v, 700);
    }
  });
});
