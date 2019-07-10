from django.db import models
import uuid
# Create your models here.


class User(models.Model):

    # 用户名 密码 邮箱 验证码
    nickname = models.CharField(max_length=128,verbose_name = "昵称")
    uid=models.AutoField(primary_key=True,verbose_name = "id")
    name = models.CharField(max_length=128, unique=True,verbose_name = "用户名")
    imgpath = models.CharField(max_length=80,default="moren/moren123.jpg",verbose_name = "头像")
    has_confiremed = models.BooleanField(default=False,verbose_name = "验证状态")
    password = models.CharField(max_length=256,verbose_name = "密码")
    email = models.EmailField(unique=True,verbose_name = "邮箱")
    c_time = models.DateTimeField(auto_now_add=True,verbose_name = "注册时间")

    used = models.IntegerField(default=0,verbose_name = "已用空间")
    available = models.IntegerField(default=50,verbose_name = "可用空间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "云盘用户"
        verbose_name_plural = "云盘用户"

class ConfirmString(models.Model):
    code = models.CharField(max_length=256,verbose_name = "确认码")
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "认证用户")
    c_time = models.DateTimeField(auto_now_add=True,verbose_name = "认证时间")

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"