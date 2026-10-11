// 翰林版 選修生物（Ⅲ）互動教材網站 - 全域互動腳本

document.addEventListener('DOMContentLoaded', () => {
  // 1. 圖片燈箱功能 (Lightbox)
  initLightbox();

  // 2. 平滑捲動至錨點
  initSmoothScroll();

  // 3. 卡片進入視野時淡入動效
  initScrollAnimations();
});

function initLightbox() {
  // 建立燈箱元素
  const modal = document.createElement('div');
  modal.className = 'lightbox-modal';
  modal.innerHTML = `
    <div class="lightbox-img-wrap">
      <button class="lightbox-close" aria-label="關閉燈箱">&times;</button>
      <img class="lightbox-img" src="" alt="放大預覽">
    </div>
  `;
  document.body.appendChild(modal);

  const modalImg = modal.querySelector('.lightbox-img');
  const closeBtn = modal.querySelector('.lightbox-close');

  // 點擊可放大的圖片
  document.querySelectorAll('.unit-thumb-img, .hero-cover-img, [data-lightbox]').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', (e) => {
      e.preventDefault();
      modalImg.src = img.src;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  const closeModal = () => {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

function initScrollAnimations() {
  const cards = document.querySelectorAll('.chapter-card, .unit-detail-card');
  if (!('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
  });
}
