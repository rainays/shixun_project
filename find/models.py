from django.db import models
from LoginRegister.models import User

#动态
class Dynamic(models.Model):
    nid = models.BigAutoField(primary_key=True,verbose_name = "id")
    comment_count = models.IntegerField(default=0,verbose_name = "评论数")
    up_count = models.IntegerField(default=0,verbose_name = "点赞数")
    collect_count = models.IntegerField(default=0,verbose_name = "收藏数")
    content = models.TextField(verbose_name = "动态内容")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    author = models.ForeignKey(User,verbose_name='作者',to_field='uid', on_delete=models.CASCADE)
    def __str__(self):
        return self.author.name+ ":   " +self.content
    class Meta:
        verbose_name_plural = "动态"

#记录赞表
class Up(models.Model):
    nid = models.BigAutoField(primary_key=True,verbose_name = "id")
    dynamic = models.ForeignKey(Dynamic,verbose_name='点赞动态', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='点赞用户', to_field='uid', on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='点赞状态')
    class Meta:
        verbose_name_plural = "点赞记录表"

#记录收藏表
class Collect(models.Model):
    nid = models.BigAutoField(primary_key=True,verbose_name = "id")
    dynamic = models.ForeignKey(Dynamic,verbose_name='收藏动态', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='收藏用户', to_field='uid', on_delete=models.CASCADE)
    is_collect = models.BooleanField(verbose_name='收藏状态')
    class Meta:
        verbose_name_plural = "收藏记录表"

#评论表
class Comment(models.Model):
    nid = models.BigAutoField(primary_key=True,verbose_name = "id")
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    dynamic = models.ForeignKey(Dynamic,verbose_name='所评动态', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='评论者',to_field='uid', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name+ ":   " +self.content 
    class Meta:
        verbose_name_plural = "评论"


#回复表
class Reply(models.Model):
    nid = models.BigAutoField(primary_key=True,verbose_name = "id")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    dynamic = models.ForeignKey(Dynamic,verbose_name="所回动态", to_field="nid", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="回复内容", max_length=255)
    user = models.ForeignKey(User,verbose_name="回复者",to_field='uid', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,verbose_name="所回评论",to_field='nid', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name+ ":   " +self.content
    class Meta:
        verbose_name_plural = "回复"