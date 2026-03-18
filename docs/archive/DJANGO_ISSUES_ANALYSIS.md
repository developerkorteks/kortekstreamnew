# Django Implementation Issues - Analysis & Fix Planning

**Date:** March 18, 2026  
**Scope:** TV Series and Anime detail pages

---

## 🔍 Issues Identified

### Issue #1: TV Series - Missing Episode Parameter
**Location:** `streaming/views.py` - `tv_detail()` function (line 240-268)

**Problem:**
```python
def tv_detail(request, tv_id):
    season = request.GET.get('season', 1)  # ✅ Has season
    # ❌ MISSING: episode parameter
    tv_show = api.get_tv_detail(tv_id, season=season)
```

**API Expected:**
```
GET /api/detail/tv/{id}?season=1&episode=1&providers=all
```

**Current Django:**
```python
# Only passes season, missing episode
api.get_tv_detail(tv_id, season=season)
```

**Impact:**
- TV detail page doesn't show specific episode
- No streaming sources for episodes
- Episode selector not working properly

---

### Issue #2: TV Series Service - Incomplete Parameters
**Location:** `streaming/services.py` - `get_tv_detail()` function (line 179-200)

**Problem:**
```python
def get_tv_detail(self, tv_id: str, season: int = 1) -> Dict:
    endpoint = f"detail/tv/{tv_id}"
    params = {"season": season}  # ❌ Missing episode parameter
    return self._make_request(endpoint, params)
```

**Should be:**
```python
def get_tv_detail(self, tv_id: str, season: int = 1, episode: int = 1, providers: str = "all") -> Dict:
    endpoint = f"detail/tv/{tv_id}"
    params = {
        "season": season,
        "episode": episode,
        "providers": providers
    }
    return self._make_request(endpoint, params)
```

---

### Issue #3: Anime - Missing Episode Parameter
**Location:** `streaming/views.py` - `anime_detail()` function (line 271-295)

**Problem:**
```python
def anime_detail(request, anime_id):
    api = get_api_client()
    anime = api.get_anime_detail(anime_id)  # ❌ No episode parameter
```

**API Expected:**
```
GET /api/detail/anime/{id}?ep=1&providers=all
```

**Impact:**
- Anime detail page doesn't show specific episode
- No streaming sources
- Episode selector not functional

---

### Issue #4: Anime Service - Missing Episode Parameter
**Location:** `streaming/services.py` - `get_anime_detail()` function (line 202-221)

**Problem:**
```python
def get_anime_detail(self, anime_id: str) -> Dict:
    endpoint = f"detail/anime/{anime_id}"
    return self._make_request(endpoint)  # ❌ No episode parameter
```

**Should be:**
```python
def get_anime_detail(self, anime_id: str, episode: int = None, providers: str = "all") -> Dict:
    endpoint = f"detail/anime/{anime_id}"
    params = {}
    if episode:
        params["ep"] = episode
        params["providers"] = providers
    return self._make_request(endpoint, params)
```

---

### Issue #5: Player Template - Missing Episode/Season Selectors
**Location:** `templates/streaming/player.html`

**Problem:**
- No UI for episode selection in TV series
- No UI for episode selection in anime
- No season selector for TV
- No SUB/DUB selector for anime

**Expected UI Elements:**

For **TV Series:**
```html
<select id="season-selector">
  <option value="1">Season 1</option>
  <option value="2">Season 2</option>
</select>

<select id="episode-selector">
  <option value="1">Episode 1 - Pilot</option>
  <option value="2">Episode 2 - Cat's in the Bag...</option>
</select>
```

For **Anime:**
```html
<select id="episode-selector">
  <option value="1">Episode 1 - I'm Luffy!</option>
  <option value="2">Episode 2 - Enter the Great Swordsman!</option>
</select>

<div id="sub-dub-selector">
  <button class="active">SUB</button>
  <button>DUB</button>
</div>
```

---

## 📋 Fix Planning

### Phase 1: Backend Services (Priority: HIGH)

#### Task 1.1: Update TV Detail Service
**File:** `streaming/services.py`

**Changes:**
```python
def get_tv_detail(self, tv_id: str, season: int = 1, episode: int = 1, providers: str = "all") -> Dict:
    """
    Get detailed information about a TV show with episode
    
    Args:
        tv_id: TMDB TV show ID
        season: Season number (default: 1)
        episode: Episode number (default: 1)
        providers: Comma-separated provider names or "all"
    """
    endpoint = f"detail/tv/{tv_id}"
    params = {
        "season": season,
        "episode": episode,
        "providers": providers
    }
    return self._make_request(endpoint, params)
```

---

#### Task 1.2: Update Anime Detail Service
**File:** `streaming/services.py`

