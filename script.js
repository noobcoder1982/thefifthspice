
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let cartTotal = cart.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);

// Migrate old favorites format
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
if (favorites.length > 0 && typeof favorites[0] === 'string') {
  favorites = [];
  localStorage.setItem('favorites', JSON.stringify(favorites));
}


function updateCartUI() {
  cartTotal = cart.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
  document.querySelectorAll('.cartCountDisplay').forEach(el => el.textContent = cart.reduce((sum, item) => sum + (item.quantity || 1), 0));
  document.querySelectorAll('.favoritesCountDisplay').forEach(el => el.textContent = favorites.length);
  const cartItems = document.getElementById('cartItems');
  const cartTotalElement = document.getElementById('cartTotal');
  
  if (cartTotalElement) cartTotalElement.textContent = cartTotal.toFixed(2);

  if (cart.length === 0) {
    cartItems.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Your Cart Is Empty</p>';
  } else {
    cartItems.innerHTML = cart.map((item) => `
      <div class="cart-item" style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05);">
        <img src="${item.image}" alt="${item.name}" loading="lazy" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
        <div class="cart-item-details" style="flex-grow: 1;">
          <div class="cart-item-name" style="font-family: var(--font-serif); font-size: 1.1rem; color: #fff;">${item.name}</div>
          <div class="cart-item-price-qty" style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-top: 0.25rem;">
            <span class="cart-item-price" style="color: var(--gold); font-family: var(--font-mono); font-size: 0.95rem;">₹${item.price.toFixed(2)}</span>
            <span class="cart-item-qty" style="color: #888; font-family: var(--font-mono); font-size: 0.9rem;">x ${item.quantity || 1}</span>
          </div>
        </div>
      </div>
    `).join('');
  }
  
  // Custom event so other elements/pages can listen to cart changes
  window.dispatchEvent(new CustomEvent('cartUpdated'));
}

function addToCart(name, price, image, quantity = 1) {
  const parsedPrice = parseFloat(price);
  const existingItem = cart.find(item => item.name === name);
  if (existingItem) {
    existingItem.quantity = (existingItem.quantity || 1) + quantity;
  } else {
    cart.push({ name, price: parsedPrice, image, quantity: quantity });
  }
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}

function removeFromCart(name) {
  cart = cart.filter(item => item.name !== name);
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}

function updateCartQuantity(name, quantity) {
  const existingItem = cart.find(item => item.name === name);
  if (existingItem) {
    existingItem.quantity = parseInt(quantity);
    if (existingItem.quantity <= 0) {
      removeFromCart(name);
      return;
    }
  } else if (quantity > 0) {
    // Should not happen normally, but safe-fallback
    addToCart(name, 0, '', quantity);
  }
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}

function updateFavoritesUI() {
  document.querySelectorAll('.favorite-btn').forEach(btn => {
    const name = btn.getAttribute('data-name');
    if (favorites.some(f => f.name === name)) {
      btn.classList.add('favorited');
    } else {
      btn.classList.remove('favorited');
    }
  });


}

function updateFavoritesList() {
  const favoritesList = document.getElementById('favoritesList');
  if (favorites.length === 0) {
    favoritesList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">No favorites yet. Add some dishes to your favorites!</p>';
  } else {
    favoritesList.innerHTML = favorites.map((name) => {
      // Find the dish card to get image and price
      const dishCard = document.querySelector(`.favorite-btn[data-name="${name}"]`);
      const image = dishCard ? dishCard.closest('.dish-card').querySelector('img').src : '';
      const price = dishCard ? dishCard.closest('.dish-card').querySelector('.dish-price').textContent : '';
      return `
        <div class="favorite-item">
          <img src="${image}" alt="${name}" loading="lazy">
          <div class="favorite-item-details">
            <div class="favorite-item-name">${name}</div>
            <div class="favorite-item-price">${price}</div>
          </div>
        </div>
      `;
    }).join('');
  }
}

