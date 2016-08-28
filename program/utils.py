from django.db.models import Q
from accounts.templatetags.tags import get_tuple_item
from .models import Registration
from django.http import HttpResponse
import xlwt
from django.core.mail import send_mail, BadHeaderError, get_connection
from program.models import Registration
from pysimplesoap.client import SoapClient


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
        object = (numberOfPayment,
                  coupling,
                  status,
                  profile__user__first_name,
                  profile__user__last_name,
                  profile__user__email,
                  profile__cellPhone)
        status_list.append(object)
    return export_users_xls(status_list)

def send_email(from_email,from_password,to,subject,content):
    my_use_tls = True
    connection = get_connection(host='smtp.gmail.com',
                                port=587,
                                username=from_email,
                                password=from_password,
                                use_tls=my_use_tls)
    connection.open()
    send_mail(subject, content, from_email, to, auth_user=from_email,
              auth_password=from_password, connection=connection)
    connection.close()
    

def filter_to_registrations(filter, program):
    registerations = Registration.objects.filter(program=program)

    if filter.get('status', []):
        registerations = registerations.filter(status__in=filter.get('status', []))

    if filter.get('people_type', []):
        registerations = registerations.filter(profile__people_type__in=filter.get('people_type', []))

    if filter.get('payment', []):
        registerations = registerations.filter(numberOfPayments__in=filter.get('payment', []))

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
            if gender_filter == 'single':
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
    if filter.get('passport', []):
        registerations = registerations.filter(profile__passport__in=filter.get('passport',
                                                                        []))  # It should be completed, with rectify model, profile

    return registerations


def sendSMS(list,text):
    client = SoapClient(wsdl='http://api.payamak-panel.com/post/Send.asmx?wsdl', trace=False)
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
    client.SendSimpleSMS2('9174486355','3496', b, '50002016008706', text ,False)

def getLastProgram():
    from .models import Program
    return Program.objects.filter(isPublic=True).last()