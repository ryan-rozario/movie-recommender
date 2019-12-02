"""recomender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from movies.views import total_view, login_user,reg_user,movie_detail_view,logout_user,genre_view,recommendation_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_user,name='login'),
    url(r'^signup/', reg_user,name='signup'),
    path('', total_view,name='total2'),
    path('movies/', total_view,name='total'),
    path('movies/recommended', recommendation_view,name='recom'),
    path('movies/<str:genre>', genre_view,name='genre'),
    path('logout/',logout_user,name='logout'),
    path('movies/<int:id>/', movie_detail_view,name='movie_detail'),
]