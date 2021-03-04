from django.urls import path

from . import views

app_name = 'ranges'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug:artist_pk>/', views.detail_artist, name='detail_artist'),
    path('detail/<slug:artist_pk>/<slug:song_pk>-<slug:release_date>', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('search-result/song/', views.result, name='result'),
    path('search-result/song/<slug:in_name>', views.result, name='result'),
    path('search-result/range-<slug:note_pk>',
         views.result_range, name='result_range'),
    path('search-result/genre-<slug:genre_pk>',
         views.result_genre, name='result_genre'),
    path('search-result/all',
         views.result_all, name='result_all'),
]