window.addEventListener('load', () => {
  document.body.style.opacity = '1';

  // Hero Logo & Element Reveal Animation
  if (typeof gsap !== 'undefined' && typeof SplitText !== 'undefined') {
    const splitTitleTop = new SplitText('.title-top', { type: 'words,chars' });
    const splitTitleBottom = new SplitText('.title-bottom', { type: 'chars' });

    // Initial states
    gsap.set(splitTitleTop.chars, { opacity: 0, y: 40, rotationX: -90, transformOrigin: '50% 50% -20px' });
    gsap.set(splitTitleBottom.chars, { opacity: 0, y: 60, scale: 0.95 });
    gsap.set('.hero-nav', { opacity: 0, y: -20 });
    gsap.set('.hero-footer', { opacity: 0, y: 20 });

    const heroTl = gsap.timeline({ delay: 0.3 });

    heroTl
      .to(splitTitleTop.chars, {
        opacity: 1,
        y: 0,
        rotationX: 0,
        duration: 1.2,
        stagger: 0.05,
        ease: 'power4.out'
      })
      .to(splitTitleBottom.chars, {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 1.5,
        stagger: 0.06,
        ease: 'back.out(1.2)'
      }, '<0.3')
      .to('.hero-nav', { opacity: 1, y: 0, duration: 1, ease: 'power2.out' }, '-=0.8')
      .to('.hero-footer', { opacity: 1, y: 0, duration: 1, ease: 'power2.out' }, '<');
  }

  setTimeout(() => {
    document.querySelectorAll('.fade-in').forEach(function (el) {
      el.classList.add('visible');
    });
  }, 300);
});

function toggleFavorite(name, price, image) {
  const index = favorites.findIndex(item => (typeof item === 'string' ? item : item.name) === name);
  if (index > -1) {
    favorites.splice(index, 1);
  } else {
    favorites.push({ name, price, image });
  }
  localStorage.setItem('favorites', JSON.stringify(favorites));
  updateFavoritesUI();
  updateFavoritesList();
  updateCartUI();
}
// Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (menuToggle && navMenu) {
  menuToggle.addEventListener('click', function () {
    navMenu.classList.toggle('active');
  });

  document.querySelectorAll('.nav-menu a').forEach(function (link) {
    link.addEventListener('click', function () {
      navMenu.classList.remove('active');
    });
  });
}

// Modal Functions
function openModal(modalID) {
  const modal = document.getElementById(modalID);
  modal.style.display = 'block';
  setTimeout(() => modal.classList.add('modal-active'), 10);
}

function closeModal(modalID) {
  const modal = document.getElementById(modalID);
  modal.classList.remove('modal-active');
  setTimeout(() => modal.style.display = 'none', 300);
}

// Close modal when clicking outside or on close button
document.querySelectorAll('.modal').forEach(modal => {
  modal.addEventListener('click', function (e) {
    if (e.target === modal || e.target.classList.contains('close')) {
      closeModal(modal.id);
    }
  });
});

// Standalone Login Page Integration & Session Management
const loginBtn = document.getElementById('loginBtn');
const loggedInUser = localStorage.getItem('userEmail');

if (loginBtn) {
  if (loggedInUser) {
    const userName = loggedInUser.split('@')[0].toUpperCase();
    loginBtn.textContent = `WELCOME, ${userName}`;
    loginBtn.style.color = '#27ae60'; // Clean accent green
    
    // Inject custom style to ensure the hover strikethrough matches the active green color
    const customStyle = document.createElement('style');
    customStyle.textContent = '#loginBtn::after { background-color: #27ae60 !important; }';
    document.head.appendChild(customStyle);
  }

  loginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (localStorage.getItem('userEmail')) {
      if (confirm('Do you want to sign out of your account?')) {
        localStorage.removeItem('userEmail');
        localStorage.removeItem('rememberUser');
        window.location.href = 'index.html'; // Go back to home page after logging out
      }
    } else {
      window.location.href = 'login.html';
    }
  });
}

// Reservation Form
const reservationForm = document.getElementById('ReservationForm'); // Note: HTML has capital R

// Contact Modal
const openContactModal = document.getElementById('openContactModal');
const contactModal = document.getElementById('contactModal');
const contactForm = document.getElementById('contactForm');

openContactModal.addEventListener('click', () => {
  openModal('contactModal');
  // Focus on the first input field after modal opens
  setTimeout(() => {
    const firstInput = contactForm.querySelector('input');
    if (firstInput) {
      firstInput.focus();
    }
  }, 100);
});

contactForm.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Message sent. Thank you!');
  contactForm.reset();
  closeModal('contactModal');
});

reservationForm.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Reservation booked. Thank you!');
  reservationForm.reset();
  if (typeof toggleMenu === 'function') toggleMenu();
});

