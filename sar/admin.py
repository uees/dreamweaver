from django.contrib import admin
from django_extensions.db.fields.json import JSONField

from .models import Table, TableHeader, Result
from .widgets import JsonEditorWidget


@admin.register(TableHeader)
class TableHeaderAdmin(admin.ModelAdmin):
    list_select_related = ('table',)
    list_max_show_all = 20
    list_per_page = 20

    formfield_overrides = {
        JSONField: {'widget': JsonEditorWidget}
    }


admin.site.register(Result)
admin.site.register(Table)
