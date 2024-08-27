from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView

from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),

    

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:  
#         urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  