/**
 * KortekStream - Watchlist & History Management (LocalStorage)
 * Stores user's watchlist and viewing history in browser
 */

const KortekStream = {
    // Get watchlist from localStorage
    getWatchlist() {
        const data = localStorage.getItem('kortekstream_watchlist');
        return data ? JSON.parse(data) : [];
    },

    // Add item to watchlist
    addToWatchlist(item) {
        const watchlist = this.getWatchlist();
        const exists = watchlist.find(i => i.id === item.id && i.type === item.type);
        
        if (!exists) {
            watchlist.unshift({
                id: item.id,
                type: item.type, // movie, tv, anime
                title: item.title,
                poster: item.poster,
                addedAt: new Date().toISOString()
            });
            localStorage.setItem('kortekstream_watchlist', JSON.stringify(watchlist));
            return true;
        }
        return false;
    },

    // Remove from watchlist
    removeFromWatchlist(id, type) {
        let watchlist = this.getWatchlist();
        watchlist = watchlist.filter(i => !(i.id === id && i.type === type));
        localStorage.setItem('kortekstream_watchlist', JSON.stringify(watchlist));
    },

    // Check if item is in watchlist
    isInWatchlist(id, type) {
        const watchlist = this.getWatchlist();
        return watchlist.some(i => i.id === id && i.type === type);
    },

    // Get viewing history
    getHistory() {
        const data = localStorage.getItem('kortekstream_history');
        return data ? JSON.parse(data) : [];
    },

    // Add to viewing history
    addToHistory(item) {
        let history = this.getHistory();
        
        // Remove if already exists (to update position)
        history = history.filter(i => !(i.id === item.id && i.type === item.type));
        
        // Add to top
        history.unshift({
            id: item.id,
            type: item.type,
            title: item.title,
            poster: item.poster,
            episode: item.episode || null,
            season: item.season || null,
            watchedAt: new Date().toISOString(),
            progress: item.progress || 0 // percentage watched
        });
        
        // Keep only last 50 items
        if (history.length > 50) {
            history = history.slice(0, 50);
        }
        
        localStorage.setItem('kortekstream_history', JSON.stringify(history));
    },

    // Get completed items
    getCompleted() {
        const data = localStorage.getItem('kortekstream_completed');
        return data ? JSON.parse(data) : [];
    },

    // Mark as completed
    markCompleted(item) {
        let completed = this.getCompleted();
        
        const exists = completed.find(i => i.id === item.id && i.type === item.type);
        if (!exists) {
            completed.unshift({
                id: item.id,
                type: item.type,
                title: item.title,
                poster: item.poster,
                completedAt: new Date().toISOString(),
                rating: item.rating || null
            });
            localStorage.setItem('kortekstream_completed', JSON.stringify(completed));
        }
    },

    // Get stats
    getStats() {
        return {
            watching: this.getHistory().length,
            toWatch: this.getWatchlist().length,
            watched: this.getCompleted().length,
            collections: 0 // For future implementation
        };
    }
};

// Make globally available
window.KortekStream = KortekStream;
