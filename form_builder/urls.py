#importing Django's function path
from django.urls import path
#importing views from blog application
from . import views

#assigning a view called post_list to the root URL
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('CLIPPER/', views.CLIP_form, name='CLIP_form'),
    path('clipper/', views.CLIP_form, name='CLIP_form'),
]