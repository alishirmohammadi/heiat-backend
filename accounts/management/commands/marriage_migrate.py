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
        cursor.execute("SELECT * FROM user_db")
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
            couple=row[3]
            try:
                if melliCode and couple and couple !="**********":
                    me=Profile.objects.filter(user__username=melliCode).first()
                    couple_obj=Profile.objects.filter(user__username=couple).first()
                    if me and couple_obj:
                        me.couple=couple_obj
                        me.save()
                        couple_obj.couple=me
                        couple_obj.save()
                        print(melliCode+'-'+couple)
            except:
                pass
