from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

def login_page(request):
     
     if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
               user = User.objects.get(username=username)
            except:
                 messages.error(request, 'User does not exists.')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                 login(request, user)
                 return redirect('home')
            else:
                 messages.error(request, 'Wrong credentials.')

     context = {}
     return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
         Q(topic__name__icontains=q) |
         Q(name__icontains=q) |
         Q(description__icontains=q)
         )

    topics = Topic.objects.all()
    room__count = rooms.count()

    context = {'rooms':rooms, 'topics': topics, 'room__count': room__count}
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, "base/room.html", context)

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, id):
        room = Room.objects.get(id=id)
        form = RoomForm(instance=room)

        if request.method == 'POST':
             form = RoomForm(request.POST, instance=room)
             if form.is_valid():
                  form.save()
                  return redirect('home')

        context = {'form': form}
        return render(request, 'base/room_form.html', context)


def delete_room(request, id):
     room = Room.objects.get(id=id)
     if request.method == 'POST':
          room.delete()
          return redirect('home')
     return render(request, 'base/delete.html', {'obj': room})