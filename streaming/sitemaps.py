"""
Sitemap configuration for KortekStream
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['streaming:home', 'streaming:movie_list', 'streaming:tv_list', 'streaming:anime_list']

    def location(self, item):
        return reverse(item)
