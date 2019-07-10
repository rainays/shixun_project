from django.urls import path
from LoginRegister import views
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
urlpatterns = [
    path('mycloud/search/',views.search),
    path('index/',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout),
    path('change/',views.change),
    path('userinfo/',views.userinfo,name='userinfo'),
    path('picupload/', views.picupload),
    path('mycloud/mypage/',views.mypage),
    path('confirm/', views.user_confirm),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$',  serve, {"document_root": settings.STATIC_ROOT}),
    path('mycloud/ToShare/',views.ToShare),
]