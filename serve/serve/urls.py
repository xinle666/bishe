from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/list', views.user_list),
    path('user/only', views.user_check),
    path('user/login', views.user_login),
    path('user/add', views.add_user),
    path('user/up', views.update_user),
    path('user/delete', views.delete_user),

    path('project/list', views.project_list),
    path('project/add', views.add_project),
    path('project/up', views.update_project),
    path('project/delete', views.delete_project),
    path('project/filelist', views.filelist),
    path('project/file_del', views.file_del),
    path('project/project_user_add', views.project_user_add),
    path('project/project_user_delete', views.project_user_delete),
    path('project/project_user_list', views.project_user_list),

    path('project/fileing', views.fileing),
    path('project/fileing_add', views.fileing_add),
    path('project/fileing_del', views.fileing_del),
    path('file/upload', views.fileupload),
    path('file/list', views.fileinlist),
    path('file/save_content', views.save_content),
    path('file/save_as_pdf', views.save_as_pdf),
    path('file/save_as_word', views.save_as_word),
    path('file/execl_get', views.execl_get),
    path('file/execl_set', views.execl_set),
    path('jpg/upload', views.jpgupload),
    # 路由处理静态文件请求，根据路径拼接生成文件 URL
    path('static/file/<path:file_path>', views.generate_file_url),

path('project/generate_exam', views.generate_exam, name='generate_exam'),
]

# 仅在开发环境中启用静态文件处理
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
