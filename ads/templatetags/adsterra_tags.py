"""
Custom template tags untuk render Adsterra ads
CRITICAL: Menggunakan mark_safe() untuk allow JavaScript execution
"""

from django import template
from django.utils.safestring import mark_safe
from django.db.models import Q
from ads.models import AdUnit

register = template.Library()


@register.simple_tag
def render_ads(position, page_type=None):
    """
    Render all active ads for a specific position and page type
    
    Usage in template:
        {% load adsterra_tags %}
        {% render_ads 'head' %}
        {% render_ads 'body_top' 'anime' %}
        {% render_ads 'content_top' page_type %}
    
    Args:
        position: Ad position (head, body_top, body_bottom, etc)
        page_type: Optional page type for filtering (home, anime, movie, etc)
    
    Returns:
        HTML string with all ad codes (marked as safe for execution)
    """
    # Get active ads for this position
    ads = AdUnit.objects.filter(
        position=position,
        is_active=True
    )
    
    # Filter by page type if specified
    if page_type:
        ads = ads.filter(
            Q(show_on_pages='') | Q(show_on_pages__icontains=page_type)
        )
    
    # Build HTML output
    html_parts = []
    
    for ad in ads.order_by('-priority'):
        # Add comment for debugging (helps identify which ad is which in source)
        html_parts.append(f'<!-- Ad: {ad.name} ({ad.ad_type}) -->')
        
        # Add the actual ad code
        html_parts.append(ad.code)
        
        html_parts.append('')  # Empty line for readability
    
    # Join all parts
    html_output = '\n'.join(html_parts)
    
    # CRITICAL: mark_safe() tells Django to NOT escape this HTML
    # Without this, <script> becomes &lt;script&gt; and won't execute!
    return mark_safe(html_output)


@register.simple_tag(takes_context=True)
def render_responsive_ads(context, position, page_type=None):
    """
    Render ads with device detection (mobile vs desktop)
    
    Usage:
        {% render_responsive_ads 'sidebar' 'anime' %}
    
    This will automatically filter based on user's device
    """
    request = context.get('request')
    
    # Get active ads for this position
    ads = AdUnit.objects.filter(
        position=position,
        is_active=True
    )
    
    # Filter by page type if specified
    if page_type:
        ads = ads.filter(
            Q(show_on_pages='') | Q(show_on_pages__icontains=page_type)
        )
    
    # Detect device from user agent
    if request:
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_mobile = any(x in user_agent for x in ['mobile', 'android', 'iphone', 'ipad', 'ipod'])
        
        if is_mobile:
            ads = ads.filter(show_on_mobile=True)
        else:
            ads = ads.filter(show_on_desktop=True)
    
    # Build HTML output
    html_parts = []
    
    for ad in ads.order_by('-priority'):
        html_parts.append(f'<!-- Ad: {ad.name} ({ad.ad_type}) -->')
        html_parts.append(ad.code)
        html_parts.append('')
    
    html_output = '\n'.join(html_parts)
    
    return mark_safe(html_output)


@register.simple_tag
def render_single_ad(position, page_type=None):
    """
    Render only ONE ad (highest priority) for a position
    Useful for A/B testing or rotation
    
    Usage:
        {% render_single_ad 'content_top' 'home' %}
    """
    # Get active ads for this position
    ads = AdUnit.objects.filter(
        position=position,
        is_active=True
    )
    
    # Filter by page type if specified
    if page_type:
        ads = ads.filter(
            Q(show_on_pages='') | Q(show_on_pages__icontains=page_type)
        )
    
    # Get only the highest priority ad
    ad = ads.order_by('-priority').first()
    
    if not ad:
        return ''
    
    html_output = f'<!-- Ad: {ad.name} ({ad.ad_type}) -->\n{ad.code}'
    
    return mark_safe(html_output)


@register.simple_tag
def render_random_ad(position, page_type=None):
    """
    Render a random ad from available ads in position
    Useful for rotating ads on each page load
    
    Usage:
        {% render_random_ad 'sidebar' %}
    """
    import random
    
    # Get active ads for this position
    ads = list(AdUnit.objects.filter(
        position=position,
        is_active=True
    ))
    
    # Filter by page type if specified
    if page_type:
        ads = [ad for ad in ads if ad.should_show_on_page(page_type)]
    
    if not ads:
        return ''
    
    # Pick random ad
    ad = random.choice(ads)
    
    html_output = f'<!-- Ad: {ad.name} ({ad.ad_type}) -->\n{ad.code}'
    
    return mark_safe(html_output)


@register.simple_tag
def has_ads(position, page_type=None):
    """
    Check if there are any ads for a position
    Useful for conditional rendering
    
    Usage:
        {% has_ads 'sidebar' 'anime' as sidebar_ads_exist %}
        {% if sidebar_ads_exist %}
            <div class="sidebar-ad-container">
                {% render_ads 'sidebar' 'anime' %}
            </div>
        {% endif %}
    """
    ads = AdUnit.objects.filter(
        position=position,
        is_active=True
    )
    
    if page_type:
        ads = ads.filter(
            Q(show_on_pages='') | Q(show_on_pages__icontains=page_type)
        )
    
    return ads.exists()


@register.filter
def safe_ad_code(value):
    """
    Simple filter to mark ad code as safe
    
    Usage:
        {{ ad_object.code|safe_ad_code }}
    
    This is an alternative to using the template tags
    """
    return mark_safe(value)
