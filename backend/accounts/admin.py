from agentacademy.admin import admin_site
from accounts.models import Account, Role, User
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.contrib import messages
from google import genai
# import google.generativeai as genai
from django.conf import settings
from data_sources.models import DataSource, DataSourceContent


class AccountAdmin(admin.ModelAdmin):
    list_display = ['product', 'account_reference', 'created_at']  # Adjust fields as needed
    # list_filter = ['is_active', 'created_at']
    search_fields = ['product', 'account_reference']
    actions = ["upload_files_to_google_cloud"]
    
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
        
        # if success_count > 0:
        #     messages.success(request, f"Uploaded files for {success_count} account(s).")
    def start_data_source_processing(modeladmin, request, queryset):
        # Logic to reset API keys for selected accounts        
        for account in queryset:
            try:
                client = genai.Client(api_key=settings.GEMINI_API)
                myfile = client.files.upload(file="/content/Introduction to Channels | HappyFox University.mp4")
            except Exception as e:
                messages.error(request, f"Error resetting API key for {account}: {str(e)}")
        
        # if success_count > 0:
        #     messages.success(request, f"Reset API keys for {success_count} account(s).")

# Register your models here.
admin_site.register(Account, AccountAdmin)
admin_site.register(Role)
admin_site.register(User)