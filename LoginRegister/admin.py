from django.contrib import admin
from LoginRegister import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('uid','name','nickname','used','available','email','c_time','has_confiremed')
    list_filter=['nickname','has_confiremed']
    search_fields=['name','nickname','email']
    list_per_page=20
    #添加修改页属性
    fieldsets=[
        ('基本信息',{'fields':['name','nickname','password']}),
        ('其它',{'fields':['imgpath','email','has_confiremed']}),]

class ConfirmStringAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('id','user','c_time')
    search_fields=['user']
    list_per_page=20
admin.site.register(models.User,UserAdmin)
admin.site.register(models.ConfirmString,ConfirmStringAdmin)
