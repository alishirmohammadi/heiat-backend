from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.views.static import serve

from program import views as program_views
from accounts import views as accounts_views
from omid_utils import views as utils_views
from pay import views as pay_views

schema_view = get_schema_view(title='هیئت الزهرا دانشگاه شریف')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'programs', program_views.ProgramViewSet, base_name='program')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('choices/', utils_views.choices),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'auth/', include('djoser.urls')),
    path(r'accounts/profile/', accounts_views.EditProfileView.as_view()),
    path(r'accounts/couple/', accounts_views.set_couple),
    path(r'expenses', pay_views.ExpenseList.as_view()),
    path(r'registration/give_up/', program_views.give_up),
    path(r'program/register/<program_id>/', program_views.register),
    path(r'pay/terminal/start/', pay_views.start_pay_terminal),
    path(r'pay/registration/start/', pay_views.start_pay_registration),
    path(r'pay/payment_callback/', pay_views.payment_callback),
    path(r'', include(router.urls)),
    path(r'media/<path>', serve, {'document_root': settings.MEDIA_ROOT, }),
    path(r'static/<path>', serve, {'document_root': settings.STATIC_ROOT}),
]
