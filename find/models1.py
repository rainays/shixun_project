from django.db import models
from LoginRegister.models import User

#动态
class Dynamic(models.Model):
    nid = models.BigAutoField(primary_key=True)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    author = models.ForeignKey(User,verbose_name='作者',to_field='uid', on_delete=models.CASCADE)

#记录赞表
class Up(models.Model):
    nid = models.BigAutoField(primary_key=True)
    dynamic = models.ForeignKey(Dynamic,verbose_name='文章', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='赞用户', to_field='uid', on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='是否赞')

#评论表
class Comment(models.Model):
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    dynamic = models.ForeignKey(Dynamic,verbose_name='评论文章', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='评论者',to_field='uid', on_delete=models.CASCADE)


#回复表
class Reply(models.Model):
    nid = models.BigAutoField(primary_key=True)
    dynamic = models.ForeignKey(Dynamic,verbose_name="回复文章", to_field="nid", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="回复内容", max_length=255)
    user = models.ForeignKey(User,verbose_name="回复用户",to_field='uid', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,verbose_name="回复评论",to_field='nid', on_delete=models.CASCADE)