# 🧪 MANUAL TESTING GUIDE - Watchlist & History

## ✅ Test Checklist

### 1. Test Watchlist Button (Home Page)
**Steps:**
1. Go to: http://localhost:8000/
2. Hover over any card in carousel
3. Click **"+ WATCHLIST"** button
4. Button should change to **"✓ ADDED"** with green background
5. Green background disappears after 2 seconds

**Expected Result:** ✅ Button shows feedback

---

### 2. Test Watchlist Button (Grid Section)
**Steps:**
1. Scroll down to "MOST POPULAR" grid
2. Hover over any card
3. Click **"+ WATCHLIST"** button
4. Same feedback as above

**Expected Result:** ✅ All cards have button

---

### 3. Test Watchlist Button (Search Page)
**Steps:**
1. Search for "naruto" or any keyword
2. Hover over result cards
3. Click **"+ WATCHLIST"** button

**Expected Result:** ✅ Search results have button

---

### 4. Test Profile Page - View Watchlist
**Steps:**
1. Add 3-5 items to watchlist
2. Go to: http://localhost:8000/profile/
3. Check stats numbers (To Watch should show 3-5)
4. Scroll down to see watchlist grid
5. Items should appear with posters

**Expected Result:** ✅ Watchlist displays correctly

---

### 5. Test Remove from Watchlist
**Steps:**
1. On profile page, find watchlist item
2. Click **trash icon (🗑️)** button
3. Page should reload
4. Item should be removed
5. Stats should decrease by 1

**Expected Result:** ✅ Remove works

---

### 6. Test Auto-Track History (Movie)
**Steps:**
1. Go to any movie player page
   Example: http://localhost:8000/movie/1265609/
2. Open browser console (F12)
3. Look for: "✅ Added to history: [Movie Title]"
4. Go to profile page
5. Check "Watching" stat increased

**Expected Result:** ✅ History auto-tracked

---

### 7. Test Auto-Track History (TV Series)
**Steps:**
1. Go to TV series player
   Example: http://localhost:8000/tv/1396/?season=1&episode=1
2. Check console for history log
3. Should save with season & episode data

**Expected Result:** ✅ TV tracked with S/E info

---

### 8. Test Auto-Track History (Anime)
**Steps:**
1. Go to anime player
   Example: http://localhost:8000/anime/one-piece-100/?ep=1
2. Check console for history log
3. Should save with episode number

**Expected Result:** ✅ Anime tracked with episode

---

### 9. Test LocalStorage Persistence
**Steps:**
1. Add items to watchlist
2. Refresh page (F5)
3. Go to profile
4. Items should still be there

**Expected Result:** ✅ Data persists

---

### 10. Test Browser Console Commands
Open browser console (F12) and test:

```javascript
// Check if KortekStream is loaded
console.log(typeof KortekStream);
// Should output: "object"

// Get watchlist
console.log(KortekStream.getWatchlist());
// Should output: Array of items

// Get stats
console.log(KortekStream.getStats());
// Should output: {watching: X, toWatch: Y, watched: Z, collections: 0}

// Get history
console.log(KortekStream.getHistory());
// Should output: Array of watched items

// Manual add test
KortekStream.addToWatchlist({
    id: 'test123',
    type: 'movie',
    title: 'Test Movie',
    poster: 'https://via.placeholder.com/300x450'
});
// Should return: true

// Check it was added
console.log(KortekStream.getWatchlist());
// Should include test item
```

**Expected Result:** ✅ All console commands work

---

## 🐛 Common Issues & Solutions

### Issue 1: "KortekStream is not defined"
**Solution:** Refresh page, script might not be loaded yet

### Issue 2: Button doesn't work
**Solution:** Check browser console for JavaScript errors

### Issue 3: Data not saving
**Solution:** 
- Check if localStorage is enabled
- Try in Incognito mode
- Clear browser cache

### Issue 4: Profile page shows 0 for all stats
**Solution:**
- Add items first
- Check console for errors
- Refresh page

---

## 📊 Expected Behavior Summary

| Action | Result |
|--------|--------|
| Click + WATCHLIST | Shows ✓ ADDED + green flash |
| Add 5 items | Profile shows "To Watch: 5" |
| Watch movie | "Watching: 1" increases |
| Remove item | Count decreases |
| Refresh page | All data persists |

---

## 🔍 Debug Mode

If something doesn't work, run in console:
```javascript
// Enable debug mode
localStorage.setItem('debug', 'true');

// Check all stored data
console.log('Watchlist:', localStorage.getItem('kortekstream_watchlist'));
console.log('History:', localStorage.getItem('kortekstream_history'));
console.log('Completed:', localStorage.getItem('kortekstream_completed'));

// Clear all data (reset)
localStorage.removeItem('kortekstream_watchlist');
localStorage.removeItem('kortekstream_history');
localStorage.removeItem('kortekstream_completed');
location.reload();
```

---

**Status:** Ready for manual testing!

