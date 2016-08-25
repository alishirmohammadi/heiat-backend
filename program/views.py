from django.shortcuts import render
from pay.models import Payment
import jdatetime
from program import jalali
from accounts.templatetags.tags import get_tuple_item
from .models import Program, User, Registration, Profile, Management, Pricing, Message, Message_reciving
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
import xlwt, time, random
from django.db.models import Sum, Q
from django.core.mail import send_mail, BadHeaderError, get_connection
from program.word import nmi
from django.core import mail


# Create your views here.

@login_required
def documentation(request, program_id):
    # if (request.method == 'GET'):
    #     post = Management.objects.all()
    #     return render(request, 'documents.html', {'post': post})
    program = Program.objects.filter(id=program_id).first()
    my_management = Management.objects.filter(program=program).filter(profile=request.user.profile).first()
    if not my_management:
        return render(request, 'danger!!!!!!! attack.html', {})
    managements = Management.objects.filter(program__type=program.type).filter(role__in=my_management.seedocument())
    managements = managements.exclude(documentation__isnull=True).exclude(documentation='')
    return render(request, 'documents.html', {'post': managements})

@login_required
def panel(request, program_id):
    programe = Program.objects.filter(id=program_id).first()
    managerlist = Management.objects.filter(profile=request.user.my_profile).filter(program=programe)
    manager = managerlist.first()
    registered = Registration.objects.filter(program=programe)

    if (request.method == 'GET'):
        if manager:
            # if manager.canEditProgram:
            #     return HttpResponseRedirect('/error')
            # else:
            if manager.canFilter:
                filter_all = request.session.get('filter',
                                                 {'status': [], 'people_type': [], 'payment': [],
                                                  'gender': ['male'],
                                                  'couple': [], 'age': [], 'entrance_year': [], 'level': [],
                                                  'conscription': [], 'passport': [], 'label1': [], 'label2': [],
                                                  'label3': [],
                                                  'label4': []})

                registered = allfilter(filter_all, programe)
                studentRange = []
                for item in range(5):
                    studentRange.append(programe.year - item)

                return render(request, 'panel.html', {'all': registered, 'program': programe,
                                                      'statusChoices': Registration.status_choices,
                                                      'peopleTypeChoices': Profile.people_type_choices,
                                                      'conscriptionChoices': Profile.conscription_choices,
                                                      # 'passportChoices': Profile.passport_choices,
                                                      'filterAll': filter_all,
                                                      'student_range': studentRange,
                                                      'label_range': range(11),
                                                      'manager': manager})

            else:
                return HttpResponseRedirect('/program/documents/' + str(programe.id))
        else:
            return HttpResponseRedirect('/error')
    else:
        action = request.POST.get('editFilter', '')

        status_filter = request.POST.getlist('status_choices')
        people_type_filter = request.POST.getlist('people_type_choices')
        payment_filter = request.POST.getlist('payment')
        gender_filter = request.POST.getlist('gender')
        couple_filter = request.POST.getlist('coupled')
        age_filter = request.POST.getlist('age')
        entrance_year_filter = request.POST.getlist('entrance_year')
        level_filter = request.POST.getlist('level')
        conscription_filter = request.POST.getlist('conscription_choices')
        passport_filter = request.POST.getlist('passport_choices')
        label1_filter = request.POST.getlist('label1')
        label2_filter = request.POST.getlist('label2')
        label3_filter = request.POST.getlist('label3')
        label4_filter = request.POST.getlist('label4')

        all_filter = {
            'status': status_filter,
            'people_type': people_type_filter,
            'payment': payment_filter,
            'gender': gender_filter,
            'couple': couple_filter,
            'age': age_filter,
            'entrance_year': entrance_year_filter,
            'level': level_filter,
            'conscription': conscription_filter,
            'passport': passport_filter,
            'label1': label1_filter,
            'label2': label2_filter,
            'label3': label3_filter,
            'label4': label4_filter,
        }
        request.session['filter'] = all_filter

        registered = Registration.objects.filter(program=programe)

        registered = allfilter(all_filter, programe)

        if action == 'show':
            if manager.canFilter:
                return HttpResponseRedirect('/program/panel/' + str(programe.id))
        elif action == 'excel':
            if manager.canFilter:
                status_list = []
                for j in registered:
                    status = get_tuple_item(Registration.status_choices, j.status)
                    numberOfPayment = j.numberOfPayments
                    coupling = j.coupling
                    profile__user__first_name = j.profile.user.first_name
                    profile__user__last_name = j.profile.user.last_name
                    profile__user__email = j.profile.user.email
                    profile__cellPhone = j.profile.cellPhone
                    object = (numberOfPayment,
                              coupling,
                              status,
                              profile__user__first_name,
                              profile__user__last_name,
                              profile__user__email,
                              profile__cellPhone)
                    status_list.append(object)
                return export_users_xls(status_list)
        elif action == 'monifest':
            # return render(request, 'panel.html', {'all': registered})
            return TestDocument(request, registered)
        elif action == 'print':
            # return render(request, 'panel.html', {'all': registered})
            return pri1(request, registered)
        elif action == 'select':
            if manager.canSelect:
                numberOfSelect = request.POST.get("selectFilter", '')
                face = int(numberOfSelect)
                total = registered.count()

                for selected in registered:
                    t = random.randint(1, total)
                    if face >= t:
                        selected.status = 'certain'
                        face = face - 1
                    else:
                        selected.status = 'reserved'
                    selected.save()
                    total = total - 1
            return HttpResponseRedirect('/program/panel/' + str(programe.id))
        else:
            return HttpResponseRedirect('/error')

