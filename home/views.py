from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .forms import SelectionForm


# Create your views here.
def home(request):
    # return HttpResponse("salut")
    # return render(request, "base.html")
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            request.session['major'] = form.cleaned_data['major']
            request.session['chapter'] = form.cleaned_data['chapter']
            return redirect('confirmation')
    else:
        form = SelectionForm()
    return render(request, 'home.html', {'form': form})


# def index(request):
#     if request.method == 'POST':
#         form = SelectionForm(request.POST)
#         if form.is_valid():
#             request.session['major'] = form.cleaned_data['major']
#             request.session['chapter'] = form.cleaned_data['chapter']
#             return redirect('confirmation')
#     else:
#         form = SelectionForm()
#     return render(request, 'base_new.html', {'form': form})

def load_chapters(request):
    major = request.GET.get('major')
    chapters = SelectionForm.CHAPTER_CHOICES.get(major, [])
    return JsonResponse(chapters, safe=False)

def confirmation(request):
    major = request.session.get('major')
    chapter = request.session.get('chapter')
    return render(request, 'confirmation.html', {'major': major, 'chapter': chapter})
