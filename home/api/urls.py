from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('room/<str:pk>/', views.get_room),

    path('topics/', views.get_topics)


]