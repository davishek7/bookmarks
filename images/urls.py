from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('',views.index,name='index'),
    path('images/create/', views.image_create, name='create'),
    path('images/detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('images/list/', views.image_list, name='list'),
    # path('ranking/', views.image_ranking, name='ranking'),
]
