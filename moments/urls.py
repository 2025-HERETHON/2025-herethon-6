from django.urls import path
from .views import get_imgaes_by_moment

urlpatterns = [
    path('moment/<int:moment_id>/images/', get_imgaes_by_moment, name='images_by_moment'),
]
