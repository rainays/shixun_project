from django.urls import path
from find import views

app_name = 'find'
urlpatterns = [
    path('write/<str:author_name>/',views.create_dynamic),
    path('delete/<int:dynamic_id>/',views.delete_dynamic),
    path('dynamic/<int:dynamic_id>/',views.detail),
    path('show/',views.show_list),
    path('dynamic/<int:dynamic_id>/<int:user_id>/',views.good),
    path('dynamic/user/<int:user_id>/',views.user_dynamic),
    path('search/',views.search_dynamic),
    path('comment/<str:user_name>/<int:dynamic_id>/',views.create_comment),
    path('delete/comment/',views.delete_comment),
    path('reply/<int:dynamic_id>/<int:comment_id>/<int:user_id>', views.comment_reply),
    path('delete/reply/',views.delete_reply),
]

