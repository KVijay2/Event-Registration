from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index, name='home'),

    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('user/<str:pk>/', views.user, name='profile'),
    path('event/<str:pk>/', views.event, name='event'),
    path('registration-confirmation/<str:pk>/', views.event_confirmation, name="registration-confirmation"),

    path('account/', views.account, name="account"),
    path('project-submission/<str:pk>/',views.submission,name='project-submission'),
    
    path('update-submission/<str:pk>/', views.update_submission, name="update-submission"),
]