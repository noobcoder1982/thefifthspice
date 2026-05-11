import os
import re

# 1. Update index.html nav-right
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

old_nav_right = re.search(r'<ul class="nav-right">.*?</ul>', index_html, flags=re.DOTALL).group(0)
new_nav_right = """<ul class="nav-right">
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-menu">MENU</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-bookings">BOOKINGS</a></li>
          <li><a href="about.html" class="strikethrough-link">ABOUT</a></li>
          <li><a href="#Contact" class="strikethrough-link" onclick="document.getElementById('openContactModal').click(); return false;">CONTACT</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-cart">CART(<span class="cartCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-fav">FAV(<span class="favoritesCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link" id="loginBtn">LOGIN</a></li>
        </ul>"""

index_html = index_html.replace(old_nav_right, new_nav_right)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)


# 2. Update about.html nav-right
with open('about.html', 'r', encoding='utf-8') as f:
    about_html = f.read()

old_about_nav = re.search(r'<ul class="nav-right">.*?</ul>', about_html, flags=re.DOTALL).group(0)
about_html = about_html.replace(old_about_nav, new_nav_right)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(about_html)


# 3. Fix CSS for side window
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .giant-menu-text
css = re.sub(r'\.giant-menu-text\s*\{[^}]*\}', """.giant-menu-text {
  text-align: center;
  position: relative;
  margin-top: 4rem;
  font-family: 'Chalga', serif;
  font-size: 8rem;
  color: #fff;
  text-transform: uppercase;
  z-index: 0;
  opacity: 0.1;
}""", css)

# Fix .menu-items-container
css = re.sub(r'\.menu-items-container\s*\{[^}]*\}', """.menu-items-container {
  padding-top: 2rem;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}""", css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 4. Fix Favorites and Cart logic in script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace cart and fav init
js = re.sub(r'let cart = \[\];\nlet cartTotal = 0;\nlet favorites = JSON\.parse\(localStorage\.getItem\(\'favorites\'\)\) \|\| \[\];', """
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let cartTotal = cart.reduce((sum, item) => sum + item.price, 0);

// Migrate old favorites format
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
if (favorites.length > 0 && typeof favorites[0] === 'string') {
  favorites = [];
  localStorage.setItem('favorites', JSON.stringify(favorites));
}
""", js)

# Update addToCart
js = js.replace("""function addToCart(name, price, image) {
  cart.push({ name, price: parseFloat(price), image });
  cartTotal += parseFloat(price);
  updateCartUI();
}""", """function addToCart(name, price, image) {
  cart.push({ name, price: parseFloat(price), image });
  cartTotal += parseFloat(price);
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}""")

# Update Favorite toggle logic
js = re.sub(r'function toggleFavorite\(name\).*?\}', """function toggleFavorite(btnElement) {
  const name = btnElement.getAttribute('data-name');
  
  let existingIndex = favorites.findIndex(f => f.name === name);
  if (existingIndex > -1) {
    favorites.splice(existingIndex, 1);
  } else {
    // Need to extract price and image
    const card = btnElement.closest('.dish-card');
    let price = '', image = '';
    if (card) {
      price = card.querySelector('.dish-price').textContent;
      image = card.querySelector('img').src;
    }
    favorites.push({ name, price, image });
  }
  localStorage.setItem('favorites', JSON.stringify(favorites));
  updateFavoritesUI();
  updateFavoritesList();
  updateCartUI();
}""", js, flags=re.DOTALL)

# Update Favorite button listeners
js = js.replace("""btn.addEventListener('click', function () {
    const name = this.getAttribute('data-name');
    toggleFavorite(name);
  });""", """btn.addEventListener('click', function () {
    toggleFavorite(this);
  });""")

# Update updateFavoritesUI
js = js.replace("""function updateFavoritesUI() {
  document.querySelectorAll('.favorite-btn').forEach(btn => {
    const name = btn.getAttribute('data-name');
    if (favorites.includes(name)) {
      btn.classList.add('favorited');
    } else {
      btn.classList.remove('favorited');
    }
  });""", """function updateFavoritesUI() {
  document.querySelectorAll('.favorite-btn').forEach(btn => {
    const name = btn.getAttribute('data-name');
    if (favorites.some(f => f.name === name)) {
      btn.classList.add('favorited');
    } else {
      btn.classList.remove('favorited');
    }
  });""")

# Update updateFavoritesList
old_fav_list = """function updateFavoritesList() {
  const favoritesList = document.getElementById('favoritesList');
  if (favorites.length === 0) {
    favoritesList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">No favorites yet. Add some dishes to your favorites!</p>';
  } else {
    favoritesList.innerHTML = favorites.map((name) => {
      const dishCard = document.querySelector(.favorite-btn[data-name=""]);
      const image = dishCard ? dishCard.closest('.dish-card').querySelector('img').src : '';
      const price = dishCard ? dishCard.closest('.dish-card').querySelector('.dish-price').textContent : '';
      return 
        <div class="favorite-item">
          <img src="" alt="" loading="lazy">
          <div class="favorite-item-details">
            <div class="favorite-item-name"></div>
            <div class="favorite-item-price"></div>
          </div>
        </div>
      ;
    }).join('');
  }
}"""
new_fav_list = """function updateFavoritesList() {
  const favoritesList = document.getElementById('favoritesList');
  if (!favoritesList) return;
  if (favorites.length === 0) {
    favoritesList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">No favorites yet. Add some dishes to your favorites!</p>';
  } else {
    favoritesList.innerHTML = favorites.map((fav) => 
        <div class="favorite-item">
          <img src="" alt="" loading="lazy">
          <div class="favorite-item-details">
            <div class="favorite-item-name"></div>
            <div class="favorite-item-price"></div>
          </div>
        </div>
      ).join('');
  }
}"""
js = js.replace(old_fav_list, new_fav_list)


# Link cart checkout button to checkout.html
checkout_js = """document.querySelectorAll('.checkout-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (cart.length === 0) {
      alert("Cart is empty!");
    } else {
      window.location.href = 'checkout.html';
    }
  });
});"""
js = re.sub(r'document\.querySelectorAll\(\'\.checkout-btn\'\)\.forEach.*?\}\);', checkout_js, js, flags=re.DOTALL)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

