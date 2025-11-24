from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('user/<int:pk>/', views.user_edit, name='user_edit'),
    path('user/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
