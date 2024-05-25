from django.shortcuts import render
from .models import Planet

def initialize_planets():
    if not Planet.objects.exists():
        planets = [
            {"name": "Mercury", "description": "Mercury is the smallest planet in our solar system.", "image_url": "https://example.com/mercury.jpg"},
            {"name": "Venus", "description": "Venus has a thick atmosphere that traps heat.", "image_url": "https://example.com/venus.jpg"},
            {"name": "Earth", "description": "Earth is the only planet known to support life.", "image_url": "https://example.com/earth.jpg"},
            {"name": "Mars", "description": "Mars is known as the Red Planet.", "image_url": "https://example.com/mars.jpg"},
            {"name": "Jupiter", "description": "Jupiter is the largest planet in our solar system.", "image_url": "https://example.com/jupiter.jpg"},
            {"name": "Saturn", "description": "Saturn is famous for its rings.", "image_url": "https://example.com/saturn.jpg"},
            {"name": "Uranus", "description": "Uranus rotates on its side.", "image_url": "https://example.com/uranus.jpg"},
            {"name": "Neptune", "description": "Neptune is known for its strong winds.", "image_url": "https://example.com/neptune.jpg"},
        ]
        for planet in planets:
            Planet.objects.create(name=planet["name"], description=planet["description"], image_url=planet["image_url"])

def card_list(request):
    initialize_planets()
    planets = Planet.objects.all()
    return render(request, 'planetgame/card_list.html', {'planets': planets})

def printable_cards(request):
    planets = Planet.objects.all()
    return render(request, 'planetgame/planetgame.html', {'planets': planets})
