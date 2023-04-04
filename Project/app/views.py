from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,User,Message
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth import authenticate,login,logout



def index(request):

    # q is the topic name
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Filter data by category
    data = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    
    topics = Topic.objects.all()

    room = data.count()

    # Filter activities by data category, limiting the activities to 5
    activities = Message.objects.filter(Q(room__topic__name__icontains = q))[0:5]

    context = {'data':data, 'topics':topics, 'room_count':room,'activities':activities}
    return render(request,'home.html',context)


# Getting a id from the HTML in the url, and passing it in function as "pk". We are doing this without GET request.
def room(request,pk):
    room = Room.objects.get(id = pk)

    # this will bring all the messages related to the post
    room_messages = room.message_set.all()

    parts = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            body = request.POST.get('body'),
            room = room
        )

        # Adding the participants which has typed a message
        room.participants.add(request.user)

        return redirect('room',pk=room.id)

    context = {'room':room,'room_messages':room_messages,'part':parts}
    return render(request,'room.html',context)


@login_required(login_url='login-page')
def DeleteMessage(request,pk):
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to do that...!')

    if request.method == 'POST':
            message.delete()
            return redirect('home')

    return render(request,'delete.html',{'obj':message})



@login_required(login_url='login-page')
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    context = {'form':form, 'topics':topics}

    if request.method == 'POST':
        new_form = RoomForm(request.POST)

        get_topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=get_topic)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')


    return render(request,'room_form.html', context)


@login_required(login_url='login-page')
def UpdateRoom(request,pk):
    # Getting the room by provided id
    room = Room.objects.get(id = pk)

    topics = Topic.objects.all()
    # We want the form to be pre-filled with old values
    form = RoomForm(instance=room)
    context = {'form':form, 'topics':topics, 'room':room}

    # A user can only update their rooms
    if request.user != room.host:
        return HttpResponse('You are not allowed to do that...!')

    if request.method == 'POST':
        get_topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=get_topic)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        return redirect('home')

    return render(request, 'room_form.html',context)


@login_required(login_url='login-page')
def Delete(request,pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to do that...!')

    if request.method == 'POST':
            room.delete()
            return redirect('home')

    return render(request,'delete.html',{'obj':room})


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User does not exists')
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR Password is incorrect')

    context = {'page':page}
    return render(request,'login_register.html',context)


def Signup(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # login the user as well when the account creates
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,'Error occurred during registration')
        
    return render(request,'login_register.html',{'form':form})


def LogoutPage(request):
    logout(request)
    return redirect('home')


def UserProfile(request,pk):
    user = User.objects.get(id = pk)

    # We have used same name of variables to fetch data in our website, because variables are same that we have passed in context dictionary.
    # If not than, data will not be rendered in the for loops used in our templates

    # This will only output the data of the user, that are clicked
    data = user.room_set.all()
    activities = user.message_set.all()

    # We have not used "_set.all()" because we want all the topics not for a single user
    topics = Topic.objects.all()
    
    context = {'user':user,'data':data,'activities':activities,'topics':topics}
    return render(request,'profile.html',context)


@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form':form}

    if request.method == 'POST':
        # Giving all the field values to the built-in form
        form = UserForm(request.POST, request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk = user.id)


    return render(request,'update_user.html',context)
