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
            request.session['domain'] = form.cleaned_data['domain']
            request.session['subdomain'] = form.cleaned_data['subdomain']
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
    domain = request.GET.get('domain')
    subdomain = SelectionForm.CHAPTER_CHOICES.get(domain, [])
    return JsonResponse(subdomain, safe=False)

def confirmation(request):
    domain = request.session.get('domain')
    subdomain = request.session.get('subdomain')
    return render(request, 'confirmation.html', {'domain': domain, 'subdomain': subdomain})
