from django.shortcuts import render, redirect
from django.contrib.auth import login
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
