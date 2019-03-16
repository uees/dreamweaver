from django.contrib import admin
from django_extensions.db.fields.json import JSONField

from .models import Pay, Result, Table, TableHeader
from .widgets import JsonEditorWidget


def make_computed_value(modeladmin, request, queryset):
    for result in queryset:
        result.make_computed_value()
        result.save()


make_computed_value.short_description = "刷新值"


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    actions = [make_computed_value]
    list_display = ('table', 'label', 'value')
    list_display_links = ('label', 'value')


class TableHeaderInline(admin.StackedInline):
    model = TableHeader
    fields = ('name', 'rank', 'data')
    list_select_related = ('table',)
    extra = 0

    formfield_overrides = {
        JSONField: {'widget': JsonEditorWidget}
    }


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    inlines = [TableHeaderInline]


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'price', 'created_at')
    list_display_links = ('price', 'created_at')
    list_select_related = ('user', 'table')
