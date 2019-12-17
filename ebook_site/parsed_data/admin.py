from django.contrib import admin
from .models import EbookData, EventData, EventLog

admin.site.register(EbookData)
admin.site.register(EventData)
admin.site.register(EventLog)