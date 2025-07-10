from django.urls import path
from .views import comment_root, comment_detail_root

urlpatterns = [
    path('', comment_root, name='comment_root'),                            # GET, POST
    path('<int:comment_id>/', comment_detail_root, name='comment_detail'),  # POST(PUT 기능), DELETE
]
