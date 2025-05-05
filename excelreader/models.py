from django.db import models


class UploadedFile(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')})"


class ExcelRow(models.Model):
    file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='rows',
        null=True,  
        blank=True  
    )
    data = models.JSONField()
    row_number = models.IntegerField()

    def __str__(self):
        if self.file:
            return f"Row {self.row_number} of {self.file.filename}"
        return f"Row {self.row_number} (no file)"
