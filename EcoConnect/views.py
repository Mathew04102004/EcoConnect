from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, WastePickupForm
from .models import WastePickup
from django.contrib.auth.models import User  # ✅ Import User model
from django.contrib import messages 
from .models import UserProfile

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def schedule(request):
    if request.method == "POST":
        form = WastePickupForm(request.POST)
        if form.is_valid():
            pickup = form.save(commit=False)
            pickup.user = request.user
            pickup.status = "pending"
            pickup.save()
            return redirect("track")
    else:
        form = WastePickupForm()
    return render(request, "schedule.html", {"form": form})

def track(request):
    pickups = WastePickup.objects.filter(user=request.user)
    return render(request, "track.html", {"pickups": pickups})

def user_logout(request):
    logout(request)
    return redirect("index")


def create_account_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Try a different one.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match! Try again.")
        else:
            user = User.objects.create_user(username=username, password=password)  # Save user
            UserProfile.objects.create(user=user, address=address)  # Save address
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    return render(request, 'create_account.html')

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    return render(request, "contact.html")

def create_account_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(f"Received data: Username={username}, Password={password}, Confirm={confirm_password}")  # Debugging

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'create_account.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'create_account.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        print(f"User {username} created successfully!")  # Debugging

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'create_account.html')
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pickup_schedule')  # Redirect to home after successful login
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')
def pickup_schedule(request):
    if request.method == 'POST':
        waste_type = request.POST['waste_type']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        address = request.POST['address']

        WastePickup.objects.create(
            user=request.user,
            waste_type=waste_type,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            address=address,
            status="Pending"
        )
        
        messages.success(request, "Your waste pickup has been successfully scheduled!")  # ✅ Success message
        return redirect('pickup_schedule')

    return render(request, 'pickup_schedule.html')

