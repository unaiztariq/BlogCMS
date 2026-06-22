from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from django.utils.text import slugify

# Create your models here.

from django.urls import reverse



class Post(models.Model):
    STATUS_CHOICES = [
        ("published","Published"),
        ("draft","Draft"),
        ("scheduled","Sheduled")
    ]

    title = models.CharField( max_length=200,unique=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    author = models.ForeignKey("Profile",on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey("Category",on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content= RichTextUploadingField()
    tags = TaggableManager()
    slug = models.SlugField(unique=True,blank=True)

    def save(self,*args,**kwargs):
         self.slug = slugify(self.title)
         return super().save(*args,**kwargs)
    

    def get_absolute_url(self):
        return reverse("blog:detail",args=[self.slug])

    def __str__(self):
        return self.title



class Category(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self):
        return self.name 


    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField( max_length=200,default="NUll",null=True)
    bio= models.TextField(null=True)
    age= models.PositiveIntegerField(null= True)
    email=models.EmailField()
    subscribed= models.BooleanField(blank= True,default= False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True,blank=True)
   

    def get_absolute_url(self):
        return reverse("blog:detail_profile",args=[self.slug])
    
    def save(self, *args,**kwargs):
         self.slug = slugify(self.name)
         return super().save(*args,**kwargs)

    def __str__(self):
        return self.name 
    
class Follow(models.Model):
     follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="followers" )
     follows_to = models.ForeignKey(Profile,on_delete=models.CASCADE ,related_name="following")

     class meta:
        unique_together = [['follower', 'follows_to']]
        

class Comment(models.Model):
    is_active= models.BooleanField(blank=True,default=False)
    content= models.TextField()
    profile= models.ForeignKey(Profile,on_delete=models.CASCADE)
    post= models.ForeignKey(Post,on_delete=models.CASCADE)

