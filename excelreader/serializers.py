from rest_framework import serializers
from .models import UploadedFile, ExcelRow


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'filename', 'uploaded_at']


class ExcelRowSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(source='file.filename', read_only=True)

    class Meta:
        model = ExcelRow
        fields = ['id', 'file', 'filename', 'row_number', 'data']
