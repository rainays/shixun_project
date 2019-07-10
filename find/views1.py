from django.shortcuts import render,HttpResponse,redirect,render_to_response,HttpResponseRedirect
import os
from find import models
from django.http import Http404
from django.core.paginator import Paginator

#检验登陆状态
def check_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/index/')
    return inner

#写动态（转到写动态的界面的url必须为find/write/【用户名】）
#写完动态的跳转链接也需自行设计
@check_login
def create_dynamic(request, author_name):
    #if request.method == "GET":
     #   return render(request, 'write.html', {'author_name': author_name})
    if request.method == "POST":
        d_content = request.POST.get('content')
        print("XXXXXX:",d_content)
        print("YYYYYY:",author_name)
        a_name = models.User.objects.get(name=author_name)
        obj = models.Dynamic.objects.create( content = d_content,author = a_name)
        return redirect("/find/show/")

#删动态（转到删除动态的界面的url必须为find/delete/【动态的id】）
#由于不清楚路由设置没有设置返回的路由，请对接时按照规定自行设计
@check_login
def delete_dynamic(request, dynamic_id):
    obj = models.Dynamic.objects.get(nid=dynamic_id)
    models.Dynamic.objects.filter(nid=dynamic_id).delete()
    return HttpResponse("AAAAA")
    #return redirect(to='/mine/' + request.session['user_info']['username'])


#动态详情
def detail(request, dynamic_id):
    obj = models.Dynamic.objects.get(nid=dynamic_id)
    d_name = obj.author
    obj_user = models.User.objects.get(name=d_name)
    head = obj_user.imgpath
    d_content = obj.content
    d_time = obj.create_time
    d_up_count = obj.up_count
    d_comment_count = obj.comment_count
    return render(request, 'detail.html', {'content': d_content,'author_name': d_name,
                                            'create_time': d_time, 'author_head':head,
                                            'up_num':d_up_count,'comment_num':d_comment_count})


#动态列表
def show_list(request):
        order = request.GET.get('order')
        name = request.COOKIES.get('name')
        obj1 = models.User.objects.get(name=name)
        #user_id =obj1.uid

        print('uid',obj1.uid)
        if order=="create_time":
            dynamic_list = models.Dynamic.objects.all().order_by('-create_time')
        elif order=="up_count":
            dynamic_list = models.Dynamic.objects.all().order_by('-up_count')
        elif order=="comment_count":
            dynamic_list = models.Dynamic.objects.all().order_by('-comment_count')
        else:dynamic_list = models.Dynamic.objects.all().order_by('-create_time')
        paginator = Paginator(dynamic_list, 8)
        # 获取 url 中的页码
        page = request.GET.get('page')
        # 将导航对象相应的页码内容返回给 articles
        dynamics = paginator.get_page(page)
        #打印的结果：<Page 1 of 1>
        #返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法
        #如：可以通过dynamics.object_list获得当前页的所有动态对象
        # 需要传递给模板（templates）的对象
        context = {}
        context['articles'] = dynamics
        context['nickname'] = obj1.nickname
        context['names'] = name
        context['imgpath'] = obj1.imgpath
        context['userid'] = obj1.uid
        listdic = []
        listdic = list(dynamics.object_list)
        context['list'] = listdic
        print('type',context['list'])
        for i in listdic:
          print('g',i.author.name,i.author.uid)

        print(context['nickname'])
        print('dddd',context['articles'],context['list'])
        # render函数：载入模板，并返回context对象
        return render(request, 'social.html', context)

#点赞
@check_login
def good(request, dynamic_id, user_id):
    result = {'status': True}
    if models.Up.objects.filter(dynamic=dynamic_id, user=user_id):
        result = {'status': False}
        #return HttpResponse(json.dumps(result))
        return HttpResponse("fail")
    else:
        d_obj = models.Dynamic.objects.get(nid=dynamic_id)
        u_obj = models.User.objects.get(uid=user_id)
        models.Up.objects.create(is_up=False, dynamic=d_obj, user=u_obj)
        new_up_count = int(models.Dynamic.objects.get(nid=dynamic_id).up_count + 1)
        models.Dynamic.objects.filter(nid=dynamic_id).update(up_count=str(new_up_count))
        models.Up.objects.filter(dynamic_id=dynamic_id, user_id=user_id).update(is_up=True)
        #return HttpResponse(json.dumps(result))
        return HttpResponse("success")

