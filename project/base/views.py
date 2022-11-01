from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #buradaki q herhangi bir karakter olabilir. Değişim yapıldığında html de de değişmeli

    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    #The icontains lookup is used to get records that contains a specified value.
    #The icontains lookup is case insensitive.

    message = Message.objects.all()

    topic = Topic.objects.all()

    room_count = room.count()

    context = {
        "room" : room,
        "message" : message,
        "topics" : topic,
        "room_count" : room_count,
    }

    return render(request,"home.html", context)

def room(request,pk):

    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all().order_by("-created")

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body') #html body name li inputtan alınan veri
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        "room" : room,
        "room_messages" : room_messages,
        "participants" : participants
    }

    return render(request,"room.html", context)

@login_required(login_url='login')
def createRoom(request):

    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context ={
        'form' : form
    }

    return render(request, "room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #instance koymamızın nedeni id=pk olanı çevirmek ve onu editlemek
    
    if request.user != room.host: # bu olay çok önemli
            return HttpResponse('Your are not allowed here!!')

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        'form' : form
    }

    return render(request, "room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # if request.user != room.host:
    #     return HttpResponse('Your are not allowed here!!')

    if request.user != room.host: # bu olay çok önemli
            return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        
        message.delete()
        return redirect("home")
    return render(request, 'delete.html', {'obj': message})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
          return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        #here we are checking if user exist. If yes, username i al, if not, error mesaj dön

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {
        "page" : page
    }
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

