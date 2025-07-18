from django.urls import path, include
from .views.moment_views import moment_create, moment_list, moment_detail, moment_update, moment_delete, toggle_like
from .views.image_views import images_by_moment, delete_image
from .views.keyword_views import get_weekly_keywords

urlpatterns = [
    # 글 작성 path
    path('create/', moment_create, name='moment_create'),                 # POST /moments/create
    path('<int:moment_id>/list/', moment_list, name='moment_list'),       # GET /moments (글 생성, 목록 조회[카테고리별])
    path('<int:moment_id>/detail/', moment_detail, name='moment_detail'), # GET /moments/<id>/detail (개별 게시글 조회) 
    path('<int:moment_id>/update/', moment_update, name='moment_update'), # POST (PUT 역할) /moments/<id>/update/
    path('<int:moment_id>/delete/', moment_delete, name='moment_delete'), # DELETE /moments/<id>/delete/

    # 이미지 관련 path
    path('<int:moment_id>/images/', images_by_moment, name='images_by_moment'), # 이미지 기본 CRUD는 글별 전체 이미지를 처리
    path('<int:moment_id>/images/<int:image_id>/', delete_image), # 삭제는 특정 이미지도 가능

    # 댓글 관련 path
    path('<int:moment_id>/comments/', include('comments.urls')),
    
    # top3 관련 path
    path('weekly_keywords/<int:category_id>/', get_weekly_keywords, name='weekly_keywords'),
    
    # 좋아요 관련 path
    path('<int:moment_id>/toggle_like/', toggle_like, name='toggle_like'),
]
