from . import views
from django.urls import path

app_name = 'fields'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_field, name='create_field'),
    path('field/<int:pk>/update/', views.update_field, name='update_field'),
]