// Side Tabs Logic
function switchSideTab(targetId) {
  document.querySelectorAll('.side-tab-content').forEach(tab => {
    tab.style.display = 'none';
  });
  document.querySelectorAll('.side-tab-btn').forEach(btn => {
    btn.classList.remove('active-strike');
  });
  
  const targetTab = document.getElementById(targetId);
  if (targetTab) {
    targetTab.style.display = 'block';
    
    // Dynamic GSAP Animations for shown tab
    if (typeof gsap !== 'undefined') {
      const tl = gsap.timeline();
      
      // 1. Giant title character reveal
      if (typeof SplitText !== 'undefined') {
        const giantText = targetTab.querySelector('.giant-menu-text');
        if (giantText) {
          const splitMenu = new SplitText(giantText, { type: 'chars' });
          tl.fromTo(splitMenu.chars, 
            { y: 120, opacity: 0 }, 
            { y: 0, opacity: 1, duration: 0.7, stagger: 0.04, ease: 'back.out(1.4)' }
          );
        }
      }
      
      // 2. Tab-specific item stagger reveals
      if (targetId === 'tab-menu') {
        // Animate menu category headers and list lines
        const items = targetTab.querySelectorAll('.menu-category, .menu-item-line');
        if (items.length > 0) {
          tl.fromTo(items, 
            { y: 35, opacity: 0 }, 
            { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'power3.out' },
            '-=0.4'
          );
        }
      } else if (targetId === 'tab-bookings') {
        // Animate reservation form rows
        const formItems = targetTab.querySelectorAll('.form-row, .btn-gold');
        if (formItems.length > 0) {
          tl.fromTo(formItems, 
            { y: 25, opacity: 0 }, 
            { y: 0, opacity: 1, duration: 0.5, stagger: 0.08, ease: 'power2.out' },
            '-=0.3'
          );
        }
      } else if (targetId === 'tab-cart') {
        // Animate active cart step container
        const activeStep = targetTab.querySelector('.cart-step[style*="display: block"]') || targetTab.querySelector('.cart-step:not([style*="display: none"])');
        if (activeStep) {
          tl.fromTo(activeStep, 
            { y: 25, opacity: 0 }, 
            { y: 0, opacity: 1, duration: 0.5, ease: 'power2.out' },
            '-=0.3'
          );
        }
      } else if (targetId === 'tab-fav') {
        // Animate favorite list items
        const favItems = targetTab.querySelectorAll('.favorite-item');
        if (favItems.length > 0) {
          tl.fromTo(favItems, 
            { y: 25, opacity: 0 }, 
            { y: 0, opacity: 1, duration: 0.5, stagger: 0.08, ease: 'power2.out' },
            '-=0.3'
          );
        }
      }
    }
  }
  
  document.querySelectorAll(`.side-tab-btn[data-target="${targetId}"]`).forEach(btn => {
    btn.classList.add('active-strike');
  });
}

document.addEventListener('click', (e) => {
  const trigger = e.target.closest('.hero-side-trigger');
  if (trigger) {
    e.preventDefault();
    const target = trigger.getAttribute('data-target');
    switchSideTab(target);
    if (typeof toggleMenu === 'function' && (!menuTimeline || menuTimeline.reversed())) {
      toggleMenu();
    }
  }
});

document.querySelectorAll('.side-tab-btn').forEach(trigger => {
  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    const target = trigger.getAttribute('data-target');
    switchSideTab(target);
  });
});

// Add to Cart Buttons
document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    const name = this.getAttribute('data-name');
    const price = this.getAttribute('data-price').replace('₹', '');
    const image = this.closest('.dish-card').querySelector('img').src;
    addToCart(name, price, image);
    this.textContent = 'Added!';
    this.classList.add('added');
    setTimeout(() => {
      this.textContent = 'Add to Cart';
      this.classList.remove('added');
    }, 2000);
  });
});

// Favorite Buttons
document.querySelectorAll('.favorite-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    toggleFavorite(this);
  });
});

// Dish Navigation
const prevDish = document.getElementById('prev-dish');
const nextDish = document.getElementById('next-dish');
const dishesContainer = document.getElementById('dishes-container');
let currentDishIndex = 0;

