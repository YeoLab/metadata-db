#importing Django's function path
from django.urls import path
#importing views from blog application
from . import views

#assigning a view called post_list to the root URL
urlpatterns = [
    path('', views.post_list, name='post_list'),
    # post/ means URL should begin w/ word post/
    # <int:pk> expects integer value and transfer it to a view as a variable called pk
    # / before finishing URL
    path('post/<int:pk>/', views.post_detail, name = 'post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('CLIP/', views.CLIP_form, name='CLIP_form'),
    path('SKIPPER/', views.SKIPPER_form, name='SKIPPER_form'),
]