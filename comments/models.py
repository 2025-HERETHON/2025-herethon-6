from django.db import models
from django.utils.timezone import now
from moments.models import Moment  
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True) 
    moment_id = models.ForeignKey(Moment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=now)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.moment_id}][{self.comment_id}] {self.user_id.nickname} - {self.content[:20]}"
    # 아래의 형식으로 출력하는 함수
    # [2][7] 닉네임 - 댓글 내용입니다. 