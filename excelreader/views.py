from django.shortcuts import render
from .forms import UploadFileForm
from .models import ExcelRow, UploadedFile
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ExcelRowSerializer, UploadedFileSerializer


# Giao diện upload file Excel/CSV
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            # Tạo bản ghi UploadedFile
            uploaded_file = UploadedFile.objects.create(filename=file.name)

            # Đọc dữ liệu từ file
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                return render(request, 'upload.html', {
                    'form': form,
                    'error': 'Chỉ hỗ trợ .xlsx và .csv'
                })

            # Lưu từng dòng vào ExcelRow
            for i, row in df.iterrows():
                cleaned = row.where(pd.notnull(row), None).to_dict()
                ExcelRow.objects.create(
                    file=uploaded_file,
                    data=cleaned,
                    row_number=i + 1
                )
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


# API: Lấy danh sách các file đã upload
@api_view(['GET'])
def get_uploaded_files(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)


# API: Lấy dữ liệu từng dòng của file cụ thể
@api_view(['GET'])
def get_rows_by_file(request, file_id):
    rows = ExcelRow.objects.filter(file_id=file_id).order_by('row_number')
    serializer = ExcelRowSerializer(rows, many=True)
    return Response(serializer.data)
