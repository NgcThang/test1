from django.urls import path
from .views import upload_file, list_uploaded_files, get_rows_by_file
from .views import upload_file, list_uploaded_files, get_rows_by_file, delete_multiple_files

urlpatterns = [
    path('', upload_file, name='upload'),
    path('api/files/', list_uploaded_files, name='list-files'),
    path('api/files/<int:file_id>/rows/', get_rows_by_file, name='file-rows'),
    path('api/delete-files/', delete_multiple_files),
]
