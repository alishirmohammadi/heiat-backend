from django.db.models import Q
from accounts.templatetags.tags import get_tuple_item
from .models import Registration
from django.http import HttpResponse
import xlwt
from django.core.mail import send_mail, BadHeaderError, get_connection
from program.models import Registration, Management
from zeep import Client
from accounts.models import Profile


def export_users_xls(status_list):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['numOfPayment', 'coupling', 'status', 'first_name', 'last_name', 'email', 'cellphone',
               'profile_mellicode', 'Registration_feedback', 'Registration_additionalOption']
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


def registrations_to_excel(registrations):
    status_list = []
    for j in registrations:
        status = get_tuple_item(Registration.status_choices, j.status)
        numberOfPayment = j.numberOfPayments
        coupling = j.coupling
        profile__user__first_name = j.profile.user.first_name
        profile__user__last_name = j.profile.user.last_name
        profile__user__email = j.profile.user.email
        profile__cellPhone = j.profile.cellPhone
        profile_mellicode = j.profile.user.username
        Registration_feedback = j.feedBack
        if j.additionalOption:
            Registration_additionalOption = j.additionalOption
        else:
            Registration_additionalOption = 'not have'
        object = (numberOfPayment,
                  coupling,
                  status,
                  profile__user__first_name,
                  profile__user__last_name,
                  profile__user__email,
                  profile__cellPhone,
                  profile_mellicode,
                  Registration_feedback,
                  Registration_additionalOption
                  )
        status_list.append(object)
    return export_users_xls(status_list)


# def send_email(from_email,from_password,bcc,subject,content):
#     my_use_tls = False
#     connection = get_connection(host='mehr.sharif.ir',
#                                 port=587,
#                                 username=from_email,
#                                 password=from_password,
#                                 use_tls=my_use_tls)
#     connection.open()
#     send_mail(subject, content, from_email, bcc, auth_user=from_email,
#               auth_password=from_password, connection=connection)
#     connection.close()



def filter_to_registrations(filter, program):
    registerations = Registration.objects.filter(program=program)

    if filter.get('status', []):
        registerations = registerations.filter(status__in=filter.get('status', []))

    if filter.get('people_type', []):
        registerations = registerations.filter(profile__people_type__in=filter.get('people_type', []))

    if filter.get('payment', []):
        registerations = registerations.filter(numberOfPayments__in=filter.get('payment', []))
    # if filter.get('passportCheck', []):
    #     registerations = registerations.filter(numberOfPayments__in=filter.get('passportCheck', []))

    gender_filter = filter.get('gender', [])
    if gender_filter:
        if len(gender_filter) == 1:
            gender_filter = gender_filter[0]
            if gender_filter == 'male':
                registerations = registerations.filter(profile__gender=True)
            elif gender_filter == 'female':
                registerations = registerations.filter(profile__gender=False)
    couple_filter = filter.get('couple', [])
    if couple_filter:
        if len(couple_filter) == 1:
            couple_filter = couple_filter[0]
            if couple_filter == 'single':
                registerations = registerations.filter(coupling=False)
            elif couple_filter == 'couple':
                registerations = registerations.filter(coupling=True)
    age_filter = filter.get('age', [])
    ## This Filter should be reorginesed after matching codes (for Date of Birth Changes)
    if age_filter:
        if len(age_filter) == 1:
            age_filter = age_filter[0]
            teen_age = program.year - 15
            old_age = program.year - 65
            if age_filter == 'can':
                registerations = registerations.filter(profile__birthYear__lt=teen_age).filter(
                    profile__birthYear__gt=old_age)
            elif age_filter == 'cannot':
                registerations = registerations.exclude(
                    Q(profile__birthYear__lt=teen_age) | Q(profile__birthYear__gt=old_age))
                # This Filter i not complete, and reqire below Filter code:
                # profile__birthYear__lt=old_age

    mugshot_filter = filter.get('mugshot', [])
    if mugshot_filter:
        if len(mugshot_filter) == 1:
            mugshot_filter = mugshot_filter[0]
            if mugshot_filter == 'y':
                registerations = registerations.filter(profile__mugshot__isnull=False).exclude(profile__mugshot='')
            elif mugshot_filter == 'n':
                registerations = registerations.filter(Q(profile__mugshot__isnull=True) | Q(profile__mugshot=''))

    label1_filter = filter.get('label1', [])
    if label1_filter:
        if len(label1_filter) == 1:
            label1_filter = label1_filter[0]
            if label1_filter == 'y':
                registerations = registerations.filter(label1=True)
            elif label1_filter == 'n':
                registerations = registerations.filter(label1=False)

    label2_filter = filter.get('label2', [])
    if label2_filter:
        if len(label2_filter) == 1:
            label2_filter = label2_filter[0]
            if label2_filter == 'y':
                registerations = registerations.filter(label2=True)
            elif label2_filter == 'n':
                registerations = registerations.filter(label2=False)

    additionalOtionFilter = filter.get('additionalOption', [])
    if additionalOtionFilter:
        if len(additionalOtionFilter) == 1:
            additionalOtionFilter = additionalOtionFilter[0]
            if additionalOtionFilter == 'y':
                registerations = registerations.filter(additionalOption=True)
            elif additionalOtionFilter == 'n':
                registerations = registerations.filter(additionalOption=False)

    if filter.get('label3', []):
        registerations = registerations.filter(label3__in=filter.get('label3', []))

    if filter.get('label4', []):
        registerations = registerations.filter(label4__in=filter.get('label4', []))
    if filter.get('entrance_year', []):
        # registerations = registerations.filter(profile__studentNumber__in= )
        pass
    if filter.get('level', []):
        pass
    if filter.get('conscription', []):
        registerations = registerations.filter(profile__conscription__in=filter.get('conscription', []))
    from .utils import getLastProgram
    import datetime

    last_program = getLastProgram()
    if filter.get('passport', []):
        if 'NotHave' not in filter.get('passport', []):
            registerations = registerations.exclude(profile__passport=Profile.PASSPORT_NOT_HAVE).exclude(
                profile__passport__isnull=True)
        if 'invalid' not in filter.get('passport', []):
            for item in registerations:
                if item.profile.passport == Profile.PASSPORT_HAVE and (not item.profile.passport_dateofexpiry or (
                        item.profile.passport_dateofexpiry - last_program.startDate < datetime.timedelta(183))):
                    registerations = registerations.exclude(id=item.id)

        if 'valid' not in filter.get('passport', []):
            for item in registerations:
                if item.profile.passport_dateofexpiry:
                    if item.profile.passport_dateofexpiry - last_program.startDate >= datetime.timedelta(183):
                        registerations = registerations.exclude(id=item.id)
    birth = filter.get('birth', [])
    if birth and len(birth) == 1:
        birth = birth[0]
        for reg in registerations:
            if reg.profile.is_birth_valid() and birth == 'invalid':
                registerations = registerations.exclude(id=reg.id)
            elif not reg.profile.is_birth_valid() and birth == 'valid':
                registerations = registerations.exclude(id=reg.id)
    if filter.get('entrance_year', []):
        c = program.year
        if len(str(c)) == 4:
            c = str(c)[2:4]
        c = int(c)
        ent_filter = filter.get('entrance_year', [])[:]
        registerations = registerations.exclude(profile__studentNumber__startswith='*').exclude(
            profile__studentNumber='').exclude(profile__studentNumber__isnull=True)
        if str(c - 4) in ent_filter:
            ent_filter.remove(str(c - 4))
            for i in range(c - 3, c + 1):
                if str(i) not in ent_filter:
                    registerations = registerations.exclude(profile__studentNumber__startswith=str(i))
        else:
            for i in range(c - 10, c + 1):
                if str(i) not in ent_filter:
                    registerations = registerations.exclude(profile__studentNumber__startswith=str(i))
    if filter.get('level', []):
        if 'other' not in filter.get('level', []):
            registerations = registerations.filter(profile__studentNumber__regex=r'[0-9]{2}[1237][0-9]{5}')
        if 'bs' not in filter.get('level', []):
            registerations = registerations.exclude(profile__studentNumber__iregex=r'[0-9]{2}[1][0-9]{5}')
        if 'ms' not in filter.get('level', []):
            registerations = registerations.exclude(profile__studentNumber__iregex=r'[0-9]{2}[27][0-9]{5}')
        if 'phd' not in filter.get('level', []):
            registerations = registerations.exclude(profile__studentNumber__iregex=r'[0-9]{2}[3][0-9]{5}')

    return registerations


