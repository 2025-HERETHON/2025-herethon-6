from django.urls import path
from .views import signup  # 네 회원가입 뷰 이름 맞게 수정

urlpatterns = [
    path('signup/', signup, name='signup'),
]