**Changes:**
```python
def get_anime_detail(self, anime_id: str, episode: int = None, providers: str = "all") -> Dict:
    """
    Get detailed information about an anime
    
    Args:
        anime_id: Anime slug (e.g., "one-piece-100")
        episode: Episode number (optional, for streaming sources)
        providers: Comma-separated provider names or "all"
    """
    endpoint = f"detail/anime/{anime_id}"
    params = {}
    
    if episode is not None:
        params["ep"] = episode
        params["providers"] = providers
    
    return self._make_request(endpoint, params)
```

---

### Phase 2: Backend Views (Priority: HIGH)

#### Task 2.1: Update TV Detail View
**File:** `streaming/views.py`

**Changes:**
```python
def tv_detail(request, tv_id):
    """TV show detail and player"""
    api = get_api_client()
    
    # Get parameters from request
    season = request.GET.get('season', 1)
    episode = request.GET.get('episode', 1)
    provider = request.GET.get('provider', 'all')
    
    try:
        season = int(season)
        episode = int(episode)
    except ValueError:
        season = 1
        episode = 1
    
    # Get TV show with episode details
    tv_show = api.get_tv_detail(tv_id, season=season, episode=episode, providers=provider)
    
    # Check for error
    if 'error' in tv_show:
        context = {
            'error': tv_show['error'],
            'title': 'Error',
        }
        return render(request, 'streaming/error.html', context)
    
    context = {
        'page_type': 'player',
        'content': tv_show,
        'content_type': 'tv',
        'current_season': season,
        'current_episode': episode,
        'title': tv_show.get('title', 'TV Show'),
    }
    
    return render(request, 'streaming/player.html', context)
```

---

#### Task 2.2: Update Anime Detail View
**File:** `streaming/views.py`

**Changes:**
```python
def anime_detail(request, anime_id):
    """Anime detail and player"""
    api = get_api_client()
    
    # Get parameters from request
    episode = request.GET.get('ep')
    provider = request.GET.get('provider', 'all')
    
    # Convert episode to int if provided
    if episode:
        try:
            episode = int(episode)
        except ValueError:
            episode = None
    
    # Get anime details
    anime = api.get_anime_detail(anime_id, episode=episode, providers=provider)
    
    # Check for error
    if 'error' in anime:
        context = {
            'error': anime['error'],
            'title': 'Error',
        }
        return render(request, 'streaming/error.html', context)
    
    context = {
        'page_type': 'player',
        'content': anime,
        'content_type': 'anime',
        'current_episode': episode,
        'title': anime.get('title', 'Anime'),
    }
    
    return render(request, 'streaming/player.html', context)
```

---

### Phase 3: Frontend Template (Priority: MEDIUM)

#### Task 3.1: Add TV Episode Selector
**File:** `templates/streaming/player.html`

**Add:**
```html
{% if content_type == 'tv' and content.seasons %}
<!-- Season & Episode Selector -->
<div class="mb-6">
    <div class="flex gap-4">
        <!-- Season Selector -->
        <div class="flex-1">
            <label class="text-xs text-secondary mb-2 block">SEASON</label>
            <select id="season-selector" 
                    class="w-full bg-card border border-white/10 rounded-lg px-4 py-2 text-sm">
                {% for season in content.seasons %}
                <option value="{{ season.seasonNumber }}" 
                        {% if season.seasonNumber == current_season %}selected{% endif %}>
                    Season {{ season.seasonNumber }} ({{ season.episodeCount }} episodes)
                </option>
                {% endfor %}
            </select>
        </div>
        
        <!-- Episode Selector -->
        <div class="flex-1">
            <label class="text-xs text-secondary mb-2 block">EPISODE</label>
            <select id="episode-selector" 
                    class="w-full bg-card border border-white/10 rounded-lg px-4 py-2 text-sm">
                {% for ep in content.episodes %}
                <option value="{{ ep.episode_number }}"
                        {% if ep.episode_number == current_episode %}selected{% endif %}>
                    Ep {{ ep.episode_number }}: {{ ep.name|truncatewords:5 }}
                </option>
                {% endfor %}
            </select>
        </div>
    </div>
</div>

<script>
// Handle season/episode change
document.getElementById('season-selector').addEventListener('change', function(e) {
    const season = e.target.value;
    window.location.href = `?season=${season}&episode=1`;
});

document.getElementById('episode-selector').addEventListener('change', function(e) {
    const season = {{ current_season }};
    const episode = e.target.value;
    window.location.href = `?season=${season}&episode=${episode}`;
});
</script>
{% endif %}
```

---

#### Task 3.2: Add Anime Episode Selector
**File:** `templates/streaming/player.html`

