from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm
# rooms = [
#     {'id':1, 'name':'Python Basic'},
#     {'id':2, 'name':'Python Advanced'},
#     {'id':3, 'name':'Java'},
# ]


# Create your views here.
def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('base.home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, "Username or password doesnot exits")
            return render(request, "base/login_register.html")
        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base.home')
        else:
            messages.error(request, "Username or Password doesnot exist")

    context = {'page':page}
    print(context)
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("base.home") 

def registerPage(request):
    form = UserCreationForm()

    if request.method =="POST":
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("base.home")
        else:
            messages.error(request, "An erro occured during registration, register again.")
    context = {"form": form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q (topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count= rooms.count()
    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'roomMessages':roomMessages}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    participants = room.participants.all()

    if request.method =="POST":
        print(request)
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('base.room', pk=room.id)


    context = {'room': room, 'roomMessages':roomMessages, 'participants':participants}
    return render(request,'base/Rooms.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    contex = {'user':user, 'rooms':rooms ,'roomMessages':roomMessages, 'topics':topics}
    return render(request, 'base/profile.html', contex)


@login_required(login_url='base.login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('base.home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base.login')
def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Not your Room, room can be updated by host only!")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("base.home")

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base.login')
def deleteRoom(request, pk):    
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("Not your Room, room can be updated by host only!")
    
    if request.method =="POST":
        room.delete()
        return redirect("base.home")
    
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='base.login')
def deleteMessage(request, pk):    
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("Not your Room, room can be updated by host only!")
    
    if request.method =="POST":
        message.delete()
        room = message.room
        context = room.id
        return redirect("base.room", context)
    
    return render(request, 'base/delete.html', {'obj':message})