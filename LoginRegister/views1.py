from django.shortcuts import render,HttpResponse,redirect,render_to_response,HttpResponseRedirect
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from LoginRegister import models
from django.http import Http404
import uuid
import datetime
import pytz
import hashlib
import math
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自cqucloud的注册确认邮件'
    text_content = '''感谢注册CQUcloud，专注云服务\
                      请复制并转入此链接 http://{}/confirm/?code={} 完成注册\
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    html_content = '''
                        <p>感谢注册<p style="color:red">http://{}/confirm/?code={} </p>，\
                        来自cqucloud的注册确认邮件</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        user_name = confirm.user.name
        obj = models.User.objects.get(name=user_name)
        #obj.nickname = user_name
        obj.has_confiremed = True
        obj.save()
        print('typeyanzheng',type(obj))
        print('obj',obj.name,'xxxx',obj.nickname,obj.has_confiremed)#
        print('name',confirm.user.name,confirm.user.has_confirmed)#

        #confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    return render(request,'index.html')


def login(request):
    if request.method == 'GET':
        # return render(request,'login.html')
        raise Http404("你所访问的页面不存在")
        return render_to_response('404.html', status=404)
    if request.method == 'POST':
        username = request.POST['name']  # 前端发送过来的学生学号/老师用户名
        pwd = request.POST['pwd']
        print(username, type, pwd)
        obj = models.User.objects.all().values('name')
        stm = {'name': username}
        if stm not in obj:
            print("not exist")
            return HttpResponse("not exist")
        else:
            obj1 = models.User.objects.get(name=username)
            print("typedenglu", type(obj1))
            print('yonghuming', obj1.name, 'xxxx', obj1.nickname, obj1.has_confiremed)
            if not obj1.has_confiremed:
                print("not confirm")
                return HttpResponse("not_confirm")
            if check_password(pwd, obj1.password):
                request.session['user_info'] = obj1.name
                stu = HttpResponse("/mycloud/mypage/")
                stu.set_cookie('name', username, httponly=False)

                stu.set_cookie('pwd', pwd, httponly=False)
                return stu
            if not check_password(pwd, obj1.password):
                return HttpResponse("password error")


def register(request):
    if request.method == 'GET':
        #    return render(request,'register.html')
        raise Http404("你所访问的页面不存在")
        return render_to_response('404.html', status=404)
    if request.method == 'POST':
            nickname = request.POST['nickname1']
            email = request.POST['email1']
            #email = request.POST['email1']
            pwd1 = request.POST['pwd1']
            pwd2 = request.POST['pwd2']
            if pwd1!=pwd2:
                return HttpResponse("different")
            dj_pwd = make_password(pwd1)
            print(email, type, dj_pwd)

            stm = request.POST['name1']
            print(stm)
            obj = models.User.objects.all().values('name')
            print(obj)
            stmobj = {'name': stm}
            print("11111")
            same_email_user = models.User.objects.filter(email=email)
            if stmobj in obj:
                print("already exist")
                # context = {}
                # context['content'] = 'not exist'
                # return render(request,'index.html',context)
                return HttpResponse("error")
            if same_email_user:
                print("same")
                return HttpResponse("same_email")
            else:
                obj = models.User(email=email, password=dj_pwd, name=stm,nickname=nickname)
                obj.save()

                code = make_confirm_string(obj)
                print("code", code)
                send_email(email, code)

                #创建文件夹
                FilesDirPath = os.path.join(os.getcwd(), 'files', stm)
                os.mkdir(FilesDirPath)
                print("succ")
                return HttpResponse("success")

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name,now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

#change by an
def userinfo(request):
    t = request.COOKIES.get('name')
    if t != "":
        #return render(request, 'login/index.html')
        context = {}
        c = request.COOKIES.get('name')
        print("??",c)
        obj = models.User.objects.get(name=c)
        #imgPath = obj.imgpath
        nickname = obj.nickname
        username = obj.name
        email = obj.email
        imgPath = obj.imgpath
        #imgPath = "zwx/zwx.png"
        print('imgpath',imgPath)
        context['nickname'] = nickname
        context['name'] = username
        context['email'] = email
        context['img'] = imgPath
        return render(request,'userinfo.html',context)
    else:
        return redirect('/index', 302)

