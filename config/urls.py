"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from excelreader.views import upload_file, get_rows_by_file, get_uploaded_files, token_report_api, delete_multiple_files


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_file),
    path('api/files/', get_uploaded_files),
    path('api/delete-files/', delete_multiple_files),
    path('api/files/<int:file_id>/rows/', get_rows_by_file), 
    path('api/report/token', token_report_api),
]
