from django.contrib import admin
from django.urls import path


from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),

    path("logout/", views.logout, name='logout'),
    path("signup/", views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),


]