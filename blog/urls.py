
from django.urls import path
from . import views

app_name= "blog"


from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, ProfileSitemap

sitemaps = {
    'post': PostSitemap,
    'profile': ProfileSitemap,
}


urlpatterns = [
    path('',views.BlogListView.as_view(),name="home" ),
    path('login/',views.UserLoginView.as_view(),name="login" ),
    path('logout/',views.UserLogoutView.as_view(),name="logout" ),
    path('signin/',views.SignView.as_view(),name="signin" ),
    path('profile/<slug:slug>/create',views.ProfileUpdateView.as_view(),name="profile" ),
    path('post/',views.PostCreateView.as_view(),name="create_post" ),
    path('post/<slug:slug>/',views.CommentCreateView.as_view(),name="detail" ),
    path('post/<slug:slug>/update',views.PostUpdateView.as_view(),name="update_post"),
    path('post/<slug:slug>/delete',views.PostDeleteView.as_view(),name="delete_post"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/", views.UnsubscribeView.as_view(), name="unsubscribe"),
    path("Comments-Approval/", views.CommentTemplateView.as_view(), name="approval_comment"),
    path("Comments-Success/<int:pk>", views.CommentView.as_view(), name="success_comment"),
    path('profile/<slug:slug>',views.ProfileDetailView.as_view(),name="detail_profile"),
    path('profile/<slug:slug>/follow',views.FollowView.as_view(),name="follow"),
    path('profile/<slug:slug>/unfollow',views.UnfollowView.as_view(),name="unfollow"),
    path("RSS-Atom-Feed/", views.RSSFeedTemplateView.as_view(), name="rssfeed"),
    path("Dashboard/<slug:slug>/", views.DashboardDetailView.as_view(), name="dashboard"),
    
]