if (prevDish && nextDish) {
  prevDish.addEventListener('click', () => {
    const dishes = document.querySelectorAll('.dish-card');
    const totalDishes = dishes.length;
    if (currentDishIndex === 0) {
      currentDishIndex = totalDishes - 1;
    } else {
      currentDishIndex--;
    }
    dishesContainer.style.transform = `translateX(-${currentDishIndex * (280 + 32)}px)`; // 280px width + 32px gap
  });

  nextDish.addEventListener('click', () => {
    const dishes = document.querySelectorAll('.dish-card');
    const totalDishes = dishes.length;
    if (currentDishIndex === totalDishes - 1) {
      currentDishIndex = 0;
    } else {
      currentDishIndex++;
    }
    dishesContainer.style.transform = `translateX(-${currentDishIndex * (280 + 32)}px)`; // 280px width + 32px gap
  });
}

// Newsletter Form
const newsletterForm = document.getElementById('newsletterForm');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for subscribing!');
    newsletterForm.reset();
  });
}

// Initialize
updateCartUI();
updateFavoritesUI();
updateFavoritesList();

// Full Screen Menu Logic (GSAP + SplitText)
const openMenuBtn = document.getElementById('openMenuBtn');
const closeFullMenu = document.getElementById('closeFullMenu');
const fullScreenMenu = document.getElementById('fullScreenMenu');
const menuBackdrop = document.getElementById('menuBackdrop');

let menuTimeline;

function initMenuAnimation() {
  if (typeof gsap === 'undefined') return;

  // Ensure elements are initially hidden before timeline
  gsap.set('.menu-backdrop', { opacity: 0 });
  gsap.set('.menu-panel', { x: '100%' });
  
  menuTimeline = gsap.timeline({ paused: true, reversed: true });

  menuTimeline
    .to('.menu-backdrop', { opacity: 1, duration: 0.6, ease: 'power3.inOut' })
    .to('.menu-panel', { x: '0%', duration: 0.8, ease: 'power4.inOut' }, '<0.1')
    .to('.menu-image-container img', { scale: 1.15, duration: 1.2, ease: 'power3.out' }, '<0.2');
}

window.addEventListener('load', () => {
  setTimeout(initMenuAnimation, 100);
});

function toggleMenu() {
  if (!menuTimeline) return;
  
  if (menuTimeline.reversed()) {
    fullScreenMenu.style.pointerEvents = 'auto';
    menuTimeline.play();
    
    // Dynamically trigger the animation sequence for the currently active tab!
    setTimeout(() => {
      const activeTabBtn = document.querySelector('.side-tab-btn.active-strike');
      if (activeTabBtn) {
        const activeTabId = activeTabBtn.getAttribute('data-target');
        switchSideTab(activeTabId);
      } else {
        switchSideTab('tab-menu');
      }
    }, 300); // Wait slightly for menu slide to complete
  } else {
    menuTimeline.reverse().then(() => {
      fullScreenMenu.style.pointerEvents = 'none';
    });
  }
}

if (openMenuBtn) {
  openMenuBtn.addEventListener('click', (e) => {
    e.preventDefault();
    toggleMenu();
  });
}

if (closeFullMenu) {
  closeFullMenu.addEventListener('click', () => {
    toggleMenu();
  });
}

if (menuBackdrop) {
  menuBackdrop.addEventListener('click', () => {
    toggleMenu();
  });
}

// Navbar Scroll Trigger
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
  
  window.addEventListener('load', () => {
    const heroNav = document.querySelector('.hero-nav');
    if (heroNav) {
      ScrollTrigger.create({
        trigger: 'body',
        start: '50px top',
        toggleClass: {targets: heroNav, className: 'scrolled-nav'}
      });
    }
  });
}

// Checkout Flow
function setCheckoutStep(stepId) {
  document.querySelectorAll('#tab-cart .cart-step').forEach(step => step.style.display = 'none');
  document.getElementById(stepId).style.display = 'block';
}

const btnProceedCheckout = document.getElementById('btn-proceed-checkout');
if (btnProceedCheckout) {
  btnProceedCheckout.addEventListener('click', () => {
    if (cart.length === 0) {
      alert("Your cart is empty!");
      return;
    }
    setCheckoutStep('cart-step-checkout');
  });
}

const btnBackCart = document.getElementById('btn-back-cart');
if (btnBackCart) btnBackCart.addEventListener('click', () => setCheckoutStep('cart-step-items'));

