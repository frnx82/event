/* ═══════════════════════════════════════════════════════
   PRABHU DEVA LIVE — JavaScript
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Configuration ──────────────────────────────────────
  // Update this URL when your Google Form is ready
  const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/1fAJ8e3Zav8EIvgYQ-yDMa4LYRp40fxwBvkgvXftXvo8/viewform';

  // ── Navigation scroll effect ───────────────────────────
  const navbar = document.getElementById('main-nav');
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });

  // Mobile menu toggle
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const spans = navToggle.querySelectorAll('span');
    if (navLinks.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity = '';
      spans[2].style.transform = '';
    }
  });

  // Close mobile menu on link click
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      const spans = navToggle.querySelectorAll('span');
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });
  });

  // ── Counter animation ─────────────────────────────────
  function animateCounters() {
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.count);
      const duration = 2000;
      const start = performance.now();

      function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        counter.textContent = Math.round(target * eased);
        if (progress < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
    });
  }

  // Run counter animation when hero is visible
  const heroObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters();
        heroObserver.disconnect();
      }
    });
  }, { threshold: 0.3 });

  const heroStats = document.querySelector('.hero-stats');
  if (heroStats) heroObserver.observe(heroStats);

  // ── Scroll reveal animation ────────────────────────────
  const revealElements = document.querySelectorAll(
    '.detail-card, .highlight-card, .step, .contact-card, .about-content-col, .about-image-wrapper, .qr-card, .register-cta'
  );

  revealElements.forEach(el => el.classList.add('reveal'));

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, index * 100);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  revealElements.forEach(el => revealObserver.observe(el));

  // ── QR Code generation ─────────────────────────────────
  function generateQR() {
    const qrCanvas = document.getElementById('qr-canvas');
    if (!qrCanvas) return;

    if (typeof QRCode !== 'undefined') {
      QRCode.toCanvas(qrCanvas, GOOGLE_FORM_URL, {
        width: 180,
        margin: 1,
        color: {
          dark: '#1a1025',
          light: '#ffffff'
        }
      }, (error) => {
        if (error) {
          console.warn('QR canvas failed, using image fallback:', error);
          useQRFallback();
        }
      });
    } else {
      // Library not loaded, use image API fallback
      useQRFallback();
    }
  }

  function useQRFallback() {
    const placeholder = document.querySelector('.qr-placeholder');
    if (placeholder) {
      const encodedURL = encodeURIComponent(GOOGLE_FORM_URL);
      placeholder.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodedURL}" alt="Scan to register" style="width:100%;height:100%;object-fit:contain;" />`;
    }
  }

  generateQR();

  // ── Registration button links ──────────────────────────
  const registerButtons = document.querySelectorAll('#hero-register-btn, #register-form-btn');
  registerButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (GOOGLE_FORM_URL.includes('YOUR_FORM_ID')) {
        e.preventDefault();
        // Scroll to register section if form not set up yet
        const registerSection = document.getElementById('register');
        if (registerSection) {
          registerSection.scrollIntoView({ behavior: 'smooth' });
        }
      } else {
        // Open form in new tab
        btn.href = GOOGLE_FORM_URL;
        btn.target = '_blank';
      }
    });
  });

  // ── Floating particles ─────────────────────────────────
  function createParticles() {
    const container = document.getElementById('hero-particles');
    if (!container) return;

    const colors = [
      'hsla(42, 92%, 56%, 0.3)',   // gold
      'hsla(330, 85%, 55%, 0.2)',   // magenta
      'hsla(270, 60%, 50%, 0.2)',   // purple
      'hsla(0, 0%, 100%, 0.1)',     // white
    ];

    for (let i = 0; i < 30; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      const size = Math.random() * 6 + 2;
      particle.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${Math.random() * 100}%;
        background: ${colors[Math.floor(Math.random() * colors.length)]};
        animation-duration: ${Math.random() * 15 + 10}s;
        animation-delay: ${Math.random() * -20}s;
      `;
      container.appendChild(particle);
    }
  }

  createParticles();

  // ── Smooth scroll for anchor links ─────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ── Parallax effect on hero image ──────────────────────
  const heroImage = document.querySelector('.hero-image-container');
  if (heroImage && window.innerWidth > 768) {
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY;
      const rate = scrolled * 0.3;
      heroImage.style.transform = `translateY(calc(-50% + ${rate}px))`;
    }, { passive: true });
  }

  // ── Send to Phone functionality ───────────────────────
  const regLink = GOOGLE_FORM_URL;
  const shareTitle = 'Prabhu Deva Live in Raleigh NC — Register as a Dancer!';
  const shareText = 'Register now to dance alongside Prabhu Deva at the live event in Raleigh, NC! 💃🕺';

  // SMS button
  const smsBtn = document.getElementById('send-sms-btn');
  if (smsBtn) {
    smsBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const message = encodeURIComponent(`${shareText}\n\n${regLink}`);
      // Use sms: protocol — works on iOS and Android
      const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
      const sep = isIOS ? '&' : '?';
      window.open(`sms:${sep}body=${message}`, '_self');
    });
  }

  // Email button
  const emailBtn = document.getElementById('send-email-btn');
  if (emailBtn) {
    emailBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const subject = encodeURIComponent(shareTitle);
      const body = encodeURIComponent(`${shareText}\n\nRegister here:\n${regLink}\n\nVisit: https://fusionvibez-studios.com`);
      window.location.href = `mailto:?subject=${subject}&body=${body}`;
    });
  }

  // Native Share API button
  const shareBtn = document.getElementById('send-share-btn');
  if (shareBtn) {
    if (navigator.share) {
      shareBtn.addEventListener('click', async () => {
        try {
          await navigator.share({
            title: shareTitle,
            text: shareText,
            url: regLink,
          });
        } catch (err) {
          if (err.name !== 'AbortError') {
            console.log('Share failed:', err);
          }
        }
      });
    } else {
      // Fallback: hide share button on desktop browsers without Web Share API
      shareBtn.style.display = 'none';
      // Adjust grid to single row for remaining 3 buttons
      const sendOptions = document.querySelector('.send-options');
      if (sendOptions) {
        sendOptions.style.gridTemplateColumns = 'repeat(3, 1fr)';
      }
    }
  }

  // Copy Link button
  const copyBtn = document.getElementById('send-copy-btn');
  const toast = document.getElementById('send-toast');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(regLink);
      } catch {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = regLink;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }

      // Visual feedback
      copyBtn.classList.add('copied');
      const label = copyBtn.querySelector('span');
      const origText = label.textContent;
      label.textContent = 'Copied!';

      // Show toast
      if (toast) {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2500);
      }

      // Reset button after delay
      setTimeout(() => {
        copyBtn.classList.remove('copied');
        label.textContent = origText;
      }, 2000);
    });
  }

});
