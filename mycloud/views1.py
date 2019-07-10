from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
import os
from LoginRegister.models import User
from mycloud.models import File


# change by zhang
def mypage(request):
    username = request.COOKIES.get('name', None)
    user = User.objects.get(name=username)
    ShowFiles = user.files.all()
    return render(request, 'mypage.html', {'ShowFiles': ShowFiles})


# change by zhang
def FileUpload(request):
    # 获取cookies的username
    username = request.COOKIES.get('name', None)

    if request.method == 'POST':
        # 获取文件
        obj = request.FILES.get('filename', None)
        uploadDirPath = os.path.join(os.getcwd(), 'files', username)

        if (getFileSize(uploadDirPath, obj.size) > 50 * 1024 * 1024):  # 待上传文件加上已经有的文件总共超出50M
            return redirect('/mycloud/mypage/')
            # 重定向回去不能带参数，所以无法显示message，我不知道咋弄了

        else:
            if not os.path.exists(uploadDirPath):
                os.mkdir(uploadDirPath)

            # 拼接全路径
            FileFullPath = uploadDirPath + os.sep + obj.name

            # 上传文件

            with open(FileFullPath, 'wb+') as fp:
                for chunk in obj.chunks():
                    fp.write(chunk)

            # File数据库写入       #change by zhang

            user = User.objects.get(name=username)
            File.objects.create(filename=obj.name, uploader=user, uploadername=username)

            return redirect('/mycloud/mypage/')

    else:
        return render(request, 'mypage.html')


def FileDownload(request, filename):
    # 定义一个内部函数分块读取下文件数据
    def fileIterator(downloadFilePath, chunkSize=512):
        # 读取二进制文件
        with open(downloadFilePath, 'rb') as fp:
            while True:
                content = fp.read(chunkSize)
                if content:
                    yield content
                else:
                    break

    username = request.COOKIES.get('name', None)

    # 获取下载文件的全路径
    downloadFilePath = os.path.join(os.getcwd(), 'files', username, filename)

    # 响应客户端
    rep = StreamingHttpResponse(fileIterator(downloadFilePath))
    # 设置响应对象的关键值选项
    rep['Content-Type'] = 'application/octet-stream'
    rep['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return rep


# change by zhang
def FileDelete(request, filename):
    username = request.COOKIES.get('name', None)

    deleteFilePath = os.path.join(os.getcwd(), 'files', username, filename)
    os.remove(deleteFilePath)

    # File数据库删除
    # 防止不同用户上传了同名文件，所以get时也需要用用户名来过滤
    File.objects.get(uploadername=username, filename=filename).delete()
    # return render(request, 'mypage.html')
    return redirect('/mycloud/mypage/')


def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    # return gmkb(size)
    return size
