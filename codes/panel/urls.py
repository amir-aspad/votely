from django.urls import path

from . import views

app_name = 'panel'
urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('register/verify/', views.RegisterVerifyCodeView.as_view(), name='verfiy'),
]