from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login,
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request,POST)
        if form.is.valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get(password1)
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('index')

        else:    
            form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})    

@login_required(login_url='/accounts/login/')
def index(request):
    images = Post.objects.all()
    # users = User.objects.exclude(id=request.user.id)
    json_posts = []
    for post in images:

        # import pdb; pdb.set_trace()
        picture = Profile.objects.filter(user=post.user.id).first()
        if picture:
            picture = picture.profile_pic.url
        else:
            picture =''
        obj = dict(
            image=post.image.url,
            author=post.user.username,
            avatar=pic,
            name=post.title,
            caption=post.caption
           

        )
        json_posts.append(obj)
    return render(request, 'index.html', {"images": json_posts})


