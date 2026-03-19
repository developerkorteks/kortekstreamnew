from django.contrib import admin
from django.utils.html import format_html
from .models import AdUnit


@admin.register(AdUnit)
class AdUnitAdmin(admin.ModelAdmin):
    """
    Admin interface for Marketing Units.
    Renamed and simplified to bypass aggressive ad blockers.
    """
    # 1. Show save button at the top too! (Bypasses bottom-only filters)
    save_on_top = True
    
    list_display = [
        'name', 
        'ad_type_badge', 
        'position_badge', 
        'status_badge',
        'priority',
        'updated_at'
    ]
    
    list_filter = ['ad_type', 'position', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at', 'code_preview']
    
    # Avoid "Ad" wording in fieldsets
    fieldsets = (
        ('📌 Basic Information', {
            'fields': ('name', 'ad_type', 'position', 'is_active', 'priority'),
        }),
        ('💻 Integration Code', {
            'fields': ('code',),
        }),
        ('🔍 Preview', {
            'fields': ('code_preview',),
            'classes': ('collapse',),
        }),
        ('📱 Targeting', {
            'fields': ('show_on_mobile', 'show_on_desktop', 'show_on_pages'),
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ad_type_badge(self, obj):
        colors = {'popunder': '#FF6B6B', 'social_bar': '#4ECDC4', 'banner': '#45B7D1'}
        color = colors.get(obj.ad_type, '#95a5a6')
        return format_html('<span style="background: {}; color: white; padding: 2px 8px; border-radius: 4px;">{}</span>', color, obj.get_ad_type_display())
    ad_type_badge.short_description = 'Type'
    
    def position_badge(self, obj):
        return format_html('<small style="color: #666;">{}</small>', obj.position)
    position_badge.short_description = 'Position'
    
    def status_badge(self, obj):
        icon = '✅' if obj.is_active else '❌'
        return format_html('<span>{}</span>', icon)
    status_badge.short_description = 'Active'

    def code_preview(self, obj):
        if obj.code:
            return format_html('<pre style="max-width: 500px; overflow: auto; background: #eee; padding: 5px;">{}</pre>', obj.code[:100] + '...')
        return '-'

    def save_model(self, request, obj, form, change):
        # Auto-add Cloudflare compatibility
        if '<script' in obj.code and 'data-cfasync' not in obj.code:
            obj.code = obj.code.replace('<script', '<script data-cfasync="false"', 1)
        super().save_model(request, obj, form, change)
