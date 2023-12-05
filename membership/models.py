from django.db import models

from accounts.models import CustomUser

from . import choices


class GeneralAndLifetimeMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="general_and_lifetime_user"
    )
    membership_type = models.CharField(max_length=1, choices=choices.MEMBERSHIP_TYPES)
    # Personal Details
    name_of_applicant = models.CharField(max_length=200)
    dob = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=choices.GENDER_CHOICES)
    nationality = models.CharField(max_length=2, choices=choices.COUNTRY_CHOICES)
    issued_from = models.CharField(max_length=200)
    permanent_address = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200)
    citizenship_card_no = models.CharField(max_length=20)
    # Educational Details
    be_subject = models.CharField(max_length=200)
    be_institution = models.CharField(max_length=200)
    be_country = models.CharField(max_length=2, choices=choices.COUNTRY_CHOICES)
    be_passed_year = models.CharField(max_length=4)
    me_subject = models.CharField(max_length=200)
    me_institution = models.CharField(max_length=200)
    me_country = models.CharField(max_length=2, choices=choices.COUNTRY_CHOICES)
    me_passed_year = models.CharField(max_length=4)
    phd_subject = models.CharField(max_length=200, blank=True, null=True)
    phd_institution = models.CharField(max_length=200, blank=True, null=True)
    phd_country = models.CharField(
        max_length=2, choices=choices.COUNTRY_CHOICES, blank=True, null=True
    )
    phd_passed_year = models.CharField(max_length=4, blank=True, null=True)
    # Documents
    pp_photo = models.ImageField(upload_to="general_and_lifetime_documents")
    citizenship = models.ImageField(upload_to="general_and_lifetime_documents")
    masters_document = models.ImageField(upload_to="general_and_lifetime_documents")
    # Work Details
    work_experience = models.TextField()

    def __str__(self):
        return self.name_of_applicant


class InstitutionalMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="institutional_user"
    )
    company_name = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    registration_no = models.CharField(max_length=200)
    pan_document = models.ImageField(upload_to="institutional_documents")
    registration_document = models.ImageField(upload_to="institutional_documents")
    company_document = models.ImageField(upload_to="institutional_documents")
    working_field = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name


class Payment(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="payment_user"
    )
    payment_ss = models.ImageField(upload_to="payment")

    def __str__(self):
        return self.user.full_name()
