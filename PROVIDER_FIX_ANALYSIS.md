# 🎬 PLAYER PAGE — STREAMING LOGIC ANALYSIS

> **Dark Cinematic · Premium Minimal · Content-First**

---

## 📊 CONTENT TYPE DIFFERENCES

### 🎥 **MOVIES**
```python
# API: /movie/{movie_id}
# Single source, direct playback
# No episode selection needed
```
**Flow:**
- Load → Sources → Auto-play first provider
- **No pagination** (1 video source)
- **Provider selector only**

---

### 📺 **TV SERIES**
```python
# API: /detail/tv/{tv_id}?season=X&episode=Y&providers=all
# Multi-season + Multi-episode structure
```
**Flow:**
- Select **Season** → Select **Episode** → Load sources
- **Episode grid** (4-6 columns, scrollable)
- **Provider selector** per episode
- **URL params:** `?season=1&episode=5`

**UI Elements:**
- Season dropdown (top-left overlay)
- Episode dropdown (top-left overlay)
- Episode cards grid (with thumbnails)
- Current episode highlight

---

### 🎌 **ANIME**
```python
# API: /detail/anime/{anime_id}?ep=X&providers=all
# Single-season, episode-based (like TV but simpler)
```
**Flow:**
- Select **Episode** → Load sources
- **Episode grid** (compact, number-focused)
- **Provider selector** per episode
- **URL params:** `?ep=12`

**UI Elements:**
- Episode dropdown (top-left overlay)
- Episode cards grid (minimal thumbnails)
- **Special data:** Studios, Premiered, Status

---

## 🎨 VISUAL STYLE IMPLEMENTATION

### **Color System**
```css
--bg-primary:    #0B0B0B;    /* Deep black */
--bg-card:       #151515;    /* Subtle card */
--text-primary:  #FFFFFF;    /* Pure white */
--text-muted:    #A0A0A0;    /* Gray secondary */
--accent:        #E50914;    /* Minimal red (CTAs only) */
--glass:         rgba(255,255,255,0.05);
```

### **Typography**
```css
/* Headers: Cinematic Serif */
font-family: 'Playfair Display', 'Cinzel', serif;
font-weight: 700-900; /* Black/Bold only */

/* Body: Clean Sans */
font-family: 'Inter', 'Poppins', sans-serif;
font-size: 10px-12px; /* Compact text */
```

### **Card Design**
```css
.episode-card {
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  transition: all 300ms ease;
}

.episode-card:hover {
  transform: scale(1.05);
  border-color: rgba(229,9,20,0.4);
  box-shadow: 0 0 20px rgba(229,9,20,0.15);
}
```

---

## 🧩 PLAYER COMPONENTS

### **1. Header (Compact)**
```html
<!-- Minimal breadcrumb -->
<a href="back">← BACK</a>

<!-- Title + Meta inline -->
<h1>Content Title</h1>
<div class="meta">
  <badge>MOVIE/TV/ANIME</badge>
  <span>2026</span>
  <span>120 min</span>
  <rating>8.5</rating>
</div>
```

### **2. Video Player Container**
```html
<div class="cinematic-glow">
  <!-- Gradient blur effect -->
  <div class="player-wrapper">
    <!-- Episode selectors (TV/Anime only) -->
    <select>Season</select>
    <select>Episode</select>
    
    <!-- 16:9 Aspect ratio enforced -->
    <iframe id="videoPlayer"></iframe>
    
    <!-- Provider bar (bottom) -->
    <div class="provider-selector">
      <button>VidSrc</button>
      <button>VidLink</button>
      <button>2Embed</button>
    </div>
  </div>
</div>
```

### **3. Episode Grid (TV/Anime)**
```html
<div class="episodes-grid">
  <!-- 6 columns on XL, 4 on MD, 2 on mobile -->
  <div class="episode-card" data-episode="1">
    <div class="aspect-video">
      <img src="thumbnail" /> <!-- TV only -->
      <span class="ep-number">01</span>
      <div class="gradient-overlay"></div>
    </div>
    <p class="ep-title">Episode Title</p>
  </div>
</div>
```

### **4. Content Info Sidebar**
```html
<div class="glass-card">
  <h3>DETAILS</h3>
  <dl>
    <dt>Status</dt><dd>Released</dd>
    <dt>Studio</dt><dd>MAPPA</dd> <!-- Anime -->
    <dt>Premiered</dt><dd>Fall 2022</dd> <!-- Anime -->
  </dl>
  
  <!-- Genre tags -->
  <div class="genre-tags">
    <span>ACTION</span>
    <span>HORROR</span>
  </div>
</div>
```

---

## ⚙️ JAVASCRIPT LOGIC

### **Episode Click Handler (Unified)**
```javascript
function handleEpisodeClick(element) {
  const epNum = element.dataset.episode;
  const contentType = '{{ content_type }}'; // movie/tv/anime
  
  if (contentType === 'tv') {
    // Reload page with new episode
    const season = {{ current_season }};
    window.location.href = `?season=${season}&episode=${epNum}`;
  } 
  else if (contentType === 'anime') {
    // Reload with ?ep parameter
    window.location.href = `?ep=${epNum}`;
  }
  else {
    // Movie: just load sources (no reload)
    loadSourcesFromCard(element);
  }
}
```

### **Provider Selector (All Types)**
```javascript
function showProviderSelector(sources) {
  const container = document.getElementById('providerButtons');
  
  sources.forEach((src, idx) => {
    const btn = createProviderButton(src);
    btn.onclick = () => loadSource(src.url, btn);
    container.appendChild(btn);
    
    // Auto-load first provider
    if (idx === 0) btn.click();
  });
}
```

