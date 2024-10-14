from django.core.management.base import BaseCommand
from core.models import Plant
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Populate the database with initial plants suitable for Irish climate'

    def handle(self, *args, **options):
        plants_data = [
            {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'description': 'A popular garden vegetable that can be grown in greenhouses or sheltered areas in Ireland.',
                'image': 'tomato.jpeg',
                'ideal_temperature_min': 15,
                'ideal_temperature_max': 24,
                'watering_frequency': 3,
                'fertilizing_frequency': 14,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Potato',
                'scientific_name': 'Solanum tuberosum',
                'description': 'A staple crop in Ireland, well-suited to the climate.',
                'image': 'potato.webp',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 20,
                'watering_frequency': 5,
                'fertilizing_frequency': 30,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Cabbage',
                'scientific_name': 'Brassica oleracea var. capitata',
                'description': 'A hardy vegetable that grows well in cool Irish weather.',
                'image': 'cabbage.jpeg',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 22,
                'watering_frequency': 4,
                'fertilizing_frequency': 21,
                'sunlight_needs': 'Full sun to partial shade',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Carrot',
                'scientific_name': 'Daucus carota subsp. sativus',
                'description': 'A root vegetable that thrives in the cool, moist conditions of Ireland.',
                'image': 'carrot.jpg',
                'ideal_temperature_min': 7,
                'ideal_temperature_max': 21,
                'watering_frequency': 5,
                'fertilizing_frequency': 28,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Rosemary',
                'scientific_name': 'Salvia rosmarinus',
                'description': 'An aromatic herb that can be grown in sheltered areas or pots in Ireland.',
                'image': 'rosemary.jpg',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 20,
                'watering_frequency': 7,
                'fertilizing_frequency': 42,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Low',
            },
            {
                'name': 'Strawberry',
                'scientific_name': 'Fragaria × ananassa',
                'description': 'A sweet fruit that grows well in Irish gardens with proper care.',
                'image': 'strawberry.jpg',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 22,
                'watering_frequency': 3,
                'fertilizing_frequency': 21,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Parsley',
                'scientific_name': 'Petroselinum crispum',
                'description': 'A hardy herb that grows well in the cool Irish climate.',
                'image': 'parsley.jpg',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 22,
                'watering_frequency': 4,
                'fertilizing_frequency': 28,
                'sunlight_needs': 'Partial shade',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Rhubarb',
                'scientific_name': 'Rheum rhabarbarum',
                'description': 'A hardy perennial vegetable that thrives in the Irish climate.',
                'image': 'rhubarb.jpg',
                'ideal_temperature_min': 5,
                'ideal_temperature_max': 20,
                'watering_frequency': 5,
                'fertilizing_frequency': 60,
                'sunlight_needs': 'Full sun to partial shade',
                'humidity_preference': 'Moderate',
            },
            {
                'name': 'Thyme',
                'scientific_name': 'Thymus vulgaris',
                'description': 'A small-leaved herb that can be grown in well-drained soil in Ireland.',
                'image': 'thyme.jpg',
                'ideal_temperature_min': 10,
                'ideal_temperature_max': 22,
                'watering_frequency': 7,
                'fertilizing_frequency': 30,
                'sunlight_needs': 'Full sun',
                'humidity_preference': 'Low',
            },
            {
                'name': 'Lettuce',
                'scientific_name': 'Lactuca sativa',
                'description': 'A cool-season crop that grows well in Irish spring and autumn.',
                'image': 'lettuce.jpeg',
                'ideal_temperature_min': 7,
                'ideal_temperature_max': 18,
                'watering_frequency': 3,
                'fertilizing_frequency': 14,
                'sunlight_needs': 'Partial shade',
                'humidity_preference': 'Moderate',
            },
        ]

        for plant_info in plants_data:
            plant, created = Plant.objects.get_or_create(
                name=plant_info['name'],
                defaults={
                    'scientific_name': plant_info['scientific_name'],
                    'description': plant_info['description'],
                    'ideal_temperature_min': plant_info['ideal_temperature_min'],
                    'ideal_temperature_max': plant_info['ideal_temperature_max'],
                    'watering_frequency': plant_info['watering_frequency'],
                    'fertilizing_frequency': plant_info['fertilizing_frequency'],
                    'sunlight_needs': plant_info['sunlight_needs'],
                    'humidity_preference': plant_info['humidity_preference'],
                }
            )
            if created:
                image_path = os.path.join('plant_images', plant_info['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        plant.image.save(plant_info['image'], File(image_file), save=True)
                    self.stdout.write(self.style.SUCCESS(f'Added plant: {plant.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Image not found for: {plant.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Plant already exists: {plant.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated plants suitable for Irish climate'))