from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'hotel/register.html', {'user_form': user_form, 'profile_form': profile_form})

def dashboard(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        # Define images based on culture choice
        images = {
            'African': [
                '/static/hotel/images/african1.jpg',
                '/static/hotel/images/african2.jpg',
                '/static/hotel/images/african3.jpg',
                '/static/hotel/images/african4.jpg',
                '/static/hotel/images/african5.jpg',
            ],
            'American': [
                '/static/hotel/images/american1.jpg',
                '/static/hotel/images/american2.jpg',
                '/static/hotel/images/american3.jpg',
                '/static/hotel/images/american4.jpg',
                '/static/hotel/images/american5.jpg',
            ],
            'European': [
                '/static/hotel/images/european1.jpg',
                '/static/hotel/images/european2.jpg',
                '/static/hotel/images/european3.jpg',
                '/static/hotel/images/european4.jpg',
                '/static/hotel/images/european5.jpg',
            ],
            'Arabic': [
                '/static/hotel/images/arabic1.jpg',
                '/static/hotel/images/arabic2.jpg',
                '/static/hotel/images/arabic3.jpg',
                '/static/hotel/images/arabic4.jpg',
                '/static/hotel/images/arabic5.jpg',
            ],
        }

        selected_images = images.get(profile.culture_choice, [])

        # Check if the user's culture matches their origin
        origin_culture_map = {
            'african': 'African',
            'american': 'American',
            'european': 'European',
            'arabic': 'Arabic',
        }

        expected_culture = origin_culture_map.get(profile.origin)

        if expected_culture and profile.culture_choice != expected_culture:
            return render(request, 'hotel/dashboard.html', {'error_message': "This is not your specific culture."})

        # Pass both selected images and profile to the template
        return render(request, 'hotel/dashboard.html', {'selected_images': selected_images, 'profile': profile})
    return redirect('register')

def make_reservation(request):
    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        # Here you can add logic to save the reservation to the database if needed
        return JsonResponse({'message': 'Reservation successful for ' + image_url})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.POST.get('next', 'dashboard')
                return redirect(next_url)
            else:
                print("User is not active")
        else:
            print("Invalid login credentials")
            print("Form errors:", form.errors)  # Print form errors
            print("Submitted data:", request.POST)  # Print submitted data
            user_exists = User.objects.filter(username=username).exists()
            print("User exists:", user_exists)  # Check if user exists
            if user_exists:
                user = User.objects.get(username=username)
                print("User is active:", user.is_active)  # Check if user is active
                print("Correct password:", user.check_password(password))  # Check if password is correct
    else:
        form = AuthenticationForm()
    return render(request, 'hotel/login.html', {'form': form})