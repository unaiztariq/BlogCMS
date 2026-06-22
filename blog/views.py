from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView,UpdateView,FormView,DeleteView,TemplateView,DetailView
from .models import Post,Profile,Comment,Follow,Category
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import View

from django.utils.text import slugify
from django.core.mail import send_mail

# Create your views here.
class BlogListView(LoginRequiredMixin,ListView):
    model=Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    def get_queryset(self):
        category = self.request.GET.get("cat")
        if category=="all" or category == None:
            query_set = Post.objects.all()
        else:
            query_set= Post.objects.filter(category__name=category)

        return query_set
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["comments"]= Comment.objects.filter(is_active=False).count()
        context["category"]= Category.objects.all()
        category = self.request.GET.get("cat")
        if category and category!="all":
            context["rsscategory"]= category


        return context
    
class SubscribeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        Profile.objects.filter(user=request.user).update(subscribed=True)
    
        return redirect("blog:home")
    


class UnsubscribeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        request.user.profile.subscribed = False
        request.user.profile.save()

        return redirect("blog:home")

    


class UserLoginView(LoginView):
    model= User
    template_name = "blog/login.html"
    def get_success_url(self):
        return reverse_lazy("blog:home")
    
    def get_initial(self):

        initial = super().get_initial()
        initial["username"]="Enter Name"
        

        return initial
    
    
    
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("blog:signin")


class SignView(FormView):

    form_class = UserCreationForm
    template_name = "blog/signin.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        profile = Profile.objects.create(user=user,name=user.username,slug=slugify(user.username))
        self.profile_slug = profile.slug
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:profile",kwargs={"slug": self.profile_slug} )
    
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = "blog/create_profile.html"
    fields=["name","email","bio","age"]
    
    def get_success_url(self):
        return reverse_lazy('blog:home')

    def get_object(self, queryset = ...):
        prof = Profile.objects.get(slug=self.kwargs["slug"])
        
        return prof

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "blog/create_post.html"
    form_class= PostForm
    

    # def dispatch(self, request, *args, **kwargs):
    #     if Profile.objects.filter(user=self.request.user).exists():
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect('blog:home')
    
    
#add it into the formvalid and update the profile to status subcribed ANAD ADD BUTTON OF SUBSCRIBE
    


    def form_valid(self, form):
    
        try:
            user = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            print("PROFILE DOES NOT EXIST")
            print(self.request.user.username)
            return super().form_invalid(form)

        form.instance.author = user
        if form.instance.status == "published":
            reci_list=[]
            profiles = Profile.objects.all()
            for profile in profiles:
                if profile.subscribed:
                    reci_list.append(profile.email)
            print("hi")
            send_mail(
                subject=form.instance.title,
                message="http://127.0.0.1:8000/blog/post/"+form.instance.slug,
                from_email=None,
                recipient_list=reci_list,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return   reverse_lazy('blog:home')
    
class PostUpdateView(UpdateView):
    template_name="blog/update_post.html"
    model= Post
    form_class=PostForm
    
        
    def get_form(self, form_class=None):
      form = super().get_form(form_class)
      form.initial["category"] = self.get_object().category.name
      return form
    
    def get_success_url(self):
        return reverse_lazy('blog:home')

class PostDeleteView(DeleteView):
    model=Post
    template_name= "blog/delete_post.html"
    def get_success_url(self):
        return reverse_lazy('blog:home')



class CommentCreateView(CreateView):
    model = Comment
    template_name="blog/detail_post.html"
    fields= ["content"]

    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        slug = self.kwargs["slug"] 
        post=Post.objects.get(slug=slug)
        context["post"]=post
        context["comment_list"]=Comment.objects.filter(is_active=True,post_id=post.id)
        return context
    

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        form.instance.post=Post.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)
    
    def get_success_url(self):
        return   reverse_lazy('blog:home')
    
class CommentTemplateView(TemplateView):
    template_name="blog/approval_comment.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["comments"]=Comment.objects.filter(is_active=False)
        return context
    

class CommentView(View):
    def post(self, request, *args, **kwargs):

       
        if request.POST.get("button") == "all":
            Comment.objects.filter(is_active=False).update(is_active=True)
            
            return redirect("blog:home")
            
        else:
            Comment.objects.filter(id=self.kwargs["pk"]).update(is_active=True)
            return redirect("blog:home")
    

class ProfileDetailView(DetailView):
    model= Profile
    template_name="blog/detail_profile.html"
    context_object_name= "profile"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts= Post.objects.filter(author=self.get_object())
        context["posts"]=posts
        user_p = self.request.user.profile
        follow= Follow.objects.all()
        for f in follow:
            if f.follower==user_p and f.follows_to == self.get_object():
                context["follower"] = True
                break
        else:
            context["follower"]=False
        my_followers=Follow.objects.filter(follows_to=self.get_object())
        my_followings=Follow.objects.filter(follower=self.get_object())
        context["my_followers"]=my_followers
        context["my_followings"]=my_followings

        return context
    
class FollowView(View):
    def post(self,request,*args,**kwargs):
        following = Profile.objects.get(slug=kwargs["slug"])
        Follow.objects.create(follower=request.user.profile,follows_to=following)

        return redirect("blog:home")
    
class UnfollowView(View):
    def post(self,request,*args,**kwargs):
        following = Profile.objects.get(slug=kwargs["slug"])
        Follow.objects.filter(follower=request.user.profile,follows_to=following).delete()

        return redirect("blog:home")
    


class RSSFeedTemplateView(TemplateView):
    template_name= "blog/rssfeed.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        rsscategory= self.request.GET.get("rsscategory")
        if rsscategory is not None:
            context["rss"]=f"http://127.0.0.1:8000/feed/{rsscategory}"
            context["atom"]= f"http://127.0.0.1:8000/feed/{rsscategory}/atom/"
            print(f"http://127.0.0.1:8000/feed/{rsscategory}")
        return context
    

class DashboardDetailView(DetailView):
    model=Profile
    template_name= "blog/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["posts"]=Post.objects.filter(author =self.request.user.profile)
        my_followers=Follow.objects.filter(follows_to=self.get_object())
        my_followings=Follow.objects.filter(follower=self.get_object())
        context["my_followers"]=my_followers
        context["my_followings"]=my_followings
        return context


