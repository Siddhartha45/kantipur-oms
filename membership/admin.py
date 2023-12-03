from django.contrib import admin

from .models import GeneralAndLifetimeMembership, InstitutionalMembership


admin.site.register(GeneralAndLifetimeMembership)
admin.site.register(InstitutionalMembership)
