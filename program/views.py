import time
import random

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError

from pay.models import Payment
from program import jalali
from .models import Program, Registration, Profile, Management, Pricing, Message, Message_reciving





# Create your views here.
from program.utils import filter_to_registrations
from program.word.export_to_word import registrations_to_print, registrations_to_manifest


@login_required
def documentation(request, management_id):
    management = Management.objects.filter(id=management_id).first()
    if not management or management.profile != request.user.my_profile:
        return render(request, 'attack.html', {})
    if request.method == 'GET':
        managements = Management.objects.filter(program__type=management.program.type).filter(
            role__in=management.seedocument())
        managements = managements.exclude(documentation__isnull=True).exclude(documentation='')
        return render(request, 'documents.html', {'document_managements': managements, 'mymanagement': management, })
    else:
        # todo: save documentation
        pass


@login_required
def panel(request, management_id):
    management = Management.objects.filter(id=management_id).first()
    if not management or management.profile != request.user.my_profile:
        return render(request, 'attack.html', {})
    if not management.canFilter:
        return HttpResponseRedirect('/program/documents/'+str(management.id))

    if request.method == 'GET':
        filter_all = request.session.get('filter',
                                         {'status': [], 'people_type': [], 'payment': [],
                                          'gender': ['male'],
                                          'couple': [], 'age': [], 'entrance_year': [], 'level': [],
                                          'conscription': [], 'passport': [], 'label1': [], 'label2': [],
                                          'label3': [],
                                          'label4': []})

        registrations = filter_to_registrations(filter_all, management.program)
        studentRange = []
        for item in range(5):
            studentRange.append(management.program.year - item)

        return render(request, 'panel.html', {'all': registrations,
                                              'mymanagement': management,
                                              'statusChoices': Registration.status_choices,
                                              'filterAll': filter_all,
                                              'student_range': studentRange,
                                              'label_range': range(11),
                                              })

    else:
        all_filter = {
            'status': request.POST.getlist('status_choices'),
            'people_type': request.POST.getlist('people_type_choices'),
            'payment': request.POST.getlist('payment'),
            'gender': request.POST.getlist('gender'),
            'couple': request.POST.getlist('coupled'),
            'age': request.POST.getlist('age'),
            'entrance_year': request.POST.getlist('entrance_year'),
            'level': request.POST.getlist('level'),
            'conscription': request.POST.getlist('conscription_choices'),
            'passport': request.POST.getlist('passport_choices'),
            'label1': request.POST.getlist('label1'),
            'label2': request.POST.getlist('label2'),
            'label3': request.POST.getlist('label3'),
            'label4': request.POST.getlist('label4'),
        }
        request.session['filter'] = all_filter

        action = request.POST.get('editFilter', 'show')
        if action == 'show':
            return HttpResponseRedirect('/program/panel/' + str(management.program.id))

        registrations = filter_to_registrations(all_filter, management.program)
        if action == 'excel':
            from .utils import registrations_to_excel

            return registrations_to_excel(registrations)
        if action == 'manifest':
            return registrations_to_manifest(registrations)
        if action == 'print':
            return registrations_to_print(registrations)
        if action == 'select':
            if management.canSelect:
                numberOfSelect = request.POST.get("selectFilter", '')
                face = int(numberOfSelect)
                total = registrations.count()

                for selected in registrations:
                    t = random.randint(1, total)
                    if face >= t:
                        selected.status = Registration.STATUS_CERTAIN
                        face = face - 1
                    else:
                        selected.status = Registration.STATUS_RESERVED
                    selected.save()
                    total = total - 1
            return HttpResponseRedirect('/program/panel/' + str(management.program.id))
        else:
            return HttpResponseRedirect('/error')


