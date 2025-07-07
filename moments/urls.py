from django.urls import path
from .views import images_by_moment

urlpatterns = [
    path('moment/<int:moment_id>/images/', images_by_moment, name='images_by_moment'),
]
