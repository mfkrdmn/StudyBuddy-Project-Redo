from .forms import *
from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):

    room = Room.objects.all()

    message = Message.objects.all()

    context = {
        "room" : room,
        "message" : message
    }

    return render(request,"home.html", context)

def room(request,pk):

    room = Room.objects.get(id=pk)

    context = {
        "room" : room,
    }

    return render(request,"room.html", context)

def createRoom(request):

    form = RoomForm()

    context ={
        'form' : form
    }

    return render(request, "room_form.html", context)