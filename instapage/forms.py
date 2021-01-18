from django import forms
# from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=60)

    class Meta:
        # model = User
        fields = ('username','email','password1','password2')

class PostForm(forms.Form):
    image = forms.ImageField()
    image_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Image Name"}))
    image_caption = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control","placeholder": "Image Caption"}))

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control","placeholder": "Leave a comment!"}))
