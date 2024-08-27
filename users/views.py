from django.shortcuts import render, redirect
from user_management import settings 
import re

import ast
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm,QRForm, BankDetailsForm
from functions.so import* 
from functions.QR import* 
from functions.sinh_trac_hoc import*
from functions.nhan_tuong_hoc import*
from functions.supa_data import* 
from functions.tinh_tien import* 

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import os
from supabase import create_client, Client
import base64
# import face_recognition
import datetime
import requests
from io import BytesIO
import json
from users.forms import FingerImageForm,FaceImageForm,UpgradeForm
from users.models import qr_image
from statistics import mean
# from .models import UploadImage  
url="https://zilpepysnqvfkpylfumn.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppbHBlcHlzbnF2ZmtweWxmdW1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjA2NzAsImV4cCI6MjAzMjYzNjY3MH0.yhOVyH2Ulk2Uhnulyu8FxkKS5zYfqgy1W_vRIGkQ300"
supabase = create_client(url, key)


def home(request):
    if request.user.is_authenticated:
        name = request.user.username
        # data=get_data(name)
        rows = supabase.table("feature").select("*").eq("username", name).execute()
        respone = supabase.table("rating").select("*").execute()
        rate = []

        for res in respone.data:
            rate.append(float(res['rating']))
        for row in rows.data:
            data = {
                'thansohoc': row['thansohoc'],
                'sinhtrachoc': row['sinhtrachoc'],
                'nhantuonghoc': row['nhantuonghoc'],
            }

        data['average_rating'] = round(mean(rate), 1)
        data['total_ratings'] = len(respone.data)
        return render(request, 'users/home.html', data)
    else:
        respone = supabase.table("rating").select("*").execute()
        rate = []

        for res in respone.data:
            rate.append(float(res['rating']))
        data = {
            'average_rating': round(mean(rate), 1),
            'total_ratings': len(respone.data),

        }
        return render(request, 'users/home.html', data)
