from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:pk>/', views.room, name='room'),
    path('topics/', views.topics, name='topics'),
    path('activity/', views.activity, name='activity'),

    ## User Section
    path('settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:pk>/', views.user_profile, name='profile'),

    ## Room CRUD
    path('create-room/',views.create_room, name='create_room'),
    path('update-room/<str:pk>/',views.update_room, name='update_room'),
    path('delete-room/<str:pk>/',views.delete_room, name='delete_room'),
    path('delete-message/<str:pk>/',views.delete_message, name='delete_message'),

    ## Authentication
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
