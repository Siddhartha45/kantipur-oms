from django.contrib import admin

from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment


admin.site.register(GeneralAndLifetimeMembership)
admin.site.register(InstitutionalMembership)
admin.site.register(Payment)
