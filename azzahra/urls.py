from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from accounts import views as accounts_views
from bot import views as bot_view
from dining import views as dining_views
from manage_app import views as manage_views
from omid_utils import views as utils_views
from pay import views as pay_views
from program import views as program_views

schema_view = get_schema_view(title='هیئت الزهرا دانشگاه شریف')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'programs', program_views.ProgramViewSet, basename='program')
router.register(r'manage', manage_views.ProgramManagement, basename='manage')
router.register(r'manage_registration', manage_views.RegistrationManagement, basename='manage_registration')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('choices/', utils_views.choices),
    path('dining/', include('dining.urls')),
    path('blanket/', dining_views.blanket),
    path('book/', dining_views.book),
    path('blanket/history/', dining_views.blanket_history),
    path('book/history/', dining_views.book_history),
    path('account/details/', accounts_views.user_detail_paboos),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'auth/', include('djoser.urls')),
    path(r'accounts/profile/', accounts_views.EditProfileView.as_view()),
    path(r'accounts/couple/', accounts_views.set_couple),
    path(r'accounts/password/reset/', accounts_views.password_reset),
    path(r'expenses', pay_views.ExpenseList.as_view()),
    path(r'cultural/<sub_program>/', program_views.cultural_program),
    path(r'cultural/<sub_program>/history/', program_views.cultural_history),
    path(r'entertainment/<sub_program>/', program_views.entertainment_program),
    path(r'entertainment/<sub_program>/history/', program_views.entertainment_history),
    path(r'registration/give_up/', program_views.give_up),
    path(r'registration/message/', program_views.NewMessage.as_view()),
    path(r'program/register/<program_id>/', program_views.register),
    path(r'pay/terminal/start/', pay_views.start_pay_terminal),
    path(r'bot/telegram/', csrf_exempt(bot_view.BotView.as_view())),

    path(r'pay/registration/start/', pay_views.start_pay_registration),
    path(r'pay/payment_callback/', pay_views.payment_callback),
    path(r'pay/view_pooyesh_karimane/', pay_views.view_payments),
    path(r'managements/', manage_views.ManagementList.as_view()),
    path(r'manage/posts/<pk>/delete/', manage_views.DeletePost.as_view()),
    path(r'manage/posts/<pk>/', manage_views.EditPost.as_view()),
    path(r'manage/posts/', manage_views.CreatePost.as_view()),
    path(r'manage/questions/<pk>/delete/', manage_views.DeleteQuestion.as_view()),
    path(r'manage/questions/<pk>/', manage_views.EditQuestion.as_view()),
    path(r'manage/questions/', manage_views.CreateQuestion.as_view()),
    path(r'', include(router.urls)),
    path(r'media/<path>', serve, {'document_root': settings.MEDIA_ROOT, }),
    path(r'static/<path>', serve, {'document_root': settings.STATIC_ROOT}),
]
