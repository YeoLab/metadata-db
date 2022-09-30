#importing Django's function path
from django.urls import path
#importing views from blog application
from . import views

#assigning a view called post_list to the root URL
urlpatterns = [
    path('', views.index_view, name='index_view'),
    # post/ means URL should begin w/ word post/
    # <int:pk> expects integer value and transfer it to a view as a variable called pk
    # / before finishing URL
    path('CLIPPER/', views.CLIP_form, name='CLIP_form'),
    path('SKIPPER/', views.SKIPPER_form, name='SKIPPER_form'),
    path('clipper/', views.CLIP_form, name='CLIP_form'),
    path('skipper/', views.SKIPPER_form, name='SKIPPER_form'),
]