### **Auto-Load on Page Load**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const sources = {{ sources|safe }}; // Django context
  
  if (sources.length > 0) {
    showProviderSelector(sources);
    loadSource(sources[0].url); // First provider auto-play
  }
});
```

---

## 🔄 DATA FLOW

### **Movie Flow**
```
Home → Click Card → /movie/{id} → Load sources → Auto-play
```

### **TV Series Flow**
```
Home → Click Card → /tv/{id}?season=1&episode=1
  ↓
Episode Grid → Click Episode → Reload with ?season=X&episode=Y
  ↓
Load sources → Provider selector → Play
```

### **Anime Flow**
```
Home → Click Card → /anime/{id}?ep=1
  ↓
Episode Grid → Click Episode → Reload with ?ep=X
  ↓
Load sources → Provider selector → Play
```

---

## 📐 LAYOUT STRUCTURE

```
┌─────────────────────────────────────────┐
│ BACK ← | TITLE (2xl-4xl)                │
│ [MOVIE] 2026 · 120min · ⭐8.5          │
├─────────────────────────────────────────┤
│ [ADSTERRA TOP AD]                       │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ [Season▼] [Episode▼]  (TV/Anime)   │ │
│ │                                     │ │
│ │    VIDEO PLAYER (16:9)             │ │
│ │    Cinematic glow effect           │ │
│ │                                     │ │
│ │ [Provider: VidSrc | VidLink | ...]│ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ EPISODES (TV/Anime only)                │
│ ┌───┬───┬───┬───┬───┬───┐              │
│ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ (Grid 6col) │
│ ├───┼───┼───┼───┼───┼───┤              │
│ │ 7 │ 8 │ 9 │10 │11 │12 │              │
│ └───┴───┴───┴───┴───┴───┘              │
├─────────────────────────────────────────┤
│ OVERVIEW (2/3) │ DETAILS (1/3)         │
│ Description    │ Status: Released      │
│ ...            │ Studio: MAPPA         │
│                │ Genres: [ACTION]      │
├─────────────────────────────────────────┤
│ [ADSTERRA BOTTOM AD]                    │
└─────────────────────────────────────────┘
```

---

## 🎯 KEY DIFFERENCES SUMMARY

| Feature | Movie | TV Series | Anime |
|---------|-------|-----------|-------|
| **URL Params** | None | `?season=X&episode=Y` | `?ep=X` |
| **Selectors** | ❌ | ✅ Season + Episode | ✅ Episode only |
| **Episode Grid** | ❌ | ✅ (with thumbnails) | ✅ (minimal) |
| **Reload on Click** | ❌ | ✅ | ✅ |
| **Special Data** | Genres | Seasons, Networks | Studios, Premiered |
| **Grid Layout** | N/A | 4-6 columns | 4-6 columns |

---

## 🎨 GLASSMORPHISM EFFECTS

```css
/* Navbar, Cards, Overlays */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Player glow (premium effect) */
.cinematic-glow::before {
  content: '';
  position: absolute;
  inset: -8px;
  background: linear-gradient(135deg, 
    rgba(229,9,20,0.3), 
    rgba(229,9,20,0.1));
  border-radius: 32px;
  blur: 40px;
  opacity: 0.5;
  animation: pulse-slow 4s infinite;
}
```

---

## 🚀 OPTIMIZATION NOTES

### **Performance**
- ✅ Auto-load first provider (no manual click)
- ✅ Lazy-load episode thumbnails (TV only)
- ✅ Horizontal scroll for 100+ episodes
- ✅ Jump-to-episode search input

### **Mobile Responsive**
```css
/* Desktop: 6 columns */
@media (min-width: 1280px) {
  .episodes-grid { grid-template-columns: repeat(6, 1fr); }
}

/* Tablet: 4 columns */
@media (min-width: 768px) {
  .episodes-grid { grid-template-columns: repeat(4, 1fr); }
}

/* Mobile: 2 columns */
.episodes-grid { 
  grid-template-columns: repeat(2, 1fr); 
}
```

### **Provider Selector Mobile**
- Desktop: Horizontal buttons
- Mobile: Dropdown select (better UX)

---

## 📝 IMPLEMENTATION CHECKLIST

- [x] **Unified player template** (`player.html`)
- [x] **Content type detection** (`{{ content_type }}`)
- [x] **Dynamic episode grid** (TV/Anime conditional)
- [x] **Provider auto-load** (first source)
- [x] **Season/Episode selectors** (overlay positioned)
- [x] **Cinematic glow effects** (player container)
- [x] **Glassmorphism styling** (cards, navbar)
- [x] **Mobile-responsive grid** (2/4/6 columns)
- [x] **Episode jump search** (100+ episodes)
- [x] **Current episode highlight** (border accent)

---

## 🎬 FINAL NOTES

**Design Philosophy:**
- **Content-first:** Video player is the hero
- **Minimal UI:** No clutter, focus on immersion
- **Dark theme:** Black (#0B0B0B) with subtle accents
- **Glassmorphism:** Light transparency, blur effects
- **Typography:** Cinematic serif headers, clean sans body
- **Interactions:** Smooth hover, scale, glow effects

**Key Success Factors:**
1. **Auto-play** on page load (no friction)
2. **Provider fallback** (multiple sources)
3. **Episode navigation** (seamless TV/Anime UX)
4. **Responsive design** (mobile-first approach)
5. **Performance** (lazy loading, optimized images)

---

*Built with Django + StreameX API · Styled with Tailwind CSS*
