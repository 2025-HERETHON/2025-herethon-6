from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Moment(models.Model):
    moment_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()  # 실패담
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=[('public', '공개'), ('private', '비공개')], default='public')

    def __str__(self):
        return self.title


class If(models.Model):
    if_id = models.AutoField(primary_key=True)
    moment_id = models.OneToOneField(Moment, on_delete=models.CASCADE, related_name="if_moment")
    if_content = models.TextField()  # 내가 다시 돌아간다면
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"If for {self.moment_id.title}"
    

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    moment_id = models.ForeignKey(Moment, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField()
    image_name = models.CharField(max_length=255)

    def __str__(self):
        return self.image_name
    
class WeeklyTop3Keyword(models.Model):
    week_start = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    keywords = models.JSONField()

    class Meta:
        unique_together = ('week_start', 'category') # 한 주에 카테고리당 하나만

    def __str__(self):
        return f"{self.week_start} - {self.category.name}"
    
class Like(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('moment', 'user')  # 한 유저는 한 글에 좋아요 한 번만 가능

    def __str__(self):
        return f"{self.user} liked {self.moment.title}"