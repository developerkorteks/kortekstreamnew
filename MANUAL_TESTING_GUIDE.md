# Manual Testing Guide - StreameX Platform

## Quick Start

### Prerequisites
1. **API Server** running on `http://localhost:5000`
2. **Django Server** running on `http://localhost:8000`

### Start Servers

```bash
# Terminal 1: Start Go API Server
cd /path/to/api
go run main.go

# Terminal 2: Start Django App
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

## Testing Flows

### 🎬 FLOW 1: Movie Streaming

#### Step 1: Browse Movies
- **URL:** `http://localhost:8000/`
- **Action:** Navigate to Movies section
- **Expected:** Grid of popular movies with posters

#### Step 2: Select Movie
- **Action:** Click on a movie (e.g., "Inception")
- **URL Changes to:** `http://localhost:8000/movie/27205/`
- **Expected:**
  - Movie title, overview, rating
  - Backdrop image
  - Release date, runtime, genres
  - "WATCH NOW" button

#### Step 3: Watch Movie
- **Action:** Click "WATCH NOW"
- **URL Changes to:** `http://localhost:8000/movie/27205/?provider=vidsrc`
- **Expected:**
  - Video player embedded
  - Player controls visible
  - Video loads and plays

#### API Test
```bash
# Get movie with streaming sources
curl "http://localhost:5000/api/movie/27205?providers=all" | jq .
```

**Expected Response:**
```json
{
  "title": "Inception",
  "sources": [
    {
      "provider": "vidsrc",
      "url": "https://vidsrc.xyz/embed/movie/27205"
    }
  ]
}
```

---

### 📺 FLOW 2: TV Series Streaming

#### Step 1: Browse TV Shows
- **URL:** `http://localhost:8000/tv/`
- **Action:** Browse popular TV series
- **Expected:** Grid of TV shows

#### Step 2: Select Series
- **Action:** Click on "Breaking Bad"
- **URL Changes to:** `http://localhost:8000/tv/1396/`
- **Expected:**
  - Series information
  - Season selector
  - Episode selector
  - "WATCH NOW" button

#### Step 3: Select Episode
- **Action:** Choose Season 1, Episode 1
- **Expected:** Episode title and info displayed

#### Step 4: Watch Episode
- **Action:** Click "WATCH NOW"
- **URL Changes to:** `http://localhost:8000/tv/1396/?season=1&episode=1`
- **Expected:**
  - Video player embedded
  - Episode navigation (Next/Previous)
  - Video plays

#### API Test
```bash
# Get TV episode with streaming
curl "http://localhost:5000/api/detail/tv/1396?season=1&episode=1&providers=all" | jq .
```

**Expected Response:**
```json
{
  "title": "Breaking Bad",
  "currentEpisode": {
    "season": 1,
    "episode": 1,
    "title": "Pilot"
  },
  "sources": [
    {
      "provider": "vidsrc",
      "url": "https://vidsrc.xyz/embed/tv/1396/1/1"
    }
  ]
}
```

---

### 🎌 FLOW 3: Anime Streaming

#### Step 1: Browse Anime
- **URL:** `http://localhost:8000/anime/`
- **Action:** Browse anime list
- **Test Filters:** Popular, Top Airing, Trending, Recently Added
- **Expected:** Grid of anime with filter tabs working

#### Step 2: Select Anime
- **Action:** Click on "One Piece"
- **URL Changes to:** `http://localhost:8000/anime/one-piece-100/`
- **Expected:**
  - Anime information
  - Episode count
  - Episode selector
  - SUB/DUB availability
  - "WATCH NOW" button

#### Step 3: Select Episode
- **Action:** Choose Episode 1
- **Action:** Select SUB or DUB
- **Expected:** Episode info updates

#### Step 4: Watch Episode
- **Action:** Click "WATCH NOW"
- **URL Changes to:** `http://localhost:8000/anime/one-piece-100/?ep=1`
- **Expected:**
  - Video player embedded
  - Episode navigation
  - SUB/DUB switcher
  - Video plays

#### API Test
```bash
# Get anime episode with streaming
curl "http://localhost:5000/api/detail/anime/one-piece-100?ep=1&providers=all" | jq .
```

**Expected Response:**
```json
{
  "title": "One Piece",
  "availableEpisodes": {
    "sub": 1122,
    "dub": 1085
  },
  "currentEpisode": {
    "number": 1,
    "title": "I'm Luffy! The Man Who's Gonna Be King of the Pirates!"
  },
  "sources": [
    {
      "provider": "gogoanime",
      "type": "sub",
      "url": "https://gogoanime.hu/one-piece-episode-1"
    }
  ]
}
```

---

### 🔍 FLOW 4: Search

#### Step 1: Use Search
- **URL:** `http://localhost:8000/`
- **Action:** Enter "naruto" in search box
- **Action:** Submit search
- **URL Changes to:** `http://localhost:8000/search/?q=naruto`

#### Step 2: View Results
- **Expected:**
  - Mixed results (Movies, TV, Anime)
  - Type badges visible (MOVIE, TV, ANIME)
  - Posters displayed
  - Result count shown

#### Step 3: Click Result
- **Action:** Click on any result
- **Expected:** Navigate to correct detail page

#### API Test
```bash
# Search for content
curl "http://localhost:5000/api/search?query=naruto&page=1" | jq .
```

