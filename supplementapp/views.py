from django.shortcuts import render , HttpResponse ,redirect
from .models import *
from .serializers import Productserializer
from rest_framework import viewsets
from rest_framework.response import Response
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    products = ProductModel.objects.all()
    whey_protein = products.filter(category='whey')  # محصولات Whey
    mass_gainers = products.filter(category='mass_gainer')  # محصولات Mass Gainers

    context = {
        'products': products,
        'whey_protein': whey_protein,
        'mass_gainers': mass_gainers,
    }
    return render(request, 'home/home.html', context)


def Product(request):
    products = ProductModel.objects.all()
    whey_protein = products.filter(category='whey')  # محصولات Whey
    mass_gainers = products.filter(category='mass_gainer')  # محصولات Mass Gainers
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)

    context = {
        'products': products,
        'whey_protein': whey_protein,
        'mass_gainers': mass_gainers,
        'selected_category': category,
        'category': ProductModel.CATEGORY_CHOICES,
    }
    return render(request,'product/product.html',context)


class Productviewset(viewsets.ModelViewSet):
    
    queryset = ProductModel.objects.all()
    serializer  = Productserializer
    




def Contactus(request):
    status = None
    form = Contactusform(request.POST or None)  # اینجا فرم را بر اساس داده‌های POST یا خالی می‌سازیم

    if request.method == 'POST':
        if form.is_valid():  # اگر فرم معتبر باشد
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data["phone"]
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']

            # ساخت پیام ایمیل
            email_subject = f"New Message from {name}"
            email_message = f"Name: {name}\nEmail: {email}\n\n{subject}\n {phone}\n Message:\n{text}\n "
            from_email = 'aliasadi3853@gmail.com'
            recipient_list = ['aliasadi3853@gmail.com']  # ایمیل دریافت‌کننده


            try:
                send_mail(email_subject, email_message, from_email, recipient_list)  # ارسال ایمیل
                status = 200  # تنظیم وضعیت موفقیت
                return redirect('supplementapp:contactus')  # ریدایرکت به صفحه موفقیت
            except Exception as e:
                status = 500  # در صورت بروز خطا در ارسال ایمیل
                print("Error sending email:", e)

    return render(request, 'contactus/contactus.html', {'form': form, 'status': status})




def Aboutus(request):
    return render(request,'aboutus/aboutus.html')




def Product_detail(request):
    return render(request,'product_detail/product_detail.html')





def Login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')  # شماره تلفن
        password = request.POST.get('password')  # رمز عبور

        try:
            # جستجوی کاربر با شماره تلفن
            user = RegisterModel.objects.get(phone=phone)
        except RegisterModel.DoesNotExist:
            user = None

        if user and user.password == password:  # چک کردن رمز عبور
            # ورود کاربر به سیستم
            login(request, user)  # ثبت نام در session
            return redirect("supplementapp:home")  # به صفحه خانه هدایت می‌شود
        else:
            # اگر شماره تلفن یا رمز عبور اشتباه بود
            messages.error(request, 'شماره تلفن یا رمز عبور اشتباه است.')  # نمایش پیام خطا
            return redirect('Supplementapp:login')  # بازگشت به صفحه ورود

    return render(request, 'login/login.html')




def Logout(request):
    logout(request)
    return redirect('supplementapp:home')




def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # گرفتن داده‌های فرم
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')

            # بررسی اگر کاربر با شماره تلفن وارد شده قبلاً ثبت‌نام کرده باشد
            if RegisterModel.objects.filter(phone=phone).exists():
                form.add_error('phone', 'این شماره تلفن قبلاً ثبت‌نام شده است.')
                return render(request, 'register/register.html', {'form': form})

            # ذخیره کردن اطلاعات کاربر و هش کردن رمز عبور
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()

            # ورود کاربر به سیستم
            login(request, user)

            # هدایت به صفحه خانه
            return redirect("supplementapp:home")
        else:
            # در صورت خطا در فرم
            return render(request, 'register/register.html', {'form': form})
        
    else:
        # در صورتی که درخواست GET باشد
        form = RegisterForm()
        return render(request, 'register/register.html', {'form': form})




