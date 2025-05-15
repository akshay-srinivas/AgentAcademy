from datetime import datetime
import uuid
import os

from django.contrib import (
    admin,
    messages,
)
from django.contrib.auth.admin import (
    GroupAdmin,
    UserAdmin,
)
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import (  # pylint: disable=imported-auth-user
    Group,
    User,
)

from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import path
from django.utils.decorators import method_decorator
from django.utils import timezone

from data_sources.models import DataSource, DataSourceContent
from accounts.models import Account  # Import Account model


class AgentAcademyAdminSite(admin.AdminSite):
    site_header = "Agent Academy Admin"
    site_title = "Agent Academy Admin Portal"
    index_title = "Welcome to Agent Academy Administration"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "file-upload/",
                self.admin_view(self.file_upload),
                name="file-upload",
            )
        ]
        return custom_urls + urls
    
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        app_list.append(
            {
                "name": "Custom Admin Pages",
                "app_label": "custom_admin_pages",
                "models": [
                    {
                        "name": "File Upload",
                        "object_name": "file_upload",
                        "admin_url": "file-upload/",
                        "view_only": True,
                    },
               ],
            }
        )
        return app_list

    def _get_source_type_from_extension(self, filename):
        """Determine the source type based on file extension"""
        ext = os.path.splitext(filename.lower())[1][1:]  # Get extension without dot
        
        # Map common extensions to source types
        if ext in ['pdf']:
            return DataSource.SourceType.PDF
        elif ext in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv']:
            return DataSource.SourceType.VIDEO
        elif ext in ['ppt', 'pptx', 'key']:
            return DataSource.SourceType.PRESENTATION
        elif ext in ['doc', 'docx', 'txt', 'rtf', 'odt']:
            return DataSource.SourceType.DOCUMENT
        elif ext in ['xls', 'xlsx', 'csv', 'tsv']:
            return DataSource.SourceType.SPREADSHEET
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']:
            return DataSource.SourceType.IMAGE
        elif ext in ['mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac']:
            return DataSource.SourceType.AUDIO
        elif ext in ['zip', 'rar', 'tar', 'gz', '7z']:
            return DataSource.SourceType.ARCHIVE
        else:
            return DataSource.SourceType.OTHER

    @method_decorator(permission_required("is_staff", login_url="admin:login"))
    def file_upload(self, request):
        if request.method == "POST":
            files = request.FILES.getlist("files")
            account_id = request.POST.get("account")

            if not files or len(files) == 0 or not account_id:
                messages.error(request, "No files selected or account not specified.")
                return HttpResponseRedirect(request.path_info)
            
            # Get selected account or use current user's account as fallback
            account = None
            if account_id:
                try:
                    account = Account.objects.get(id=account_id)
                except Account.DoesNotExist:
                    messages.error(request, f"Selected account does not exist.")
                    
            # # Fallback to current user's account if no selection or selection failed
            # if not account and hasattr(request.user, 'account'):
            #     account = request.user.account
            
            success_count = 0
            file_types = {}  # Track count of each file type
            
            for file in files:
                try:
                    # Determine file type
                    source_type = self._get_source_type_from_extension(file.name)
                    
                    # Create or get DataSource for this file type
                    data_source, created = DataSource.objects.get_or_create(
                        source_type=source_type,
                        account=account,
                        defaults={
                            'last_sync_at': timezone.now(),
                            'last_sync_status': {'status': 'success', 'message': 'Created via admin upload'},
                            'is_active': True,
                            'metadata': {'upload_method': 'admin_interface'}
                        }
                    )
                    
                    # Generate a unique reference ID for the file
                    reference_id = f"{source_type}_{uuid.uuid4().hex}"
                    
                    # Create the DataSourceContent entry
                    content = DataSourceContent.objects.create(
                        data_source=data_source,
                        reference_id=reference_id,
                        title=file.name,  # Use filename as title
                        file=file,  # Django will handle file saving
                        raw_content={},  # Empty for now
                        metadata={
                            'original_filename': file.name,
                            'file_size': file.size,
                            'content_type': file.content_type if hasattr(file, 'content_type') else 'application/octet-stream',
                            'uploaded_by': request.user.username,
                            'upload_date': timezone.now().isoformat(),
                            'account_id': account.id if account else None
                        },
                        last_sync_at=timezone.now(),
                        last_sync_status={'status': 'success', 'message': 'Uploaded successfully'},
                        is_active=True
                    )
                    success_count += 1
                    
                    # Track file types for reporting
                    file_types[source_type] = file_types.get(source_type, 0) + 1
                    
                    # Update the DataSource with latest sync info
                    data_source.last_sync_at = timezone.now()
                    data_source.last_sync_status = {
                        'status': 'success',
                        'uploaded': file_types[source_type],
                        'timestamp': timezone.now().isoformat()
                    }
                    data_source.save()
                    
                except Exception as e:
                    # Log the error and continue with next file
                    print(f"Error saving file {file.name}: {str(e)}")
                    messages.error(request, f"Failed to upload {file.name}: {str(e)}")
            
            # Generate success message with file type breakdown
            if success_count > 0:
                account_info = f" for account {account.account_reference}" if account else ""
                type_breakdown = ", ".join([f"{count} {file_type}" for file_type, count in file_types.items()])
                messages.success(request, f"{success_count} file(s) uploaded successfully{account_info}. Breakdown: {type_breakdown}")
            
            return HttpResponseRedirect(request.path_info)

        # Get all accounts for the dropdown
        accounts = Account.objects.all().order_by('account_reference')
        
        context = dict(
           # Include common admin headers
           self.each_context(request),
           title="File Upload",
           source_types=DataSource.SourceType.choices,
           accounts=accounts,
        )
        return render(request, "accounts/file_upload.html", context)
    
    # Keep the old video_upload method for backward compatibility
    @method_decorator(permission_required("is_staff", login_url="admin:login"))
    def video_upload(self, request):
        return self.file_upload(request)


admin_site = AgentAcademyAdminSite(name="hfadmin")

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)