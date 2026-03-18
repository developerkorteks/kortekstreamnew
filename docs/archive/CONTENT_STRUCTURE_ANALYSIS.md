# 🔍 CONTENT STRUCTURE ANALYSIS - Movie vs TV vs Anime

## 📊 API Response Structures

### 1. MOVIE
```json
{
  "id": "1265609",
  "title": "War Machine",
  "poster": "https://image.tmdb.org/t/p/w500/...",
  "backdrop_path": "/...",
  "release_date": "2026-01-10",
  "vote_average": 8.5,
  "episodes": [
    {
      "sources": [
        {"provider": "streamx", "url": "..."},
        {"provider": "vidsrc", "url": "..."}
      ]
    }
  ]
}
```

**Key Points:**
- Single episode with sources
- No season/episode number
- URL: `/movie/{id}/`
- Type: `movie`

---

### 2. TV SERIES
```json
{
  "id": "1396",
  "name": "Breaking Bad",
  "poster_path": "/...",
  "backdrop_path": "/...",
  "first_air_date": "2008-01-20",
  "vote_average": 9.5,
  "seasons": [...],
  "episodes": [
    {
      "episode_number": 1,
      "name": "Pilot",
      "still_path": "/...",
      "sources": [...]
    }
  ]
}
```

**Key Points:**
- Multiple seasons & episodes
- URL: `/tv/{id}/?season=X&episode=Y`
- Type: `tv`
- Uses `name` instead of `title`

---

### 3. ANIME
```json
{
  "id": "one-piece-100",
  "title": "One Piece",
  "poster": "https://...",
  "image": "https://...",
  "episodes": [
    {
      "episode_no": 1,
      "title": "Episode 1",
      "sources": [...]
    }
  ]
}
```

**Key Points:**
- Episode-based (no seasons)
- URL: `/anime/{id}/?ep=X`
- Type: `anime`
- Uses `episode_no` instead of `episode_number`

---

## 🎯 Template Context Variables

### Player Page Context

#### Movie:
```python
context = {
    'content_type': 'movie',
    'content': {
        'id': '1265609',
        'title': 'War Machine',
        'poster': '...',
        # ...
    }
}
```

#### TV Series:
```python
context = {
    'content_type': 'tv',
    'current_season': 1,
    'current_episode': 5,
    'content': {
        'id': '1396',
        'name': 'Breaking Bad',
        'poster_path': '...',
        # ...
    }
}
```

#### Anime:
```python
context = {
    'content_type': 'anime',
    'current_episode': 100,
    'content': {
        'id': 'one-piece-100',
        'title': 'One Piece',
        'poster': '...',
        # ...
    }
}
```

---

## 🔧 History Tracking Implementation

### What to Track:

```javascript
// MOVIE
{
  id: content.id,
  type: 'movie',
  title: content.title,
  poster: content.poster || content.poster_path,
  watchedAt: new Date().toISOString()
}

// TV SERIES
{
  id: content.id,
  type: 'tv',
  title: content.name,
  poster: content.poster_path,
  season: current_season,
  episode: current_episode,
  watchedAt: new Date().toISOString()
}

// ANIME
{
  id: content.id,
  type: 'anime',
  title: content.title,
  poster: content.poster || content.image,
  episode: current_episode,
  watchedAt: new Date().toISOString()
}
```

---

## 📝 Template Variable Mapping

| Field | Movie | TV | Anime |
|-------|-------|----|----|
| **ID** | `content.id` | `content.id` | `content.id` |
| **Type** | `movie` | `tv` | `anime` |
| **Title** | `content.title` | `content.name` | `content.title` |
| **Poster** | `content.poster` or `content.poster_path` | `content.poster_path` | `content.poster` or `content.image` |
| **Season** | N/A | `current_season` | N/A |
| **Episode** | N/A | `current_episode` | `current_episode` |

---

## 🎬 Player Page URLs

### Movie:
```
/movie/1265609/
```

### TV Series:
```
/tv/1396/?season=1&episode=5
```

### Anime:
```
/anime/one-piece-100/?ep=100
```

---

## ✅ Implementation Plan

### 1. Auto-Track History on Player Load
Add to `player.html` at bottom:

```javascript
<script>
document.addEventListener('DOMContentLoaded', function() {
    if (typeof KortekStream !== 'undefined') {
        const content = {
            id: '{{ content.id }}',
            type: '{{ content_type }}',
            title: '{% if content.title %}{{ content.title|escapejs }}{% else %}{{ content.name|escapejs }}{% endif %}',
            poster: '{% if content.poster %}{{ content.poster }}{% elif content.poster_path %}https://image.tmdb.org/t/p/w500{{ content.poster_path }}{% elif content.image %}{{ content.image }}{% endif %}',
            {% if content_type == 'tv' %}
            season: {{ current_season|default:'null' }},
            episode: {{ current_episode|default:'null' }},
            {% elif content_type == 'anime' %}
            episode: {{ current_episode|default:'null' }},
            {% endif %}
        };
        
        KortekStream.addToHistory(content);
        console.log('Added to history:', content.title);
    }
});
</script>
```

### 2. Add Watchlist Button to Cards
Unified approach for all card types:

```html
<button onclick="event.preventDefault(); 
                 const item = {
                     id: '{{ item.id }}',
                     type: '{{ page_type }}',
                     title: '{% if item.title %}{{ item.title|escapejs }}{% else %}{{ item.name|escapejs }}{% endif %}',
                     poster: '{% if item.poster %}{{ item.poster }}{% elif item.poster_path %}https://image.tmdb.org/t/p/w500{{ item.poster_path }}{% endif %}'
                 };
                 if(KortekStream.addToWatchlist(item)) {
                     this.innerHTML = '✓ ADDED';
                     this.classList.add('bg-green-500');
                 }" 
        class="glass px-3 py-1.5 rounded-lg text-[9px] font-bold hover:bg-accent transition-all">
    + WATCHLIST
</button>
```

---

**Status: Ready to implement** ✅

