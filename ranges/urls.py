from django.urls import path

from . import views

app_name = 'ranges'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:artist_pk>/<slug:song_pk>/detail/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('search-result/song/', views.result, name='result'),
    path('search-result/range-<slug:note_pk>', views.result_range, name='result_range'),
]
