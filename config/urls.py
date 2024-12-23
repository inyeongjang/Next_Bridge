from django.contrib import admin
from django.urls import path, include

from home.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('common/', include('common.urls')),
    path('jobs/', include('jobs.urls')),
    path('reviews/', include('reviews.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]
