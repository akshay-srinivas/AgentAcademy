from agentacademy.admin import admin_site
from .models import DataSource, DataSourceContent

# Register your models here.
admin_site.register(DataSource)
admin_site.register(DataSourceContent)