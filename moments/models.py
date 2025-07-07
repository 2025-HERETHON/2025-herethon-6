from django.db import models

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    moment_id = models.IntegerField(null=True, blank=True)  # 추후 일기장 기본 crud 작성후 ForeignKey로 수정 예정
    image_url = models.URLField()
    image_name = models.CharField(max_length=255)

    def __str__(self):
        return self.image_name
