import re

with open('d:/restaurant site/PeaceBites/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Reservation Modal
content = re.sub(r'<!-- Reservation Modal -->.*?</div>\s*</div>\s*<!-- Contact Modal -->', '<!-- Contact Modal -->', content, flags=re.DOTALL)

# Remove Favorites Modal
content = re.sub(r'<!-- Favorites Modal -->.*?</div>\s*</div>\s*<!-- Full Screen Sliding Menu -->', '<!-- Full Screen Sliding Menu -->', content, flags=re.DOTALL)

# Replace .menu-left-half and Cart Sidebar
# We need to find the Cart Sidebar which comes after the fullScreenMenu
content = re.sub(r'<!-- Cart Sidebar -->.*?</div>\s*</div>\s*<!-- Landing Page Hero -->', '<!-- Landing Page Hero -->', content, flags=re.DOTALL)

new_menu_content = '''      <div class="menu-left-half">
        <div class="menu-nav-top">
          <button id="closeFullMenu" class="close-menu-btn">CLOSE</button>
          <ul class="nav-right menu-nav-right" id="sideMenuNav">
            <li><a href="#" class="strikethrough-link active-strike side-tab-btn" data-target="tab-menu">MENU</a></li>
            <li><a href="#" class="strikethrough-link side-tab-btn" data-target="tab-bookings">BOOKINGS</a></li>
            <li><a href="#" class="strikethrough-link side-tab-btn" data-target="tab-cart">CART(<span class="cartCountDisplay">0</span>)</a></li>
            <li><a href="#" class="strikethrough-link side-tab-btn" data-target="tab-fav">FAV(<span class="favoritesCountDisplay">0</span>)</a></li>
          </ul>
        </div>
        
        <div class="side-tabs-container">
          <!-- MENU TAB -->
          <div id="tab-menu" class="side-tab-content" style="display:block;">
            <h2 class="giant-menu-text">Menu</h2>
            <div class="menu-items-container">
              <h3 class="menu-category">BURGERS</h3>
              <ul class="menu-list">
                <li class="menu-item-line"><div class="menu-item-header"><span class="item-name">DOUBLE CHEESE</span><span class="item-dots"></span><span class="item-price">7.80</span></div><div class="menu-item-desc">Double steak patty, double American cheese, relish, mustard and gherkins.</div></li>
                <li class="menu-item-line"><div class="menu-item-header"><span class="item-name">BIG CHEESE</span><span class="item-dots"></span><span class="item-price">9.50</span></div><div class="menu-item-desc">Double steak patty, double American cheese, Swiss and Monterey jack cheese, baconnaise top and bottom.</div></li>
                <li class="menu-item-line"><div class="menu-item-header"><span class="item-name">THE BIG G</span><span class="item-dots"></span><span class="item-price">10.50</span></div><div class="menu-item-desc">Double steak patty, double American cheese, house made garlic mayo, sweet pickled red onions and iceberg lettuce.</div></li>
              </ul>
              <h3 class="menu-category" style="margin-top: 2rem;">MAINS</h3>
            </div>
          </div>

          <!-- BOOKINGS TAB -->
          <div id="tab-bookings" class="side-tab-content" style="display:none;">
            <h2 class="giant-menu-text">Book</h2>
            <div class="menu-items-container" style="padding-top: 10rem;">
              <form id="ReservationForm" autocomplete="off" class="dark-form">
                <div class="form-row">
                  <div class="form-group"><input type="text" placeholder="Your name" required></div>
                  <div class="form-group"><input type="email" placeholder="Your Email" required></div>
                </div>
                <div class="form-row">
                  <div class="form-group"><input type="tel" placeholder="Phone Number" required></div>
                  <div class="form-group">
                    <select required>
                      <option value="" disabled selected>Select number of guests</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                    </select>
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group"><input type="date" required></div>
                  <div class="form-group"><input type="time" required></div>
                </div>
                <button type="submit" class="btn btn-gold w-100">Make Reservation</button>
              </form>
            </div>
          </div>

          <!-- CART TAB -->
          <div id="tab-cart" class="side-tab-content" style="display:none;">
            <h2 class="giant-menu-text">Cart</h2>
            <div class="menu-items-container" style="padding-top: 10rem; width: 100%;">
              <div id="cartItems" class="cart-items" style="max-height: 40vh; overflow-y: auto; padding-right: 1rem;"></div>
              <div class="cart-footer" style="padding-top: 2rem; margin-top: 1rem; border-top: 1px solid #ddd;">
                <div class="cart-total-row" style="display:flex; justify-content:space-between; margin-bottom: 1.5rem; font-family: var(--font-mono);">
                  <span>Total:</span>
                  <span style="color:var(--gold);">$<span id="cartTotal">0.00</span></span>
                </div>
                <button class="btn btn-gold w-100 checkout-btn">Proceed To Checkout</button>
              </div>
            </div>
          </div>

          <!-- FAV TAB -->
          <div id="tab-fav" class="side-tab-content" style="display:none;">
            <h2 class="giant-menu-text">Favs</h2>
            <div class="menu-items-container" style="padding-top: 10rem; width: 100%;">
              <div id="favoritesList" class="favorites-list" style="max-height: 50vh; overflow-y: auto; padding-right: 1rem;"></div>
            </div>
          </div>
        </div>
      </div>'''

content = re.sub(r'      <div class="menu-left-half">.*?</div>\s*</div>\s*<div class="menu-right-half">', new_menu_content + '\n      <div class="menu-right-half">', content, flags=re.DOTALL)

old_nav = """        <ul class="nav-right">
          <li><a href="#" class="strikethrough-link" id="openMenuBtn">MENU</a></li>
          <li><a href="#Reservation" class="strikethrough-link" onclick="document.getElementById('openReservationModal').click(); return false;">BOOKINGS</a></li>
          <li><a href="#About" class="strikethrough-link">ABOUT</a></li>
          <li><a href="#Contact" class="strikethrough-link" onclick="document.getElementById('openContactModal').click(); return false;">CONTACT</a></li>
          <li><a href="#" class="strikethrough-link" id="cartIcon">CART(<span class="cartCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link" id="favoritesIcon">FAV(<span class="favoritesCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link" id="loginBtn">LOGIN</a></li>
        </ul>"""

new_nav = """        <ul class="nav-right">
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-menu">MENU</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-bookings">BOOKINGS</a></li>
          <li><a href="#About" class="strikethrough-link">ABOUT</a></li>
          <li><a href="#Contact" class="strikethrough-link" onclick="document.getElementById('openContactModal').click(); return false;">CONTACT</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-cart">CART(<span class="cartCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link hero-side-trigger" data-target="tab-fav">FAV(<span class="favoritesCountDisplay">0</span>)</a></li>
          <li><a href="#" class="strikethrough-link" id="loginBtn">LOGIN</a></li>
        </ul>"""

content = content.replace(old_nav, new_nav)
content = content.replace('id="cartCount"', 'class="cartCountDisplay"')
content = content.replace('id="favoritesCount"', 'class="favoritesCountDisplay"')

with open('d:/restaurant site/PeaceBites/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
