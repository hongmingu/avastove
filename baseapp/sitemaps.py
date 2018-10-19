from django.contrib.sitemaps import Sitemap
from django.core.cache import cache
from django.core.paginator import Paginator
from django.urls import reverse
from object.models import *
from authapp.models import *


class MainSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ['baseapp:main_create_log_in']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = "https"

    def items(self):
        return Post.objects.filter(is_open=True).order_by('-post_chat_created')

    def lastmod(self, obj):
        return obj.post_chat_created


class UserSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = "https"

    def items(self):
        return UserUsername.objects.all().order_by('-created')

    def lastmod(self, obj):
        return obj.updated

sitemaps = {
    # 'postarabic': PostArabicSitemap,
    'main': MainSitemap,
    'post': PostSitemap,
    'user': UserSitemap,
    # 'postchinese': PostChineseSitemap,
    # 'postportuguese': PostPortugueseSitemap,
    # 'postspanish': PostSpanishSitemap,
    # 'celebrityarabic': CelebrityArabicSitemap,
    # 'celebritychinese': CelebrityChineseSitemap,
    # 'celebrityportuguese': CelebrityPortugueseSitemap,
    # 'celebrityspanish': CelebritySpanishSitemap,
    # 'main_lang': Main_LangSitemap,
}
