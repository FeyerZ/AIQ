"""
URL configuration for AIQ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_quiz, name='start_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    # path('generate/', views.generate_quiz, name='generate_quiz'),
    # path('ask_chatgpt_question/', views.ask_chatgpt_question, name='ask_chatgpt_question'),
    # path('', views.generate_quiz_from_response, name='generate_quiz_from_response'),
    path('', views.generate_quiz, name='generate_quiz'),

]
