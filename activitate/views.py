from django.shortcuts import render

def activitate(request):
    return render(request, 'activitygenerator.html')

def rhyme_story(request):
    return render(request, 'rhyme.html')