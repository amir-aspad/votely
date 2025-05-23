from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vote/', include('vote.urls', namespace='vote'))
]
