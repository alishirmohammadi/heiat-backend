from django.db import models
from program.models import Program
from accounts.models import Profile


class Management(models.Model):
    program = models.ForeignKey(Program, related_name='managements', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='managements', on_delete=models.CASCADE)
    canEditProgram = models.BooleanField(default=False)
    canFilter = models.BooleanField(default=False)
    canSelect = models.BooleanField(default=False)
    canEditRegistration = models.BooleanField(default=False)
    canMessage = models.BooleanField(default=False)
    canAdd = models.BooleanField(default=False)
    documentation = models.CharField(null=True, blank=True, max_length=10000)
    ROLE_MASTER_MANAGER = 'master manager'
    ROLE_VICAR = 'vicar'
    ROLE_REGISTRATION_MANAGER = 'registration manager'
    ROLE_SISTERS_MANAGER = 'sisters manager'
    ROLE_SISTERS_REGISTRATION_MANAGER = 'sister registration manager'
    ROLE_COMMUNICATION_SISTERS_MANAGER = 'communication sisters manager'
    ROLE_LOGISTIC_MANAGER = 'logistic manager'
    ROLE_LOGISTIC_CREW = 'logistic crew'
    ROLE_EXECUTIVE_MANAGER = 'executive manager'
    ROLE_EXECUTIVE_CREW = 'executive crew'
    ROLE_PANTRY_MANAGER = 'pantry manager'
    ROLE_PANTRY_CREW = 'pantry crew'
    ROLE_ADVERTISING_MANAGER = 'advertising manager'
    ROLE_ADVERTISING_CREW = 'advertising crew'
    ROLE_CREW = 'crew'
    ROLE_KITCHEN_MANAGER = 'kitchen manager'
    ROLE_KITCHEN_VICAR = 'kitchen vicar'
    ROLE_KITCHEN_CREW = 'kitchen crew'
    ROLE_CHOICES = (
        (ROLE_MASTER_MANAGER, 'مسئول برنامه'),
        (ROLE_VICAR, 'جانشین'),
        (ROLE_REGISTRATION_MANAGER, 'مسئول ثبت نام'),
        (ROLE_SISTERS_MANAGER, 'مسئول خواهران'),
        (ROLE_SISTERS_REGISTRATION_MANAGER, 'مسئول ثبت نام خواهران'),
        (ROLE_COMMUNICATION_SISTERS_MANAGER, 'مسئول ارتباط با خواهران'),
        (ROLE_LOGISTIC_MANAGER, 'مسئول تدارکات'),
        (ROLE_LOGISTIC_CREW, 'کادر تداراکات'),
        (ROLE_EXECUTIVE_MANAGER, 'مسئول اجرایی'),
        (ROLE_EXECUTIVE_CREW, 'کادر اجرایی'),
        (ROLE_PANTRY_MANAGER, 'مسئول آبدارخانه'),
        (ROLE_PANTRY_CREW, 'کادر آبدارخانه'),
        (ROLE_ADVERTISING_MANAGER, 'مسئول تبلیغات'),
        (ROLE_ADVERTISING_CREW, 'کادر تبلیغات'),
        (ROLE_CREW, 'کادر'),
        (ROLE_KITCHEN_MANAGER, 'مسئول سلف'),
        (ROLE_KITCHEN_VICAR, 'معاون سلف'),
        (ROLE_KITCHEN_CREW, 'کادر سلف'),
    )
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default=ROLE_MASTER_MANAGER)
    comment = models.CharField(max_length=800, null=True, blank=True)

    class Meta:
        verbose_name = 'مسئولیت'
        verbose_name_plural = 'مسئولیت‌ها'

    def seedocument(self):
        return {
            Management.ROLE_MASTER_MANAGER: [Management.ROLE_MASTER_MANAGER, Management.ROLE_VICAR,
                                             Management.ROLE_REGISTRATION_MANAGER, Management.ROLE_SISTERS_MANAGER,
                                             Management.ROLE_SISTERS_REGISTRATION_MANAGER,
                                             Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                             Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_LOGISTIC_CREW,
                                             Management.ROLE_EXECUTIVE_MANAGER,
                                             Management.ROLE_EXECUTIVE_CREW, Management.ROLE_PANTRY_MANAGER,
                                             Management.ROLE_PANTRY_CREW, Management.ROLE_ADVERTISING_MANAGER,
                                             Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW,
                                             Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                             Management.ROLE_KITCHEN_CREW],
            Management.ROLE_VICAR: [Management.ROLE_VICAR, Management.ROLE_REGISTRATION_MANAGER,
                                    Management.ROLE_SISTERS_MANAGER,
                                    Management.ROLE_SISTERS_REGISTRATION_MANAGER,
                                    Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                    Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_LOGISTIC_CREW,
                                    Management.ROLE_EXECUTIVE_MANAGER,
                                    Management.ROLE_EXECUTIVE_CREW, Management.ROLE_PANTRY_MANAGER,
                                    Management.ROLE_PANTRY_CREW, Management.ROLE_ADVERTISING_MANAGER,
                                    Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW,
                                    Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                    Management.ROLE_KITCHEN_CREW],
            Management.ROLE_REGISTRATION_MANAGER: [Management.ROLE_REGISTRATION_MANAGER, Management.ROLE_CREW],
            Management.ROLE_SISTERS_MANAGER: [Management.ROLE_SISTERS_MANAGER,
                                              Management.ROLE_SISTERS_REGISTRATION_MANAGER, Management.ROLE_CREW],
            Management.ROLE_COMMUNICATION_SISTERS_MANAGER: [Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                                            Management.ROLE_CREW],
            Management.ROLE_LOGISTIC_MANAGER: [Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_CREW,
                                               Management.ROLE_LOGISTIC_CREW, Management.ROLE_PANTRY_MANAGER,
                                               Management.ROLE_PANTRY_CREW,
                                               Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                               Management.ROLE_KITCHEN_CREW, Management.ROLE_CREW],
            Management.ROLE_LOGISTIC_CREW: [Management.ROLE_LOGISTIC_CREW, Management.ROLE_CREW],
            Management.ROLE_EXECUTIVE_MANAGER: [Management.ROLE_EXECUTIVE_MANAGER, Management.ROLE_EXECUTIVE_CREW,
                                                Management.ROLE_CREW],
            Management.ROLE_PANTRY_MANAGER: [Management.ROLE_PANTRY_MANAGER, Management.ROLE_CREW,
                                             Management.ROLE_PANTRY_CREW],
            Management.ROLE_PANTRY_CREW: [Management.ROLE_PANTRY_CREW, Management.ROLE_CREW],
            Management.ROLE_ADVERTISING_MANAGER: [Management.ROLE_ADVERTISING_MANAGER, Management.ROLE_CREW,
                                                  Management.ROLE_ADVERTISING_CREW],
            Management.ROLE_ADVERTISING_CREW: [Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW],
            Management.ROLE_KITCHEN_MANAGER: [Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_CREW,
                                              Management.ROLE_CREW, Management.ROLE_KITCHEN_VICAR],
            Management.ROLE_KITCHEN_VICAR: [Management.ROLE_KITCHEN_VICAR, Management.ROLE_KITCHEN_CREW,
                                            Management.ROLE_CREW],
            Management.ROLE_KITCHEN_CREW: [Management.ROLE_KITCHEN_CREW, Management.ROLE_CREW],
            Management.ROLE_CREW: Management.ROLE_CREW,

        }[self.role]

    def __str__(self):
        return str(self.profile) + '-' + str(self.role) + '-' + str(self.program)
