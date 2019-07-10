from django.urls import path
from mycloud import views
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
urlpatterns = [
    #path('files/',views.upload,name='files'),

    #path('users/',views.userinfo),
    #path('mypage/',views.mypage),
    path('mycloud/FileUpload/',views.FileUpload),
    path('mycloud/FileDownload/<str:filename>',views.FileDownload),
    path('mycloud/FileDelete/<str:filename>',views.FileDelete),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$',  serve, {"document_root": settings.STATIC_ROOT}),

]