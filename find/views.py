from django.shortcuts import render,HttpResponse,redirect,render_to_response,HttpResponseRedirect
import os
from find import models
from django.http import Http404
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder


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
    print("dshdhbsdhj")
    obj = models.Dynamic.objects.get(nid=dynamic_id)
    user_uid = obj.author.uid

    models.Dynamic.objects.filter(nid=dynamic_id).delete()
    return redirect("/find/dynamic/user/"+str(user_uid))
    #return redirect(to='/mine/' + request.session['user_info']['username'])


#动态详情
def detail(request, dynamic_id):

    print('进来了')
    obj = models.Dynamic.objects.get(nid=dynamic_id)
    d_name = obj.author
    user_id = obj.author.uid
    obj_user = models.User.objects.get(name=d_name)
    head = obj_user.imgpath
    d_content = obj.content
    d_time = obj.create_time
    d_up_count = obj.up_count
    d_comment_count = obj.comment_count
    d_collect_count=obj.collect_count
    d_comment = models.Comment.objects.filter(dynamic=obj)
    d_reply = models.Reply.objects.filter(dynamic=obj)
    now_name = request.COOKIES.get('name')
    now_usernick = models.User.objects.get(name=now_name).nickname
    now_img = models.User.objects.get(name=now_name).imgpath
    now_uid=models.User.objects.get(name=now_name).uid
    return render(request, 'detail.html', {'userimg':now_img,'mynickname':now_usernick,'content': d_content,'author_name': d_name,
                                            'create_time': d_time, 'author_head':head,'name':now_name,'nowid':now_uid,
                                            'up_num':d_up_count,'comment_num':d_comment_count,
                                           'collect_num':d_collect_count,'comments':d_comment,'dynamic_id':dynamic_id,'user_id':user_id,'replys':d_reply})
def detail1(request, dynamic_id, comment_id):
    print('进来了')
    obj = models.Dynamic.objects.get(nid=dynamic_id)
    d_name = obj.author
    user_id = obj.author.uid
    obj_user = models.User.objects.get(name=d_name)
    head = obj_user.imgpath
    d_content = obj.content
    d_time = obj.create_time
    d_up_count = obj.up_count
    d_comment_count = obj.comment_count
    d_collect_count=obj.collect_count
    d_comment = models.Comment.objects.filter(dynamic=obj)
    d_reply = models.Reply.objects.filter(comment=comment_id)
    now_name = request.COOKIES.get('name')
    now_uid=models.User.objects.get(name=now_name).uid
    print ("d_reply",d_reply)
    return render(request, 'detail.html', {'content': d_content,'author_name': d_name,
                                            'create_time': d_time, 'author_head':head,'name':now_name,'nowid':now_uid,
                                            'up_num':d_up_count,'comment_num':d_comment_count,
                                           'collect_num':d_collect_count,'comments':d_comment,'dynamic_id':dynamic_id,'user_id':user_id,'replys':d_reply})


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
        context['imgpath1'] = obj1.imgpath
        context['userid'] = obj1.uid
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
    #result = {'status': True}
    if models.Up.objects.filter(dynamic=dynamic_id, user=user_id):
        if models.Up.objects.get(dynamic=dynamic_id, user=user_id).is_up==True:
            #result = {'status': False}
            dc_obj = models.Dynamic.objects.get(nid=dynamic_id)
            uc_obj = models.User.objects.get(uid=user_id)
            #models.Up.objects.filter(dynamic=dc_obj, user=uc_obj)create(is_up=False, dynamic=d_obj, user=u_obj)
            newc_up_count = int(models.Dynamic.objects.get(nid=dynamic_id).up_count - 1)
            models.Dynamic.objects.filter(nid=dynamic_id).update(up_count=str(newc_up_count))
            models.Up.objects.filter(dynamic=dc_obj, user=uc_obj).update(is_up=False)
            #return HttpResponse(json.dumps(result))
            return redirect( "/find/show/")
        elif models.Up.objects.get(dynamic=dynamic_id, user=user_id).is_up==False:
            da_obj = models.Dynamic.objects.get(nid=dynamic_id)
            ua_obj = models.User.objects.get(uid=user_id)
            new_up_count = int(models.Dynamic.objects.get(nid=dynamic_id).up_count + 1)
            models.Dynamic.objects.filter(nid=dynamic_id).update(up_count=str(new_up_count))
            models.Up.objects.filter(dynamic=da_obj, user=ua_obj).update(is_up=True)
            #return HttpResponse(json.dumps(result))
            return redirect( "/find/show/")
    else:
        d_obj = models.Dynamic.objects.get(nid=dynamic_id)
        u_obj = models.User.objects.get(uid=user_id)
        models.Up.objects.create(is_up=False, dynamic=d_obj, user=u_obj)
        new_up_count = int(models.Dynamic.objects.get(nid=dynamic_id).up_count + 1)
        models.Dynamic.objects.filter(nid=dynamic_id).update(up_count=str(new_up_count))
        models.Up.objects.filter(dynamic_id=dynamic_id, user_id=user_id).update(is_up=True)
        #return HttpResponse(json.dumps(result))
        return redirect( "/find/show/")

