from django.db import models
from django.db.models import Q


class AdUnit(models.Model):
    """
    Model untuk menyimpan dan manage Adsterra ads dari Django Admin
    Support semua jenis ad units: Popunder, Social Bar, Banner, Native, Smartlink
    """
    
    AD_TYPES = [
        ('popunder', 'Popunder'),
        ('social_bar', 'Social Bar'),
        ('banner', 'Display Banner'),
        ('native', 'Native Banner'),
        ('smartlink', 'Smartlink'),
    ]
    
    POSITIONS = [
        ('head', 'Head Section (for Popunder)'),
        ('body_top', 'Body Top (after opening <body>)'),
        ('body_bottom', 'Body Bottom (before closing </body>)'),
        ('sidebar', 'Sidebar'),
        ('content_top', 'Before Content'),
        ('content_bottom', 'After Content'),
        ('between_content', 'Between Content Items'),
        ('player_top', 'Above Video Player'),
        ('player_bottom', 'Below Video Player'),
    ]
    
    # Basic Info
    name = models.CharField(
        max_length=200,
        help_text="Descriptive name for this ad unit (e.g., 'Home Page Popunder')"
    )
    ad_type = models.CharField(
        max_length=20, 
        choices=AD_TYPES,
        help_text="Type of Adsterra ad unit"
    )
    position = models.CharField(
        max_length=30, 
        choices=POSITIONS,
        help_text="Where to display this ad on the page"
    )
    
    # Ad Code (CRITICAL: This stores the raw JavaScript from Adsterra)
    code = models.TextField(
        help_text="Paste your Adsterra code exactly as provided (including <script> tags)"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to disable this ad without deleting it"
    )
    
    # Device Targeting
    show_on_mobile = models.BooleanField(
        default=True,
        help_text="Show this ad on mobile devices"
    )
    show_on_desktop = models.BooleanField(
        default=True,
        help_text="Show this ad on desktop devices"
    )
    
    # Page Targeting
    show_on_pages = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma separated page types: home,anime,movie,series,player (leave empty for all pages)"
    )
    
    # Priority (for ordering when multiple ads in same position)
    priority = models.IntegerField(
        default=0,
        help_text="Higher number = higher priority. Use for A/B testing or rotation"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Marketing Unit"
        verbose_name_plural = "Marketing Units"
    
    def __str__(self):
        return f"{self.name} ({self.get_ad_type_display()} - {self.get_position_display()})"
    
    def clean(self):
        """Validation untuk ensure code tidak kosong"""
        from django.core.exceptions import ValidationError
        if not self.code.strip():
            raise ValidationError({'code': 'Ad code cannot be empty'})
        
        # Warn jika code tidak mengandung script tag (kemungkinan salah paste)
        if '<script' not in self.code.lower():
            raise ValidationError({
                'code': 'Ad code should contain <script> tags. Make sure you copied the complete code from Adsterra.'
            })
    
    def get_page_types(self):
        """Return list of page types where this ad should show"""
        if not self.show_on_pages:
            return []
        return [page.strip() for page in self.show_on_pages.split(',') if page.strip()]
    
    def should_show_on_page(self, page_type):
        """Check if this ad should show on given page type"""
        if not self.show_on_pages:  # Empty = show on all pages
            return True
        return page_type in self.get_page_types()