@login_required
def addregistration(request, program_id):
    program = Program.objects.filter(id=program_id).first()
    management = Management.objects.filter(profile=request.user.my_profile).filter(program=program).first()
    if not management or not management.canAdd:
        return render(request, 'attack.html', {})

    codemelli = request.POST.get('mellicode', '')
    coupled = request.POST.get('coupled', '')
    prof = Profile.objects.filter(melliCode=codemelli).first()
    if prof:
        peopletype = prof.people_type
        alreadyRegistered = Registration.objects.filter(program=program).filter(profile=prof).exclude(
            status=Registration.STATUS_REMOVED)

        if not alreadyRegistered:
            price = Pricing.objects.filter(program=program).filter(Coupling=bool(coupled)).filter(
                people_type=peopletype).first()
            if price:
                addregister = Registration()
                addregister.profile = prof
                addregister.program = program
                if program.hasCoupling and prof.coupling:
                    if coupled == 'married':
                        addregister.coupling = True
                        registeredCouple = Registration.objects.filter(program=program).filter(
                            profile=prof.couple).first()
                        if registeredCouple:
                            registeredCouple.coupling = True
                            registeredCouple.save()
                        else:
                            registeredCouple = Registration()
                            registeredCouple.profile = prof.coupling
                            registeredCouple.program = program
                            registeredCouple.coupling = True
                            registeredCouple.save()
                addregister.save()
    return HttpResponseRedirect('/program/panel/' + management.id)


@login_required
def editStatus(request, program_id):
    program = Program.objects.filter(id=program_id).first()
    management = Management.objects.filter(profile=request.user.my_profile).filter(program=program).first()
    if not management or not management.canEditRegistration:
        return render(request, 'attack.html', {})

    editingRegs = Registration.objects.filter(id__in=request.POST.getlist('tick')).filter(program=program)
    action = request.POST.get('editAction', '')
    if action == 'label1':
        selectValue = request.POST.get('label1', '')
        if selectValue == 'lab1-yes':
            editingRegs.update(label1=True)
        elif selectValue == 'lab1-no':
            editingRegs.update(label1=False)
    elif action == 'label2':
        selectValue = request.POST.get('label2', '')
        if selectValue == 'lab2-yes':
            editingRegs.update(label2=True)
        elif selectValue == 'lab2-no':
            editingRegs.update(label2=False)
    elif action == 'label3':
        editingRegs.update(label3=int(request.POST.get('label3', '')))
    elif action == 'label4':
        editingRegs.update(label4=int(request.POST.get('label4', '')))
    elif action == 'status_choices':
        editingRegs.update(status=int(request.POST.get('status_choices', '')))
    elif action == 'numberOfPayments':
        editingRegs.update(numberOfPayments=int(request.POST.get('numberOfPayments', '')))
    elif action == 'coupled':
        selectValue = request.POST.get('coupled', '')
        if program.hasCoupling:
            for item in editingRegs:
                if selectValue == 'coupled':
                    if item.profile.couple:
                        item.coupling = True
                        registeredCouple = Registration.objects.filter(program=program).filter(
                            profile=item.profile.couple).first()
                        if registeredCouple:
                            registeredCouple.coupling = True
                            registeredCouple.save()
                        else:
                            registeredCouple = Registration()
                            registeredCouple.profile = item.profile.couple
                            registeredCouple.program = program
                            registeredCouple.coupling = True
                            registeredCouple.save()
                elif selectValue == 'single':
                    item.coupling = False
                    if item.profile.couple:
                        registeredCouple = Registration.objects.filter(program=program).filter(
                            profile=item.profile.couple).first()
                        if registeredCouple:
                            registeredCouple.coupling = False
                            registeredCouple.save()
                item.save()
    elif action == 'message':
        if management.canMessage:
                title = request.POST.get('title', '')
                textcontent = request.POST.get('message text', '')
                message = Message()
                message.subject = title
                message.content = textcontent
                message.sender = management
                message.save()
                for item in editingRegs:
                    message_reciving = Message_reciving()
                    message_reciving.message_id = message.id
                    message_reciving.registration_id = item.id
                    message_reciving.save()
                inbox_filter = request.POST.get('inbox', 'false')
                if inbox_filter == 'inbox':
                    message.sendInbox=True
                    message.save()

                inbox_filter = request.POST.get('email', 'false')
                if inbox_filter == 'email':
                    message.sendEmail=True
                    message.save()
                    to_email = editingRegs.filter(program=program).values_list(
                        'profile__user__email', flat=True)
                    if title and textcontent:
                        try:
                            from .utils import send_email

                            send_email(program.email, program.emailPassword, to_email, title, textcontent)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                    else:
                        return HttpResponse('Make sure all fields are entered and valid.')

                inbox_filter = request.POST.get('sms', 'false')
                if inbox_filter == 'sms':
                    message.sendEmail=True
                    message.save()
                    # todo: send sms

    return HttpResponseRedirect('/program/panel/' + str(program.id))


