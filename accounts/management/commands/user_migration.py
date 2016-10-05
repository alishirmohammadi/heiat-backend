from django.core.management.base import BaseCommand, CommandError
from accounts.models import Profile
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        import MySQLdb

        # connect
        db = MySQLdb.connect(host="localhost", user="omid", passwd="omidTheHorse",
                             db="heiat_old", use_unicode=True,charset="utf8")

        cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("SELECT * FROM user_db where userId>653")
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        print(field_names)

        # commit your changes
        db.commit()

        # get the number of rows in the resultset
        numrows = int(cursor.rowcount)

        # get and display one row at a time.
        for x in range(0, numrows):
            row = cursor.fetchone()
            print(str(row[0]), "-->", str(row[2]))
            melliCode = row[2]
            password = row[6]
            first_name = row[7]
            last_name = row[8]
            address = row[12]
            she = row[13]
            stu = row[14]
            father = row[15]
            email = row[16]
            cellPhone = row[17]
            emer = row[18]
            day = row[27]
            gender = bool(row[3])
            peopleType = {
                0: Profile.PEOPLE_TYPE_SHARIF_MASTER,
                1: Profile.PEOPLE_TYPE_SHARIF_STUDENT,
                2: Profile.PEOPLE_TYPE_SHARIF_GRADUATED,
                3: Profile.PEOPLE_TYPE_TALABE,
                4: Profile.PEOPLE_TYPE_NOTSHARIF_GRADUATED,
                5: Profile.PEOPLE_TYPE_NOTSHARIF_STUDENT,
                6: Profile.PEOPLE_TYPE_NOTSHARIF_GRADUATED,
                7: Profile.PEOPLE_TYPE_OTHER,
                8: Profile.PEOPLE_TYPE_OTHER,
                9: Profile.PEOPLE_TYPE_OTHER,
                10: Profile.PEOPLE_TYPE_TALABE,
                11: Profile.PEOPLE_TYPE_NOTSHARIF_GRADUATED,
                12: Profile.PEOPLE_TYPE_SHARIF_EMPLOYED,
                13: Profile.PEOPLE_TYPE_OTHER,
                14: Profile.PEOPLE_TYPE_OTHER
            }[row[9]]
            try:
                if email and email!='mail@domain.com' and cellPhone and cellPhone !='09*********':
                    new_user = User.objects.create_user(username=melliCode,
                                     email=email,
                                     password=password)
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.save()
                    p = Profile()
                    p.user=new_user
                    p.cellPhone = cellPhone
                    p.address=address
                    year = row[25]
                    month = row[26]
                    p.birthYear=year
                    p.birthMonth=month
                    p.birthDay=day
                    p.emergencyPhone=emer
                    p.fatherName=father
                    p.people_type=peopleType
                    p.gender=gender
                    p.shenasname=she
                    if p.people_type ==Profile.PEOPLE_TYPE_SHARIF_GRADUATED or p.people_type==Profile.PEOPLE_TYPE_SHARIF_STUDENT:
                        p.studentNumber=stu
                    p.save()
            except:
                pass
