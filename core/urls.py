from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    # Define image create url
    path('create/', views.image_create, name="create"),
    path('detail/<int:pk>/<slug:slug>/', views.image_detail, name="detail"),
]
