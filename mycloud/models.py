from django.db import models
from LoginRegister.models import User
# Create your models here.
class File(models.Model):
    fid = models.AutoField(primary_key=True,verbose_name = "id")
    
    filename = models.CharField(max_length=80,verbose_name = "文件名")
    #FilePathField实在不会用，遂放弃，用CharField

    uploadername = models.CharField(max_length=80)
    upload_date = models.DateField(auto_now_add=True,verbose_name = "上传时间")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files',verbose_name = "上传者")
    def __str__(self):
        return self.uploader.name+": "+self.filename
        verbose_name_plural = "云文件"

    class Meta:  
        verbose_name_plural = "云文件"  