def change(request):
    oldname = request.COOKIES.get('name')
    print('旧名字',oldname)
    if request.method == 'POST':
         newusername = request.POST['newname']
         obj = models.User.objects.get(name=oldname)
         obj.name=newusername

         print('新名字',obj.name)
        #赵文璇修改更改用户文件夹名
         dirs = os.listdir(os.path.join(os.getcwd(),'media',oldname ))
         os.rename(os.path.join(os.getcwd(), 'files', oldname), os.path.join(os.getcwd(), 'files', newusername))
         os.rename(os.path.join(os.getcwd(), 'media', oldname), os.path.join(os.getcwd(), 'media', newusername))
         os.rename(os.path.join(os.getcwd(), 'media',newusername,dirs[0]),os.path.join(os.getcwd(), 'media', newusername,newusername+'.png') )
         obj.imgpath = newusername + "/" + newusername + '.png'

         #userinfo()
         obj.save()
         stu = HttpResponseRedirect("/userinfo/")
         stu.set_cookie('name', newusername, httponly=False)
         t = request.COOKIES.get('name')
         print("cookie",t)
         obj.save()
         return stu


def picupload(request):
    username = request.COOKIES.get('name')
    obj = models.User.objects.get(name=username)
    if request.POST:
        f = request.FILES.get('img1',None)
        print('33333',request.FILES)
        print('2222',f)
        fileType = os.path.splitext(f.name)[1] # 获取上传文件的扩展名
        # 创建可接受的类型的集合
        allowedTypes = ['.jpg', '.png', '.jpeg', '.bmp']
        if '.png' in allowedTypes:
            # 可以上传
            # 创建上传文件的文件夹
            startPath = settings.MEDIA_ROOT
            uploadDirPath = os.path.join(os.getcwd(), 'media',username+'1')
            print('upload dizhi', uploadDirPath)
            #uploadDirPath = os.path.join(os.getcwd(), 'media/upfile')
            if not os.path.exists(uploadDirPath):
                os.mkdir(uploadDirPath)
            # 生成唯一文件名
            newName = str(uuid.uuid1()) + '.png'
            # 拼接要上传的文件在服务器上的全路径
            filePath = os.path.join(os.getcwd(), 'media',username, username + '.png')
            #赵文璇修改
            if  os.path.exists(filePath):
                os.remove(filePath)
                print('filePath',filePath)

            #storePath = 'media/' + username + "/" + username + '.png'
            storePath =  username + "/" + username + '.png'
            print('store',storePath)
            # 上传文件
            with open(filePath, 'wb+') as fp:
                for chunk in f.chunks():
                    fp.write(chunk)
            obj.imgpath= storePath
            obj.save()

            print("ok")
            user1 = HttpResponseRedirect("/userinfo/")
            user1.set_cookie('imgpath', obj.imgpath, httponly=False)
            return user1
            #return render(request, 'userinfo.html', context)
        else:
            return render(request, 'userinfo.html', {'msg': '文件类型错误，请选择一张图片'})

    else:
        return render(request, 'userinfo.html')

