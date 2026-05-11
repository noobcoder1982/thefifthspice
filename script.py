import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update ABOUT link
html = html.replace('<a href="#About" class="strikethrough-link">ABOUT</a>', '<a href="about.html" class="strikethrough-link">ABOUT</a>')

# 2. Add CDN links before script.js
gsap_links = """  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/SplitText.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/Flip.min.js"></script>"""
html = re.sub(r'  <script src="https://cdn\.jsdelivr\.net/npm/gsap@3\.15/dist/gsap\.min\.js"></script>\s*<script src="https://cdn\.jsdelivr\.net/npm/gsap@3\.15/dist/SplitText\.min\.js"></script>', gsap_links, html)

# 3. Create about.html
about_content = re.search(r'  <!-- About Section -->\s*<section id="About" class="about">.*?</section>', html, flags=re.DOTALL).group(0)

about_html = html.replace('<!-- Landing Page Hero -->', '<!-- Landing Page Hero Removed -->')
about_html = re.sub(r'<section id="Home" class="hero-new">.*?</section>', '', about_html, flags=re.DOTALL)
about_html = re.sub(r'  <!-- Popular Dishes Section -->.*?</section>', '', about_html, flags=re.DOTALL)
about_html = re.sub(r'  <!-- Services Section -->.*?</section>', '', about_html, flags=re.DOTALL)

# Let's insert a navbar into about_html
nav_html = """
  <nav class="hero-nav scrolled-nav" style="position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; padding: 2rem 4rem; background: #0c0c0c;">
    <div class="nav-left">
      <div class="main-title nav-logo-mode" style="display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1; transform: scale(0.3); transform-origin: left center; margin: 0;">
        <span class="title-top" style="transform: translateY(0.5rem);">The Fifth</span>
        <span class="title-bottom">SPICE</span>
      </div>
    </div>
    <ul class="nav-right">
      <li><a href="index.html" class="strikethrough-link">HOME</a></li>
      <li><a href="about.html" class="strikethrough-link">ABOUT</a></li>
      <li><a href="#Contact" class="strikethrough-link" onclick="document.getElementById('openContactModal').click(); return false;">CONTACT</a></li>
    </ul>
  </nav>
  <div style="height: 100px;"></div>
"""
about_html = about_html.replace('<body>', '<body>\n' + nav_html)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(about_html)

# 4. Remove About section from index.html
html = html.replace(about_content, '')

# 5. Remove nav-logo from index.html
nav_logo_regex = r'          <div class="nav-logo">\s*<span class="nav-logo-top">The Fifth</span>\s*<span class="nav-logo-bottom">SPICE</span>\s*</div>'
html = re.sub(nav_logo_regex, '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make hero-nav sticky
css = css.replace('.hero-nav {\n  display: flex;', '.hero-nav {\n  display: flex;\n  position: fixed;\n  top: 0;\n  left: 0;\n  width: 100%;\n  padding: 2rem 4rem;\n  z-index: 1000;\n  transition: background 0.3s;\n')

# Add scrolled-nav class
css += "\n.hero-nav.scrolled-nav { background: rgba(12, 12, 12, 0.95); backdrop-filter: blur(10px); padding: 1rem 4rem; }\n"

new_css_rules = """
.main-title.nav-logo-mode {
  transform: scale(0.3);
  transform-origin: left center;
  margin: 0;
  line-height: 1;
}

.main-title.nav-logo-mode .title-top {
  transform: translateY(0.5rem);
}
"""
css += new_css_rules

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

flip_js = """
// Flip Logo on Scroll
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined' && typeof Flip !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger, Flip);
  
  window.addEventListener('load', () => {
    setTimeout(() => {
      const mainTitle = document.querySelector('.main-title');
      const navLeft = document.querySelector('.nav-left');
      
      // Ensure we are on home page where both exist
      if (mainTitle && navLeft && document.querySelector('.hero-new')) {
        const state = Flip.getState(mainTitle);
        
        navLeft.appendChild(mainTitle);
        mainTitle.classList.add('nav-logo-mode');
        
        const flipTween = Flip.from(state, {
          scale: true,
          paused: true,
          ease: 'none'
        });
        
        ScrollTrigger.create({
          trigger: '.hero-new',
          start: 'top top',
          end: '+=500',
          scrub: 1,
          animation: flipTween
        });
      }
      
      // Navbar background
      const heroNav = document.querySelector('.hero-nav');
      if (heroNav) {
        ScrollTrigger.create({
          trigger: 'body',
          start: '50px top',
          toggleClass: {targets: heroNav, className: 'scrolled-nav'}
        });
      }
    }, 1500); // Wait for GSAP intro animation to finish before grabbing initial state
  });
}
"""

if "gsap.registerPlugin(ScrollTrigger, Flip);" not in js:
    js += flip_js

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

