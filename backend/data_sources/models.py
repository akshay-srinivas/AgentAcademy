from django.db import models
from accounts.models import Account

# Create your models here.
class DataSource(models.Model):
    class SourceType(models.TextChoices):
        PDF = "pdf", "PDF Document"
        VIDEO = "video", "Video File"
        PRESENTATION = "presentation", "Presentation (e.g., PPT, Keynote)"
        DOCUMENT = "document", "Text Document (e.g., DOCX, TXT)"
        SPREADSHEET = "spreadsheet", "Spreadsheet (e.g., XLSX, CSV)"
        IMAGE = "image", "Image File"
        AUDIO = "audio", "Audio File"
        ARCHIVE = "archive", "Archive File (e.g., ZIP, RAR)"
        WEB_LINK = "web_link", "Web Link"
        OTHER = "other", "Other File Type"

    source_type = models.CharField(
        max_length=255,
        choices=SourceType.choices,
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)  # to enable/disable the data source
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.source_type} - {self.account}"

    class Meta:
        verbose_name = "Data Source"
        verbose_name_plural = "Data Sources"


class DataSourceContent(models.Model):
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=255)
    title = models.CharField()
    file = models.FileField(upload_to='content_files/%Y/%m/%d/', null=True, blank=True)
    raw_content = models.JSONField(default=dict)
    metadata = models.JSONField(default=dict)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)  # to enable/disable the data source
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DataSource ID: {self.data_source.id} - DataSourceContent ID:{self.id} - DataSourceContent Title: {self.title} - {self.created_at}"

    class Meta:
        verbose_name = "Data Source Content"
        verbose_name_plural = "Data Source Contents"
        unique_together = ["data_source", "reference_id"]