@login_required
def my_programs(request):
    user = request.user
    programregistered = Registration.objects.filter(profile__user__exact=user)
    programregisteredbool = bool(programregistered)
    lastprogram = Program.objects.filter(isPublic=True).last()
    lastprogrambool = bool(lastprogram)
    lastpricing = Pricing.objects.filter(program=lastprogram)
    profile = Profile.objects.filter(user=user).first()
    # passport error About atlest passportexpatitondata must be 6 month after creationdata
    passportexparitonalert = 'شماره تاریخ شما تا زمان سفر اعتبار ندارد'
    passportcheck = bool(profile.passport != None)
    if passportcheck:
        if profile.passport_dateofexpiry.year >= lastprogram.creationDate.year + 2:
            passportexparitonalert = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'

        if profile.passport_dateofexpiry.year >= lastprogram.creationDate.year + 1:
            if lastprogram.creationDate.month <= 6:
                passportexparitonalert = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'
        if profile.passport_dateofexpiry.year == lastprogram.creationDate.year:
            if lastprogram.creationDate.month >= profile.passport_dateofexpiry.month + 6:
                passportexparitonalert = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'
    else:
        return HttpResponseRedirect('/accounts/signin/')
    mytype = profile.people_type
    typecheck = bool(lastpricing.filter(people_type=mytype))
    mycoupling = profile.couple
    mycouplingb = bool(mycoupling)
    mypricing = lastpricing.filter(people_type=mytype).filter(Coupling=mycouplingb).first()
    bmypricing = lastpricing.filter(people_type=mytype).filter(additionalObject=True).first()
    fmypricing = lastpricing.filter(people_type=mytype).filter(Coupling=mycouplingb).first()
    boolmypricing = bool(bmypricing)
    type_pricing = lastpricing.filter(people_type=mytype).first()
    registered = Registration.objects.filter(profile=profile).filter(program=lastprogram).exclude(
        status='removed').first()
    if request.method == "GET":
        if lastprogrambool:
            additionalboolean = bool(lastprogram.additionalObject)
            additional = lastprogram.additionalObject
            return render(request, 'program.html',
                          {'registered': registered,
                           'fmypricing': fmypricing,
                           'boolmypricing': boolmypricing,
                           'mycoupling': mycoupling,
                           'additionalboolean': additionalboolean,
                           'additional': additional,
                           'type_pricing': type_pricing,
                           'mypricing': mypricing,
                           'lastpricing': lastpricing,
                           'profile': profile,
                           'lastprogram': lastprogram,
                           'programregistered': programregistered,
                           'allStatus': Registration.status_choices,
                           'peopletype': Pricing.people_type_choices,
                           'comment': passportexparitonalert, }
                          )
        else:
            return render(request, 'registrationlist.html', {'registered': registered,
                                                             'profile': profile,
                                                             'lastprogram': lastprogram,
                                                             'programregistered': programregistered,
                                                             'programregisteredbool': bool(programregistered),
                                                             'allStatus': Registration.status_choices,
                                                             'peopletype': Pricing.people_type_choices,
                                                             'comment': passportexparitonalert})
    if request.method == "POST":
        hascoupling = request.POST.get("hascoupling", '')
        boolhascoupling = bool(hascoupling)
        additonaltick = request.POST.get("additonaltick", '')
        booladditonaltick = bool(additonaltick)
        pricecheck = Pricing.objects.filter(people_type=mytype).filter(program=lastprogram).filter(
            Coupling=boolhascoupling).filter(
            additionalObject=booladditonaltick).first()
        if pricecheck:
            programcheck = bool(lastprogram.type == Program.TYPE_ARBAEEN)
            if programcheck:
                if passportcheck:
                    if typecheck:
                        if Registration.objects.filter(profile=profile).filter(program=lastprogram).exclude(
                                status='removed').first():
                            pass
                        else:
                            if profile.couple:
                                hascoupling = request.POST.get("hascoupling", '')
                                additonaltick = request.POST.get("additonaltick", '')
                                registration = Registration()
                                registration.profile = profile
                                registration.program = lastprogram
                                registration.coupling = hascoupling
                                registration.additionalObject = additonaltick
                                registration.save()
                                if hascoupling:
                                    couplepasscheck = bool(mycoupling.passport != None)
                                    if couplepasscheck:
                                        coupleregistration = Registration()
                                        coupleregistration.profile = profile.coupling
                                        coupleregistration.program = lastprogram
                                        coupleregistration.coupling = hascoupling
                                        coupleregistration.additionalObject = additonaltick
                                        coupleregistration.save()
                                    else:
                                        return render(request, 'attack.html', {})
                            else:
                                hascoupling = False
                                additonaltick = request.POST.get("additonaltick", '')
                                registration = Registration()
                                registration.profile = profile
                                registration.program = lastprogram
                                registration.coupling = hascoupling
                                registration.additionalObject = additonaltick
                                registration.save()
                    else:
                        return render(request, 'attack.html', {})
                else:
                    return render(request, 'attack.html', {})
            else:
                if typecheck:
                    if Registration.objects.filter(profile=profile).filter(program=lastprogram).exclude(
                            status='removed').first():
                        pass
                    else:
                        if profile.coupling:
                            hascoupling = request.POST.get("hascoupling", '')
                            additonaltick = request.POST.get("additonaltick", '')
                            registration = Registration()
                            registration.profile = profile
                            registration.program = lastprogram
                            registration.coupling = hascoupling
                            registration.additionalObject = additonaltick
                            registration.save()
                            if hascoupling:
                                coupleregistration = Registration()
                                coupleregistration.profile = profile.coupling
                                coupleregistration.program = lastprogram
                                coupleregistration.coupling = hascoupling
                                coupleregistration.additionalObject = additonaltick
                                coupleregistration.save()
                        else:
                            registered = Registration.objects.filter(profile=profile).filter(
                                program=lastprogram).exclude(
                                status='removed').first()
                            hascoupling = False
                            additonaltick = request.POST.get("additonaltick", '')
                            registration = Registration()
                            registration.profile = profile
                            registration.program = lastprogram
                            registration.coupling = hascoupling
                            registration.additionalObject = additonaltick
                            registration.save()
                else:
                    return render(request, 'attack.html', {})

            registered = Registration.objects.filter(profile=profile).filter(program=lastprogram).exclude(
                status='removed').first()
            programregistered = Registration.objects.filter(profile__user__exact=user)
            return render(request, 'program.html',
                          {'registered': registered, 'lastpricing': lastpricing, 'lastprogram': lastprogram,
                           'programregistered': programregistered,
                           'allStatus': Registration.status_choices
                              , 'peopletype': Pricing.people_type_choices})
        else:
            additionalboolean = bool(lastprogram.additionalObject)
            additional = lastprogram.additionalObject
            error = True
            return render(request, 'program.html', {'error': error,
                                                    'registered': registered,
                                                    'fmypricing': fmypricing,
                                                    'boolmypricing': boolmypricing,
                                                    'mycoupling': mycoupling,
                                                    'additionalboolean': additionalboolean,
                                                    'additional': additional,
                                                    'type_pricing': type_pricing,
                                                    'mypricing': mypricing,
                                                    'lastpricing': lastpricing,
                                                    'profile': profile,
                                                    'lastprogram': lastprogram,
                                                    'programregistered': programregistered,
                                                    'allStatus': Registration.status_choices,
                                                    'peopletype': Pricing.people_type_choices,
                                                    'comment': comment
                                                    })


