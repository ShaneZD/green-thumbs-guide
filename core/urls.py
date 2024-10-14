from django.urls import path, include
from . import views

app_name = 'core'  # Add this line

urlpatterns = [
    path('', views.home, name='home'),
    path('plant-database/', views.plant_database, name='plant_database'),
    path('my-garden/', views.my_garden, name='my_garden'),
    path('care-for-plant/<int:plant_id>/<str:care_type>/', views.care_for_plant, name='care_for_plant'),
    path('forum/', include('forum.urls')), 
    path('add_plant/', views.add_plant, name='add_plant'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update-plant-care/<int:plant_id>/', views.update_plant_care, name='update_plant_care'),
    path('plant/<int:plant_id>/', views.plant_detail, name='plant_detail'),
    path('get-weather-by-coords/', views.get_weather_by_coords, name='get_weather_by_coords'),
]