from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import Topic, Room, Message, User
from django.core.mail import EmailMessage
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404
# Room 
def index(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(room__name__icontains=q)
        ).order_by('-created_at')
    context = {'topics':topics, 'rooms':rooms, 'room_messages': room_messages}
    return render(request, 'home/index.html', context)

def room(request,pk):
    get_room = Room.objects.get(id=pk)
    room_messages = get_room.message_set.all().order_by('-created_at')
    participants = get_room.participants.all()

    if request.method == 'POST':
        message_body = request.POST.get('message_body')
        message = Message.objects.create(
            host = request.user,
            room = get_room,
            body = message_body
        )
        get_room.participants.add(request.user)
        return redirect('room',pk=get_room.id)

    context={'room':get_room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'home/room.html',context)

def topics(request):
    topics=Topic.objects.all()
    context={'topics':topics}
    return render(request, 'home/topics.html',context)

def activity(request):
    return render(request, 'home/activity.html')

## Room CRUD

@login_required
def update_room(request,pk):
    room = Room.objects.get(id=pk)

    if room.host != request.user:
        raise Http404
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room_topic = request.POST.get('room_topic')
        room_about = request.POST.get('room_about')
        topic,created = Topic.objects.get_or_create(name=room_topic)
        room.name = room_name
        room.topic = topic
        room.description = room_about
        room.save()
        return redirect('index')
    context = {'action':'Update','room':room}
    return render(request, 'home/room_form.html', context)

@login_required
def create_room(request):
    # form = RoomForm()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     form.save(commit=False)
        #     form.host = request.user
        #     form.save()
        #     return redirect('index')
        room_name = request.POST.get('room_name')
        room_topic = request.POST.get('room_topic')
        room_about = request.POST.get('room_about')
        topic,created = Topic.objects.get_or_create(name=room_topic)
        room = Room.objects.create(
            name=room_name, 
            host=request.user, 
            topic=topic, 
            description=room_about)
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    topics = Topic.objects.all()
    context = {'topics':topics, 'action':'Create'}
    return render(request, 'home/room_form.html', context)

@login_required
def delete_room(request,pk):
    if request.method == 'POST':
        room = Room.objects.get(id=pk)
        room.delete()
        return redirect('index')
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'home/delete.html',context)

@login_required
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if request.method == 'POST':
        message.delete()
        return redirect('room',pk=room.id)
    context = {'message':message, 'room':room}
    return render(request, 'home/delete.html', context)

## Authentication
def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login_user')
    context = {'form':form}
    return render(request, 'home/signup.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else: 
            messages.error(request, 'Incorrect username or password')

    return render(request, 'home/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

## User Section
@login_required
def profile_settings(request):
    return render(request, 'home/settings.html')

def user_profile(request,pk:str):
    profile = get_object_or_404(User,username=pk)
    topics = Topic.objects.all()

    print(profile.avatar)
    rooms = Room.objects.filter(host=profile)
    room_messages = profile.message_set.all()
    context = {'profile': profile, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'home/profile.html', context)

