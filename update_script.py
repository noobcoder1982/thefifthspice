import re

with open('d:/restaurant site/PeaceBites/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
"""function updateCartUI() {
  const cartCount = document.getElementById('cartCount');
  const cartItems = document.getElementById('cartItems');
  const cartTotalElement = document.getElementById('cartTotal');
  const favoritesCount = document.getElementById('favoritesCount');

  cartCount.textContent = cart.length;
  cartTotalElement.textContent = cartTotal.toFixed(2);
  favoritesCount.textContent = favorites.length;""",
"""function updateCartUI() {
  document.querySelectorAll('.cartCountDisplay').forEach(el => el.textContent = cart.length);
  document.querySelectorAll('.favoritesCountDisplay').forEach(el => el.textContent = favorites.length);
  const cartItems = document.getElementById('cartItems');
  const cartTotalElement = document.getElementById('cartTotal');
  
  if (cartTotalElement) cartTotalElement.textContent = cartTotal.toFixed(2);"""
)

text = text.replace('updateFavoritesModal() {', 'updateFavoritesList() {')
text = text.replace('updateFavoritesModal();', 'updateFavoritesList();')

text = text.replace(
"""  // Assuming there's a favorites icon, but it's not in HTML, so commenting out
  // document.getElementById('favoritesIcon').style.color = favorites.length > 0 ? 'red' : '#666';""",
""
)

old_reservation = """// Reservation Modal
const openReservationModal = document.getElementById('openReservationModal');
const reservationModal = document.getElementById('reservationModal');
const reservationForm = document.getElementById('ReservationForm'); // Note: HTML has capital R

openReservationModal.addEventListener('click', () => {
  openModal('reservationModal');
  // Focus on the first input field after modal opens
  setTimeout(() => {
    const firstInput = reservationForm.querySelector('input');
    if (firstInput) {
      firstInput.focus();
    }
  }, 100);
});"""

new_reservation = """// Reservation Form
const reservationForm = document.getElementById('ReservationForm'); // Note: HTML has capital R"""

text = text.replace(old_reservation, new_reservation)

text = text.replace("""reservationForm.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Reservation booked. Thank you!');
  reservationForm.reset();
  closeModal('reservationModal');
});""", """reservationForm.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Reservation booked. Thank you!');
  reservationForm.reset();
  if (typeof toggleMenu === 'function') toggleMenu();
});""")

old_cart_fav = """// Favorites Modal
const favoritesIcon = document.getElementById('favoritesIcon');
const favoritesModal = document.getElementById('favoritesModal');

favoritesIcon.addEventListener('click', () => {
  updateFavoritesList();
  openModal('favoritesModal');
});

// Cart Sidebar
const cartIcon = document.getElementById('cartIcon');
const cartSidebar = document.getElementById('cartSidebar');
const cartClose = document.querySelector('.cart-close');

cartIcon.addEventListener('click', () => {
  cartSidebar.classList.toggle('active');
});

cartClose.addEventListener('click', () => {
  cartSidebar.classList.remove('active');
});"""

new_cart_fav = """// Side Tabs Logic
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
    
    // Animate the text in the newly opened tab
    if (typeof gsap !== 'undefined' && typeof SplitText !== 'undefined') {
      const giantText = targetTab.querySelector('.giant-menu-text');
      if (giantText) {
        const splitMenu = new SplitText(giantText, { type: 'chars' });
        gsap.fromTo(splitMenu.chars, 
          { y: 100, opacity: 0 }, 
          { y: 0, opacity: 1, duration: 0.6, stagger: 0.03, ease: 'back.out(1.2)' }
        );
      }
    }
  }
  
  document.querySelectorAll(.side-tab-btn[data-target=""]).forEach(btn => {
    btn.classList.add('active-strike');
  });
}

document.querySelectorAll('.hero-side-trigger').forEach(trigger => {
  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    const target = trigger.getAttribute('data-target');
    switchSideTab(target);
    if (!menuTimeline || menuTimeline.reversed()) {
      toggleMenu();
    }
  });
});

document.querySelectorAll('.side-tab-btn').forEach(trigger => {
  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    const target = trigger.getAttribute('data-target');
    switchSideTab(target);
  });
});

document.querySelectorAll('.checkout-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (cart.length === 0) {
      alert("Cart is empty!");
    } else {
      alert("Proceeding to checkout!");
    }
  });
});"""

text = text.replace(old_cart_fav, new_cart_fav)

if 'updateFavoritesList();\n\n// Full Screen Menu Logic' not in text:
    text = text.replace('updateFavoritesUI();\n\n// Full Screen Menu Logic', 'updateFavoritesUI();\nupdateFavoritesList();\n\n// Full Screen Menu Logic')

with open('d:/restaurant site/PeaceBites/script.js', 'w', encoding='utf-8') as f:
    f.write(text)
