"""
URL configuration for linksphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="register"),
    path('',views.SigninView.as_view(),name="signin"),
    path('linksphere/index/',views.IndexView.as_view(),name="index"),
    path('linksphere/logout/',views.SignOutView.as_view(),name="signout"),
    path('likshpere/profile/<int:pk>/change/',views.ProfileUpdateView.as_view(),name="profile-update"),
    path('linkshpere/profile/<int:pk>/',views.ProfileDetailView.as_view(),name="profile-details"),
    path('linkshpere/profile/all/',views.ProfileListView.as_view(),name="profile-list"),
    path('linksphere/post/add/',views.PostUploadView.as_view(),name="upload-post"),
    path('linkshpere/post/<int:pk>/delete/',views.PostDeleteView.as_view(),name="post-delete"),
    path('linksphere/profile/<int:pk>/follow/',views.FollowsView.as_view(),name="follow"),
    path('linksphere/post/<int:pk>/like/',views.PostLikeView.as_view(),name="like"),
    path('linksphere/post/<int:pk>/comment/add/',views.CommentView.as_view(),name="comment"),
    path('linksphere/profile/<int:pk>/block/',views.ProfileBlockView.as_view(),name="block"),
    path('linksphere/storie/add/',views.StorieCreateView.as_view(),name="storie-create"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
