from django.urls import path
from moments.views.moment_views import (
    moment_create_view, moment_list_view, moment_detail_view, moment_update_view
)

urlpatterns = [
    path('create/', moment_create_view, name='moment_create_view'),
    path('list/', moment_list_view, name='moment_list_view'),
    path('<int:moment_id>/detail/', moment_detail_view, name='moment_detail_view'),
    path('<int:moment_id>/update/', moment_update_view, name='moment_update_view'),
]