@login_required
def my_management(request):
    user = request.user
    programmanaged = Management.objects.filter(profile__user__exact=user)
    return render(request, 'management.html',
                  {'programmanaged': programmanaged,
                   'programmanagedbool': bool(programmanaged),
                   'role_choices': Management.role_choices})


@login_required
def manage(request, management_id):
    user = request.user
    pric = Pricing.people_type_choices
    regType = dict(Profile.people_type_choices).keys()
    pri = Pricing.objects.all()
    canFilter = Management.objects.filter(id=management_id).filter().first().canFilter
    mymanagement = Management.objects.filter(id=management_id).first()
    h = mymanagement.pk
    kk = mymanagement.program.additionalObject
    additonal = bool(mymanagement.program.additionalObject)
    muser = mymanagement.profile.user
    if user == muser:
        if mymanagement.canEditProgram:
            if request.method == 'GET':
                pricelist = []
                if additonal:
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=False).filter(
                            program=mymanagement.program).filter(additionalObject=True).first()
                        obj = {'pe': p, 'c': False, 'pri': pr, 'add': True}
                        pricelist.append(obj)
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=True).filter(
                            program=mymanagement.program).filter(additionalObject=True).first()
                        obj = {'pe': p, 'c': True, 'pri': pr, 'add': True}
                        pricelist.append(obj)
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=False).filter(
                            program=mymanagement.program).filter(additionalObject=False).first()
                        obj = {'pe': p, 'c': False, 'pri': pr, 'add': False}
                        pricelist.append(obj)
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=True).filter(
                            program=mymanagement.program).filter(additionalObject=False).first()
                        obj = {'pe': p, 'c': True, 'pri': pr, 'add': False}
                        pricelist.append(obj)
                else:
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=False).filter(
                            program=mymanagement.program).first()
                        obj = {'pe': p, 'c': False, 'pri': pr}
                        pricelist.append(obj)
                    for p in regType:
                        pr = Pricing.objects.filter(people_type=p).filter(Coupling=True).filter(
                            program=mymanagement.program).first()
                        obj = {'pe': p, 'c': True, 'pri': pr}
                        pricelist.append(obj)
                return render(request, 'reg.html',
                              {'canFilter': canFilter,
                               'mymanagement': mymanagement,
                               'list': pricelist, 'pri': pri,
                               'regType': Profile.people_type_choices,
                               'additonal': additonal,
                               'allStatus': Registration.status_choices})
            title = request.POST.get("title", '')
            programinterval = request.POST.get("programinterval", '')
            registerinterval = request.POST.get("registrinterval", '')
            hascoupling = request.POST.get("hascoupling", '')
            isopen = request.POST.get("isopen", '')
            email = request.POST.get("email", '')
            emailPassword = request.POST.get("emailPassword", '')
            note = request.POST.get("note", '')
            program = mymanagement.program
            program.title = title
            program.programInterval = programinterval
            program.registerInterval = registerinterval
            program.hasCoupling = hascoupling
            program.isOpen = isopen
            program.emailPassword = emailPassword
            program.email = email
            program.notes = note
            program.save()
            proman = Management.objects.filter(program=program).filter(profile=request.user.my_profile).first()
            pm = proman.id
            return HttpResponseRedirect('/program/manage/' + str(pm))
        elif mymanagement.canFilter:
            program = mymanagement.program
            proman = Management.objects.filter(program=program).filter(profile=request.user.my_profile).first()
            pm = proman.id
            return HttpResponseRedirect('/program/panel/' + str(pm))
        else:
            program = mymanagement.program
            proman = Management.objects.filter(program=program).filter(profile=request.user.my_profile).first()
            pm = proman.id
            return HttpResponseRedirect('/program/documents/' + str(pm))
    else:
        return render(request, 'attack.html', {})


