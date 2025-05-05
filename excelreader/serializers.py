from rest_framework import serializers
from .models import ExcelRow, UploadedFile

class ExcelRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelRow
        fields = ['id', 'file', 'data', 'row_number']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'filename', 'uploaded_at']
