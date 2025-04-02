from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import WastePickup
from django.contrib.auth.models import User
from waste_management.models import Profile
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LogoutView
import pprint

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

WASTE_PICKERS = {
    "plastic": {"name": "Ravi", "phone": "9876543210", "password": "staff1"},
    "paper": {"name": "Asha", "phone": "8765432109", "password": "staff2"},
    "metal": {"name": "Mohammed", "phone": "7654321098", "password": "staff3"},
    "glass": {"name": "John", "phone": "6543210987", "password": "staff4"},
    "e-waste": {"name": "Sneha", "phone": "5432109876", "password": "staff5"},
    "organic": {"name": "Karthik", "phone": "4321098765", "password": "staff6"},
}

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

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")  # "Admin", "User", or "Staff"

        if user_type == "Admin":
            if username == "admin" and password == "admin123":  # Change credentials if needed
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid admin credentials")
        
        elif user_type == "Staff":
             if username in WASTE_PICKERS and WASTE_PICKERS[username]["password"] == password:
                request.session["staff_username"] = username  # Store session for the logged-in staff
                return redirect("staff_dashboard")  # Redirect to staff dashboard
             else:
                messages.error(request, "Invalid staff credentials")

        else:
            messages.error(request, "Invalid login type")

    return render(request, "login.html")


# def user_login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("index")  # Redirects to the home page after login
#     else:
#         form = AuthenticationForm()
    
#     return render(request, "login.html", {"form": form})  # Shows login page separately


def create_account_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'create_account.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'create_account.html')

        # Validate phone number (must be exactly 10 digits)
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Invalid phone number! Please enter a 10-digit number.")
            return render(request, 'create_account.html')

        # Create user
        user = User.objects.create_user(username=username, password=password)
       
        profile, created = Profile.objects.get_or_create(user=user, defaults={"phone": phone})
        profile.phone = phone  # Save phone number in the user's profile
        profile.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'create_account.html')



# def login_view(request):
#     if request.method == "POST":
#         role = request.POST['role']
#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # Redirect based on role
#             if role == "user":
#                 return redirect('user_dashboard')  # Change to actual user dashboard URL
#             elif role == "admin":
#                 return redirect('admin_dashboard')  # Change to actual admin dashboard URL
#             elif role == "staff":
#                 return redirect('staff_dashboard')  # Change to actual staff dashboard URL
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, 'login.html')

def pickup_schedule(request):
    if request.method == "POST":
        waste_type = request.POST.get("waste_type")
        pickup_date = request.POST.get("pickup_date")
        pickup_time = request.POST.get("pickup_time")
        address = request.POST.get("address")

        if not waste_type or not pickup_date or not pickup_time or not address:
            messages.error(request, "All fields are required.")
        else:
            WastePickup.objects.create(
                user=request.user,
                waste_type=waste_type,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                address=address,
                status="Scheduled"
            )
            messages.success(request, "Pickup scheduled successfully!...")
            return redirect("pickup_schedule")

    return render(request, "pickup_schedule.html")
def dashboard(request):
    return render(request, "dashboard.html")


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

    pickup_list = []
    for pickup in pickups:
        waste_type = pickup.waste_type.strip().lower() if pickup.waste_type else None
        picker_details = WASTE_PICKERS.get(waste_type, {"name": "Not Assigned", "phone": "N/A"})

        pickup_data={
            "id": pickup.id,
            "waste_type": pickup.waste_type,
            "pickup_date": pickup.pickup_date,
            "pickup_time": pickup.pickup_time,
            "address": pickup.address,
            "status": pickup.status,
            "picker_name": picker_details["name"] if pickup.status == "Scheduled" else "N/A",
            "picker_phone": picker_details["phone"] if pickup.status == "Scheduled" else "N/A",
        }
        pickup_list.append(pickup_data)
    pprint.pprint(pickup_list)

    pickups = WastePickup.objects.filter(user=request.user)

    return render(request, "schedules.html", {"pickups": pickup_list})

