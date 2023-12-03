from django.db import models

from . import choices


class GeneralAndLifetimeMembership(models.Model):
    membership_type = models.CharField(max_length=1, choices=choices.MEMBERSHIP_TYPES)
    name_of_applicant = models.CharField(max_length=200)
    dob = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=choices.GENDER_CHOICES)
    nationality = models.CharField(max_length=200)
    issued_from = models.CharField(max_length=200)
    permanent_address = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200)
    citizenship_card_no = models.CharField(max_length=20)
    degree = models.CharField(max_length=3, choices=choices.DEGREE_CHOICES)
    subject = models.CharField(max_length=200, blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    passed_year = models.CharField(max_length=4, blank=True, null=True)
    pp_photo = models.ImageField()
    citizenship = models.ImageField()
    masters_document = models.ImageField()
    work_experience = models.TextField()


class InstitutionalMembership(models.Model):
    company_name = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    registration_no = models.CharField(max_length=200)
    company_documents = models.ImageField()
    working_field = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)