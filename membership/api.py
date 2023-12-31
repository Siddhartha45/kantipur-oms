from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment
from django.http import JsonResponse
from django.core.serializers import serialize


def membership_api(request, id):
    host = request.get_host()
    membership_instance = GeneralAndLifetimeMembership.objects.get(id=id)
    
    try:
        payment_instance = Payment.objects.get(user=membership_instance.created_by)
    except Payment.DoesNotExist:
        payment_instance = None
    
    if payment_instance:
        payment_status = True
    else:
        payment_status = False
    
    
    serialized_data = {
        "name_of_applicant": membership_instance.name_of_applicant,
        "dob": membership_instance.dob,
        "gender": membership_instance.get_gender_display(),
        "permanent_address": membership_instance.permanent_address,
        "affiliation": membership_instance.affiliation,
        "nationality": membership_instance.get_nationality_display(),
        "citizenship_no": membership_instance.citizenship_card_no,
        "issued_from": membership_instance.get_issued_from_display(),
        "be_subject": membership_instance.be_subject,
        "be_institution": membership_instance.be_institution,
        "be_country": membership_instance.get_be_country_display(),
        "be_passed_year": membership_instance.be_passed_year,
        "me_subject": membership_instance.me_subject,
        "me_institution": membership_instance.me_institution,
        "me_country": membership_instance.get_me_country_display(),
        "me_passed_year": membership_instance.me_passed_year,
        "phd_subject": membership_instance.phd_subject,
        "phd_institution": membership_instance.phd_institution,
        "phd_country": membership_instance.get_phd_country_display(),
        "phd_passed_year": membership_instance.phd_passed_year,
        "work_experience": membership_instance.work_experience,
        "pp_photo": f"http://{host}{membership_instance.pp_photo.url}",
        "citizenship_photo": f"http://{host}{membership_instance.citizenship.url}",
        "masters_document": f"http://{host}{membership_instance.masters_document.url}",
        "payment_status": payment_status,
        "payment_created_at": payment_instance.created_at,
        "payment_ss": f"http://{host}{payment_instance.payment_ss.url}",
        "amount": payment_instance.amount_in_rs,
        "paypal_id": payment_instance.paypal_payer_id,
    }
    return JsonResponse(serialized_data, safe=False)