@login_required
def myform(request, registration_id):
    user = request.user
    myregister = Registration.objects.filter(id=registration_id).first()
    pro = myregister.program
    payment = Payment.objects.filter(registration=myregister)
    dpayment = Payment.objects.filter(registration=myregister).first()
    date_list = []
    for t in payment:
        print(t)
        dat = str(t.takingDate)[0:10]
        shamsidate = jalali.Gregorian(dat).persian_string()
        time = str(t.takingDate)[11:19]
        amount = t.amount
        refId = t.refId
        saleRefId = t.saleRefId
        success = t.success
        obj = {'taking_date': shamsidate,
               'taking_time': time,
               'amount': amount,
               'refId': refId,
               'saleRefId': saleRefId,
               'success': success, }
        date_list.append(obj)

    massageinbox = Message_reciving.objects.filter(registration_id=registration_id)
    add = myregister.additionalObject
    us = myregister.profile.user
    pr = myregister.program
    usco = myregister.coupling
    mycoupleregister = Registration.objects.filter(program=pro).filter(profile=usco).first()
    usercoupling = bool(usco)
    pt = myregister.profile.people_type
    pricerow = Pricing.objects.filter(program=pr).filter(people_type=pt).filter(Coupling=usercoupling).filter(
        additionalObject=add).first()
    # pricerow = Pricing.objects.filter(program=pr).filter(people_type=pt).filter(Coupling=usercoupling).first()
    lastprogram = Program.objects.filter(isPublic=True).last()
    registerprogram = Pricing.objects.filter(program=pr)
    lastprogramprice = Pricing.objects.filter(program=lastprogram)
    if request.method == 'GET':

        if (user == us):
            return render(request, 'myform.html',
                          {'massageinbox': massageinbox,
                           'payment': payment,
                           'date_list': date_list,
                           'myregister': myregister,
                           'pricerow': pricerow,
                           'registerprogram': registerprogram,
                           'pricing': lastprogramprice,
                           'allStatus': Registration.status_choices,
                           'peopletype': Profile.people_type_choices})
        else:
            return render(request, 'attack.html', {})
    else:
        if 'givenup_btn' in request.POST:
            myregister.status = 'given up'
            if myregister.coupling:
                mycoupleregister.status = 'given up'
                mycoupleregister.save()
            myregister.save()
        if 'feedback_btn' in request.POST:
            registration_feedback = request.POST.get("feedback", '')
            myregister.feedBack = registration_feedback
            myregister.save()
        return render(request, 'myform.html',
                      {'massageinbox': massageinbox,
                       'payment': payment,
                       'date_list': date_list,
                       'myregister': myregister,
                       'pricerow': pricerow,
                       'registerprogram': registerprogram,
                       'pricing': lastprogramprice,
                       'allStatus': Registration.status_choices,
                       'peopletype': Profile.people_type_choices})