#查看指定用户所发的所有动态
# def user_dynamic(request,user_id):
#     obj_user = models.User.objects.get(uid=user_id)
#     user_name = obj_user.name
#     print('username',user_name)
#     dynamic_list = models.Dynamic.objects.filter(author=obj_user)
#     print(dynamic_list)
#     #return HttpResponse("success") 'dynamic_list': dynamic_list,
#     context = {}
#     context['dynamic_list'] =dynamic_list
#     if obj_user.name == request.COOKIES.get('name'):
#         return render(request, 'myshare.html', context)
#     else:
#         return render(request, 'other.html', context)

def user_dynamic(request,user_id):
    obj_user = models.User.objects.get(uid=user_id)
    order = request.GET.get('order')
    if order=="create_time":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-create_time')
    elif order=="up_count":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-up_count')
    elif order=="comment_count":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-comment_count')
    else:dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-create_time')
    paginator = Paginator(dynamic_list, 8)
    # 获取 url 中的页码
    paginator = Paginator(dynamic_list, 8)
    # 获取 url 中的页码
    page = request.GET.get('page')
    dynamics = paginator.get_page(page)
    allobj_dynamics=list(dynamics.object_list)
    context = {}
    context['allobj_dynamics'] = dynamics
    context['userid'] = user_id
    print(obj_user.uid)
    print('name',obj_user.name,request.COOKIES.get('name'))
    if obj_user.name == request.COOKIES.get('name'):
    #if obj_user == request.session.get('user_info'):
        return render(request, 'myshare.html', context)
    else:
        return render(request, 'user.html', context)


#关键词动态搜索
def search_dynamic(request):
    dynamic = models.Dynamic.objects.all()
    show_dynamic = list()
    for i in dynamic:
        show_dynamic.append(i.content)
    selected = []
    if request.method == 'POST':
        kw = request.POST.get('keywords')
        for icontent in show_dynamic:
            if ("test" in icontent):
                obj = models.Dynamic.objects.get(content=icontent)
                selected.append(obj)
    return HttpResponse("success")

#评论
@check_login
def create_comment(request, user_name, dynamic_id):
    if request.method == "POST":
        new_comment_count = int(models.Dynamic.objects.get(nid=dynamic_id).comment_count) + 1
        models.Dynamic.objects.filter(nid=dynamic_id).update(comment_count=str(new_comment_count))
    c_content = request.POST.get('content')
    c_user = models.User.objects.get(username=user_name)
    c_dynamic = models.Dynamic.objects.get(nid=dynamic_id)
    models.Comment.objects.create(content=c_content, dynamic=c_dynamic,user=c_user)
    return HttpResponse("OK")

#删除评论
@check_login
def delete_comment(request):
    c_nid = request.POST.get('comment_nid')
    models.Comment.objects.filter(nid=c_nid).delete()
    return HttpResponse("OK")

#回复评论
@check_login
def comment_reply(request,dynamic_id,comment_id,user_id,):
    r_content = request.POST.get('content')
    r_user = models.User.objects.get(uid=user_id)
    r_dynamic = models.Dynamic.objects.get(nid=dynamic_id)
    r_comment = models.Comment.objects.get(comment_id=comment_id)
    models.Reply.objects.create(dynamic=r_dynamic,content=r_content,user=r_user,comment=r_comment)
    return HttpResponse("OK")

#删除回复
@check_login
def delete_reply(request):
    r_nid = request.POST.get('comment_nid')
    models.Reply.objects.filter(nid=r_nid).delete()
    return HttpResponse("OK")