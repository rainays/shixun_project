from django.db import models
from LoginRegister.models import User
# Create your models here.
class File(models.Model):
    fid = models.AutoField(primary_key=True)
    
    filename = models.CharField(max_length=80)
    #FilePathField实在不会用，遂放弃，用CharField

    uploadername = models.CharField(max_length=80)
    upload_date = models.DateField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')