#change by zwx
def mypage(request):
  t = request.COOKIES.get('name')
  if t != " ":
    print("ok")
    username = request.COOKIES.get('name', None)
    context={}

    user = models.User.objects.get(name=username)
    context['username'] = user.nickname
    context['name'] = user.name

    FilesDirPath = os.path.join(os.getcwd(), 'files', username)
    #context['ShowFiles'] = os.listdir(FilesDirPath)

    context['ShowFiles1'] = user.files.all()  ###################
    context['ShowFiles'] = list()
    #
    for i in context['ShowFiles1']:
        context['ShowFiles'].append(i.filename)

    print('????',context['ShowFiles'] )
    pathlist = []
    pic = []
    video = []
    office = []
    other = []

    for file in context['ShowFiles']:
        fileType = os.path.splitext(file)[1]
        Types1 = ['.jpg', '.png', '.jpeg', '.bmp']
        Types2 = ['.doc', '.docx','.docm','.dotx','.dotm']
        Types3 = ['.xls','.xlsx', '.xlsm', '.xltx', '.xltm','.xlsb','.xlam']
        Types4 = ['.mp4','.mov','.rm','.AVI']
        if fileType in Types1:
            imgPath = username+'/'+ file
            pic.append({'path':imgPath, 'file':file})
        elif fileType in Types2:
            imgPath = 'icons'+ '/' + 'doc.png'
            office.append({'path':imgPath, 'file':file})
        elif fileType in Types3:
            imgPath = 'icons'+ '/' + 'xls.png'
            office.append({'path':imgPath, 'file':file})
        elif fileType in Types4:
            imgPath = 'icons' + '/' + 'video.png'
            video.append({'path':imgPath, 'file':file})
        else:
            imgPath = os.path.join(os.getcwd(), 'static', 'icons', 'others.png')
            other.append({'path':imgPath, 'file':file})
        imgPath.replace('\\', '/')
        pathlist.append ({'path':imgPath, 'file':file})


    context['Imgpath']= pathlist   #全部
    context['Picture']= pic
    context['Videos']=video
    context['offices']=office
    context['others']=other
    print('path', context['Imgpath'])
    print('picturepath', context['Picture'])
    print('path', context['Videos'])
    print('path', context['offices'])
    print('path', context['others'])


    dlist = pathlist
    paginator = Paginator(dlist, 4)  # 每页显示4条
    page = request.GET.get('page', 1)
    print('page', page)
    try:
        dlist = paginator.page(page)
    except EmptyPage:
        dlist = paginator.page(1)
    except PageNotAnInteger:
        dlist = paginator.page(paginator.num_pages)

    context['dlist'] = dlist
    print('dlist', dlist)


    dlistother = other
    print("dlistother",dlistother)
    paginator = Paginator(dlistother, 4)  # 每页显示4条
    page = request.GET.get('page', 1)
    print('page', page)
    try:
        dlistother = paginator.page(page)
    except EmptyPage:
        dlistother = paginator.page(1)
    except PageNotAnInteger:
        dlistother = paginator.page(paginator.num_pages)

    context['dlistother'] = dlistother
    print('dlist', dlistother)


    dlistoffice = office
    paginator = Paginator(dlistoffice, 4)  # 每页显示4条
    page = request.GET.get('page', 1)
    print('page',page)
    try:
        dlistoffice = paginator.page(page)
    except EmptyPage:
        dlistoffice = paginator.page(1)
    except PageNotAnInteger:
        dlistoffice = paginator.page(paginator.num_pages)

    context['dlistoffice'] = dlistoffice
    print('dlistoffice', dlistoffice)



    dlistvideo =video
    paginator = Paginator(dlistvideo, 4)  # 每页显示4条
    page = request.GET.get('page', 1)
    print('page',page)
    try:
        dlistvideo = paginator.page(page)
    except EmptyPage:
        dlistvideo = paginator.page(1)
    except PageNotAnInteger:
        dlistvideo = paginator.page(paginator.num_pages)

    context['dlistvideo'] = dlistvideo
    print('dlistvideo', dlistvideo)


    dlistpic = pic
    paginator = Paginator(dlistpic, 4)  # 每页显示4条
    page = request.GET.get('page', 1)
    print('page',page)
    try:
        dlistpic = paginator.page(page)
    except EmptyPage:
        dlistpic = paginator.page(1)
    except PageNotAnInteger:
        dlistpic = paginator.page(paginator.num_pages)

    context['dlistpic'] = dlistpic
    print('dlistpic', dlistpic)

    uploadDirPath = os.path.join(os.getcwd(), 'files', username)
    context["size"]= int(getFileSize(uploadDirPath, size=0) / 1048576)
    context["size_"] = 50-int(getFileSize(uploadDirPath, size=0) / 1048576)
    context["size1"] = (int(getFileSize(uploadDirPath, size=0) / 1048576))*2
    context["size2"] = 100-context["size1"]
    return render(request, 'mypage.html', context)
  else:
    return redirect('/index', 302)


def search(request):
    t = request.COOKIES.get('name')
    if t != " ":
        print("ok")
        username = request.COOKIES.get('name', None)
        context = {}
        FilesDirPath = os.path.join(os.getcwd(), 'files', username)
        # context['ShowFiles'] = os.listdir(FilesDirPath)
        user = models.User.objects.get(name=username)
        context['username'] = user.nickname
        context['ShowFiles1'] = user.files.all()  ###################
        context['ShowFiles'] = list()
        #
        for i in context['ShowFiles1']:
            context['ShowFiles'].append(i.filename)

        print('????', context['ShowFiles'])
        selected = []
        if request.method == 'GET':
            kw = request.GET.get('search', None)
            print('kwwww', kw)
            for file in context['ShowFiles']:
                if (kw in file):
                    fileType = os.path.splitext(file)[1]
                    Types1 = ['.jpg', '.png', '.jpeg', '.bmp']
                    Types2 = ['.doc', '.docx', '.docm', '.dotx', '.dotm']
                    Types3 = ['.xls', '.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xlam']
                    Types4 = ['.mp4', '.mov', '.rm', '.AVI']
                    if fileType in Types1:
                        imgPath = username + '/' + file
                    elif fileType in Types2:
                        imgPath = 'icons' + '/' + 'doc.png'
                    elif fileType in Types3:
                        imgPath = 'icons' + '/' + 'xls.png'
                    elif fileType in Types4:
                        imgPath = 'icons' + '/' + 'video.png'
                    else:
                        imgPath = 'icons' + '/' + 'others.png'
                    print('path', imgPath)
                    selected.append({'path': imgPath, 'file': file})

            context['seleted'] = selected
            print('???', selected, type(selected))
            print('json', json.dumps(selected), type(json.dumps(selected)))
            data4 = json.dumps(list(selected), cls=DjangoJSONEncoder)
            print(data4)
            return HttpResponse(json.dumps(selected, cls=DjangoJSONEncoder))



def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    # return gmkb(size)
    return size


