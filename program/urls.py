from django.conf.urls import url
from django.contrib import admin

urlpatterns = [

    url(r'^$', 'program.views.my_programs'),
    url(r'^manage/$', 'program.views.my_managements'),
    url(r'^manage/(?P<management_id>\d+)/', 'program.views.manage'),
    url(r'^registration/(?P<registration_id>\d+)/', 'program.views.registration'),
    url(r'^add$', 'program.views.addInstallment'),
    url(r'^remove/(?P<pricing_id>\d+)/(?P<price_num>\d+)', 'program.views.removeInstallment'),
    url(r'^documents/(?P<management_id>\d+)', 'program.views.documentation'),
    url(r'^panel/(?P<management_id>\d+)/', 'program.views.panel'),
    url(r'^addreg/(?P<program_id>\d+)', 'program.views.addregistration'),
    url(r'^editregisteration/(?P<program_id>\d+)', 'program.views.editStatus'),
    url(r'print/(?P<management_id>\d+)/(?P<profile_id>\d+)', 'program.views.only_print'),

    # url(r'^signout/', 'accounts.views.signout'),
    # url(r'^signup/', 'accounts.views.signup'),
    # url(r'^passwordchange/', 'accounts.views.change_password'),
    # url(r'^recovery/', 'accounts.views.recovery'),
]
