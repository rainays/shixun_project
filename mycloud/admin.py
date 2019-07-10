from django.contrib import admin
from mycloud import models
# Register your models here.

class FileAdmin(admin.ModelAdmin):
    #列表页属性
    list_display = ('fid','filename','uploader','upload_date')
    list_filter=['uploader','filename','uploadername']
    search_fields=['uploader','filename']
    list_per_page=20
    #添加修改页属性
    fields=['uploader','uploadername','filename']
admin.site.register(models.File,FileAdmin)
