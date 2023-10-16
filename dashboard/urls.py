from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_login, name='login'),
    path('dashboard/', views.home, name="home"),
    path('instructions/', views.instructions, name='instructions'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('quiz_question/', views.quiz_question, name='quiz_question'),
    path('quiz_result/', views.quiz_result, name='quiz_result'),
    path('register/', views.register, name='register'),
    path('logout', views.auth_logout, name='logout'),
]
