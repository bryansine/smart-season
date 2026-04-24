from django.contrib import admin
from .models import Field, FieldUpdate


class FieldUpdateInline(admin.TabularInline):
    model = FieldUpdate
    extra = 0
    readonly_fields = ('created_at', 'updated_by')


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'crop_type', 'current_stage',
        'assigned_agent', 'planting_date', 'computed_status'
    )
    list_filter = ('current_stage', 'crop_type')
    inlines = [FieldUpdateInline]


@admin.register(FieldUpdate)
class FieldUpdateAdmin(admin.ModelAdmin):
    list_display = ('field', 'stage', 'updated_by', 'created_at')
    readonly_fields = ('created_at',)