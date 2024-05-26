from django.shortcuts import render

def print_images(request):
    images = [
        'planetgame/Mercury_in_true_color.jpg',
        'planetgame/Venus-real_color.jpg',
        'planetgame/The_Earth_seen_from_Apollo_17.jpg',
        'planetgame/OSIRIS_Mars_true_color.jpg',
        'planetgame/Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
        'planetgame/Saturn_during_Equinox2.jpg',
        'planetgame/Uranus2.jpg',
        'planetgame/Neptune_Full.jpg',
        'planetgame/pluto.jpg',
    ]
    return render(request, 'planetgame/printable_images.html', {'images': images})
def rhyme(request):
    return render(request, 'planetgame/rhyme.html')