from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import Topic, Room, Message, User
from django.core.mail import EmailMessage
from .forms import RoomForm

# Room 
def index(request):
    topics = Topic.objects.all()
    rooms = Room.objects.all()
    context = {'topics':topics, 'rooms':rooms}
    return render(request, 'home/index.html', context)

def room(request,pk:str):
    get_room = Room.objects.get(id=pk)
    room_messages = get_room.message_set.all()
    context={'room':get_room, 'room_messages':room_messages}
    return render(request, 'home/room.html',context)

def topics(request):
    topics=Topic.objects.all()
    context={'topics':topics}
    return render(request, 'home/topics.html',context)

def activity(request):
    return render(request, 'home/activity.html')

## Room CRUD
def update_room(request,pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request, 'home/create-room.html', context)

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.host = request.user
            form.save()
            return redirect('index')
        # room_name = request.POST.get('room_name')
        # room_topic = request.POST.get('room_topic')
        # room_about = request.POST.get('room_about')
        # print(room_name, room_topic ,room_about)
        # topic = Topic.objects.get(name=room_topic)
        # room = Room.objects.create(name=room_name, host=request.user, topic=topic, description=room_about)

    topics = Topic.objects.all()
    context = {'topics':topics,'form':form}
    return render(request, 'home/create-room.html', context)

def delete_room(request,pk):
    if request.method == 'POST':
        room = Room.objects.get(id=pk)
        room.delete()
        return redirect('index')
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'home/delete.html',context)

def delete_message(request,pk):
    return render(request, 'home/delete.html')

## Authentication
def register_user(request):
    return render(request, 'home/signup.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')

    return render(request, 'home/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

## User Section
def profile_settings(request):
    return render(request, 'home/settings.html')

def user_profile(request,pk:str):
    return render(request, 'home/profile.html')
