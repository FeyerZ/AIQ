from django.urls import path
from . import views

urlpatterns = [
    path('', views.card_list, name='card_list'),
    path('print/', views.printable_cards, name='printable_cards'),
]