@login_required
def TestDocument(request, registered):
    docx_title = "monifest.docx"
    f = nmi.crea(request, registered)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response


def pri1(request, registered):
    docx_title="print.docx"
    f=nmi.pri(request, registered)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response



def allfilter(filter, programe):
    registered = Registration.objects.filter(program=programe)

    if filter.get('status', []):
        registered = registered.filter(status__in=filter.get('status', []))

    if filter.get('people_type', []):
        registered = registered.filter(profile__people_type__in=filter.get('people_type', []))

    if filter.get('payment', []):
        registered = registered.filter(numberOfPayments__in=filter.get('payment', []))

    gender_filter = filter.get('gender', [])
    if gender_filter:
        if len(gender_filter) == 1:
            gender_filter = gender_filter[0]
            if gender_filter == 'male':
                registered = registered.filter(profile__gender=True)
            elif gender_filter == 'female':
                registered = registered.filter(profile__gender=False)
    couple_filter = filter.get('couple', [])
    if couple_filter:
        if len(couple_filter) == 1:
            couple_filter = couple_filter[0]
            if gender_filter == 'single':
                registered = registered.filter(coupling=False)
            elif couple_filter == 'couple':
                registered = registered.filter(coupling=True)
    age_filter = filter.get('age', [])
    ## This Filter should be reorginesed after matching codes (for Date of Birth Changes)
    if age_filter:
        if len(age_filter) == 1:
            age_filter = age_filter[0]
            teen_age = programe.year - 15
            old_age = programe.year - 65
            if age_filter == 'can':
                registered = registered.filter(profile__birthYear__lt=teen_age).filter(
                    profile__birthYear__gt=old_age)
            elif age_filter == 'cannot':
                registered = registered.exclude(
                    Q(profile__birthYear__lt=teen_age) | Q(profile__birthYear__gt=old_age))
                # This Filter i not complete, and reqire below Filter code:
                # profile__birthYear__lt=old_age

    label1_filter = filter.get('label1', [])
    if label1_filter:
        if len(label1_filter) == 1:
            label1_filter = label1_filter[0]
            if label1_filter == 'y':
                registered = registered.filter(label1=True)
            elif label1_filter == 'n':
                registered = registered.filter(label1=False)

    label2_filter = filter.get('label2', [])
    if label2_filter:
        if len(label2_filter) == 1:
            label2_filter = label2_filter[0]
            if label2_filter == 'y':
                registered = registered.filter(label2=True)
            elif label2_filter == 'n':
                registered = registered.filter(label2=False)

    if filter.get('label3', []):
        registered = registered.filter(label3__in=filter.get('label3', []))

    if filter.get('label4', []):
        registered = registered.filter(label4__in=filter.get('label4', []))
    if filter.get('entrance_year', []):
        # registered = registered.filter(profile__studentNumber__in= )
        pass
    if filter.get('level', []):
        pass
    if filter.get('conscription', []):
        registered = registered.filter(profile__conscription__in=filter.get('conscription', []))
    if filter.get('passport', []):
        registered = registered.filter(profile__passport__in=filter.get('passport',
                                                                        []))  # It should be completed, with rectify model, profile

    return registered



