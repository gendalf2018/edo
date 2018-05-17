# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
# from .models import DocHistory
#
# class DocHistoryResource(resources.ModelResource):
#     class Meta:
#         model = DocHistory
#
# class DocHistoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = DocHistoryResource
#     # class Media:
#     #     css = {
#     #         "all": ("css/board.css",)
#     #     }
# admin.site.register(DocHistory, DocAdmin)
