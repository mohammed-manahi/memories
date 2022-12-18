from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    # Define image create url
    path('create/', views.image_create, name="create"),
    # Define image detail url
    path('detail/<int:pk>/<slug:slug>/', views.image_detail, name="detail"),
    # Define image like/dislike url
    path('like/', views.image_like, name="like"),
    # Define image list url
    path('', views.image_list, name='list'),
]
