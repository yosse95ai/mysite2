from django.urls import path

from . import views

app_name = 'ranges'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:artist_pk>/<slug:song_pk>/detail/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('song-search-result/', views.result, name='result')
]
