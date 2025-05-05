from django.contrib import admin
from .models import ExcelRow, UploadedFile

@admin.register(ExcelRow)
class ExcelRowAdmin(admin.ModelAdmin):
    list_display = ['id', 'row_number', 'file']

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'uploaded_at']
