import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Plant, Tip, Garden, GardenPlant, Notification
from .forms import UserProfileForm, AddPlantForm, UpdatePlantCareForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.db.models import Q
import datetime
from forum.models import ForumPost

# Generates notifications for the user based on weather data and plant care schedules.
def generate_notifications(user, weather_data):
    garden_plants = user.garden.gardenplant_set.all()  # Fetch all plants in user's garden
    today = timezone.now().date()  # Get today's date
    
    # Check weather data and create appropriate notifications for extreme temperatures
    if weather_data and 'temperature' in weather_data:
        temperature = weather_data['temperature']
        if temperature < 5:
            Notification.objects.get_or_create(
                user=user,
                message="Cold weather alert! Protect your sensitive plants.",
                defaults={'created_at': timezone.now()}
            )
        elif temperature > 30:
            Notification.objects.get_or_create(
                user=user,
                message="Heat wave alert! Make sure your plants are well-watered.",
                defaults={'created_at': timezone.now()}
            )
    
    # Create notifications for plants needing watering today
    for garden_plant in garden_plants:
        plant = garden_plant.plant
        if garden_plant.next_watering_date <= today:
            Notification.objects.get_or_create(
                user=user,
                message=f"Your {plant.name} needs watering!",
                defaults={'created_at': timezone.now()}
            )
    
    # Remove notifications older than one day
    Notification.objects.filter(user=user, created_at__lt=timezone.now() - timezone.timedelta(days=1)).delete()

# Clears specific notifications for the user.
def clear_notification(user, message):
    Notification.objects.filter(user=user, message=message).delete()

# Fetches weather data from OpenWeatherMap API based on latitude and longitude.
def get_weather_data(lat, lon):
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data['name'],
            'temperature': round(data['main']['temp']),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed'], 1)
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Renders the home page with relevant data like weather, plant of the month, and notifications.
def home(request):
    weather_data = None  # Initialize as None
    plant_of_month = Plant.get_plant_of_month()
    monthly_tip = Tip.objects.filter(is_active=True).order_by('?').first()
    current_season = get_current_season()
    seasonal_plants = Plant.objects.filter(best_planting_season=current_season)[:6]
    recent_posts = ForumPost.objects.order_by('-created_at')[:5]
    notifications = []
    
    # Fetch user's garden and notifications if authenticated
    if request.user.is_authenticated:
        garden, created = Garden.objects.get_or_create(user=request.user)
        notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    context = {
        'weather_data': weather_data,
        'plant_of_month': plant_of_month,
        'monthly_tip': monthly_tip,
        'seasonal_plants': seasonal_plants,
        'notifications': notifications,
        'recent_posts': recent_posts,
        'current_season': current_season,
    }
    return render(request, 'core/home.html', context)

# Returns weather data as JSON based on coordinates.
def get_weather_by_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if lat and lon:
        weather_data = get_weather_data(lat, lon)
        if weather_data:
            return JsonResponse(weather_data)
    return JsonResponse({'error': 'Unable to fetch weather data'}, status=400)

# Renders the plant database and allows searching and sorting.
def plant_database(request):
    plants = Plant.objects.all()
    query = request.GET.get('q')
    if query:
        plants = plants.filter(
            Q(name__icontains=query) |
            Q(scientific_name__icontains=query) |
            Q(description__icontains=query)
        )
    sort = request.GET.get('sort', 'name')
    if sort == 'name':
        plants = plants.order_by('name')
    elif sort == 'watering':
        plants = plants.order_by('watering_frequency')
    elif sort == 'difficulty':
        plants = plants.order_by('difficulty')
    
    context = {
        'plants': plants,
        'query': query,
        'current_sort': sort
    }
    return render(request, 'core/plant_database.html', context)

# Renders user's garden page and allows adding plants.
@login_required
def my_garden(request):
    garden, created = Garden.objects.get_or_create(user=request.user)
    garden_plants = GardenPlant.objects.filter(garden=garden).select_related('plant')
    
    if request.method == 'POST':
        form = AddPlantForm(request.POST)
        if form.is_valid():
            garden_plant = form.save(commit=False)
            garden_plant.garden = garden
            garden_plant.planted_date = timezone.now().date()
            garden_plant.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('core:my_garden')
    else:
        form = AddPlantForm()
    
    context = {
        'garden': garden,
        'garden_plants': garden_plants,
        'form': form,
    }
    return render(request, 'core/my_garden.html', context)

# Handles care actions for specific plants in the user's garden.
@login_required
@require_POST
def care_for_plant(request, plant_id, care_type):
    garden_plant = get_object_or_404(GardenPlant, id=plant_id, garden__user=request.user)
    
    # Update the care type accordingly
    if care_type == 'water':
        garden_plant.last_watered = timezone.now()
        clear_notification(request.user, f"Your {garden_plant.plant.name} needs watering!")
    elif care_type == 'fertilize':
        garden_plant.last_fertilized = timezone.now()
    elif care_type == 'prune':
        garden_plant.last_pruned = timezone.now()
    else:
        return JsonResponse({'success': False, 'error': 'Invalid care type'})
    
    garden_plant.save()
    return JsonResponse({'success': True})

# Renders the page for adding a new plant to the user's garden.
@login_required
def add_plant(request):
    if request.method == 'POST':
        form = AddPlantForm(request.POST)
        if form.is_valid():
            garden_plant = form.save(commit=False)
            garden_plant.garden = request.user.garden
            garden_plant.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('core:my_garden')
    else:
        form = AddPlantForm()
    return render(request, 'core/add_plant.html', {'form': form})

# Renders the page for updating plant care details.
@login_required
def update_plant_care(request, plant_id):
    garden_plant = get_object_or_404(GardenPlant, id=plant_id, garden__user=request.user)
    if request.method == 'POST':
        form = UpdatePlantCareForm(request.POST, instance=garden_plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant care updated successfully!')
            return redirect('core:my_garden')
    else:
        form = UpdatePlantCareForm(instance=garden_plant)
    return render(request, 'core/update_plant_care.html', {'form': form, 'plant': garden_plant})

# Renders the user's profile page.
@login_required
def user_profile(request):
    user = request.user
    garden = user.garden
    garden_plants = garden.gardenplant_set.all()
    
    context = {
        'user': user,
        'garden': garden,
        'garden_plants': garden_plants,
    }
    return render(request, 'core/user_profile.html', context)

# Placeholder for forum homepage rendering.
def forum(request):
    return render(request, 'forum/forum_home.html')

# Handles user registration using custom user creation form.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

# Renders detailed view of a specific plant.
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    return render(request, 'core/plant_detail.html', {'plant': plant})

# Determines the current season based on the month.
def get_current_season():
    month = datetime.datetime.now().month
    if month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'autumn'
    else:
        return 'winter'