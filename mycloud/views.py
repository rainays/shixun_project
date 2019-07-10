from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
import os
from LoginRegister.models import User
from mycloud.models import File
import base64


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

            #更新可用空间和已用空间
            #不能直接用.get().update()
            #.get() returns an individual object and .update() only works on querysets
            #所以要么用save要么用.filter()
            user = User.objects.get(name=username)
            user.used=gmkb(getFileSize(uploadDirPath))[1]
            user.available=50 - gmkb(getFileSize(uploadDirPath))[1]
            user.save()
            # File数据库写入       #change by zhang
            File.objects.create(filename=obj.name, uploader=user, uploadername=username)

            return redirect('/mycloud/mypage/')

    else:
        return render(request, 'mypage.html')



def FileDelete(request, filename):
    username = request.COOKIES.get('name', None)

    DirPath = os.path.join(os.getcwd(), 'files', username)
    deleteFilePath = os.path.join(os.getcwd(), 'files', username, filename)
    os.remove(deleteFilePath)

    # File数据库删除
    # 防止不同用户上传了同名文件，所以get时也需要用用


# def FileDownload(request, filename):
#     # 定义一个内部函数分块读取下文件数据
#     def fileIterator(downloadFilePath, chunkSize=512):
#         # 读取二进制文件
#         with open(downloadFilePath, 'rb') as fp:
#             while True:
#                 content = fp.read(chunkSize)
#                 if content:
#                     yield content
#                 else:
#                     break

#     username = request.COOKIES.get('name', None)

#     # 获取下载文件的全路径
#     downloadFilePath = os.path.join(os.getcwd(), 'files', username, filename)

#     # 响应客户端
#     rep = StreamingHttpResponse(fileIterator(downloadFilePath))
#     # 设置响应对象的关键值选项
#     rep['Content-Type'] = 'application/octet-stream'
#     rep['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
#     return rep
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

    DirPath = os.path.join(os.getcwd(), 'files', username)
    deleteFilePath = os.path.join(os.getcwd(), 'files', username, filename)
    os.remove(deleteFilePath)

    # File数据库删除
    # 防止不同用户上传了同名文件，所以get时也需要用用户名来过滤
    File.objects.get(uploadername=username, filename=filename).delete()
    # return render(request, 'mypage.html')

    # 更新已用空间和可用空间
    User.objects.get(name=username).update(used=gmkb(getFileSize(DirPath))[1],available=50 - gmkb(getFileSize(DirPath))[1])

    return redirect('/mycloud/mypage/')

def gmkb(bites):        #换算成相应的单位便于查看
    gb=mb=kb=bb=0
    if(bites >= 1024):
        kb = bites/1024
        bb = bites%1024
        if kb >= 1024 :
            mb = kb/1024
            kb = kb%1024
            if mb >= 1024 :
                gb = mb/1024
                mb = mb%1024
            else:
                gb = 0
        else:
            mb = 0
    else:
        kb = 0
        bb = bites
    return [int(gb), int(mb), int(kb), int(bb)]      #取消小数点输出



def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    # return gmkb(size)
    return size

# def ShareDownloadPage(request, link):
#     link = base64.b64decode(link).decode()
#     filename = link.split('/')[1]
#     context = {}
#     context['path'] = link
#     context['filename'] = filename
#     #print(context['path'],)
#     # filetype = filename.
#     # 获取文件类型你们自己写，然后加到context里面
#     filetype = os.path.splitext(filename)[1]
#     context['fileType'] = filetype
#     return render(request, 'ShareDownloadPage.html', context)
# def ShareDownloadPage(request, link):
#     link = base64.b64decode(link).decode()
#     filename = link.split('/')[1]
#     context = {}
#     context['path'] = link
#     context['filename'] = filename

#     pathlist=[]

#     fileType = os.path.splitext(filename)[1]
#     Types1 = ['.jpg', '.png', '.jpeg', '.bmp']
#     Types2 = ['.doc', '.docx','.docm','.dotx','.dotm']
#     Types3 = ['.xls','.xlsx', '.xlsm', '.xltx', '.xltm','.xlsb','.xlam']
#     Types4 = ['.mp4','.mov','.rm','.AVI']
#     if fileType in Types1:
#         imgPath = link

#     elif fileType in Types2:
#         imgPath = 'icons'+ '/' + 'doc.png'

#     elif fileType in Types3:
#         imgPath = 'icons'+ '/' + 'xls.png'

#     elif fileType in Types4:
#         imgPath = 'icons' + '/' + 'video.png'

#     else:
#         imgPath = 'icons' + '/' + 'others.png'

#     imgPath.replace('\\', '/')

#     context['Imgpath']= imgPath   #全部
#     return render(request, 'ShareDownloadPage.html', context)


def ShareDownloadPage(request, link):
    link = base64.b64decode(link).decode()
    filename = link.split('/')[1]
    user=link.split('/')[0]
    context = {}
    context['path'] = link
    context['filename'] = filename
    context['user']=user
    pathlist=[]

    fileType = os.path.splitext(filename)[1]
    Types1 = ['.jpg', '.png', '.jpeg', '.bmp']
    Types2 = ['.doc', '.docx','.docm','.dotx','.dotm']
    Types3 = ['.xls','.xlsx', '.xlsm', '.xltx', '.xltm','.xlsb','.xlam']
    Types4 = ['.mp4','.mov','.rm','.AVI']
    if fileType in Types1:
        imgPath = link

    elif fileType in Types2:
        imgPath = 'icons'+ '/' + 'doc.png'

    elif fileType in Types3:
        imgPath = 'icons'+ '/' + 'xls.png'

    elif fileType in Types4:
        imgPath = 'icons' + '/' + 'video.png'

    else:
        imgPath = 'icons' + '/' + 'others.png'

    imgPath.replace('\\', '/')

    context['Imgpath']= imgPath   #全部


    return render(request, 'ShareDownloadPage.html', context)

def ShareDownload(request, username, filename):
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

    # 获取下载文件的全路径
    downloadFilePath = os.path.join(os.getcwd(), 'files', username, filename)

    # 响应客户端
    rep = StreamingHttpResponse(fileIterator(downloadFilePath))
    # 设置响应对象的关键值选项
    rep['Content-Type'] = 'application/octet-stream'
    rep['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return rep

def yulan(request,user,filename):
    context = {}
    path = user+'/'+filename
    print(path)
    context['path'] = path
    #print(path,filename)
    return render(request,'yulan.html',context)

def yulan2(request,user,filename):
    context = {}
    path = user+'/'+filename
    print(path)
    context['path'] = path
    #print(path,filename)
    return render(request,'shipin.html',context)
