from django.urls import path

from . import views

app_name = 'vote'
urlpatterns = [
    path('poll/', views.ListingAllPollView.as_view(), name='poll_listing'),
    path('poll/create/', views.CreatePollView.as_view(), name='create_poll'),
]