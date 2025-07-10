from django.urls import path
from .views import comment_create, comment_list, comment_update, comment_delete

urlpatterns = [
    path('create/', comment_create, name='comment_create'),  # POST
    path('list/', comment_list, name='comment_list'),        # GET
    path('<int:comment_id>/update/', comment_update, name='comment_update'),  # POST(PUT 기능)
    path('<int:comment_id>/delete/', comment_delete, name='comment_delete'),  # DELETE
]
