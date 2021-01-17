from django.db import models
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField


# Create your models here.
class Post(models.Model):
    image = CloudinaryField('posts')
    title = models.CharField(max_length=30, default='')
    name= models.CharField(max_length=250, blank=True)
    caption = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    @classmethod
    def all_posts(cls) :
        posts = cls.objects.all()
        return posts

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def update_post(cls, id, value):
        cls.objects.filter(id=id).update(image=value)


    def __str__(self):
        return self.title



class ProfilePic(models.Model):
    image = CloudinaryField('images')
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', null=True)
    name = models.CharField(blank=True,max_length=50)
    bio = models.TextField(max_length=500, default="My Bio", blank=True)

    def save_profile(self):
        self.save

    def delete_user(self):
        self.delete()

    @classmethod
    def update_profile(cls, id, value):
        cls.objects.filter(id=id).update(profile_name=value)

   
    def __str__(self):
        return f'{self.user.username} ProfilePic'
    