def sendSMS(list, text):
    client = Client(wsdl='http://api.payamak-panel.com/post/Send.asmx?wsdl')
    if len(list) // 100 == len(list) / 100:
        t = (len(list) // 100)
    else:
        t = (len(list) // 100) + 1
    for i in range(0, t):
        b = ""
        for j in range(0, 100):
            if (j + (i * 100)) == len(list):
                break
            if j == 0:
                b = b + str(list[j + (i * 100)])
            else:
                b = b + "," + str(list[j + (i * 100)])
        client.service.SendSimpleSMS2('9174486355', '3496', b, '50002016008706', text, False)


def getLastProgram():
    from .models import Program

    return Program.objects.filter(isPublic=True).last()


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def farsiNumber(Num):
    Num1 = str(Num)
    Num1.replace('1', '1')
    Num1.replace('1', '2')
    Num1.replace('1', '3')
    Num1.replace('1', '4')
    Num1.replace('1', '5')
    Num1.replace('1', '6')
    Num1.replace('1', '7')
    Num1.replace('1', '8')
    Num1.replace('1', '9')


def checkMelliCode(mellicode):
    a = mellicode
    if (len(a) == 8):
        a = '00' + a
    if (len(a) == 9):
        a = '0' + a
    print(a)
    if (len(a) == 10):
        r = 0
        for i in range(0, 9):
            r1 = int(a[i]) * (10 - i)
            r = r1 + r
        c = r % 11
        if (int(a[9]) == 1) and (c == 1):
            return True
        elif (int(a[9]) == 0) and (c == 0):
            return True
        elif (int(a[9]) == 11 - c):
            return True
        else:
            return False
    else:
        return False


def student_enterance(studentnumber):
    return studentnumber[0:2]


def student_type(studentnumber):
    a = studentnumber[2]
    if a == 1:
        type = 'bs'
    elif a == 2 or a == 7:
        type = 'ms'
    elif a == 3:
        type = 'phd'
    else:
        type = 'unkhown'
    return type
