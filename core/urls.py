from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('',include('images.urls',namespace = 'images')),
    path('social-auth/',include('social_django.urls', namespace='social')),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name="password_reset"),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name="password_reset_complete"),
     
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html'), name='password_change'),

    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
