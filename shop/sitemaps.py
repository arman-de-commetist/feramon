from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, GiftPerfume, Product


class PagesSitemap(Sitemap):
    changefreq = 'weekly'

    PAGES = {
        'index': 1.0, 'catalog': 0.9, 'order': 0.9, 'promotions': 0.9, 'dyson': 0.9, 'gifts': 0.8, 'compare': 0.7,
        'quiz': 0.6, 'reviews': 0.6, 'gallery': 0.5, 'blog': 0.6, 'about': 0.5, 'pheromones': 0.6, 'certificates': 0.5, 'delivery': 0.6,
        'payment': 0.5, 'returns': 0.4, 'faq': 0.5, 'contacts': 0.6, 'privacy': 0.2, 'offer': 0.2,
    }

    def items(self):
        return list(self.PAGES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item]


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True)


class GiftSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return GiftPerfume.objects.filter(is_active=True)


class ArticleSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published


SITEMAPS = {'pages': PagesSitemap, 'products': ProductSitemap, 'gifts': GiftSitemap, 'blog': ArticleSitemap}
