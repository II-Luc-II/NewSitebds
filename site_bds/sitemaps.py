from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Gallery, Testimonials, Team, Ask


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['index']  # Nom de la vue pour la page d'accueil

    def location(self, item):
        return reverse(item)