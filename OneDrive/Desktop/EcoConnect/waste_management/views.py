from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    return render(request, "contact.html")

def create_account_view(request):
    return render(request, 'create_account.html')

def index(request):
    return render(request, "index.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirects to the home page after login
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})  # Shows login page separately

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

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