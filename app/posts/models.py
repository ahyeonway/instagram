from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ctrl+클릭하면 원본소스 볼 수 있읍
    # imagefield는 filefield를 상속받은 걸 확인할 수 있습니다
    # 어디로 올라갈지 정해줘야 함 upload_to
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    #auto_now_add처음 create될때, auto_now는 저장될때마다 사용
    created_at = models.DateTimeField(auto_now_add=True)


