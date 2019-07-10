from django.db import models
import uuid
# Create your models here.


class User(models.Model):

    # 用户名 密码 邮箱 验证码
    nickname = models.CharField(max_length=128)
    uid=models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    imgpath = models.CharField(max_length=80,default="moren/moren123.jpg")
    has_confiremed = models.BooleanField(default=False)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    used = models.IntegerField(default=0,verbose_name = "已用空间")    #change by zhang
    available = models.IntegerField(default=50,verbose_name = "可用空间") #change by zhang

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"