const checkoutForm = document.getElementById('checkoutForm');
if (checkoutForm) {
  checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();
    document.getElementById('payTotal').textContent = cartTotal.toFixed(2);
    setCheckoutStep('cart-step-payment');
  });
}

const btnBackCheckout = document.getElementById('btn-back-checkout');
if (btnBackCheckout) btnBackCheckout.addEventListener('click', () => setCheckoutStep('cart-step-checkout'));

const btnPayNow = document.getElementById('btn-pay-now');
if (btnPayNow) {
  btnPayNow.addEventListener('click', () => {
    setCheckoutStep('cart-step-processing');
    
    // Simulate payment delay
    setTimeout(() => {
      setCheckoutStep('cart-step-success');
      
      // Populate invoice
      document.getElementById('invoiceNumber').textContent = Math.floor(10000 + Math.random() * 90000);
      document.getElementById('invoiceTotal').textContent = cartTotal.toFixed(2);
      
      const invoiceItems = document.getElementById('invoice-items');
      invoiceItems.innerHTML = cart.map(item => `
        <div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem; font-family: var(--font-mono); font-size: 0.95rem;">
          <span>${item.name} ${item.quantity > 1 ? `x ${item.quantity}` : ''}</span>
          <span>₹${(item.price * (item.quantity || 1)).toFixed(2)}</span>
        </div>
      `).join('');
      
      // Print animation
      setTimeout(() => {
        document.getElementById('invoice-content').classList.add('print');
      }, 500);
      
    }, 2500);
  });
}

const btnDownloadInvoice = document.getElementById('btn-download-invoice');
if (btnDownloadInvoice) {
  btnDownloadInvoice.addEventListener('click', () => {
    const element = document.getElementById('invoice-content');
    if (typeof html2pdf !== 'undefined') {
      html2pdf().from(element).save('The_Fifth_Spice_Invoice.pdf');
    } else {
      window.print();
    }
  });
}

const btnTrackOrder = document.getElementById('btn-track-order');
if (btnTrackOrder) {
  btnTrackOrder.addEventListener('click', () => {
    setCheckoutStep('cart-step-tracking');
    // Clear cart since order is placed
    cart = [];
    cartTotal = 0;
    updateCartUI();
    
    // Simulate tracking progression
    setTimeout(() => updateTracking(2), 3000);
    setTimeout(() => updateTracking(3), 6000);
    setTimeout(() => updateTracking(4), 9000);
  });
}

function updateTracking(step) {
  if (step > 1) {
    document.getElementById('track-node-' + step).classList.add('active');
    document.getElementById('track-line-' + (step-1)).style.background = 'var(--gold)';
  }
}

const btnNewOrder = document.getElementById('btn-new-order');
if (btnNewOrder) {
  btnNewOrder.addEventListener('click', () => {
    document.querySelectorAll('.track-node').forEach((el, i) => { if(i>0) el.classList.remove('active') });
    document.querySelectorAll('.track-line').forEach(el => el.style.background = '#333');
    document.getElementById('invoice-content').classList.remove('print');
    
    setCheckoutStep('cart-step-items');
    toggleMenu(); // close menu
  });
}


// Sticky Nav Logo Laser Scan Animation on Scroll
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
  const navLogo = document.querySelector('.nav-logo');
  const scanLine = document.querySelector('.nav-logo-scan-line');
  
  if (navLogo && scanLine && document.getElementById('Menu')) {
    const scanTl = gsap.timeline({
      scrollTrigger: {
        trigger: '#Menu',
        start: 'top 90%',
        end: 'top 60%',
        scrub: 0.5,
      }
    });
    
    scanTl.set(scanLine, { opacity: 1, top: '0%' })
          .to(navLogo, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none' }, 0)
          .to(scanLine, { top: '100%', ease: 'none' }, 0)
          .set(scanLine, { opacity: 0 });
  }
}

// Circular Scroll to Top Action
const btnScrollToTop = document.getElementById('btnScrollToTop');
if (btnScrollToTop) {
  btnScrollToTop.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Redesigned Newsletter Submit Interaction
const footerNewsletterForm = document.getElementById('footerNewsletterForm');
if (footerNewsletterForm) {
  footerNewsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const emailInput = footerNewsletterForm.querySelector('input[type="email"]');
    if (emailInput && emailInput.value) {
      alert(`Welcome to the Culinary Circle! A confirmation invite has been dispatched to: ${emailInput.value}`);
      emailInput.value = '';
    }
  });
}
