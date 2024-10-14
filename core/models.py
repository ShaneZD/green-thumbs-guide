from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from django.db import models
from django.utils import timezone

class Plant(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    ]
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField()
    is_plant_of_month = models.BooleanField(default=False)
    ideal_temperature_min = models.FloatField(null=True, blank=True, help_text="Minimum ideal temperature in Celsius")
    ideal_temperature_max = models.FloatField(null=True, blank=True, help_text="Maximum ideal temperature in Celsius")
    watering_frequency = models.IntegerField(null=True, blank=True, help_text="Number of days between watering")
    fertilizing_frequency = models.IntegerField(null=True, blank=True, help_text="Number of days between fertilizing")
    sunlight_needs = models.CharField(max_length=50, blank=True)
    humidity_preference = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='plant_images/', null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    plant_of_month_start = models.DateField(null=True, blank=True)
    best_planting_season = models.CharField(max_length=20, choices=SEASON_CHOICES)

    def save(self, *args, **kwargs):
        if self.is_plant_of_month and not self.plant_of_month_start:
            self.plant_of_month_start = timezone.now().date()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_difficulty_display(self):
        return dict(self.DIFFICULTY_CHOICES)[self.difficulty]

    @classmethod
    def get_plant_of_month(cls):
        current_month = timezone.now().month
        season = cls.get_current_season(current_month)
        return cls.objects.filter(is_plant_of_month=True, best_planting_season=season).first()

    @staticmethod
    def get_current_season(month):
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        else:
            return 'winter'
        
class Garden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='garden')
    name = models.CharField(max_length=100, default="My Garden")
    location = models.CharField(max_length=100, blank=True)  # For weather data

    def __str__(self):
        return f"{self.user.username}'s Garden"

class GardenPlant(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    planted_date = models.DateField()
    last_watered = models.DateTimeField(null=True, blank=True)
    last_fertilized = models.DateTimeField(null=True, blank=True)
    last_pruned = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)  # Add this line

    @property
    def next_watering_date(self):
        if self.last_watered:
            return (self.last_watered + datetime.timedelta(days=self.plant.watering_frequency)).date()
        return (self.planted_date + datetime.timedelta(days=self.plant.watering_frequency))

    @property
    def growth_percentage(self):
        plant_lifespan = 365  # Assume 1 year for simplicity
        days_since_planting = (timezone.now().date() - self.planted_date).days
        return min(int((days_since_planting / plant_lifespan) * 100), 100)

class Tip(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.content[:50]

class PlantCare(models.Model):
    CARE_TYPES = [
        ('WATER', 'Watering'),
        ('PRUNE', 'Pruning'),
        ('FERTILIZE', 'Fertilizing'),
    ]
    garden_plant = models.ForeignKey(GardenPlant, on_delete=models.CASCADE, related_name='care_tasks')
    care_type = models.CharField(max_length=10, choices=CARE_TYPES)
    last_performed = models.DateTimeField(null=True, blank=True)
    next_due = models.DateTimeField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_care_type_display()} for {self.garden_plant}"

    def reset(self):
        self.is_done = False
        self.last_performed = timezone.now()
        if self.care_type == 'WATER':
            self.next_due = self.last_performed + timezone.timedelta(days=self.garden_plant.plant.watering_frequency or 7)
        elif self.care_type == 'FERTILIZE':
            self.next_due = self.last_performed + timezone.timedelta(days=self.garden_plant.plant.fertilizing_frequency or 30)
        else:  # PRUNE
            self.next_due = self.last_performed + timezone.timedelta(days=30)  # Default to monthly pruning
        self.save()

class WeatherData(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    wind_speed = models.FloatField()

    class Meta:
        unique_together = ('garden', 'date')

    def __str__(self):
        return f"Weather for {self.garden.name} on {self.date}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."