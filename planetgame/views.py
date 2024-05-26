from django.shortcuts import render

def print_images(request):
    # Get image URLs (replace this with your logic)
    image_urls = [
        'planetgame/Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
        'planetgame/Mercury_in_true_color.jpg',
        'planetgame/Uranus2.jpg',
        'planetgame/Venus-real_color.jpg',
        'planetgame/Neptune_Full.jpg',
        'planetgame/OSIRIS_Mars_true_color.jpg',
        'planetgame/Saturn_during_Equinox.jpg',
        'planetgame/The_Earth_seen_from_Apollo_17.jpg'
    ]

    return render(request, 'planetgame/printable_images.html', {'image_urls': image_urls})