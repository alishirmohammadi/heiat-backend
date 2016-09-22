import time
import random
from django.contrib import messages

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
from . import jalali




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
        return HttpResponseRedirect('/program/documents/' + str(management.id))

    if request.method == 'GET':
        filter_all = request.session.get('filter',
                                         {'status': [], 'people_type': [], 'payment': [],
                                          'gender': ['male'],
                                          'couple': [], 'age': [], 'entrance_year': [], 'level': [],
                                          'conscription': [], 'passport': [], 'label1': [], 'label2': [],
                                          'label3': [],
                                          'label4': [],'additionalOption':[]})

        registrations = filter_to_registrations(filter_all, management.program)
        studentRange = []
        c = management.program.year
        if len(str(c)) == 4:
            c = str(c)[2:4]
        c = int(c)
        for item in range(5):
            studentRange.append(c - item)

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
            'passport': request.POST.getlist('passport'),
            'label1': request.POST.getlist('label1'),
            'label2': request.POST.getlist('label2'),
            'label3': request.POST.getlist('label3'),
            'label4': request.POST.getlist('label4'),
            'additionalOption':request.POST.getlist('additionalOption'),

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
                    if all_filter.get('couple', [])==['couple']:
                        if len(all_filter.get('gender', []) )==1:
                            if selected.status == Registration.STATUS_CERTAIN:
                                Registration.objects.filter(profile=selected.profile.couple).first().status = Registration.STATUS_CERTAIN

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
            price = Pricing.objects.filter(program=program).filter(coupling=bool(coupled)).filter(
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
                else:
                         messages.add_message(request, messages.INFO, 'این فرد متاهل ثبت نام نکرده است')
                addregister.save()
                messages.add_message(request, messages.INFO, 'با موفقیت انجام شد')

            else:
                messages.add_message(request, messages.INFO, 'قیمت تعریف نشده')
        else:
            messages.add_message(request, messages.INFO, 'این فرد در این برنامه حضور دارد')
    else:
        messages.add_message(request, messages.INFO, 'این فرد وجود ندارد')

    return HttpResponseRedirect('/program/panel/' + str(management.id))


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
        editingRegs.update(status=request.POST.get('status_choices', ''))
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
            title = request.POST.get('subject', '')
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
                message.sendInbox = True
                message.save()

            inbox_filter = request.POST.get('email', 'false')
            if inbox_filter == 'email':
                message.sendEmail = True
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
                message.sendEmail = True
                message.save()
                to = editingRegs.filter(program=program).values_list(
                    'profile__cellPhone', flat=True)
                from .utils import sendSMS

                sendSMS(to, title)

    return HttpResponseRedirect('/program/panel/' + str(program.id))

from .models import Program
@login_required
def my_managements(request):
    managements = Management.objects.filter(profile__user__exact=request.user)
    # jalali_date=[]
    # for item in managements:
    #     startdate=item.program.startDate
    #     jalalii = jalali.Gregorian(startdate).persian_string()
    #     jalali_date.append(jalalii)

    return render(request, 'my_managements.html', {'managements': managements})


@login_required
def manage(request, management_id):
    management = Management.objects.filter(id=management_id).first()
    if not management or management.profile != request.user.my_profile:
        return render(request, 'attack.html', {})
    if not management.canEditProgram:
        return HttpResponseRedirect('/program/panel/' + str(management.id))
    if request.method == 'GET':
        pricelist = []
        for p,q in Profile.people_type_choices:
            pr = Pricing.objects.filter(people_type=p).filter(coupling=False).filter(additionalOption=False).filter(
                program=management.program).first()
            obj = {'people_type': p, 'coupling': False, 'obj': pr}
            pricelist.append(obj)
        for p,q  in Profile.people_type_choices:
            pr = Pricing.objects.filter(people_type=p).filter(coupling=True).filter(additionalOption=False).filter(
                program=management.program).first()
            obj = {'people_type': p, 'coupling': True, 'obj': pr}
            pricelist.append(obj)
        if management.program.additionalOption:
            for p,q  in Profile.people_type_choices:
                pr = Pricing.objects.filter(people_type=p).filter(coupling=False).filter(
                    program=management.program).filter(additionalOption=True).first()
                obj = {'people_type': p, 'coupling': False, 'obj': pr, 'additional': True}
                pricelist.append(obj)
            for p,q  in Profile.people_type_choices:
                pr = Pricing.objects.filter(people_type=p).filter(coupling=True).filter(
                    program=management.program).filter(additionalOption=True).first()
                obj = {'people_type': p, 'coupling': True, 'obj': pr, 'additional': True}
                pricelist.append(obj)

        return render(request, 'manage.html', {'mymanagement': management, 'pricelist': pricelist})
    title = request.POST.get("title", '')
    programinterval = request.POST.get("programinterval", '')
    registerinterval = request.POST.get("registrinterval", '')
    hascoupling = request.POST.get("hascoupling", '')
    isopen = request.POST.get("isopen", '')
    AdditionalOption = request.POST.get("AdditionalOption", '')
    startDate = jalali.Persian(request.POST.get("startDate", '')).gregorian_string()
    email = request.POST.get("email", '')
    emailPassword = request.POST.get("emailPassword", '')
    note = request.POST.get("note", '')
    program = management.program
    program.title = title
    program.programInterval = programinterval
    program.registerInterval = registerinterval
    program.hasCoupling = hascoupling
    program.isOpen = isopen
    program.additionalOption = AdditionalOption
    program.emailPassword = emailPassword
    program.email = email
    program.notes = note
    program.startDate=startDate
    program.save()
    return HttpResponseRedirect('/program/manage/' + str(management_id))


@login_required
def registration(request, registration_id):
    myregister = Registration.objects.filter(id=registration_id).first()
    if not myregister or request.user != myregister.profile.user:
        return HttpResponseRedirect('/error')
    if request.method == 'GET':
        date_list = []
        for t in Payment.objects.filter(registration=myregister):
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
        pricings = Pricing.objects.filter(program=myregister.program)
        return render(request, 'registration_details.html',
                      {'massageinbox': massageinbox,
                       'date_list': date_list,
                       'myregister': myregister,
                       'pricings': pricings
                       })


    else:
        if 'givenup_btn' in request.POST:
            myregister.status = Registration.STATUS_GIVEN_UP
            myregister.save()
            if myregister.coupling:
                couple_registerarion = Registration.objects.filter(program=myregister.program).filter(
                    profile=myregister.profile.couple).first()
                couple_registerarion.status = Registration.STATUS_GIVEN_UP
                couple_registerarion.save()
        if 'feedback_btn' in request.POST:
            registration_feedback = request.POST.get("feedback", '')
            myregister.feedBack = registration_feedback
            myregister.save()
        return HttpResponseRedirect('/program/registration/' + str(registration_id))


@login_required
def addInstallment(request):
    programid = request.POST.get("programId", '')
    program = Program.objects.filter(id=int(programid)).first()
    peopletype = request.POST.get("peopleType", '')
    additionalOption = request.POST.get("additionalobject", '')
    coupling = request.POST.get("coupling", '')
    price = request.POST.get("price", '')
    c = (coupling == 'True')
    add = (additionalOption == 'True')
    pricing, created = Pricing.objects.get_or_create(
        people_type=peopletype,
        coupling=c,
        additionalOption=add,
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
    # return render(request, 'manage.html', {'pricing': pricing})
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

@login_required
def my_programs(request):
    profile = request.user.my_profile
    from .utils import getLastProgram

    last_program = getLastProgram()
    if request.method == 'GET':
        my_registrations = Registration.objects.filter(profile=profile).exclude(status=Registration.STATUS_REMOVED)
        lastpricing = Pricing.objects.filter(program=last_program)
        fmypricing = lastpricing.filter(people_type=profile.people_type).filter(coupling=profile.coupling()).first()
        type_pricing = lastpricing.filter(people_type=profile.people_type).first()
        passportCheck = True
        if last_program.type == Program.TYPE_ARBAEEN:
            if not profile.passport or profile.passport == Profile.PASSPORT_NOT_HAVE or not profile.passport_dateofexpiry:
                passportCheck = False
            else:
                import datetime

                if profile.passport_dateofexpiry - last_program.startDate < datetime.timedelta(183):
                    passportCheck = False
        return render(request, 'my_programs.html',
                      {'regs': my_registrations, 'last_program': last_program, 'fmypricing': fmypricing,
                       'lastpricing': lastpricing,
                       'type_pricing': type_pricing, 'passportCheck': passportCheck})
    else:
        wants_coupling = bool(request.POST.get("hascoupling", '')) and last_program.hasCoupling
        additional = bool(request.POST.get("additonaltick", ''))
        if Pricing.objects.filter(people_type=profile.people_type).filter(program=last_program).filter(
                coupling=wants_coupling).filter(
            additionalOption=additional).first() and not profile.registered_on_last():
            reg = Registration()
            reg.program = last_program
            reg.profile = profile
            reg.coupling = wants_coupling
            reg.additionalOption = additional
            reg.save()
            if wants_coupling and profile.coupling():
                couple_reg = profile.couple.registered_on_last()
                if not couple_reg:
                    couple_reg = Registration()
                    couple_reg.profile = profile.couple
                    couple_reg.program = last_program
                couple_reg.coupling = True
                couple_reg.additionalOption = additional
                couple_reg.save()
        return HttpResponseRedirect('/program/')
def only_print (request, management_id, profile_id):
    management = Management.objects.filter(id=management_id).first()
    registerations = Registration.objects.filter(program=management.program)
    registerations = registerations.filter(profile__user_id=profile_id)
    return registrations_to_print(registerations)