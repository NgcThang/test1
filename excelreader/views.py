from django.shortcuts import render
from .forms import UploadFileForm
from .models import ExcelRow, UploadedFile
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ExcelRowSerializer, UploadedFileSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import traceback

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        print(f"📁 Nhận file: {file.name}")

        # Ghi thông tin file upload vào DB
        uploaded_file = UploadedFile.objects.create(filename=file.name)

        try:
            # Đọc file Excel
            if file.name.endswith('.xlsx'):
                print("📄 Đọc Excel bằng pandas")
                df = pd.read_excel(file)

            # Đọc file CSV có tiếng Việt
            elif file.name.endswith('.csv'):
                print("📄 Đọc CSV (ưu tiên UTF-8, fallback latin1)")
                try:
                    df = pd.read_csv(file, encoding='utf-8')
                except UnicodeDecodeError:
                    print("⚠️ UTF-8 lỗi, thử latin1")
                    df = pd.read_csv(file, encoding='latin1')

            else:
                return JsonResponse({'error': 'Chỉ hỗ trợ .xlsx và .csv'}, status=400)

            print(f"✅ Số dòng đọc được: {len(df)}")
            print(f"📌 Cột: {df.columns.tolist()}")

            # Ghi từng dòng vào ExcelRow
            for i, row in df.iterrows():
                cleaned = row.where(pd.notnull(row), None).to_dict()
                ExcelRow.objects.create(
                    file=uploaded_file,
                    data=cleaned,
                    row_number=i + 1
                )

            return JsonResponse({'success': True})

        except Exception as e:
            print("❌ Lỗi khi xử lý file:")
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Yêu cầu không hợp lệ'}, status=400)


# API: Danh sách file đã upload
@api_view(['GET'])
def get_uploaded_files(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)


# API: Lấy dữ liệu từng dòng theo file
@api_view(['GET'])
def get_rows_by_file(request, file_id):
    rows = ExcelRow.objects.filter(file_id=file_id).order_by('row_number')
    serializer = ExcelRowSerializer(rows, many=True)
    return Response(serializer.data)
