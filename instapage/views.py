from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect, JsonResponse
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Post


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request,POST)
        if form.is_valid():
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
def home(request):
    all_posts = Image.all_images()
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES, instance= request.user.profile)
        if update_form.is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'update_form': update_form,
        'profile_form': profile_form,
        'all_posts': all_posts
    }
    return render(request, 'index.html', context)

