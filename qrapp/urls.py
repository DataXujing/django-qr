from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index,name='index'),
    path('intro/', views.qr_intro,name='intro'),
    path('about/', views.abouts,name='about'),
    
]

