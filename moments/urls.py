from django.urls import path, include
from .views.moment_views import moment_root, moment_detail_root, moment_update
from .views.image_views import images_by_moment, delete_image

urlpatterns = [
    # 글 작성 path
    path('', moment_root, name='moment_root'),          # POST /moments || GET /moments (글 생성, 목록 조회[카테고리별])
    path('<int:moment_id>/', moment_detail_root, name='moment_detail_root'), 
    # GET /moments/<id> (개별 게시글 조회) || DELETE /moments/<id>
    path('<int:moment_id>/update/', moment_update, name='moment_update'), # POST (PUT 역할) /moments/<id>/update/

    # 이미지 관련 path
    path('<int:moment_id>/images/', images_by_moment, name='images_by_moment'), # 이미지 기본 CRUD는 글별 전체 이미지를 처리
    path('<int:moment_id>/images/<int:image_id>/', delete_image), # 삭제는 특정 이미지도 가능

    # 댓글 관련 path
    path('<int:moment_id>/comments/', include('comments.urls')),
]
