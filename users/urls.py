from django.urls import path
from .views import  *
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView,GuestLoginView,UpgradeForm

from users.forms import LoginForm
urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('hoadon/', hoadon, name='hoadon'),
    path('nangcap/', nangcap, name='nangcap'),
    path('lichsumua/', lichsumua, name='lichsumua'),
    path('hoadon/<str:bill_id>/', hoadon, name='hoadon'),
    path('approvehoadon/', approvehoadon, name='approvehoadon'),
    path('user_voucher/', user_voucher, name='user_voucher'),
    path('xacnhan/<str:voucher_id>/', xacnhan, name='xacnhan'),
    path('allhoadon/', allhoadon, name='allhoadon'),
    path('admin_voucher/', admin_voucher, name='admin_voucher'),
    path('voucherall/', voucherall, name='voucherall'),
    path('rating/', rating, name='rating'),
    path('voucher/<str:voucher_id>/', voucher, name='voucher'),
    
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),
     
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('login/guest/', GuestLoginView.as_view(), name='login-guest'),
    path('thanhtoanhoadon/', thanhtoanhoadon, name='thanhtoanhoadon'),
    path('thanhtoanhoadon/xacnhanhoadon/', xacnhanhoadon, name='xacnhanhoadon'),
    path('thansohoc/' , thansohoc , name='thansohoc'),
    path('thansohoc/calculate_numerology/' , calculate_numerology , name='numerology_result'),
    path('sinhtrachoc/' , sinhtrachoc , name='sinhtrachoc'),
    path('sinhtrachoc_result' , sinhtrachoc_result , name='sinhtrachoc_result'),
    path('nhantuonghocimage/' ,nhantuonghoc_image , name='nhantuonghocimage'),
    path('introvideo/' ,intro_video , name='introvideo'),
    path('nhantuonghocvideo/' ,nhantuonghoc_video , name='nhantuonghocvideo'),
    path('nhantuonghocvideo/videoresult/' ,video_result, name='videoresult'),
    path('nhantuonghocresult/' ,nhantuonghoc_result, name='nhantuonghocresult'),
    path('predict/', predict_shape, name='predict'),
     


    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