#收藏
@check_login
def collection(request, dynamic_id, user_id):
    #result = {'status': True}
    if models.Collect.objects.filter(dynamic=dynamic_id, user=user_id):
        if models.Collect.objects.get(dynamic=dynamic_id, user=user_id).is_collect==True:
            #result = {'status': False}
            dc_obj = models.Dynamic.objects.get(nid=dynamic_id)
            uc_obj = models.User.objects.get(uid=user_id)
            newc_collect_count = int(models.Dynamic.objects.get(nid=dynamic_id).collect_count - 1)
            models.Dynamic.objects.filter(nid=dynamic_id).update(collect_count=str(newc_collect_count))
            models.Collect.objects.filter(dynamic=dc_obj, user=uc_obj).update(is_collect=False)
            #return HttpResponse(json.dumps(result))
            return redirect( "/find/show/")
        elif models.Collect.objects.get(dynamic=dynamic_id, user=user_id).is_collect==False:
            da_obj = models.Dynamic.objects.get(nid=dynamic_id)
            ua_obj = models.User.objects.get(uid=user_id)
            newa_collect_count = int(models.Dynamic.objects.get(nid=dynamic_id).collect_count + 1)
            models.Dynamic.objects.filter(nid=dynamic_id).update(collect_count=str(newa_collect_count))
            models.Collect.objects.filter(dynamic=da_obj, user=ua_obj).update(is_collect=True)
            #return HttpResponse(json.dumps(result))
            return redirect( "/find/show/")
    else:
        d_obj = models.Dynamic.objects.get(nid=dynamic_id)
        u_obj = models.User.objects.get(uid=user_id)
        models.Collect.objects.create(is_collect=False, dynamic=d_obj, user=u_obj)
        new_collect_count = int(models.Dynamic.objects.get(nid=dynamic_id).collect_count + 1)
        models.Dynamic.objects.filter(nid=dynamic_id).update(collect_count=str(new_collect_count))
        models.Collect.objects.filter(dynamic_id=dynamic_id, user_id=user_id).update(is_collect=True)
        #return HttpResponse(json.dumps(result))
        return redirect( "/find/show/")

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

# def user_dynamic(request,user_id):
#     obj_user = models.User.objects.get(uid=user_id)
#     order = request.GET.get('order')
#     if order=="create_time":
#         dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-create_time')
#     elif order=="up_count":
#         dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-up_count')
#     elif order=="comment_count":
#         dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-comment_count')
#     else:dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-create_time')
#
#     paginator = Paginator(dynamic_list, 8)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码内容返回给 articles
#     dynamics = paginator.get_page(page)
#     # 打印的结果：<Page 1 of 1>
#     # 返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法
#     # 如：可以通过dynamics.object_list获得当前页的所有动态对象
#     # 需要传递给模板（templates）的对象
#     context = {}
#     context['articles'] = dynamics
#     context['user_id'] = user_id
#     allobj_dynamics=list(dynamics.object_list)
#     context['allobj_dynamics'] = allobj_dynamics
#     context['imgpath'] = obj_user.imgpath
#     print("imgpath",context['imgpath'])
#     # context['userid'] = user_id
#     # print(obj_user.uid)
#     # print('name',obj_user.name,request.COOKIES.get('name'))
#     if obj_user.name == request.COOKIES.get('name'):
#     #if obj_user == request.session.get('user_info'):
#         return render(request, 'myshare.html', context)
#     else:
#         return render(request, 'user.html', context)



