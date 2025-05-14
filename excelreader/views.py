from django.shortcuts import render
from .forms import UploadFileForm
from .models import ExcelRow, UploadedFile
from .serializers import ExcelRowSerializer, UploadedFileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
import traceback

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        print(f"📁 Nhận file: {file.name}")

        uploaded_file = UploadedFile.objects.create(filename=file.name)

        try:
            if file.name.endswith('.xlsx'):
                print("📄 Đọc Excel bằng pandas")
                df = pd.read_excel(file)
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


@api_view(['GET'])
def get_uploaded_files(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_rows_by_file(request, file_id):
    rows = ExcelRow.objects.filter(file_id=file_id).order_by('row_number')
    serializer = ExcelRowSerializer(rows, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def token_report_api(request):
    try:
        file_id = request.GET.get('file_id')
        if not file_id:
            return JsonResponse({'error': 'Thiếu file_id'}, status=400)

        file_obj = UploadedFile.objects.filter(id=file_id).first()
        if not file_obj:
            return JsonResponse({'error': 'Không tìm thấy file'}, status=404)

        rows = ExcelRow.objects.filter(file=file_obj)
        if not rows.exists():
            return JsonResponse({'error': 'Không có dòng dữ liệu cho file này'}, status=404)

        df = pd.DataFrame([row.data for row in rows])

        # Kiểm tra cột Start_time tồn tại
        if "Start_time" not in df.columns:
            return JsonResponse({'error': 'Thiếu cột Start_time trong dữ liệu'}, status=400)

        # Chuyển đổi kiểu ngày
        df["Start_time"] = pd.to_datetime(df["Start_time"], errors="coerce", utc=True)
        df = df.dropna(subset=["Start_time"])

        # Xử lý thống kê nếu có cột tương ứng
        browsers = df["Browser"].value_counts().reset_index().values.tolist() if "Browser" in df else []
        platforms = df["Platform"].value_counts().reset_index().values.tolist() if "Platform" in df else []
        regions = df["Region"].value_counts().reset_index().values.tolist() if "Region" in df else []

        by_day = df["Start_time"].dt.date.value_counts().sort_index().reset_index()
        by_day.columns = ["date", "count"]
        created_per_day = by_day.values.tolist()

        return Response({
            'browsers': browsers,
            'platforms': platforms,
            'regions': regions,
            'created_per_day': created_per_day
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_multiple_files(request):
    try:
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'Danh sách ID rỗng.'}, status=status.HTTP_400_BAD_REQUEST)

        files = UploadedFile.objects.filter(id__in=ids)
        count = files.count()
        files.delete()  # Xoá cả ExcelRow nhờ on_delete=models.CASCADE
        return Response({'message': f'Đã xoá {count} file.'}, status=status.HTTP_200_OK)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
