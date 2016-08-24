from django.conf.urls import url
from django.contrib import admin

urlpatterns = [

    url(r'^$', 'program.views.my_programs'),
    url(r'^manage/$', 'program.views.my_management'),
    url(r'^manage/(?P<management_id>\d+)/', 'program.views.manage'),
    url(r'^myform/(?P<registration_id>\d+)/', 'program.views.myform'),
    url(r'^add$', 'program.views.addInstallment'),
    url(r'^remove/(?P<pricing_id>\d+)/(?P<price_num>\d+)', 'program.views.removeInstallment'),
    url(r'^documents/(?P<program_id>\d+)', 'program.views.documentation'),
    url(r'^panel/(?P<program_id>\d+)/', 'program.views.panel'),
    url(r'^addreg/(?P<program_id>\d+)', 'program.views.addregistration'),
    url(r'^editregisteration/(?P<program_id>\d+)', 'program.views.editstatus'),
    # url(r'^signout/', 'accounts.views.signout'),
    # url(r'^signup/', 'accounts.views.signup'),
    # url(r'^passwordchange/', 'accounts.views.change_password'),
    # url(r'^recovery/', 'accounts.views.recovery'),
]