def numerology_result(request):
    return render(request, 'users/numerology_result.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # Chuyển hướng tới trang chủ nếu người dùng đã đăng nhập
        if request.user.is_authenticated:
            return redirect(to='/')

        # Nếu không, xử lý dispatch như bình thường
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

class GuestLoginView(View):
    def get(self, request, *args, **kwargs):
        guest_user = authenticate(username='Guest', password='Duy487141543')  # Thay thế mật khẩu bằng mật khẩu thực tế
        if guest_user is not None:
            login(request, guest_user)
            return redirect('users-home')  # Chuyển hướng tới trang chủ hoặc bất kỳ đâu
        else:
            messages.error(request, 'Unable to login as guest')
            return redirect('login')
def read_file_content(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()       

def process_file_thansohoc(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Tách nội dung theo phần mô tả và phần nghề nghiệp
    parts = content.split("\n\nNghề nghiệp phù hợp:\n")
    
    if len(parts) == 2:
        mota = parts[0].strip().replace('\n', '<br>')   
        nganhnghe = parts[1].strip().replace('\n', '<br>')   
        
        # Đưa vào dictionary với hai keys "mota" và "nganhnghe"
        result = {
            "mota": mota,
            "nganhnghe": nganhnghe
        }
        
        return result
    else:
        return None
@login_required
def profile(request):
    bank_choices = [
        ('None',"None"),
        ('VietcomBank', 'VietcomBank'),
        ('VietinBank', 'VietinBank'),
        ('Techcombank', 'Techcombank'),
        ('BIDV', 'BIDV'),
        ('AgriBank', 'AgriBank'),
        ('Navibank', 'Navibank'),
        ('Sacombank', 'Sacombank'),
        ('ACB', 'ACB'),
        ('MBBank', 'MBBank'),
        ('TPBank', 'TPBank'),
        ('Shinhan Bank', 'Shinhan Bank'),
        ('VIB Bank', 'VIB Bank'),
        ('VPBank', 'VPBank'),
        ('SHB', 'SHB'),
        ('Eximbank', 'Eximbank'),
        ('BaoVietBank', 'BaoVietBank'),
        ('VietcapitalBank', 'VietcapitalBank'),
        ('SCB', 'SCB'),
        ('DongABank', 'DongABank'),
        ('KienLongBank', 'KienLongBank'),
        
        # Add more banks as needed
    ]
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        bank_form = BankDetailsForm(request.POST, bank_choices=bank_choices)
        # if bank_form['bank'] and bank_form['account_number']:
        bank=bank_form['bank']
        number =bank_form['account_number']
        if bank.data == 'None':
            pass
        else:
            
            data={
                'username':request.user.username,
                'bank':bank.data,
                'id':number.data
            }
            
            supabase.table('bank').upsert(data, on_conflict=['username']).execute()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        response = supabase.table('bank').select('*').eq('username', request.user.username).execute()
        if response.data:
            initial_bank = response.data[0]['bank']
            initial_account_number = response.data[0]['id']
            bank_form = BankDetailsForm(initial={'bank': initial_bank, 'account_number': initial_account_number}, bank_choices=bank_choices)
        else:
            bank_form = BankDetailsForm(bank_choices=bank_choices)
        # print(bank_form.bank)
        # print('------------')
        # print(bank_form.account_number)
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form,'bank_form': bank_form})

def calculate_numerology(request):
        name = request.user.username
        # data=get_data(name)
        rows = supabase.table("feature").select("*").eq( "username",name).execute()

        # Assert we pulled real data.
        assert len(rows.data) > 0
        for row in rows.data:
            data = {
                    'Thần số học': row['thansohoc'],
                    'Sinh trắc học': row['sinhtrachoc'],
                    'Nhân tướng học': row['nhantuonghoc'],
            }
        ngay = request.GET.get('ngay')
        thang = request.GET.get('thang')
        nam = request.GET.get('nam')
        ten = request.GET.get('ten')

        
            
        # Thực hiện tính toán các số thần số học ở đây
        # so_chu_dao_result = so_chu_dao(f"{ngay}/{thang}/{nam}")
        # so_linh_hon_result = so_linh_hon(ten)
        # so_su_menh_result = so_su_menh(ten)

        if not ngay or not thang or not nam or not ten:
            return render(request, 'numerology_form.html', {'error': 'Vui lòng nhập đầy đủ thông tin'})
        
        sochudao = {
            "filename": None,
            'result':None,
            "content": None
        }

        sosumenh = {
            "filename": None,
            'result':None,
            "content": None
        }

        solinhhon = {
            "filename": None,
            'result':None,
            "content": None
        }

        def format_date(day, month, year):
            formatted_day = str(day).zfill(2)
            formatted_month = str(month).zfill(2)
            formatted_year = str(year)
            return f"{formatted_day}/{formatted_month}/{formatted_year}"
        
        sochudao['result'] = so_chu_dao(format_date(ngay, thang, nam))
        solinhhon['result'] = so_linh_hon(ten)
        sosumenh['result'] = so_su_menh(ten)
        vip=None
        status = None
        api=False
        
        if data['Thần số học'] > 0: 
            status="Vip"
            sochudao['filename']= f"data/thansohoc_vip/sochudao/{sochudao['result']}.txt"
            solinhhon['filename']= f"data/thansohoc_vip/solinhhon/{solinhhon['result']}.txt"
            sosumenh['filename']= f"data/thansohoc_vip/sosumenh/{sosumenh['result']}.txt"
            # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
            new_vip_count = data['Thần số học'] - 1
            supabase.table("feature").update({"thansohoc": new_vip_count}).eq("username", name).execute()
            vip=True
            
            try:
                # Đường dẫn API và các tham số
                base_url = "https://openapi.cozeable.com/numerology/"
                params = {
                    'fullName': ten,
                    'dateOfBirth': format_date(ngay, thang, nam)
                }
                # Gửi yêu cầu GET đến API
                response = requests.get(base_url, params=params)
                response.raise_for_status()  # Nếu có lỗi HTTP, ném ra exception
                data = response.json()  # Chuyển đổi dữ liệu JSON trả về thành Python dict
                
                sochudao["data"] = process_file_thansohoc(sochudao["filename"]) 
                solinhhon["data"] = process_file_thansohoc(solinhhon["filename"])
                sosumenh["data"] =process_file_thansohoc(sosumenh["filename"])  
                # mota = sochudao["data"]["mota"]
                mota = data['cacConSo']['duongDoi']['noiDung']
                nganhnghe = sochudao["data"]["nganhnghe"]
                sochudao["content"] = f"Mô tả: {mota} \n\nNghề nghiệp phù hợp: \n\n{nganhnghe}".replace('\n', '<br>')   
                mota = data['cacConSo']['linhHon']['noiDung']
                nganhnghe = solinhhon["data"]["nganhnghe"]
                solinhhon["content"] = f"Mô tả: {mota}  \n\nNghề nghiệp phù hợp: \n\n{nganhnghe}".replace('\n', '<br>')  
                mota = data['cacConSo']['suMenh']['noiDung']
                nganhnghe = sosumenh["data"]["nganhnghe"]
                sosumenh["content"] =f"Mô tả: {mota}  \n\nNghề nghiệp phù hợp: \n\n{nganhnghe}".replace('\n', '<br>') 
                api=True 

                for key, value in data['cacConSo'].items():
                    value["noiDung"] = value["noiDung"].replace('\n', '<br>')

                test=data['chuKiHangNam']
                test
                for temp in test:
                    temp['noiDung'] = temp['noiDung'].replace('\n', '<br>')
            
                    temp['giaTri']= str(datetime.datetime.now().year + int(temp['giaTri']))
                test2=data['chuKiHangThang']
                test2
                for index,temp in enumerate(test2):
                    temp['noiDung'] = temp['noiDung'].replace('\n', '<br>')
                    # Lấy năm và tháng hiện tại
                    nam_hien_tai = datetime.datetime.now().year
                    thang_hien_tai = datetime.datetime.now().month
                    # Tính toán tháng kết quả
                    thang_ket_qua = thang_hien_tai + index+1

                    # Xử lý trường hợp tháng kết quả vượt quá 12
                    while thang_ket_qua > 12:
                        thang_ket_qua -= 12
                        nam_hien_tai += 1
                    temp['giaTri']= f"{thang_ket_qua}/{nam_hien_tai}"

                    test3=data['cacChangDuongDoi']
                    for index,temp in enumerate(test3):
                        temp['noiDung']=temp['noiDung'].replace('\n', '<br>')
                        


                    test4=data['thachThuc']
                    for index,temp in enumerate(test4):
                        temp['noiDung']=temp['noiDung'].replace('\n', '<br>')
                        temp['index']=index+1
            except:
                sochudao["content"] = read_file_content(sochudao["filename"]) .replace('\n', '<br>')   
                solinhhon["content"] = read_file_content(solinhhon["filename"]).replace('\n', '<br>')   
                sosumenh["content"] =read_file_content(sosumenh["filename"]).replace('\n', '<br>') 
              
                data={}
                data['cacConSo'] =None
                data['chuKiHangNam']=None
                data['chuKiHangThang']=None
                data['cacChangDuongDoi']=None
                data['thachThuc']=None
            
        else:
            status='Non-Vip'
            sochudao['filename']= f"data/thansohoc_nor/sochudao/{sochudao['result']}.txt"
            solinhhon['filename']= f"data/thansohoc_nor/solinhhon/{solinhhon['result']}.txt"
            sosumenh['filename']= f"data/thansohoc_nor/sosumenh/{sosumenh['result']}.txt"
            vip=False
            sochudao["content"] = read_file_content(sochudao["filename"]) .replace('\n', '<br>')   
            solinhhon["content"] = read_file_content(solinhhon["filename"]).replace('\n', '<br>')   
            sosumenh["content"] =read_file_content(sosumenh["filename"]).replace('\n', '<br>')
            data={}
            data['cacConSo'] =None
            data['chuKiHangNam']=None
            data['chuKiHangThang']=None
            data['cacChangDuongDoi']=None
            data['thachThuc']=None
              


        context = {
            "username":request.user.username,
            'so_chu_dao_result': sochudao['result'],
            'so_linh_hon_result':solinhhon['result'],
            'so_su_menh_result': sosumenh['result'],
            'so_chu_dao_cotent':sochudao["content"] ,
            'so_linh_hon_content':solinhhon["content"],
            'so_su_menh_cotent': sosumenh["content"],
            'status':status,
            'vip':vip,
            'api':api,
            'cacConso': data['cacConSo'],
            'chuKiHangNam': data['chuKiHangNam'],
            'chuKiHangThang':data['chuKiHangThang'],
            'cacChangDuongDoi':data['cacChangDuongDoi'],
            'thachThuc':data['thachThuc'],
        }
        context['context']=context
        # context['content']=render_to_pdf('users/numerology_result.html', context)
        content=None
        
        return render(request, 'users/numerology_result.html', context)


def sinhtrachoc_result(request):
    pass


def thansohoc(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    context = {
        'username':name,
        'data': data['Thần số học'],
        
    }
    return render(request, 'users/thansohoc.html',context)     

def sinhtrachoc(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    sinhtrachoc = {
            "filename": None,
            'result':None,
            "content": None
        }
    # return render(request, 'users/sinhtrachoc.html',context)
    def delete_files_in_folder(folder_path):
        # num_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
        num_files = len(files)
        if num_files > 100:
            files_to_delete = files[:50]  # Chọn 50 tệp đầu tiên để xóa
            for filename in files_to_delete:
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            counter = num_files
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                new_filename = f'DSPfinger{counter}{os.path.splitext(filename)[1]}'  # Giữ nguyên phần mở rộng của tệp
                new_file_path = os.path.join(folder_path, new_filename)
                try:
                    os.rename(file_path, new_file_path)
                    counter += 1
                except Exception as e:
                    print(f'Failed to rename {file_path} to {new_file_path}. Reason: {e}')
    if request.method == 'POST':  
        form = FingerImageForm(request.POST, request.FILES)  
        if form.is_valid(): 
            upload_folder = os.path.join(settings.MEDIA_ROOT, 'finger_images')  # Thay 'path_to_upload_folder' bằng đường dẫn thực tế
            delete_files_in_folder(upload_folder)
            form.save()  

            # Getting the current instance object to display in the template  
            img_object = form.instance  

            image_path = img_object.image.path
            img= Image.open(image_path)
            sinhtrachoc['result'] = predict_label(img)

            status = None
            if data['Sinh trắc học'] > 0: 
                status="Vip"
                sinhtrachoc['filename']= f"data/sinhtrachoc_vip/{sinhtrachoc['result']}.txt"
                # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                sinhtrachoc["content"] = read_file_content(sinhtrachoc["filename"]).replace('\n', '<br>') 
                new_vip_count = data['Sinh trắc học'] - 1
                supabase.table("feature").update({"sinhtrachoc": new_vip_count}).eq("username", name).execute()
        
            else:
                status='Non-Vip'
                sinhtrachoc['filename']= f"data/sinhtrachoc_nor/{sinhtrachoc['result']}.txt"
                sinhtrachoc["content"] = read_file_content(sinhtrachoc["filename"]).replace('\n', '<br>') 


            context = {
                "username":request.user.username,
                'form': form,
                'img_obj': img_object,
                'biometric_info': sinhtrachoc['result'],
                'status':status,
                'result':sinhtrachoc['result'],
                'content':sinhtrachoc['content'],
                
            }
            return render(request, 'users/sinhtrachoc_result.html', context)  
    else:  
        form = FingerImageForm()  
    context = {
        'username':name,
        'data': data['Sinh trắc học'],
        'form': form
    }
    return render(request, 'users/sinhtrachoc.html', context)  
           
def nhantuonghoc_image(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    nhantuonghoc = {
            "filename": None,
            'result':None,
            "content": None
        }
   
    def delete_files_in_folder(folder_path):
        # num_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
        num_files = len(files)
        if num_files > 100:
            files_to_delete = files[:50]  # Chọn 50 tệp đầu tiên để xóa
            for filename in files_to_delete:
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            counter = num_files
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                new_filename = f'DSPface{counter}{os.path.splitext(filename)[1]}'  # Giữ nguyên phần mở rộng của tệp
                new_file_path = os.path.join(folder_path, new_filename)
                try:
                    os.rename(file_path, new_file_path)
                    counter += 1
                except Exception as e:
                    print(f'Failed to rename {file_path} to {new_file_path}. Reason: {e}')
    if request.method == 'POST':  
        form = FaceImageForm(request.POST, request.FILES)  
        if form.is_valid(): 
            upload_folder = os.path.join(settings.MEDIA_ROOT, 'face_images')  # Thay 'path_to_upload_folder' bằng đường dẫn thực tế
            try:
                delete_files_in_folder(upload_folder)
            except: pass
            form.save()  

            # Getting the current instance object to display in the template  
            img_object = form.instance  

            image_path = img_object.image.path
            img= Image.open(image_path)
            # nhantuonghoc['result'] = predict_from_image(img)
            # image_np = np.array(img)
            # face_locations = face_recognition.face_locations(image_np)
            
            # top, right, bottom, left = face_locations[0]
            # face_image_np = image_np[top:bottom, left:right]
            nhantuonghoc['result'] = predict_from_image(img)
            status = None
            if nhantuonghoc['result'] =="No face detected.":
                context = {
                    "username":request.user.username,
                    'form': form,
                    'img_obj': img_object,
                    'biometric_info': nhantuonghoc['result'],
                    'status':status,
                    'result':nhantuonghoc['result'],
                    'content':nhantuonghoc['content'],
                    
                }
                nhantuonghoc["content"]='Không phát hiện thấy khuôn mặt nào trong ảnh. Đảm bảo khuôn mặt của bạn được nhìn thấy trong ảnh! Nếu có thể, mời bạn thử lại với ảnh khác'
                return render(request, 'users/nhantuonghoc_result.html', context) 
            else:
                if data['Nhân tướng học'] > 0: 
                    status="Vip"
                    nhantuonghoc['filename']= f"data/nhantuonghoc_vip/{nhantuonghoc['result']}.txt"
                    # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                    
                    nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                    
                    new_vip_count = data['Nhân tướng học'] - 1
                    supabase.table("feature").update({"nhantuonghoc": new_vip_count}).eq("username", name).execute()
            
                else:
                    status='Non-Vip'
                    nhantuonghoc['filename']= f"data/nhantuonghoc_nor/{nhantuonghoc['result']}.txt"
                    
                    nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
            
                
                context = {
                    "username":request.user.username,
                    'form': form,
                    'img_obj': img_object,
                    'biometric_info': nhantuonghoc['result'],
                    'status':status,
                    'result':nhantuonghoc['result'],
                    'content':nhantuonghoc['content'],
                    
                }
                return render(request, 'users/nhantuonghoc_result.html', context)  
            # nhantuonghoc_result(request,context)
    else:  
        form = FaceImageForm()  
    context = {
        'username':name,
        'data': data['Nhân tướng học'],
        'form': form
    }
    return render(request, 'users/nhantuonghoc_image.html',context) 
face_content={}
status_face=False
def nhantuonghoc_video(request):
    name = request.user.username
        # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    nhantuonghoc = {
            "filename": None,
            'result':None,
            "content": None
        }
    if request.method == 'POST':
        
        # face_content={}
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        # Decode base64 string to bytes
        decoded_data = base64.b64decode(str_img)

        # Create PIL image from bytes
        pil_image = Image.open(BytesIO(decoded_data))
        # image_np = np.array(pil_image)
        # face_locations = face_recognition.face_locations(image_np)
        # if face_locations:
        #     top, right, bottom, left = face_locations[0]
        #     face_image_np = image_np[top:bottom, left:right]
        nhantuonghoc['result'] = predict_from_image(pil_image )
        status = None
        if nhantuonghoc['result'] =="No face detected.":
                # content = {

                #     'biometric_info': nhantuonghoc['result'],
                #     'status':status,
                #     'result':nhantuonghoc['result'],
                #     'content':nhantuonghoc['content'],
                    
                # }
                # nhantuonghoc["content"]='Không phát hiện thấy khuôn mặt nào trong ảnh. Đảm bảo khuôn mặt của bạn được nhìn thấy trong ảnh! Nếu có thể, mời bạn thử lại với ảnh khác'
                # return render(request, 'users/nhantuonghoc_result.html', content) 
                pass
        else:
            if data['Nhân tướng học'] > 0: 
                status="Vip"
                nhantuonghoc['filename']= f"data/nhantuonghoc_vip/{nhantuonghoc['result']}.txt"
                # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                
                nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                
                new_vip_count = data['Nhân tướng học'] - 1
                supabase.table("feature").update({"nhantuonghoc": new_vip_count}).eq("username", name).execute()
        
            else:
                status='Non-Vip'
                nhantuonghoc['filename']= f"data/nhantuonghoc_nor/{nhantuonghoc['result']}.txt"
                
                nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                

            content = {
                "username":request.user.username,
                'biometric_info': nhantuonghoc['result'],
                'status':status,
                'result':nhantuonghoc['result'],
                'content':nhantuonghoc['content'],
                
            }
            request.session['content'] = content
            return JsonResponse({'success': True, 'redirect_url': reverse('videoresult')})
       
        
       
    else:

        return render(request, 'users/nhantuonghoc_video.html')
 
def intro_video(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    content={
        "username": name,
        "data": data['Nhân tướng học']
    }
    return render(request, 'users/intro_video.html',content)     


def change_QR(qr):
    buffer_png = BytesIO()
    qr.save(buffer_png, kind='PNG')
    return base64.b64encode(buffer_png.getvalue()).decode('utf-8')

def nhantuonghoc_result(request):
    pass

def predict_shape(request):
    pass

def video_result(request):
    global face_content
    content = request.session.get('content')
    # print(content)
    return render(request, 'users/video_result.html', content)

def hoadon(request):
    return render(request, 'users/hoadon.html')

def nangcap(request):
    username = request.user.username
    form = UpgradeForm(request.POST)
    vouchers = []
    total_discount = 0
    context ={
        'error' :''
    } 
    current_user = request.user.username
    response2 = supabase.table('voucher').select('*').eq('username', current_user).eq('status', 'wait').execute()
    vouchers = response2.data
    context['form']= form 
    if request.GET: 
        temp = {}
        temp['Thần số học']= request.GET['thansohoc'] 
        temp['Nhân tướng học']= request.GET['nhantuonghoc'] 
        temp['Sinh trắc học']= request.GET['sinhtrachoc'] 
        
        if (temp['Thần số học']== '0') and (temp['Sinh trắc học']== '0') and (temp['Nhân tướng học']== '0'):
            context = {'form': form,   'vouchers': vouchers}
            context['error']= 'Không thể tiến hành thanh toán khi cả ba lựa chọn đều là 0. Vui lòng chọn lại!'

            return render(request,'users/nangcap.html',context)
        def change_QR(qr):
            buffer_png = BytesIO()
            qr.save(buffer_png, kind='PNG')
            return base64.b64encode(buffer_png.getvalue()).decode('utf-8')
        thansohoc = int(temp['Thần số học'])
        nhantuonghoc = int(temp['Nhân tướng học']) 
        sinhtrachoc = int(temp['Sinh trắc học'])

        response4 = supabase.table('services').select('*').eq('username', current_user).execute()
        t=response4.data
        response5 = supabase.table('bills_copy').select('thansohoc','nhantuonghoc','sinhtrachoc').eq('username', current_user).execute()
        his3=False
        count=0
        his={
            '12':0,
            "13":0,
            '23':0,
        }
        for i in response5.data:
            if i['thansohoc'] >0 and i['nhantuonghoc']>0 and i['sinhtrachoc']>0:
                    his3=True
                    count+=1
            if i['thansohoc'] >0 and i['nhantuonghoc']>0 and i['sinhtrachoc']==0:
                his['12']+=1
            if i['thansohoc'] >0 and i['sinhtrachoc']>0 and  i['nhantuonghoc']==0:
                his['13']+=1
            if i['sinhtrachoc'] >0 and i['nhantuonghoc']>0 and i['thansohoc']==0:
                his['23']+=1
        cont=False

        tong_tien= tinh_tien(thansohoc,nhantuonghoc,sinhtrachoc,his=his,ser_sale=t[0],his3=his3,count=count)
        
        if len(response5.data)==0 and tong_tien >150000:
            cont=True
        # Lấy bill_id cuối cùng và tăng lên 1
        response = supabase.table('bills').select('bill_id').order('bill_id', desc=True).limit(1).execute()
        if response.data:
            last_bill_id = response.data[0]['bill_id']
            last_number = int(last_bill_id[3:])
            new_number = last_number + 1
            new_bill_id = f'DSP{new_number:010d}'
        else:
            new_bill_id = 'DSP0000000001'
        
        qr= QR(new_bill_id,tong_tien )
        # temp_path=os.path.join(settings.MEDIA_ROOT, f'QR_images/{new_bill_id}.png')
        
        
        # image_path = img_object.image.path
        new_bill = {
            'bill_id': new_bill_id,
            'username': username,
            'thansohoc': thansohoc,
            'nhantuonghoc': nhantuonghoc,
            'sinhtrachoc': sinhtrachoc,
            'total':tong_tien,
            'approved': False,
            'img_str': change_QR(qr),
            'error': '',
            'cont':cont,
        }
        new_bill['bill']=new_bill
        voucher_ids=[]
        
        selected_vouchers = request.GET.getlist('vouchers')
        for voucher_id in selected_vouchers:
            voucher = next((v for v in vouchers if v['voucher_id'] == voucher_id), None)
            if voucher:
                total_discount += voucher['total']
                voucher_ids.append(voucher['voucher_id'])
        
        # form = UpgradeForm(request.GET)
        # if form.is_valid():
            
        new_bill['total_discount']=total_discount
        new_bill['voucher_ids']=voucher_ids
        if new_bill['total'] <new_bill['total_discount'] : 
            context = {'form': form,   'vouchers': vouchers}
            context['error']= 'Không thể tiến hành thanh toán vì số tiềm giảm giá đã vượt quá tổng tiền'
            return render(request,'users/nangcap.html',context)
        new_bill['cost']=new_bill['total']-new_bill['total_discount']
        # new_bill['vouchers']= vouchers
        
        response3 = supabase.table('bills').select('approved').eq('username', current_user).execute()
        data = response3.data
        has_false_approval = any(item['approved'] == False for item in data)
        
        if has_false_approval:
            context = {'form': form,   'vouchers': vouchers}
            context['error']= 'Không thể tiến hành thanh toán vì bạn vẫn còn hoá đơn chưa xử lí xong. Nếu bạn đã thanh toán cho hoá đơn đó, xin cho chúng tôi một chút thời gian để xử lí'
            return render(request,'users/nangcap.html',context) 
        
        return render(request,'users/thanhtoanhoadon.html',new_bill)
    else:
        form = UpgradeForm()
    context = {'form': form,   'vouchers': vouchers}
    return render(request, 'users/nangcap.html',context)

def thanhtoanhoadon(request,new_bill):
    if request.GET: 
        
        return render(request,'users/xacnhanhoadon.html',new_bill)
    return render(request,'users/thanhtoanhoadon.html',new_bill)
def xacnhanhoadon(request):
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        username = request.POST.get('username')
        thansohoc = request.POST.get('thansohoc')
        nhantuonghoc = request.POST.get('nhantuonghoc')
        sinhtrachoc = request.POST.get('sinhtrachoc')
        total = request.POST.get('total')
        img_str = request.POST.get('img_str')
        approved =request.POST.get('approved')
        referral_code=request.POST.get('referral_code')
        voucher_ids=request.POST.get('voucher_ids')
        if referral_code is not None:
            response = supabase.table('auth_user').select('username').eq('email', referral_code).execute()
            if len(response.data)==0:
                new_bill = {
                'bill_id': bill_id,
                'username': username,
                'thansohoc': thansohoc,
                'nhantuonghoc': nhantuonghoc,
                'sinhtrachoc': sinhtrachoc,
                'total':total,
                'approved': False,
                'img_str': img_str,
                'error': 'Mã giới thiệu sai. Mời bạn nhập lại. Bạn có thể không dùng mã giới thiệu vẫn có thể thanh toán!',
            }
                return render(request,'users/thanhtoanhoadon.html',new_bill)
            else:
                def get_max_voucher_id():
                    response = supabase.table('voucher').select('voucher_id').execute()
                    voucher_ids = [row['voucher_id'] for row in response.data if re.match(r'^dsp\d+$', row['voucher_id'])]
                    if not voucher_ids:
                        return "dsp0"
                    max_id = max(voucher_ids, key=lambda x: int(re.search(r'\d+', x).group()))
                    return max_id

                def create_voucher(username, total):
                    max_id = get_max_voucher_id()
                    max_num = int(re.search(r'\d+', max_id).group())
                    new_id = f"dsp{max_num + 1}"
                    
                    data = {
                        "voucher_id": new_id,
                        "username": username,
                        "total": total
                    }
        
                    supabase.table('voucher').insert(data).execute()
                    return data
            t= create_voucher(response.data[0]['username'],round(int(total)*0.1))
        # print(t)
        new_bill=new_bill = {
            'bill_id': bill_id,
            'username': username,
            'thansohoc': thansohoc,
            'nhantuonghoc': nhantuonghoc,
            'sinhtrachoc': sinhtrachoc,
            'total':total,
            'approved':approved,
        }
        supabase.table('bills').insert(new_bill).execute()
        voucher_ids = ast.literal_eval(voucher_ids)
        for voucher_id in voucher_ids:
            supabase.table('voucher').delete().eq('voucher_id', voucher_id).execute()
            
        new_bill = {
            'bill_id': bill_id,
            'username': username,
            'thansohoc': thansohoc,
            'nhantuonghoc': nhantuonghoc,
            'sinhtrachoc': sinhtrachoc,
            'total':total,
            'approved':approved,
            'img_str': img_str,
            'referral_code':referral_code,
        }
        # print(new_bill)
        # Render xacnhanhoadon.html with the received data
        
        return render(request, 'users/xacnhanhoadon.html', new_bill)
def lichsumua(request):
    username = request.user.username
    response = supabase.table('bills').select('*').eq('username', username).execute()
    bills = response.data
    
    return render(request,'users/lichsumua.html', {'bills': bills})

def hoadon(request, bill_id):
    username = request.user.username
    response = supabase.table('bills').select('*').eq('bill_id', bill_id).eq('username', username).execute()
    bills = response.data
    bill=bills[0]
    # print(bill)
    qr= QR(bill_id, bill['total'] )
    new_bill = {
            'bill_id': bill_id,
            'username': username,
            'thansohoc': bill['thansohoc'],
            'nhantuonghoc': bill['nhantuonghoc'],
            'sinhtrachoc': bill['sinhtrachoc'],
            'total':bill['total'],
            'approved': bill['approved'],
            'img_str': change_QR(qr),
        }
    # if not bills:
    #     return redirect('bill_list')
    
    return render(request,'users/hoadon.html',new_bill)



def user_voucher(request):
    username = request.user.username
    response = supabase.table('voucher').select('*').eq('username', username).eq('status', 'wait').execute()
    vouchers = response.data
    context={
        'vouchers':vouchers,
        'error':"",
        'notice':'',
    }
    if request.method == 'POST':
        voucher_id = request.POST.get('voucher_id')
        response2=  supabase.table('bank').select('*').eq('username', username).execute()
        if len(response2.data) ==0:
            context['error']='Bạn chưa cập nhật thông tin tài khoản ngân hàng! Vui lòng vào mục profile để cập nhật!'
        else:
            context['error']=f'Chúc mừng! Bạn đã khởi động rút tiền thành công cho voucher {voucher_id}! Xin hãy cho chúng tôi chút thời gian để chuyển tiền đến tài khoản ngân hàng của bạn!'
            context['notice']='Nếu có thắc mắc hay cần hỗ trợ. Hãy liên hệ với chúng tôi tại gmail: directionalpathway@gmail.com hoặc Facebook: https://www.facebook.com/DirectionalPathway'
            supabase.table('voucher').update({'status': 'request'}).eq('voucher_id',voucher_id).execute()
        response = supabase.table('voucher').select('*').eq('username', username).eq('status', 'wait').execute()
        vouchers = response.data
        context['vouchers']=vouchers
    return render(request,'users/user_voucher.html',context)



def xacnhan(request,voucher_id):
    
    response = supabase.table('voucher').select('total').eq('voucher_id', voucher_id).execute()
    context={
        'voucher_id':voucher_id,
        'total':response.data[0]['total']
    }
    return render(request,'users/xacnhan.html',context)



@user_passes_test(lambda u: u.is_superuser)
def approvehoadon(request):
    # Lấy tất cả các hoá đơn từ Supabase
    response = supabase.table('bills').select('*').eq('approved', False).execute()
    bills = response.data
    
    if request.method == 'POST':
        # Xử lý duyệt hoá đơn
        approved_bills = request.POST.getlist('approve')
        for bill_id in approved_bills:
            supabase.table('bills').update({'approved': True}).eq('bill_id', bill_id).execute()
            return redirect('approvehoadon')
    return render(request,'users/approvehoadon.html', {'bills': bills})

@user_passes_test(lambda u: u.is_superuser)
def admin_voucher(request):
    response = supabase.table('voucher').select('*').eq('status', "request").execute()
    vouchers = response.data
    context={
        'vouchers':vouchers
    }
    
    if request.method == 'POST':
        approved_vouhcers = request.POST.getlist('approve')
        for voucher_id in approved_vouhcers:
            supabase.table('voucher').update({'status': 'done'}).eq('voucher_id', voucher_id).execute()
            return redirect('admin_voucher')
    return render(request,'users/admin_voucher.html',context)


@user_passes_test(lambda u: u.is_superuser)
def allhoadon(request):
    # Lấy tất cả các hoá đơn từ Supabase
    response = supabase.table('bills').select('*').order('bill_id').execute()
    bills = response.data
    
    # if request.method == 'POST':
    #     # Xử lý duyệt hoá đơn
    #     approved_bills = request.POST.getlist('approve')
    #     for bill_id in approved_bills:
    #         supabase.table('bills').update({'approved': True}).eq('bill_id', bill_id).execute()
    #         return redirect('approvehoadon')
    return render(request,'users/allhoadon.html', {'bills': bills})

@user_passes_test(lambda u: u.is_superuser)
def voucherall(request):
    # Lấy tất cả các hoá đơn từ Supabase
    response = supabase.table('voucher').select('*').order('voucher_id').execute()
    vouchers = response.data
    
    # if request.method == 'POST':
    #     # Xử lý duyệt hoá đơn
    #     approved_bills = request.POST.getlist('approve')
    #     for bill_id in approved_bills:
    #         supabase.table('bills').update({'approved': True}).eq('bill_id', bill_id).execute()
    #         return redirect('approvehoadon')
    return render(request,'users/voucher_all.html', {'vouchers': vouchers})

@user_passes_test(lambda u: u.is_superuser)
def voucher(request,voucher_id):
    # Lấy tất cả các hoá đơn từ Supabase
    response = supabase.table('voucher').select('*').eq('voucher_id', voucher_id).execute()
    username=response.data[0]['username']
    response2 = supabase.table('bank').select('*').eq('username', username).execute()
    voucher = response.data[0]
    print(voucher)
    bank=response2.data[0]['bank']
    number=response2.data[0]['id']
    context={
        'voucher':voucher,
        'bank':bank,
        'number':number
    }
    voucher_id=voucher['voucher_id']
    username=voucher['username']
    content=(f'Hoan tien voucher {voucher_id} tu Web DirectionalPathway cho nguoi dung {username}')
    qr= QRforadmin(bank,number,content,voucher['total'])
    context['img_str']= change_QR(qr)
    context['content']=content
    return render(request,'users/voucher.html', context)

from .forms import RatingForm
@login_required
def rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # rating = form.save(commit=False)
            # rating.user = request.user
            # rating.save()
            rating = form.save(commit=False)
            rating.user = request.user
            rate={
                'username':str(rating.user.username),
                "rating":float(rating.stars)
            }
            try:
                supabase.table('rating').insert(rate).execute()
            except:
                supabase.table('rating').update({'rating': rate['rating']}).eq('username',rate['username']).execute()
            
            return redirect('users-home')  # Thay 'rate' bằng tên của view hoặc URL bạn muốn chuyển hướng đến sau khi đánh giá
    else:
        form = RatingForm()
    return render(request, 'users/rating.html')

