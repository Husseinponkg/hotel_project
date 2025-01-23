from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
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
            'African': '/static/hotel/images/african.jpg',
            'American': '/static/hotel/images/american.jpg',
            'European': '/static/hotel/images/european.jpg',
            'Arabic': '/static/hotel/images/arabic.jpg',
        }

        selected_image = images.get(profile.culture_choice, None)

        # Pass both selected image and profile to the template
        return render(request, 'hotel/dashboard.html', {'selected_image': selected_image, 'profile': profile})
    return redirect('register')

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