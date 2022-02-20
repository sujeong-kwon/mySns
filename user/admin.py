from django.contrib import admin
from .models import UserModel
#.models는 동일한 위치에 있는 파이썬 파일(models.py)을 불러오겠단 의미, 그 중에서 UserModel을 가져옴

# Register your models here.
admin.site.register(UserModel)
#가져온 UserModel을 관리자페이지에 넣어주겠단 의미