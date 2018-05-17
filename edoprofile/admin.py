# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import EdoUser

class EdoUserResource(resources.ModelResource):
    class Meta:
        model = EdoUser

class EdoUserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = EdoUserResource

    def get_fieldsets(self, request, obj=None):
        fs = super(EdoUserAdmin, self).get_fieldsets(request, obj)

        fs[1][1]['fields'] = ('first_name', 'last_name', 'email', 'color')
        # fs = fs+ ('Color', {
        #     'fields': ('color',)
        # })
        return fs
admin.site.register(EdoUser, EdoUserAdmin)
