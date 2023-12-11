from accounts.models import CustomUser
from django.shortcuts import get_object_or_404

from .models import Payment, InstitutionalMembership


def a(id):
    user = get_object_or_404(InstitutionalMembership, id=id)