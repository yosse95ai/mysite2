from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:artist_pk>/<slug:song_pk>/detail',views.detail,name='detail'),
]
