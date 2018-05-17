# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Doc

class DocResource(resources.ModelResource):
    class Meta:
        model = Doc

class DocAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DocResource
    # class Media:
    #     css = {
    #         "all": ("css/board.css",)
    #     }
admin.site.register(Doc, DocAdmin)
