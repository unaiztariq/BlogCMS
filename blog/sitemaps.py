
from django.contrib.sitemaps import Sitemap
from .models import Post,Profile
from django.contrib.auth.models import User

class PostSitemap(Sitemap):
    changefreq = "weekly"  
    priority = 0.9
    
    def items(self):
        return Post.objects.filter(status="published")
    
    def lastmod(self, obj):
        return obj.updated_at  
    
class ProfileSitemap(Sitemap):
    changefreq = "monthly"  
    priority = 0.6
    
    def items(self):
        return Profile.objects.filter(user__is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at  