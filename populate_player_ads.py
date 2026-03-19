
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from ads.models import AdUnit

def update_or_create_ad(name, position, ad_type, code, mobile=True, desktop=True):
    AdUnit.objects.update_or_create(
        position=position,
        name=name,
        defaults={
            'ad_type': ad_type,
            'code': code,
            'is_active': True,
            'show_on_mobile': mobile,
            'show_on_desktop': desktop,
            'priority': 150
        }
    )
    print(f"Configured: {name} at {position}")

# 1. Player Top - Use 728x90 Leaderboard (Desktop)
player_top_desktop = """<script>
  atOptions = {
    'key' : '1e8dc14785d6c8ed7ec9c073cd415528',
    'format' : 'iframe',
    'height' : 90,
    'width' : 728,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/1e8dc14785d6c8ed7ec9c073cd415528/invoke.js"></script>"""
update_or_create_ad("Player Top Banner 728x90", "player_top", "banner", player_top_desktop, mobile=False, desktop=True)

# 2. Player Top - Use 320x50 Banner (Mobile)
player_top_mobile = """<script>
  atOptions = {
    'key' : '7700434bbb648ffeb4036cfa91bede94',
    'format' : 'iframe',
    'height' : 50,
    'width' : 320,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/7700434bbb648ffeb4036cfa91bede94/invoke.js"></script>"""
update_or_create_ad("Player Top Mobile 320x50", "player_top", "banner", player_top_mobile, mobile=True, desktop=False)

# 3. Player Bottom - Use 300x250 Rect Banner
player_bottom_code = """<script>
  atOptions = {
    'key' : 'a294d5ec7eecd30b1379c7692f666c5d',
    'format' : 'iframe',
    'height' : 250,
    'width' : 300,
    'params' : {}
  };
</script>
<script src="https://www.highperformanceformat.com/a294d5ec7eecd30b1379c7692f666c5d/invoke.js"></script>"""
update_or_create_ad("Player Bottom Banner 300x250", "player_bottom", "banner", player_bottom_code)

print("
SUCCESS: Player page ads populated.")