**Add:**
```html
{% if content_type == 'anime' %}
<!-- Episode Selector for Anime -->
<div class="mb-6">
    <div class="flex gap-4 items-end">
        <!-- Episode Selector -->
        <div class="flex-1">
            <label class="text-xs text-secondary mb-2 block">EPISODE</label>
            <select id="anime-episode-selector" 
                    class="w-full bg-card border border-white/10 rounded-lg px-4 py-2 text-sm">
                {% for i in content.totalEpisodes|make_list_range %}
                <option value="{{ i }}" {% if i == current_episode %}selected{% endif %}>
                    Episode {{ i }}
                </option>
                {% endfor %}
            </select>
        </div>
        
        <!-- SUB/DUB Selector -->
        {% if content.availableEpisodes %}
        <div>
            <label class="text-xs text-secondary mb-2 block">AUDIO</label>
            <div class="flex gap-2">
                {% if content.availableEpisodes.sub %}
                <button class="sub-dub-btn active px-4 py-2 rounded-lg text-sm font-bold bg-accent">
                    SUB
                </button>
                {% endif %}
                {% if content.availableEpisodes.dub %}
                <button class="sub-dub-btn px-4 py-2 rounded-lg text-sm font-bold bg-card border border-white/10">
                    DUB
                </button>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
</div>

<script>
// Handle episode change
document.getElementById('anime-episode-selector').addEventListener('change', function(e) {
    const episode = e.target.value;
    window.location.href = `?ep=${episode}`;
});

// Handle SUB/DUB toggle
document.querySelectorAll('.sub-dub-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Toggle active state
        document.querySelectorAll('.sub-dub-btn').forEach(b => {
            b.classList.remove('active', 'bg-accent');
            b.classList.add('bg-card', 'border', 'border-white/10');
        });
        this.classList.add('active', 'bg-accent');
        this.classList.remove('bg-card', 'border', 'border-white/10');
        
        // Reload with new type
        const episode = document.getElementById('anime-episode-selector').value;
        const type = this.textContent.trim().toLowerCase();
        window.location.href = `?ep=${episode}&type=${type}`;
    });
});
</script>
{% endif %}
```

---

### Phase 4: Video Player Integration (Priority: HIGH)

#### Task 4.1: Update Player Embed Logic
**File:** `templates/streaming/player.html`

**Current Issue:**
Player doesn't show correct streaming source for TV episodes and Anime episodes

**Fix:**
```html
{% if content.sources and content.sources|length > 0 %}
    {% if content_type == 'tv' %}
        <!-- TV Episode Player -->
        <iframe 
            src="{{ content.sources.0.url }}"
            class="w-full aspect-video rounded-2xl"
            allowfullscreen
            frameborder="0">
        </iframe>
    {% elif content_type == 'anime' %}
        <!-- Anime Episode Player -->
        <iframe 
            src="{{ content.sources.0.url }}"
            class="w-full aspect-video rounded-2xl"
            allowfullscreen
            frameborder="0">
        </iframe>
    {% else %}
        <!-- Movie Player -->
        <iframe 
            src="{{ content.sources.0.url }}"
            class="w-full aspect-video rounded-2xl"
            allowfullscreen
            frameborder="0">
        </iframe>
    {% endif %}
{% else %}
    <!-- No streaming source available -->
    <div class="w-full aspect-video rounded-2xl bg-card flex items-center justify-center">
        <p class="text-secondary">No streaming sources available</p>
    </div>
{% endif %}
```

---

## 🎯 Implementation Order

### Step 1: Fix Backend Services (30 min)
1. ✅ Update `streaming/services.py` - `get_tv_detail()`
2. ✅ Update `streaming/services.py` - `get_anime_detail()`

### Step 2: Fix Backend Views (20 min)
3. ✅ Update `streaming/views.py` - `tv_detail()`
4. ✅ Update `streaming/views.py` - `anime_detail()`

### Step 3: Update Templates (40 min)
5. ✅ Add TV season/episode selector UI
6. ✅ Add Anime episode selector UI
7. ✅ Add SUB/DUB toggle for anime
8. ✅ Fix video player embed logic

### Step 4: Testing (20 min)
9. ✅ Test TV series flow (Breaking Bad S1E1)
10. ✅ Test Anime flow (One Piece Ep 1)
11. ✅ Test episode navigation
12. ✅ Test provider switching

**Total Estimated Time:** ~2 hours

---

## 📝 Test Cases

### TV Series Test
```
URL: http://localhost:8000/tv/1396/?season=1&episode=1
Expected:
- Show Breaking Bad S1E1
- Display episode title
- Show streaming sources
- Video player loads
- Season/Episode selector works
```

### Anime Test
```
URL: http://localhost:8000/anime/one-piece-100/?ep=1
Expected:
- Show One Piece Episode 1
- Display episode title
- Show SUB/DUB availability
- Streaming sources available
- Video player loads
- Episode selector works
```

---

## 🚨 Critical Points

1. **Episode parameter is mandatory** for streaming sources
2. **Without episode**, API returns only basic info (no sources)
3. **Default episode should be 1** when not specified
4. **Provider parameter** should default to "all"
5. **Template must handle** missing episodes gracefully

---

**Priority:** HIGH  
**Complexity:** Medium  
**Impact:** Critical (blocks TV/Anime streaming)