def export_users_xls(status_list):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['numOfPayment', 'coupling', 'status', 'first_name', 'last_name', 'email', 'cellphone']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in status_list:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 1:
                if row[1] == True:
                    x = 'متاهلی'
                else:
                    x = 'مجردی'
                ws.write(row_num, col_num, x, font_style)

                continue
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required
def addregistration(request, program_id):
    programe = Program.objects.filter(id=program_id).first()
    managerlist = Management.objects.filter(profile=request.user.my_profile).filter(program=programe)
    manager = managerlist.first()
    programcheck = bool(programe.type == 'arbaeen')

    if request.method == 'GET':
        return HttpResponseRedirect('/program/panel/' + str(programe.id))

    else:
        if manager.canAdd:

            codemelli = request.POST.get('mellicode', '')
            coupled = request.POST.get('coupled', '')
            a = bool(coupled)
            prof = Profile.objects.filter(melliCode=codemelli).first()
            if prof:
                peopletype = prof.people_type
                price = Pricing.objects.filter(program=programe).filter(Coupling=bool(coupled)).filter(
                    people_type=peopletype).first()
                passportcheck = prof.passport
                passportcheck1 = bool(prof.passport == 'have')
                passportcheck2 = bool(prof.passport == 'have 7')
                alreadyRegistered = Registration.objects.filter(program=programe).filter(profile=prof)
                if alreadyRegistered:
                    a = 'a'
                    registered = Registration.objects.filter(program=programe)
                    return render(request, 'panel.html', {'all': registered, 'program': programe,
                                                          'statusChoices': Registration.status_choices,
                                                          'peopleTypeChoices': Profile.people_type_choices,
                                                          'label_range': range(9),
                                                          'manager': manager, 'a': a})

                else:
                    if price:
                        if price.price1:
                            addregister = Registration()
                            addregister.profile = prof
                            addregister.program = programe
                            if programe.hasCoupling:
                                if prof.coupling:
                                    if coupled == 'married':
                                        addregister.coupling = True
                                        registeredcouple = Registration.objects.filter(program=programe).filter(
                                            profile=prof.coupling).first()
                                        if registeredcouple:
                                            registeredcouple.coupling = True
                                            registeredcouple.save()
                                        else:
                                            addcouple = Registration()
                                            addcouple.profile = prof.coupling
                                            addcouple.program = programe
                                            addcouple.coupling = True
                                            addcouple.save()
                                    else:
                                        addregister.coupling = False
                                else:
                                    addregister.coupling = False
                            else:
                                addregister.coupling = False

