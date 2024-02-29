# roomrentalapp/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Room, Application
from .forms import RoomForm, CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
import pickle
import pandas
import json

model = pickle.load(open('AI/model.pkl', 'rb'))

def home(request):
    return redirect('marketplace')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    rooms_posted = Room.objects.filter(owner=user_profile)
    applications = Application.objects.filter(applicant=user_profile)
    return render(request, 'registration/profile.html', {'user_profile': user_profile, 'rooms': rooms_posted, 'applications': applications})

@login_required
def post_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = UserProfile.objects.get(user=request.user)
            room.save()
            return redirect('user_profile')  
    else:
        form = RoomForm()

    return render(request, 'room/post_room.html', {'form': form})


def marketplace(request):
    if request.GET.get("location"):
        rooms = Room.objects.filter(location__contains='location')
    else:
        rooms = Room.objects.all()
    return render(request, 'room/marketplace.html', {'rooms': rooms})

@login_required
def room_detail(request, id):
    userprof = UserProfile.objects.get(user=request.user)
    room = Room.objects.get(id=id)
    applicants = Application.objects.filter(room=room).all()
    return render(request, 'room/room_detail.html', {'room': room, 'user':request.user, 'profile':userprof, 'application':applicants})


@login_required
def room_apply(request, room_id):
    room = Room.objects.get(id=room_id)
    userprof = UserProfile.objects.get(user=request.user)
    if room.owner != userprof and not Application.objects.filter(room=room, applicant=userprof).exists():
        app = Application.objects.create(room=room, applicant=userprof)

    return redirect('user_profile')

@login_required
def accept_application(request, app_id):
    app = Application.objects.get(pk=app_id)
    if app.room.owner.user == request.user:
        app.accepted = True
        app.save()
    return redirect('room_detail', id = app.room.pk)


def predict_price(request):
    bhk = int(request.GET['bhk'])
    bathroom = int(request.GET['bathroom'])
    
    prediction = model.predict([[bhk, bathroom]])
    retr_data = {'prediction':int(prediction[0])}
    return HttpResponse(json.dumps(retr_data), status=200)

# Authentication 

def logout_view(request):
    logout(request)
    return redirect('user_login')

def register(request):
    if request.method == 'POST':
        print("Post captured")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("login success")
            return redirect('user_profile')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    form_errors = ""
    if request.method == 'POST':
        print("Post captured")
        print(request.POST)
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            print("login success")
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('user_profile')
        form_errors = "Invalid Password username combination"  
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'form_errors': form_errors})