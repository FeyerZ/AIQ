from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .forms import InputForm

# Create your views here.
# def profilcopil(request):
#     major = request.session.get('major')
#     chapter = request.session.get('chapter')
#     return render(request, "profilcopil.html", {'major': major, 'chapter': chapter})


def profilcopil(request):
    # return HttpResponse("salut")
    # return render(request, "base.html")
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['age_number'] = form.cleaned_data['age_number']
            request.session['interest_points'] = form.cleaned_data['interest_points']
            request.session['personality'] = form.cleaned_data['personality']
            return redirect('/agent')
    else:
        form = InputForm()
    return render(request, 'profilcopil.html', {'form': form})
