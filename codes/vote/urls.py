from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'vote'
urlpatterns = [
    path('poll/', views.ListingAllPollView.as_view(), name='poll_listing'),
]


router = DefaultRouter()
router.register(r'poll', views.PollViewSet, basename='poll')

urlpatterns += router.urls