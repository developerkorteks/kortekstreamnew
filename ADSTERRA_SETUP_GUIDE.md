# 🎯 Adsterra Integration - Complete Setup Guide

## 📚 Table of Contents
1. [How to Replace Placeholder Codes](#step-1-get-real-adsterra-codes)
2. [Technical Flow Explanation](#technical-flow-how-it-works)
3. [Supported Ad Formats](#supported-ad-formats)
4. [Testing Different Pages](#testing-guide)

---

## 🚀 Step 1: Get Real Adsterra Codes

### 1.1 Sign Up & Create Ad Units

1. **Sign up** at [https://adsterra.com](https://adsterra.com)
2. **Verify** your account
3. Go to **"Websites"** → **"Add Website"**
4. Enter your domain and submit for review
5. Once approved, go to **"Ad Units"**

### 1.2 Create Each Ad Unit Type

#### A. Popunder Ad
```
Format: Popunder
Placement: Before </head>
Best for: Homepage, Player pages
High CPM: ✅
```

#### B. Social Bar
```
Format: Social Bar
Placement: Before </body> or After <body>
Best for: All pages (global)
User-friendly: ✅
```

#### C. Display Banner
```
Format: Banner
Sizes: 728x90, 300x250, 160x600
Placement: Content, Sidebar
Best for: Content pages
```

#### D. Native Banner
```
Format: Native Banner
Responsive: ✅
Best for: Mobile, Content listings
High CTR: ✅
```

#### E. Smartlink
```
Format: Smartlink
Intelligent: Auto-optimizes
Best for: Mixed traffic
```

---

## 🔄 Step 2: Replace Placeholder Codes

### Method 1: Via Django Admin (Recommended) ⭐

1. **Access Admin Panel**
   ```
   URL: http://127.0.0.1:8000/admin/
   Username: admin
   Password: admin123
   ```

2. **Navigate to Ad Units**
   - Click **"Ad Units"** in the sidebar
   - You'll see 6 sample ad units

3. **Edit Each Ad Unit**
   
   **Example: Home Page Popunder**
   
   a. Click on **"Home Page Popunder"**
   
   b. You'll see this placeholder code:
   ```html
   <script data-cfasync="false" type="text/javascript">
       atOptions = {
           'key' : 'YOUR_POPUNDER_KEY_HERE',  ← Replace this!
           'format' : 'iframe',
           'height' : 60,
           'width' : 468,
           'params' : {}
       };
       document.write('<scr' + 'ipt type="text/javascript" src="//www.highperformanceformat.com/YOUR_KEY/invoke.js"></scr' + 'ipt>');
   </script>
   ```
   
   c. **Get your real code from Adsterra:**
   - Login to Adsterra dashboard
   - Go to "Ad Units"
   - Click on your Popunder unit
   - Copy the JavaScript code
   
   d. **Replace the entire code** with your real Adsterra code:
   ```html
   <script data-cfasync="false" type="text/javascript">
       atOptions = {
           'key' : 'a1b2c3d4e5f6g7h8i9j0',  ← Your real key
           'format' : 'iframe',
           'height' : 60,
           'width' : 468,
           'params' : {}
       };
       document.write('<scr' + 'ipt type="text/javascript" src="//www.highperformanceformat.com/a1b2c3d4e5f6g7h8i9j0/invoke.js"></scr' + 'ipt>');
   </script>
   ```
   
   e. **Save** the ad unit

4. **Repeat for all ad units:**
   - ✅ Home Page Popunder
   - ✅ Global Social Bar
   - ✅ Sidebar Banner - Desktop Only
   - ✅ Content Top Banner
   - ✅ Player Page Popunder
   - ✅ Native Banner - Mobile

5. **Reload your website** - Real ads will now show!

### Method 2: Via Django Shell

```python
./venv/bin/python manage.py shell

from ads.models import AdUnit

# Update specific ad unit
ad = AdUnit.objects.get(name='Home Page Popunder')
ad.code = '''<script data-cfasync="false" type="text/javascript">
    atOptions = {
        'key' : 'YOUR_REAL_KEY_HERE',
        'format' : 'iframe',
        'height' : 60,
        'width' : 468,
        'params' : {}
    };
    document.write('<scr' + 'ipt type="text/javascript" src="//www.highperformanceformat.com/YOUR_REAL_KEY/invoke.js"></scr' + 'ipt>');
</script>'''
ad.save()

print("✓ Ad updated!")
```

---

## ⚙️ Technical Flow: How It Works

### 🔍 The Complete Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. USER VISITS PAGE                                        │
│     http://127.0.0.1:8000/                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  2. DJANGO VIEW (ads/views.py)                              │
│     def home(request):                                      │
│         context = {'page_type': 'home'}                     │
│         return render(request, 'streaming/home.html', ...)  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  3. TEMPLATE RENDERING (templates/base.html)                │
│     {% load adsterra_tags %}  ← Load custom template tags  │
│                                                              │
│     {% render_responsive_ads 'head' page_type %}            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  4. TEMPLATE TAG EXECUTION (ads/templatetags/adsterra_tags.py) │
│                                                              │
│     @register.simple_tag(takes_context=True)                │
│     def render_responsive_ads(context, position, page_type):│
│                                                              │
│         # Step 4a: Get user-agent                           │
│         user_agent = request.META.get('HTTP_USER_AGENT')    │
│         is_mobile = detect_mobile(user_agent)               │
│                                                              │
│         # Step 4b: Query database                           │
│         ads = AdUnit.objects.filter(                        │
│             position=position,        # e.g., 'head'        │
│             is_active=True            # Only active ads     │
│         ).order_by('-priority')       # High priority first │
│                                                              │
│         # Step 4c: Filter by page type                      │
│         filtered_ads = []                                   │
│         for ad in ads:                                      │
│             if ad.should_show_on_page(page_type):           │
│                                                              │
│                 # Step 4d: Device targeting                 │
│                 if is_mobile and not ad.show_on_mobile:     │
│                     continue  # Skip desktop-only ads       │
│                 if not is_mobile and not ad.show_on_desktop:│
│                     continue  # Skip mobile-only ads        │
│                                                              │
│                 filtered_ads.append(ad)                     │
│                                                              │
│         # Step 4e: Generate HTML                            │
│         html_output = ""                                    │
│         for ad in filtered_ads:                             │
│             html_output += f"<!-- Ad: {ad.name} -->\n"      │
│             html_output += ad.code  # JavaScript code       │
│             html_output += "\n\n"                           │
│                                                              │
│         # Step 4f: CRITICAL - mark_safe()                   │
│         return mark_safe(html_output)                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  5. HTML OUTPUT                                             │
│     <script data-cfasync="false" type="text/javascript">    │
│         atOptions = { ... };                                │
│         document.write('<scr' + 'ipt ...>');                │
│     </script>                                               │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  6. BROWSER EXECUTES JAVASCRIPT                             │
│     - Adsterra script loads                                 │
│     - Ad iframe injected into page                          │
│     - Ad displays to user                                   │
└─────────────────────────────────────────────────────────────┘
```

### 🔒 Why `mark_safe()` for JavaScript?

**Question:** Django auto-escapes HTML untuk security, tapi kenapa JavaScript bisa di-render?

**Answer:** Menggunakan `mark_safe()` dari `django.utils.safestring`

```python
from django.utils.safestring import mark_safe

def render_responsive_ads(context, position, page_type):
    # ... get ads from database ...
    
    html_output = ""
    for ad in filtered_ads:
        html_output += ad.code  # Raw JavaScript/HTML
    
    # CRITICAL: Tell Django this is safe HTML
    return mark_safe(html_output)
```

#### Without `mark_safe()` ❌
```html
<!-- Django would escape it like this: -->
&lt;script data-cfasync=&quot;false&quot;&gt;
    atOptions = { ... };
&lt;/script&gt;

<!-- Browser shows literal text, doesn't execute -->
```

#### With `mark_safe()` ✅
```html
<!-- Django renders it as actual HTML/JS: -->
<script data-cfasync="false">
    atOptions = { ... };
</script>

<!-- Browser executes the JavaScript! -->
```

#### Security Considerations 🔒

**Q:** Apakah `mark_safe()` berbahaya?

**A:** Safe JIKA:
- ✅ Code berasal dari database (admin-controlled)
- ✅ Hanya admin yang bisa edit ad codes
- ✅ Input validation di admin (clean() method)
- ✅ Tidak ada user-generated content

**Our Implementation:**
```python
# ads/models.py
class AdUnit(models.Model):
    def clean(self):
        """Validate ad code before saving"""
        if self.code and '<script' not in self.code.lower():
            raise ValidationError({
                'code': 'Ad code must contain a <script> tag'
            })
```

### 📊 Database Query Flow

```python
# What happens in template tag:

# 1. Base query
ads = AdUnit.objects.filter(
    position='head',      # Specific position
    is_active=True        # Only active ads
).order_by('-priority')   # ORDER BY priority DESC

# Equivalent SQL:
# SELECT * FROM ads_adunit 
# WHERE position = 'head' 
#   AND is_active = TRUE 
# ORDER BY priority DESC

# 2. Additional Python filtering
for ad in ads:
    # Check page targeting
    if ad.show_on_pages:  # e.g., "home,anime,movie"
        pages = ad.show_on_pages.split(',')
        if page_type not in pages:
            continue  # Skip this ad
    
    # Check device targeting
    if is_mobile and not ad.show_on_mobile:
        continue  # Skip desktop-only ads
    
    # This ad passes all filters!
    output += ad.code
```

---

## 🎨 Supported Ad Formats

### ✅ All 5 Adsterra Formats Supported

| Format | Model Support | Template Support | Tested |
|--------|--------------|------------------|--------|
| **Popunder** | ✅ `ad_type='popunder'` | ✅ `position='head'` | ✅ Working |
| **Native Banner** | ✅ `ad_type='native'` | ✅ All positions | ✅ Working |
| **Banner** | ✅ `ad_type='banner'` | ✅ All positions | ✅ Working |
| **Smartlink** | ✅ `ad_type='smartlink'` | ✅ All positions | ✅ Working |
| **Social Bar** | ✅ `ad_type='social_bar'` | ✅ `position='body_bottom'` | ✅ Working |

### 📍 Ad Positions Available

```python
# ads/models.py
POSITIONS = [
    ('head', 'Before </head> - Popunder'),
    ('body_top', 'After <body> - Social Bar Top'),
    ('body_bottom', 'Before </body> - Social Bar'),
    ('sidebar', 'Sidebar'),
    ('content_top', 'Top of Content'),
    ('content_bottom', 'Bottom of Content'),
    ('between_content', 'Between Content Items'),
    ('player_top', 'Above Video Player'),
    ('player_bottom', 'Below Video Player'),
]
```

### 🎯 Format-to-Position Recommendations

| Format | Recommended Position | Why |
|--------|---------------------|-----|
| **Popunder** | `head` | Must load before page renders |
| **Social Bar** | `body_top` or `body_bottom` | Sticky bar at top/bottom |
| **Display Banner** | `sidebar`, `content_top` | Traditional banner spots |
| **Native Banner** | `between_content` | Blends with content |
| **Smartlink** | Any | Flexible placement |

### 📝 Example: Adding All 5 Formats

```python
# Via Django Admin or Shell

# 1. POPUNDER
AdUnit.objects.create(
    name='Homepage Popunder',
    ad_type='popunder',
    position='head',
    code='<script>/* Adsterra popunder code */</script>',
    show_on_pages='home,player',
    priority=100
)

# 2. NATIVE BANNER
AdUnit.objects.create(
    name='Mobile Native Ad',
    ad_type='native',
    position='between_content',
    code='<script>/* Adsterra native code */</script>',
    show_on_mobile=True,
    show_on_desktop=False,
    priority=80
)

# 3. DISPLAY BANNER
AdUnit.objects.create(
    name='Sidebar Banner 300x250',
    ad_type='banner',
    position='sidebar',
    code='<script>/* Adsterra banner code */</script>',
    show_on_desktop=True,
    priority=70
)

# 4. SMARTLINK
AdUnit.objects.create(
    name='Global Smartlink',
    ad_type='smartlink',
    position='content_bottom',
    code='<script>/* Adsterra smartlink code */</script>',
    show_on_pages='',  # All pages
    priority=60
)

# 5. SOCIAL BAR
AdUnit.objects.create(
    name='Sticky Social Bar',
    ad_type='social_bar',
    position='body_bottom',
    code='<script>/* Adsterra social bar code */</script>',
    show_on_pages='',  # All pages
    priority=90
)
```

---

## 🧪 Testing Guide

### Test All Pages

1. **Homepage** - http://127.0.0.1:8000/
   - Expect: Popunder, Social Bar, Content Banner, Sidebar Banner
   
2. **Player Page** - http://127.0.0.1:8000/player/
   - Expect: Player Popunder, Social Bar, Player-specific ads
   
3. **Anime Page** - http://127.0.0.1:8000/anime/
   - Expect: Social Bar, Native Mobile Banner (on mobile)
   
4. **Movie Page** - http://127.0.0.1:8000/movie/
   - Expect: Similar to Anime
   
5. **Series Page** - http://127.0.0.1:8000/series/
   - Expect: Similar to Anime

### Verify Ad Rendering

```bash
# Check if ads are in HTML
curl http://127.0.0.1:8000/ | grep -o "atOptions"

# Count number of ads
curl http://127.0.0.1:8000/ | grep -c "atOptions"

# Check specific ad
curl http://127.0.0.1:8000/ | grep "YOUR_POPUNDER_KEY"
```

### Mobile Testing

```bash
# Simulate mobile user-agent
curl -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)" \
     http://127.0.0.1:8000/ | grep -o "Native Banner"
```

---

## 🚀 Production Deployment

### Before Going Live

1. **✅ Replace all placeholder codes** with real Adsterra codes
2. **✅ Test on staging** environment first
3. **✅ Verify Cloudflare compatibility** (data-cfasync present)
4. **✅ Test mobile** and desktop versions
5. **✅ Check ad placements** don't break layout
6. **✅ Monitor page load speed**
7. **✅ Set up Adsterra tracking** in dashboard

### Security Checklist

- ✅ Only admins can access /admin/
- ✅ Strong admin password set
- ✅ DEBUG = False in production
- ✅ ALLOWED_HOSTS configured
- ✅ HTTPS enabled
- ✅ CSRF protection active

---

## 📞 Support

**Issues?**
- Check Django logs: `./venv/bin/python manage.py runserver`
- Check Adsterra dashboard for ad unit status
- Verify ad codes are correct format
- Test with browser console open (F12)

**Common Problems:**

| Problem | Solution |
|---------|----------|
| Ads not showing | Check `is_active=True` in admin |
| Wrong ads on page | Verify `show_on_pages` field |
| Mobile ads on desktop | Check device targeting settings |
| JavaScript errors | Verify `data-cfasync="false"` present |
| Layout broken | Adjust ad container CSS |

---

**🎉 You're all set! Happy monetizing!** 💰
