from django.urls import path
from . import views

urlpatterns = [
    path("", views.activitate, name="activitate"),
    path('rhymed-story', views.rhyme_story, name='rhymed_story'),
]