from agentacademy.admin import admin_site
from accounts.models import Account, Role, User, AccountDetail
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.contrib import messages
from google import genai
# import google.generativeai as genai
from django.conf import settings
from data_sources.models import DataSource, DataSourceContent
from data_sources.ingestion import run_ingestion_pipeline


class AccountAdmin(admin.ModelAdmin):
    list_display = ['product', 'account_reference', 'created_at']  # Adjust fields as needed
    # list_filter = ['is_active', 'created_at']
    search_fields = ['product', 'account_reference']
    actions = ["upload_files_to_google_cloud","ingest_data_sources"]
    
    # Add any other customizations you need
    fieldsets = (
        (None, {
            'fields': ('product', 'account_reference')
        }),
        ('Status', {
            'fields': ()
        }),
    )

    @admin.action(description="Upload Files to Google Cloud")
    def upload_files_to_google_cloud(modeladmin, request, queryset):
        # Logic to upload files to Google Cloud
        for account in queryset:
            try:
                client = genai.Client(api_key=settings.GEMINI_API)
                data_source = DataSource.objects.filter(account=account).first()
                for files in DataSourceContent.objects.filter(
                            data_source=data_source,
                            file__isnull=False
                        ).exclude(file=''):
                    # Assuming you have a method to get the file path
                #     file_path = files.get_file_path()
                    myfile = client.files.upload(file=files.file.path)
                    print(f"Uploaded file: {myfile}")
                # myfile = client.files.upload(file="/content/Introduction to Channels | HappyFox University.mp4")
            except Exception as e:
                messages.error(request, f"Error uploading file for {account}: {str(e)}")
        
    @admin.action(description="Ingest Data Sources")
    def ingest_data_sources(self, request, queryset):
        # Logic to ingest data sources
        for account in queryset:
            try:
                run_ingestion_pipeline(account)
            except Exception as e:
                messages.error(request, f"Error uploading file for {account}: {str(e)}")

# Register your models here.
admin_site.register(Account, AccountAdmin)
admin_site.register(AccountDetail)
admin_site.register(Role)
admin_site.register(User)