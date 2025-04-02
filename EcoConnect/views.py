from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, WastePickupForm
from .models import WastePickup
from django.contrib.auth.models import User  
from django.contrib import messages 
from .models import UserProfile

WASTE_PICKERS = {
    "plastic": {"name": "Ravi", "phone": "9876543210", "password": "staff1"},
    "paper": {"name": "Asha", "phone": "8765432109", "password": "staff2"},
    "metal": {"name": "Mohammed", "phone": "7654321098", "password": "staff3"},
    "glass": {"name": "John", "phone": "6543210987", "password": "staff4"},
    "e-waste": {"name": "Sneha", "phone": "5432109876", "password": "staff5"},
    "organic": {"name": "Karthik", "phone": "4321098765", "password": "staff6"},
}

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

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_view(request):
    if request.method == "POST":
        role = request.POST.get('role')
        username = request.POST.get('username').strip()  # Remove extra spaces
        password = request.POST.get('password')

        # Admin authentication
        if role == "admin" and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect('admin_portal')

        # Staff authentication
        if role == "staff":
            for waste_type, details in WASTE_PICKERS.items():
                if details["name"].lower() == username.lower() and details["password"] == password:
                    request.session["staff_username"] = details["name"]  # Store name in session
                    request.session["staff_waste_type"] = waste_type  # Store waste type in session
                    return redirect("staff_portal")

            messages.error(request, "Invalid username or password.")  # Show error if not found
            return render(request, 'login.html')

        # Normal user authentication
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#             return redirect("/admin_portal/")
        
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('pickup_schedule')  # Redirect to home after successful login
#         else:
#             messages.error(request, "Invalid username or password. Please try again.")

#     return render(request, 'login.html')
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

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def cancel_pickup(request, pickup_id):
    pickup = get_object_or_404(WastePickup, id=pickup_id, user=request.user)

    if pickup.status == "Scheduled":  # Ensure only pending pickups can be canceled
        pickup.status = "Canceled"
        pickup.save()
        

    return redirect("schedules")  # Redirect back to schedules page

from django.utils import timezone


def schedules(request):
    # Get all pickups for the logged-in user
    pickups = WastePickup.objects.filter(user=request.user)

    # Update status of past pickups
    for pickup in pickups:
        pickup_datetime = timezone.make_aware(
            timezone.datetime.combine(pickup.pickup_date, pickup.pickup_time)
        )

        if pickup.status == "Scheduled" and pickup_datetime < timezone.now():
            pickup.status = "Completed"
            pickup.save()
    
    if not request.session.get("seen_canceled"):
        WastePickup.objects.filter(user=request.user, status="Canceled").delete()
        request.session["seen_canceled"] = True

    # Refresh pickups after deletion
    pickups = WastePickup.objects.filter(user=request.user)

    return render(request, "schedules.html", {"pickups": pickups})

from django.shortcuts import render

RECYCLING_CENTERS = {
    "Plastic": "Green Earth Recycling Center",
    "Paper": "Eco Paper Mills",
    "Metal": "Urban Metal Recycling",
    "Glass": "PureGlass Recyclers",
    "E-Waste": "Tech Recycle Hub",
}

@login_required
def admin_portal(request):
    users = User.objects.all()
    pickups = WastePickup.objects.all()

    pickup_data = []
    for pickup in pickups:
        user_profile = UserProfile.objects.filter(user=pickup.user).first()
        phone_number = user_profile.phone_number if user_profile else "Not Available"
        recycling_center = RECYCLING_CENTERS.get(getattr(pickup, 'waste_type', None), "General Recycling Center")

        pickup_data.append({
            "id": pickup.id,
            "user": pickup.user,
            "address": pickup.address,
            "pickup_date": pickup.pickup_date,
            "status": pickup.status,
            "phone_number": phone_number,
            "recycling_center": recycling_center
        })
    
    return render(request, "admin_portal.html", {'users': users, 'pickups': pickup_data})

def logout_view(request):
    logout(request)
    return redirect("admin_portal")

# def login_view(request):
#     return render(request, 'login.html')


def user_login(request):
    """ Handles user login """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None and not user.is_staff and not user.is_superuser:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid user credentials.")
    
    return render(request, "login.html")


def admin_login(request):
    """ Handles admin login """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect("admin_portal")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admin_portal")
        else:
            messages.error(request, "Invalid admin credentials.")
    
    return render(request, "login.html")


def staff_login(request):
    """ Handles staff login """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("staff_dashboard")
        else:
            messages.error(request, "Invalid staff credentials.")
    
    return render(request, "login.html")

def staff_portal(request):
    """Display pickups assigned to the logged-in staff if credentials match WASTE_PICKERS"""
    
    username = request.session.get("staff_username")
    waste_type = request.session.get("staff_waste_type")  # Retrieve assigned waste type

    if not username or not waste_type:
        messages.error(request, "Please log in first")
        return redirect("login")  # Redirect if not logged in

    # Fetch only scheduled pickups for the staff's assigned waste type
    assigned_pickups = WastePickup.objects.filter(waste_type=waste_type, status="Scheduled")

    return render(request, "staff_portal.html", {
        "staff_name": WASTE_PICKERS[waste_type]["name"],  # Access by waste type
        "phone": WASTE_PICKERS[waste_type]["phone"],  # Access by waste type
        "waste_type": waste_type.capitalize(),
        "assigned_pickups": assigned_pickups,  # Pass filtered pickup data to template
    })

def dashboard(request):
    return render(request, "dashboard.html")
