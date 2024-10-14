# Green Thumbs Guide

**Green Thumbs Guide** is a feature-rich web application designed for gardening enthusiasts. Built with Django, it provides functionalities such as plant management, weather updates, gardening tips, and a community forum.

## Table of Contents
- [Features]
- [Installation]
- [Usage]


## Features
- **Home Page**: A welcoming landing page introducing the application.
- **User Authentication**: Registration, login, and logout functionalities.
- **Dashboard**: Personalized user dashboard with gardening insights and notifications.
- **Plant Management**: CRUD operations for managing plants.
- **Weather Updates**: Real-time weather alerts relevant to gardening.
- **Gardening Tips**: Monthly tips to help users improve their gardening skills.
- **Forum**: Community forum for discussing gardening topics and sharing advice.

## Installation
1. Clone the repository:
git clone https://github.com/ShaneZD/green-thumbs-guide.git
1.a cd green-thumbs-guide

## Usage 

1. Create a virtual environment
python -m venv env

2. Activate the virtual environment
source env/bin/activate  # On Windows, use `env\Scripts\activate`

3. Install dependencies
pip install -r requirements.txt

4. You must run this command after migrating to populate the initial data with a function i made (populate plants):
python manage.py migrate
python manage.py populate_plants

5. Run your development server
python manage.py runserver
   

   
