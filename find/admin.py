from django.contrib import admin
from find import models
# Register your models here.
class DynamicAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('nid','author','content','create_time','up_count','collect_count','comment_count')
    list_filter=['author']
    search_fields=['content']
    list_per_page=20
    #添加修改页属性
    fieldsets=[
        ('基本信息',{'fields':['author','content']}),
        ('其它',{'fields':['up_count','collect_count','comment_count']}),]

class UpAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('nid','dynamic','user','is_up')
    list_filter=['user','dynamic']
    search_fields=['user','dynamic']
    list_per_page=20
    #添加修改页属性
    fields=['user','dynamic','is_up']

class CollectAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('nid','dynamic','user','is_collect')
    list_filter=['user','dynamic']
    search_fields=['user','dynamic']
    list_per_page=20
    #添加修改页属性
    fields=['user','dynamic','is_collect']

class CommentAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('nid','user','content','create_time','dynamic')
    list_filter=['user','dynamic']
    search_fields=['user','content','dynamic']
    list_per_page=20
    #添加修改页属性
    fields=['user','dynamic','content']

class ReplyAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('nid','user','content','create_time','comment','dynamic')
    list_filter=['user','comment','dynamic']
    search_fields=['user','content','comment','dynamic']
    list_per_page=20
    #添加修改页属性
    fields=['user','dynamic','comment','content']

admin.site.register(models.Dynamic,DynamicAdmin)
admin.site.register(models.Up,UpAdmin)
admin.site.register(models.Collect,CollectAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Reply,ReplyAdmin)