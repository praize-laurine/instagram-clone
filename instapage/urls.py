from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
# from django.urls import url,include
from . import views

urlpatterns=[
    url('instagramHome/home.html', views.home, name='instagramHome-home'),
    url('Pabout/', views.about, name='instagramHome-about'),
    url('new_post/', views.add_post, name='add_post'),
    url("<int:pk>/", views.post_detail, name="post_detail"),
    url('<int:pk>',views.like, name='likes')
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)