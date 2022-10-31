from multiprocessing import context
from .forms import *
from django.shortcuts import render, redirect
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

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context ={
        'form' : form
    }

    return render(request, "room_form.html", context)

def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room) #instance koymamızın nedeni id=pk olanı çevirmek ve onu editlemek

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        'form' : form
    }

    return render(request, "room_form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # if request.user != room.host:
    #     return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})