from django.urls import path, include
from instapage.views import PostLikeToggle, PostLikeAPIToggle
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profileUser/<username>/', views.profileUser, name='profileUser'),
    path('post/<id>', views.post_comment, name='comment'),
    path('post/<id>/like', PostLikeToggle.as_view(), name='liked'),
    path('api/post/<id>/like', PostLikeAPIToggle.as_view(), name='liked-api'),
    path('like', views.like_post, name='like_post'),
    path('search/', views.search_profile, name='search'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/<to_follow>', views.follow, name='follow')
]