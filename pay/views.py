from django.shortcuts import render
from  program.models import Registration, Program, Pricing, Profile
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Expense
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


# Create your views here.
def start_pay(request, registration_id):
    reg = Registration.objects.filter(id=registration_id).first()
    if not reg or request.user != reg.profile.user:
        return HttpResponseRedirect('/error')
    price = reg.get_pricing()
    if reg.numberOfPayments == 0:
        numberOfInstallment = 1
        amount = price.price1
    elif reg.numberOfPayments == 1:
        amount = price.price2
        numberOfInstallment = 2
    elif reg.numberOfPayments == 2:
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
    if payment.success and payment.registration:
        numofpayment = payment.registration.numberOfPayments
        a = numofpayment + 1
        payment.registration.numberOfPayments = a
        payment.registration.save()
    return render(request, 'result.html', {'payment': payment})


@csrf_exempt
def terminal(request, expense_id=None):
    if request.method == 'GET':
        from django.db.models import Q
        all_expenses = Expense.objects.filter(is_open=True).filter(Q(callback_url__isnull=True)|Q(callback_url=''))
        if expense_id:
            all_expenses = all_expenses.filter(id=expense_id)
        return render(request, 'terminal.html', {'all_expenses': all_expenses})
    else:
        expense = Expense.objects.get(id=request.POST.get('expense', 1))
        amount = int(request.POST.get('amount', 10000))

        payment = Payment.create(amount=amount, expense=expense)
        if expense.callback_url:
            resp = {
                'amount': amount,
                'refId': payment.refId,
                'orderId': payment.id
            }
            return JsonResponse(resp)
        return render(request, "post.html", {'payment': payment})