@login_required
def addInstallment(request):
    programid = request.POST.get("programId", '')
    program = Program.objects.filter(id=int(programid)).first()
    peopletype = request.POST.get("peopleType", '')
    additionalobject = request.POST.get("additionalobject", '')
    coupling = request.POST.get("coupling", '')
    price = request.POST.get("price", '')
    c = (coupling == 'True')
    add = (additionalobject == 'True')
    pricing, created = Pricing.objects.get_or_create(
        people_type=peopletype,
        Coupling=c,
        additionalObject=add,
        program=program,
    )
    if pricing.price1 is None:
        pricing.price1 = price
    else:
        if pricing.price2 is None:
            pricing.price2 = price
        else:
            if pricing.price3 is None:
                pricing.price3 = price
    pricing.save()
    # print(pricing)
    # return render(request, 'reg.html', {'pricing': pricing})
    pid = Management.objects.filter(program=program).filter(profile=request.user.my_profile).first().id
    # rid = Registration.objects.filter(program=program).filter(profile=request.user.profile).first().id
    return HttpResponseRedirect('/program/manage/' + str(pid))


@login_required
def removeInstallment(request, pricing_id, price_num):
    pricing = Pricing.objects.filter(id=pricing_id).first()
    if price_num == '1':
        pricing.price1 = pricing.price2
        pricing.price2 = pricing.price3
        pricing.price3 = None
        pricing.save()
        if pricing.price1 == None:
            Pricing.objects.filter(id=pricing_id).delete()

    elif price_num == '2':
        pricing.price2 = pricing.price3
        pricing.price3 = None
        pricing.save()
    elif price_num == '3':
        pricing.price3 = None
        pricing.save()

    programid = pricing.program.id
    program = Program.objects.filter(id=int(programid)).first()

    rid = Management.objects.filter(program=program).filter(profile=request.user.my_profile).first().id
    return HttpResponseRedirect('/program/manage/' + str(rid))
