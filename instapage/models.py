from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Post(models.Model):
    image = CloudinaryField('posts')
    title = models.CharField(max_length=30, default='')
    name= models.CharField(max_length=250, blank=True)
    caption = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(ProfilePic, on_delete=models.CASCADE, related_name='posts')



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
    