@login_required
def editstatus(request, program_id):
    programe = Program.objects.filter(id=program_id).first()
    managerlist = Management.objects.filter(profile=request.user.my_profile).filter(program=programe)
    registered = Registration.objects.filter(program=programe)
    manager = managerlist.first()
    if (request.method == 'GET'):
        return HttpResponseRedirect('/program/panel/' + str(programe.id))

    else:
        if manager.canEditRegistration:
            checked = request.POST.getlist('tick')
            editingreg = Registration.objects.filter(id__in=checked).filter(program=programe)
            action = request.POST.get('editAction', '')
            if action == 'label1':
                selectValue = request.POST.get('label1', '')
                for item in editingreg:
                    if selectValue == 'lab1-yes':
                        item.label1 = True
                    elif selectValue == 'lab1-no':
                        item.label1 = False
                    item.save()
            elif action == 'label2':
                selectValue = request.POST.get('label2', '')
                for item in editingreg:
                    if selectValue == 'lab2-yes':
                        item.label2 = True
                    elif selectValue == 'lab2-no':
                        item.label2 = False
                    item.save()
            elif action == 'label3':
                selectValue = request.POST.get('label3', '')
                for item in editingreg:
                    if selectValue == '0':
                        item.label3 = 0
                    elif selectValue == '1':
                        item.label3 = 1
                    elif selectValue == '2':
                        item.label3 = 2
                    elif selectValue == '3':
                        item.label3 = 3
                    elif selectValue == '4':
                        item.label3 = 4
                    elif selectValue == '5':
                        item.label3 = 5
                    elif selectValue == '6':
                        item.label3 = 6
                    elif selectValue == '7':
                        item.label3 = 7
                    elif selectValue == '8':
                        item.label3 = 8
                    item.save()
            elif action == 'label4':
                selectValue = request.POST.get('label4', '')
                for item in editingreg:
                    if selectValue == '0':
                        item.label4 = 0
                    elif selectValue == '1':
                        item.label4 = 1
                    elif selectValue == '2':
                        item.label4 = 2
                    elif selectValue == '3':
                        item.label4 = 3
                    elif selectValue == '4':
                        item.label4 = 4
                    elif selectValue == '5':
                        item.label4 = 5
                    elif selectValue == '6':
                        item.label4 = 6
                    elif selectValue == '7':
                        item.label4 = 7
                    elif selectValue == '8':
                        item.label4 = 8
                    item.save()
            elif action == 'status_choices':
                selectValue = request.POST.get('status_choices', '')
                for item in editingreg:
                    if selectValue == 'default':
                        item.status = 'default'
                    elif selectValue == 'certain':
                        item.status = 'certain'
                    elif selectValue == 'reserved':
                        item.status = 'reserved'
                    elif selectValue == 'given up':
                        item.status = 'given up'
                    elif selectValue == 'removed':
                        item.status = 'removed'
                    elif selectValue == 'suspended':
                        item.status = 'suspended'
                    elif selectValue == 'not chosen':
                        item.status = 'not chosen'
                    elif selectValue == 'came':
                        item.status = 'came'
                    elif selectValue == 'not came':
                        item.status = 'not came'
                    elif selectValue == 'temporary':
                        item.status = 'temporary'
                    elif selectValue == 'first stage':
                        item.status = 'first stage'
                    item.save()
            elif action == 'numberOfPayments':
                selectValue = request.POST.get('numberOfPayments', '')
                for item in editingreg:
                    if selectValue == 'numberOfPayments-0':
                        item.numberOfPayments = 0
                    elif selectValue == 'numberOfPayments-1':
                        item.numberOfPayments = 1
                    elif selectValue == 'numberOfPayments-2':
                        item.numberOfPayments = 2
                    elif selectValue == 'numberOfPayments-3':
                        item.numberOfPayments = 3
                    item.save()
            elif action == 'coupled':
                selectValue = request.POST.get('coupled', '')
                if programe.hasCoupling:
                    for item in editingreg:
                        if selectValue == 'coupled':
                            if item.profile.couple:
                                item.coupling = True
                                registeredcouple = Registration.objects.filter(program=programe).filter(
                                    profile=item.profile.couple).first()
                                if registeredcouple:
                                    registeredcouple.coupling = True
                                    registeredcouple.save()
                                else:
                                    addcouple = Registration()
                                    addcouple.profile = item.profile.couple
                                    addcouple.program = programe
                                    addcouple.coupling = True
                                    addcouple.save()
                        elif selectValue == 'single':
                            if item.profile.couple:
                                item.coupling = False
                                registeredcouple = Registration.objects.filter(program=programe).filter(
                                    profile=item.profile.couple).first()
                                if registeredcouple:
                                    registeredcouple.coupling = False
                                    registeredcouple.save()

                            else:
                                item.coupling = False
                        item.save()
        if manager.canMessage:
            checked = request.POST.getlist('tick')
            sendingreg = Registration.objects.filter(id__in=checked).filter(program=programe)
            action = request.POST.get('editAction', '')

            if action == 'message':
                inbox_filter = request.POST.get('inbox', 'false')
                if inbox_filter == 'inbox':
                    title = request.POST.get('title', '')
                    textcontent = request.POST.get('message text', '')
                    nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
                    # manager = request.user.id
                    managerlist = Management.objects.filter(profile=request.user.my_profile).filter(program=programe)
                    manager = managerlist.first()
                    post = Message()
                    post.subject = title
                    post.content = textcontent
                    post.messageSendDate = nowtime
                    post.sender = manager
                    post.save()
                    for item in registered:
                        post2 = Message_reciving()
                        post2.message_id = post.id
                        post2.registration_id = item.id
                        post2.save()
                        # post2.save()

                inbox_filter = request.POST.get('email', 'false')
                if inbox_filter == 'email':
                    subject = request.POST.get('messageTitle', '')
                    message = request.POST.get('message text', '')
                    # from_email = request.POST.get('from_email', 'debugpls@gmail.com')#hard code for try
                    # to_email = request.POST.get('to_email', 'ivyblackmail@gmail.com')#hard code for try
                    from_email = request.POST.get('from_email',
                                                  programe.email)  # sender email name who is maneger of the program
                    to_email = Registration.objects.filter(id__in=checked).filter(program=programe)
                    my_host = 'smtp.gmail.com'
                    my_port = 587
                    my_username = from_email
                    my_password = programe.emailPassword
                    my_use_tls = True
                    connection = get_connection(host=my_host,
                                                port=my_port,
                                                username=my_username,
                                                password=my_password,
                                                use_tls=my_use_tls)

                    for sendemail in to_email:
                        to_person_mail = sendemail.profile.user.email
                        if subject and message:
                            try:
                                connection.open()
                                send_mail(subject, message, from_email, [to_person_mail], auth_user=my_username,
                                          auth_password=my_password, connection=connection)
                                connection.close()
                            except BadHeaderError:
                                return HttpResponse('Invalid header found.')
                        else:

                            return HttpResponse('Make sure all fields are entered and valid.')

                    else:
                        return HttpResponseRedirect('/error')

                inbox_filter = request.POST.get('sms', 'false')
                if inbox_filter == 'sms':
                    pass
                    sms_methode = send()

        return HttpResponseRedirect('/program/panel/' + str(programe.id))

