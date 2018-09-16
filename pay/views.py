from django.shortcuts import render
from program.models import Registration, Program, Profile
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Expense
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework import response, decorators, generics, permissions
from .serializers import *


class ExpenseList(generics.ListAPIView):
    queryset = Expense.objects.filter(is_open=True)
    serializer_class = ExpenseListSerializer


# Create your views here.
# def start_pay(request, registration_id):
#     reg = Registration.objects.filter(id=registration_id).first()
#     if not reg or request.user != reg.profile.user:
#         return HttpResponseRedirect('/error')
#     price = reg.get_pricing()
#     if reg.numberOfPayments == 0:
#         numberOfInstallment = 1
#         amount = price.price1
#     elif reg.numberOfPayments == 1:
#         amount = price.price2
#         numberOfInstallment = 2
#     elif reg.numberOfPayments == 2:
#         amount = price.price3
#         numberOfInstallment = 3
#     payment = Payment.create(registration=reg, amount=amount, numberOfInstallment=numberOfInstallment)
#     return render(request, "post.html", {'payment': payment})


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
    if payment.registration:
        if payment.success:
            numofpayment = payment.registration.numberOfPayments
            a = numofpayment + 1
            payment.registration.numberOfPayments = a
            payment.registration.save()
        return HttpResponseRedirect('/program/' + str(payment.registration.program_id) + '/payments')
    return render(request, 'result.html', {'payment': payment})


@decorators.api_view(['POST'])
def start_pay_terminal(request):
    amount = request.data.get('amount', 10000)
    expense_id = request.data.get('expense_id', 10000)
    payment = Payment.create(amount=amount, expense=Expense.objects.get(id=expense_id))
    return HttpResponse(payment.refId)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def start_pay_registration(request):
    registration_id = request.data.get('registration_id')
    if not registration_id:
        return response.Response('درخواست نامعتبر', status=400)
    registration = Registration.objects.filter(id=registration_id).first()
    if not registration or registration.profile.user.username != request.user.username:
        return response.Response('درخواست نامعتبر', status=400)
    price = registration.next_installment()
    if not price or price < 100:
        return response.Response('مبلغ نامعتبر', status=400)
    payment = Payment.create(registration=registration, amount=price,
                             numberOfInstallment=registration.numberOfPayments + 1)
    return HttpResponse(payment.refId)
