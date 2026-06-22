from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from .models import Post, Category


class LatestPostsFeed(Feed):
    title = "My Blog,Latest Posts"
    link = "/posts/"
    description = "the latest published posts."

    def items(self):
        return Post.objects.filter(
            status='published'
        ).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content          

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at       

    def item_author_name(self, item):
        return item.author.name



class LatestPostsAtomFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description


class CategoryPostsFeed(Feed):

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return f"My Blog — {obj.name}"

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return f"Latest published posts in the {obj.name} category."

    def items(self, obj):
        return Post.objects.filter(
            category=obj,
            status='published'
        ).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at

    def item_author_name(self, item):
        return item.author.user.get_full_name() or item.author.user.username
    
class CategoryPostsAtomFeed(CategoryPostsFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return f"Latest published posts in the {obj.name} category."
    

