from django.shortcuts import render
from  program.models import Registration, Program, Pricing, Profile
from django.views.decorators.csrf import csrf_exempt
from .models import Payment


# Create your views here.
def start_pay(request, registration_id):
    user = request.user
    reg = Registration.objects.filter(id=registration_id).first()
    numofpay = reg.numberOfPayments
    progid = reg.program.id
    profid = reg.profile.id
    cou = reg.coupling
    add = reg.additionalObject
    peotyp = reg.profile.people_type
    price = Pricing.objects.filter(program_id__exact=progid).filter(program__pricing__Coupling=cou).filter(
        people_type__exact=peotyp).filter(program__pricing__additionalObject=add).first()
    if numofpay == 0:
        numberOfInstallment = 1
        amount = price.price1
    elif numofpay == 1:
        amount = price.price2
        numberOfInstallment = 2
    elif numofpay == 2:
        amount = price.price3
        numberOfInstallment = 3
    payment = Payment.create(registration=reg, amount=amount, numberOfInstallment=numberOfInstallment)
    return render(request, "post.html", {'payment': payment})


@csrf_exempt
def payment_callback(request):
    refId = request.POST.get("RefId")
    saleReferenceId = request.POST.get("SaleReferenceId")
    saleOrderId = request.POST.get("SaleOrderId")
    resCode = request.POST.get("ResCode")

    if resCode != '0':
        return render(request, 'result.html', {'token': {'success': False, 'verify_rescode': 'Incomplete Transaction'}})

    payment = Payment.objects.filter(refId=refId).first()

    payment.verify(saleReferenceId, saleOrderId)
    if payment.success:
        numofpayment = payment.registration.numberOfPayments
        a = numofpayment + 1
        payment.registration.numberOfPayments = a
        payment.registration.save()
    return render(request, 'result.html', {'payment': payment})