def user_dynamic(request,user_id):
    print(114556456)
    print(user_id,int(user_id))
    obj_user = models.User.objects.get(uid=int(user_id))
    nowusername = request.COOKIES.get('name',None)
    nowuser = models.User.objects.get(name = nowusername)

    order = request.GET.get('paixu')
    print("order",order)
    if order=="collect_count":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-collect_count')
    elif order=="up_count":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-up_count')
    elif order=="comment_count":
        dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-comment_count')
    else:dynamic_list = models.Dynamic.objects.filter(author=obj_user).order_by('-create_time')

    paginator = Paginator(dynamic_list, 8)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    dynamics = paginator.get_page(page)
    user_id = int(user_id)
    # 打印的结果：<Page 1 of 1>
    # 返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法
    # 如：可以通过dynamics.object_list获得当前页的所有动态对象
    # 需要传递给模板（templates）的对象
    context = {}
    context['articles'] = dynamics
    allobj_dynamics=[]
    allobj_dynamics_list=list(dynamics.object_list)
    for objs in allobj_dynamics_list:
        author={'nickname':objs.author.nickname,'uid':objs.author.uid,'name':objs.author.name,
                'imgpath' :objs.author.imgpath}
        allobj_dynamics.append({'nid':objs.nid,'comment_count':objs.comment_count,'up_count':objs.up_count,
                                'collect_count':objs.collect_count,'content':objs.content,'create_time':objs.create_time,
                                'author':author,'nickname':objs.author.nickname})
    context['allobj_dynamics'] = allobj_dynamics
    context['imgpath'] = obj_user.imgpath
    context['userssid'] = str(obj_user.uid)
    context['user_id'] = obj_user.uid
    context['nicknames'] = nowuser.nickname
    context['onickname'] = obj_user.nickname
    print("usersssid",str(obj_user.uid))
    print("imgpath",context['imgpath'])
    # context['userid'] = user_id
    # print(obj_user.uid)
    # print('name',obj_user.name,request.COOKIES.get('name'))
    if((order=="collect_count")or(order=="up_count")or(order=="comment_count")):
        return HttpResponse(json.dumps(allobj_dynamics, cls=DjangoJSONEncoder))
    else:
        if obj_user.name == request.COOKIES.get('name'):
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
    context={}
    if request.method == 'POST':
        kw = request.POST.get('keywords')
        for icontent in show_dynamic:
            if (kw in icontent):
                obj = models.Dynamic.objects.get(content=icontent)
                selected.append(obj)


    paginator = Paginator(selected, 8)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    dynamics = paginator.get_page(page)
    # 打印的结果：<Page 1 of 1>
    # 返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法
    # 如：可以通过dynamics.object_list获得当前页的所有动态对象
    # 需要传递给模板（templates）的对象
    context = {}
    context['articles'] = dynamics
    context["selected"]=selected
    return render(request,"social1.html",context)

#评论
@check_login
def create_comment(request, user_name, dynamic_id):
    print("ssnsdjksd")
    if request.method == "POST":
        new_comment_count = int(models.Dynamic.objects.get(nid=dynamic_id).comment_count) + 1
        models.Dynamic.objects.filter(nid=dynamic_id).update(comment_count=str(new_comment_count))
        c_content = request.POST.get('content')
        print("c_content",c_content)
        print ('user_name',user_name)
        c_user = models.User.objects.get(name=user_name)
        c_dynamic = models.Dynamic.objects.get(nid=dynamic_id)
        dynamic_id=c_dynamic.nid
        print("dynamic_id",dynamic_id)
        models.Comment.objects.create(content=c_content, dynamic=c_dynamic,user=c_user)
    return redirect("/find/dynamic/"+ str(dynamic_id) )

#删除评论
@check_login
def delete_comment(request,comment_id,dynamic_id):
    models.Comment.objects.filter(nid=comment_id).delete()

    newc_comment_count = int(models.Dynamic.objects.get(nid=dynamic_id).comment_count - 1)
    models.Dynamic.objects.filter(nid=dynamic_id).update(comment_count=str(newc_comment_count))
    return redirect("/find/dynamic/"+str(dynamic_id))

#回复评论
@check_login
def comment_reply(request,dynamic_id,comment_id,user_name,):
    print ("评论了")
    myname = request.COOKIES.get('name')
    myuser = models.User.objects.get(name=myname)
    print (myname)

    r_content = request.POST.get('content')
    r_user = models.User.objects.get(name=user_name)
    r_dynamic = models.Dynamic.objects.get(nid=dynamic_id)
    r_comment = models.Comment.objects.get(nid=comment_id)
    models.Reply.objects.create(dynamic=r_dynamic,content=r_content,user=r_user,comment=r_comment)
    context={}
    context["content"]=r_content
    return redirect("/find/dynamic/" + str(dynamic_id) + "/" + str(comment_id))

#删除回复
@check_login
def delete_reply(request,reply_id):
    comment_id = models.Reply.objects.get(nid=reply_id).comment.nid
    dynamic_id = models.Reply.objects.get(nid=reply_id).dynamic.nid
    models.Reply.objects.filter(nid=reply_id).delete()
    return redirect("/find/dynamic/" + str(dynamic_id) + "/" + str(comment_id))

#我的收藏
@check_login
def my_collection(request,user_id):
    print ('user_id',user_id)
    obj_user = models.User.objects.get(uid=user_id)
    obj_collect= models.Collect.objects.filter(user=obj_user)
    context={'c_list':obj_collect}
    context['imgpath'] = obj_user.imgpath
    paginator = Paginator(obj_collect, 8)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    dynamics = paginator.get_page(page)
    # 打印的结果：<Page 1 of 1>
    # 返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法
    # 如：可以通过dynamics.object_list获得当前页的所有动态对象
    # 需要传递给模板（templates）的对象
    context['articles'] = dynamics
    return render(request,"mycollection.html",context)