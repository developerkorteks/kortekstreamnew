from django.contrib import admin
from django.utils.html import format_html
from .models import AdUnit


@admin.register(AdUnit)
class AdUnitAdmin(admin.ModelAdmin):
    """
    Admin interface untuk manage Adsterra ads
    User-friendly dengan preview dan helpful descriptions
    """
    
    list_display = [
        'name', 
        'ad_type_badge', 
        'position_badge', 
        'status_badge',
        'device_targeting',
        'page_targeting',
        'priority',
        'updated_at'
    ]
    
    list_filter = [
        'ad_type', 
        'position', 
        'is_active',
        'show_on_mobile',
        'show_on_desktop',
    ]
    
    search_fields = ['name', 'code', 'show_on_pages']
    
    readonly_fields = ['created_at', 'updated_at', 'code_preview']
    
    fieldsets = (
        ('📌 Basic Information', {
            'fields': ('name', 'ad_type', 'position', 'is_active', 'priority'),
            'description': 'Basic settings for this ad unit'
        }),
        ('💻 Ad Code', {
            'fields': ('code', 'code_preview'),
            'description': '<strong>⚠️ IMPORTANT:</strong> Paste your Adsterra code EXACTLY as provided. Include the complete &lt;script&gt; tags.'
        }),
        ('📱 Device Targeting', {
            'fields': ('show_on_mobile', 'show_on_desktop'),
            'description': 'Choose which devices should see this ad'
        }),
        ('🎯 Page Targeting', {
            'fields': ('show_on_pages',),
            'description': 'Leave empty to show on ALL pages, or specify: home,anime,movie,series,player'
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ad_type_badge(self, obj):
        """Display ad type with colored badge"""
        colors = {
            'popunder': '#FF6B6B',
            'social_bar': '#4ECDC4',
            'banner': '#45B7D1',
            'native': '#96CEB4',
            'smartlink': '#FFEAA7',
        }
        color = colors.get(obj.ad_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_ad_type_display()
        )
    ad_type_badge.short_description = 'Ad Type'
    
    def position_badge(self, obj):
        """Display position with badge"""
        return format_html(
            '<span style="background-color: #636e72; color: white; padding: 3px 8px; border-radius: 3px; font-size: 10px;">{}</span>',
            obj.position
        )
    position_badge.short_description = 'Position'
    
    def status_badge(self, obj):
        """Display active/inactive status"""
        if obj.is_active:
            return format_html(
                '<span style="color: {}; font-weight: bold;">✓ Active</span>',
                '#27ae60'
            )
        else:
            return format_html(
                '<span style="color: {}; font-weight: bold;">✗ Inactive</span>',
                '#e74c3c'
            )
    status_badge.short_description = 'Status'
    
    def device_targeting(self, obj):
        """Show device targeting info"""
        devices = []
        if obj.show_on_mobile:
            devices.append('📱 Mobile')
        if obj.show_on_desktop:
            devices.append('🖥️ Desktop')
        return ' + '.join(devices) if devices else '❌ None'
    device_targeting.short_description = 'Devices'
    
    def page_targeting(self, obj):
        """Show page targeting info"""
        if not obj.show_on_pages:
            return format_html('<span style="color: {};">All Pages</span>', '#27ae60')
        pages = obj.get_page_types()
        return ', '.join(pages[:3]) + ('...' if len(pages) > 3 else '')
    page_targeting.short_description = 'Pages'
    
    def code_preview(self, obj):
        """Show preview of the ad code (first 200 chars)"""
        if obj.code:
            preview = obj.code[:200] + ('...' if len(obj.code) > 200 else '')
            return format_html(
                '<pre style="background: #f4f4f4; padding: 10px; border-radius: 5px; font-size: 11px;">{}</pre>',
                preview
            )
        return '-'
    code_preview.short_description = 'Code Preview'
    
    def save_model(self, request, obj, form, change):
        """Add any auto-fixes before saving"""
        # Auto-add Cloudflare compatibility if missing
        if '<script' in obj.code and 'data-cfasync' not in obj.code:
            obj.code = obj.code.replace('<script', '<script data-cfasync="false"', 1)
        
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Optional: custom admin CSS
        }