@login_required
def my_programs(request):
    user = request.user
    programregistered = Registration.objects.filter(profile__user__exact=user)
    programregisteredbool = bool(programregistered)
    lastprogram = Program.objects.filter(isPublic=True).last()
    lastprogrambool = bool(lastprogram)
    lastpricing = Pricing.objects.filter(program=lastprogram)
    profile = Profile.objects.filter(user=user).first()
    comment = 'شماره تاریخ شما تا زمان سفر اعتبار ندارد'

    if profile.passport_dateofexpiry.year >= lastprogram.creationDate.year + 2:
        comment = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'

    if profile.passport_dateofexpiry.year >= lastprogram.creationDate.year + 1:
     if lastprogram.creationDate.month <= 6 :
         comment = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'
    if profile.passport_dateofexpiry.year == lastprogram.creationDate.year:
        if lastprogram.creationDate.month >= profile.passport_dateofexpiry.month + 6:
            comment = 'شماره تاریخ شما تا زمان سفر اعتبار دارد'

    passportcheck = bool(profile.passport != None)
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
                           'allStatus': Registration.status_choices,'comment': comment ,
                           'peopletype': Pricing.people_type_choices}
                          )
        else:
            return render(request, 'registrationlist.html', {'registered': registered,
                                                             'profile': profile,
                                                             'lastprogram': lastprogram,
                                                             'programregistered': programregistered,
                                                             'programregisteredbool': bool(programregistered),
                                                             'allStatus': Registration.status_choices,
                                                             'peopletype': Pricing.people_type_choices})
    if request.method == "POST":
        hascoupling = request.POST.get("hascoupling", '')
        boolhascoupling = bool(hascoupling)
        additonaltick = request.POST.get("additonaltick", '')
        booladditonaltick = bool(additonaltick)
        pricecheck = Pricing.objects.filter(people_type=mytype).filter(program=lastprogram).filter(
            Coupling=boolhascoupling).filter(
            additionalObject=booladditonaltick).first()
        if pricecheck:
            programcheck = bool(lastprogram.type == 'arbaeen')
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
                                        return render(request, 'danger!!!!!!! attack.html', {})
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
                        return render(request, 'danger!!!!!!! attack.html', {})
                else:
                    return render(request, 'danger!!!!!!! attack.html', {})
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
                    return render(request, 'danger!!!!!!! attack.html', {})

            registered = Registration.objects.filter(profile=profile).filter(program=lastprogram).exclude(
                status='removed').first()
            programregistered = Registration.objects.filter(profile__user__exact=user)
            return render(request, 'program.html',
                          {'registered': registered, 'lastpricing': lastpricing, 'lastprogram': lastprogram,
                           'programregistered': programregistered,
                           'allStatus': Registration.status_choices
                              , 'peopletype': Pricing.people_type_choices ,'comment': comment})
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
                                                    'comment': comment ,
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
    mymanagement = Management.objects.filter(id=management_id).first()
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
                              {'mymanagement': mymanagement,
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
            note = request.POST.get("note", '')
            program = mymanagement.program
            program.title = title
            program.programInterval = programinterval
            program.registerInterval = registerinterval
            program.hasCoupling = hascoupling
            program.isOpen = isopen
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
        return render(request, 'danger!!!!!!! attack.html', {})

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
               'success': success,}
        date_list.append(obj)

    massageinbox = Message_reciving.objects.filter(registration_id=registration_id)
    add = myregister.additionalObject
    us = myregister.profile.user
    pr = myregister.program
    usco = myregister.coupling
    mycoupleregister = Registration.objects.filter(program=pro).filter(profile=usco).first()
    usercoupling = bool(usco)
    pt = myregister.profile.people_type
    pricerow = Pricing.objects.filter(program=pr).filter(people_type=pt).filter(Coupling=usercoupling).filter(additionalObject=add).first()
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
            return render(request, 'danger!!!!!!! attack.html', {})
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
