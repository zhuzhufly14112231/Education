from django.test import TestCase
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your tests here.

# 接口模型继承
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Text(BaseContent):
    body = models.TextField()

# 多表继承
# Text 表中除了有body字段,还有一个一对一的外键关联BaseContent表
class BaseConent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class Text(BaseContent):
    body = models.TextField()

# 代理模型
class OrderContent(BaseContent):
    class Meta:
        proxy = True

    def get_title(self):
        return self.title

