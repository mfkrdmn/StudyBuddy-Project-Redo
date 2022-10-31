from .forms import *
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
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