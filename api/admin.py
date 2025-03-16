from django.contrib import admin
from .models import Request, Response

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'file', 'created_at']
    search_fields = ['prompt', 'file']
    list_filter = ['created_at']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ai_response_html', 'prompt__prompt', 'tokens_used', 'created_at']
    search_fields = ['ai_response_html', 'prompt__prompt']
    list_filter = ['created_at']
    readonly_fields = ['ai_response_html']