@login_required
def cancel_pickup(request, pickup_id):
    pickup = get_object_or_404(WastePickup, id=pickup_id, user=request.user)

    if pickup.status == "Scheduled": 
        pickup.status = "Canceled"
        pickup.save()
        messages.success(request, "Pickup has been canceled successfully.")

    return redirect("schedules")  # Redirect back to schedules page

from django.shortcuts import render
RECYCLING_CENTERS = {
    "plastic": "Green Earth Recycling Center",
    "paper": "Eco Paper Mills",
    "metal": "Urban Metal Recycling",
    "glass": "PureGlass Recyclers",
    "e-waste": "Tech Recycle Hub",
    "organic": "GreenCompost Solutions",
}

@login_required
def admin_portal(request):
    users = User.objects.all()
    pickups = WastePickup.objects.all()

    pickup_data = []
    for pickup in pickups:
        user_profile = Profile.objects.filter(user=pickup.user).first()
        phone_number = user_profile.phone if user_profile else "Not Available"
        waste_type = pickup.waste_type.strip() if pickup.waste_type else None
        recycling_center = RECYCLING_CENTERS.get(waste_type, "General Recycling Center")
        picker_details = WASTE_PICKERS.get(waste_type, {"name": "Not Assigned", "phone": "N/A"})

        pickup_data.append({
            "id": pickup.id,
            "user": pickup.user,
            "address": pickup.address,
            "pickup_date": pickup.pickup_date,
            "pickup_time":pickup.pickup_time,
            "waste_type":pickup.waste_type,
            "status": pickup.status,
            "phone_number": phone_number,
            "recycling_center": recycling_center,
            "picker_name": picker_details["name"] if pickup.status == "Scheduled" else "N/A",
            "picker_phone": picker_details["phone"] if pickup.status == "Scheduled" else "N/A",
        })
    
    return render(request, "admin_portal.html", {'users': users, 'pickups': pickup_data})
@login_required
def staff_portal(request):
    username = request.session.get("staff_username")
    waste_type = request.session.get("staff_waste_type")

    if not username or not waste_type or waste_type not in WASTE_PICKERS:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect("login")

    # Ensure waste_type exists in model fields before querying
    assigned_pickups = WastePickup.objects.filter(waste_type=waste_type, status="Scheduled")

    staff_details = WASTE_PICKERS.get(waste_type, {"name": "Unknown", "phone": "N/A"})

    return render(request, "staff_portal.html", {
        "staff_name": staff_details["name"],
        "phone": staff_details["phone"],
        "waste_type": waste_type.capitalize(),
        "assigned_pickups": assigned_pickups,
    })


def logout_view(request):
    logout(request)
    return redirect("admin_portal")
def login_view(request):
    return render(request, 'signin.html')


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

def user_dashboard(request):
    return render(request, 'dashboard.html')

def admin_dashboard(request):
    return render(request, 'admin_portal.html')

def staff_dashboard(request):
    return render(request, 'staff_portal.html')

def staff_portal_view(request):
    """Display pickups assigned to the logged-in staff if credentials match WASTE_PICKERS"""
    
    username = request.session.get("staff_username")
    waste_type = request.session.get("staff_waste_type")  # Retrieve assigned waste type
    staff = request.user
    if not username or not waste_type:
        messages.error(request, "Please log in first")
        return redirect("login")  # Redirect if not logged in
    staff_details = WASTE_PICKERS.get(waste_type, {"name": "Unknown", "phone": "N/A"})

    # Check if profile exists before accessing phone number
    staff_profile = getattr(staff, "profile", None)
    phone_no = staff_profile.phone if staff_profile and hasattr(staff_profile, "phone") else "N/A"

    # Fetch only scheduled pickups for the staff's assigned waste type
    assigned_pickups = WastePickup.objects.filter(waste_type=waste_type, status="Scheduled")
    for pickup in assigned_pickups:  
        user_profile = Profile.objects.filter(user=pickup.user).first()
        pickup.phone_number = user_profile.phone if user_profile else "Not Available"
       

    return render(request, "staff_portal.html", {
        "staff_name": staff_details["name"],
        "phone": staff_details["phone"],
        "waste_type": waste_type.capitalize(),
        "assigned_pickups": assigned_pickups,  # Pass filtered pickup data to template
    })