**Expected Response:**
```json
[
  {
    "id": "46260",
    "title": "Naruto",
    "type": "tv",
    "poster": "https://image.tmdb.org/t/p/w342/...",
    "vote_average": 8.361
  }
]
```

---

## API Endpoints Reference

### Search
```bash
# All categories
GET /api/search?query=naruto&page=1

# Specific category
GET /api/search?query=inception&category=movie&page=1
GET /api/search?query=breaking%20bad&category=tv&page=1
GET /api/search?query=one%20piece&category=anime&page=1
```

### List
```bash
# Movies
GET /api/list/movie?page=1

# TV Shows
GET /api/list/tv?page=1

# Anime (with status filters)
GET /api/list/anime?page=1
GET /api/list/anime?status=top-airing&page=1
GET /api/list/anime?status=trending&page=1
GET /api/list/anime?status=recently-added&page=1
```

### Movie Detail
```bash
# Basic info
GET /api/movie/27205

# With streaming sources
GET /api/movie/27205?providers=all
GET /api/movie/27205?providers=vidsrc
GET /api/movie/27205?providers=vidsrc,vidlink
```

### TV Detail
```bash
# Basic info
GET /api/detail/tv/1396

# With episode streaming
GET /api/detail/tv/1396?season=1&episode=1
GET /api/detail/tv/1396?season=1&episode=1&providers=all
GET /api/detail/tv/1396?season=1&episode=1&providers=vidsrc
```

### Anime Detail
```bash
# Basic info
GET /api/detail/anime/one-piece-100

# With episode streaming
GET /api/detail/anime/one-piece-100?ep=1
GET /api/detail/anime/one-piece-100?ep=1&providers=all
GET /api/detail/anime/one-piece-100?ep=1&providers=gogoanime
```

### Provider Health
```bash
# All providers
GET /api/providers/health

# By category
GET /api/providers/health?category=movie
GET /api/providers/health?category=tv
GET /api/providers/health?category=anime

# Specific provider
GET /api/providers/health?provider=vidsrc
```

---

## Test Checklist

### ✅ Essential Features

#### Homepage
- [ ] Hero banner displays
- [ ] "Special for You" section shows 8 items
- [ ] "Most Popular" grid loads
- [ ] Navigation menu works
- [ ] Search bar visible
- [ ] Carousel navigation works

#### Movies
- [ ] Movie list loads with posters
- [ ] Pagination works
- [ ] Movie detail page shows all info
- [ ] Streaming sources available
- [ ] Video player loads
- [ ] Video plays successfully

#### TV Series
- [ ] TV list loads with posters
- [ ] Series detail shows seasons
- [ ] Episode selector works
- [ ] Season selector works
- [ ] Streaming sources available
- [ ] Episode navigation works
- [ ] Video plays successfully

#### Anime
- [ ] Anime list loads
- [ ] Filter tabs work (Popular, Airing, Trending, New)
- [ ] Anime detail shows episode count
- [ ] Episode selector works
- [ ] SUB/DUB indicator shows
- [ ] Streaming sources available
- [ ] Episode navigation works
- [ ] Video plays successfully

#### Search
- [ ] Search bar accepts input
- [ ] Search executes correctly
- [ ] Results display properly
- [ ] Type badges show (MOVIE/TV/ANIME)
- [ ] Result links work
- [ ] Pagination works (if many results)

#### General
- [ ] All images load correctly
- [ ] No console errors
- [ ] Mobile responsive (test on mobile view)
- [ ] Links work correctly
- [ ] Error pages show for invalid IDs

---

## Common Issues & Solutions

### Issue: API not responding
**Solution:**
```bash
# Check if API is running
ps aux | grep "main"

# If not, start it
cd /path/to/api
go run main.go
```

### Issue: Django not loading
**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Issue: Video not playing
**Possible Causes:**
1. Provider is down - Try different provider
2. Content ID invalid - Check API response
3. Network issue - Check internet connection

**Debug:**
```bash
# Check streaming sources
curl "http://localhost:5000/api/movie/27205?providers=all" | jq .sources
```

### Issue: Images not loading
**Check:**
1. TMDB API is accessible
2. Image URLs are valid
3. CORS settings correct

---

## Performance Benchmarks

### Expected Response Times

| Endpoint Type | Expected Time |
|--------------|---------------|
| Search | < 3 seconds |
| List | < 2 seconds |
| Detail (no streaming) | < 2 seconds |
| Detail (with streaming) | < 5 seconds |
| Provider Health | < 20 seconds |

### Page Load Times

| Page | Expected Time |
|------|---------------|
| Homepage | < 2 seconds |
| List pages | < 2 seconds |
| Detail pages | < 3 seconds |
| Player pages | < 4 seconds |

---

## Test Data

### Recommended Test IDs

**Movies:**
- Inception: `27205`
- The Dark Knight: `155`
- Interstellar: `157336`

**TV Series:**
- Breaking Bad: `1396`
- Game of Thrones: `1399`
- The Walking Dead: `1402`

**Anime:**
- One Piece: `one-piece-100`
- Naruto: `naruto`
- Attack on Titan: `attack-on-titan`

**Search Queries:**
- Popular: "naruto", "inception", "breaking bad"
- Specific: "one piece", "game of thrones"
- General: "action", "comedy", "anime"

---

## Notes

- All streaming sources use embed URLs
- Provider availability may vary
- Some older content may have limited providers
- API response times depend on external services
- Health check is non-critical (used for monitoring only)

---

**Last Updated:** March 18, 2026  
**Version:** 1.0
