from django.urls import path
from .views.image_views import images_by_moment, delete_image

urlpatterns = [
    path('<int:moment_id>/images/', images_by_moment, name='images_by_moment'), # 이미지 기본 CRUD는 글별 전체 이미지를 처리
    path('<int:moment_id>/images/<int:image_id>/', delete_image) # 삭제는 특정 이미지도 가능
]
