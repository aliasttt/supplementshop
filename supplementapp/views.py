from django.shortcuts import render , HttpResponse ,redirect
from .models import *
from .serializers import Productserializer
from rest_framework import viewsets
from rest_framework.response import Response
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login ,logout ,get_backends
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from django.contrib.auth.hashers import make_password

import json
# برای چت بات این 3 تا اخری باید ایمپورت بشه

# مقداردهی اولیه به کلاینت Dialogflow
DIALOGFLOW_PROJECT_ID = 'supplementshop@supplement-shop-451721.iam.gserviceaccount.com'  # آیدی پروژه Dialogflow خود را وارد کنید
SESSION_CLIENT = dialogflow.SessionsClient()

@csrf_exempt  # در صورت نیاز به غیرفعال کردن CSRF برای تست، در محیط تولید توصیه می‌شود روش امن‌تری به کار ببرید.
def detect_intent_text(request):
    if request.method == 'POST':
        req_data = json.loads(request.body)
        text_input = req_data.get('text')
        session_id = req_data.get('sessionId', str(uuid.uuid4()))
        
        session = SESSION_CLIENT.session_path(DIALOGFLOW_PROJECT_ID, session_id)
        text_input_obj = dialogflow.types.TextInput(text=text_input, language_code='fa')
        query_input = dialogflow.types.QueryInput(text=text_input_obj)
        
        try:
            response = SESSION_CLIENT.detect_intent(session=session, query_input=query_input)
            # استخراج پاسخ نهایی از Dialogflow
            fulfillment_text = response.query_result.fulfillment_text
            return JsonResponse({
                'fulfillmentText': fulfillment_text,
                'intent': response.query_result.intent.display_name,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def home(request):
    
    


    products = ProductModel.objects.all()
    whey_protein = products.filter(category='whey')  
    mass_gainers = products.filter(category='mass_gainer') 
    casein = products.filter(category='casein')
    isolate = products.filter(category='isolate')

    context = {
        'products': products,
        'whey_protein': whey_protein,
        'mass_gainers': mass_gainers,
        'isolate' : isolate,
        'casein':casein
        
    }
    return render(request, 'home/home.html', context)


def Product(request):
    products = ProductModel.objects.all()
    category = request.GET.get('category', '')  # گرفتن دسته‌بندی از URL

    if category:
        products = products.filter(category=category)  # فیلتر کردن بر اساس دسته‌بندی

    whey_protein = products.filter(category='whey')  # محصولات Whey
    mass_gainers = products.filter(category='mass_gainer')  # محصولات Mass Gainers

    context = {
        'products': products,
        'whey_protein': whey_protein,
        'mass_gainers': mass_gainers,
        'selected_category': category,
        'category': ProductModel.CATEGORY_CHOICES,  # دسته‌بندی‌ها برای نمایش
    }
    return render(request, 'product/product.html', context)

class Productviewset(viewsets.ModelViewSet):
    
    queryset = ProductModel.objects.all()
    serializer  = Productserializer
    




def Contactus(request):
    status = None
    form = Contactusform(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data["phone"]
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']

            email_subject = f"New Message from {name}"
            email_message = f"Name: {name}\nEmail: {email}\n\n{subject}\n {phone}\n Message:\n{text}\n "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['aliasadi3853@gmail.com']

            try:
                send_mail(email_subject, email_message, from_email, recipient_list)
                status = 'success'
            except Exception as e:
                status = 'error'
                print(f"Error sending email: {e}")

    return render(request, 'contactus/contactus.html', {'form': form, 'status': status})

# اگه کل فیلد های تعریف شده در فایل اچ تی ام ال نباشه باعص میشه ایمیل کار نکنه پس هر متغیری که اینجا میگیری تو صفحه اچ تی ام ال بزار 

def Aboutus(request):
    return render(request,'aboutus/aboutus.html')




def product_detail(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)  # گرفتن محصول بر اساس شناسه
    return render(request, 'product_detail/product_detail.html', {'product': product})





def Login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')      # دریافت شماره تلفن از فرم
        password = request.POST.get('password')  # دریافت رمز عبور از فرم

        # استفاده از authenticate برای اعتبارسنجی کاربر
        user = authenticate(request, phone=phone, password=password)
        
        if user is not None:
            # اگر کاربر معتبر بود، وارد سیستم می‌شویم
            login(request, user)
            return redirect("home")
        else:
            # در صورت عدم تطابق شماره تلفن یا رمز عبور
            messages.error(request, 'شماره تلفن یا رمز عبور اشتباه است.')
            return redirect('login')

    return render(request, 'login/login.html')




def Logout(request):
    logout(request)
    return redirect('home')




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
            user.password = make_password(password)  # استفاده از make_password برای هش کردن رمز عبور
            user.save()

            # بارگذاری مجدد داده‌های کاربر از پایگاه داده
            user.refresh_from_db()  # این خط اطمینان می‌دهد که اطلاعات سشن به‌روز باشد

            # وارد کردن کاربر به سیستم
            login(request, user)  # وارد کردن کاربر پس از ثبت‌نام

            # هدایت به صفحه خانه بعد از ورود موفق
            return redirect("home")  # به صفحه خانه هدایت می‌شود
        else:
            # در صورت وجود خطا در فرم
            return render(request, 'register/register.html', {'form': form})

    else:
        # در صورت درخواست GET
        form = RegisterForm()
        return render(request, 'register/register.html', {'form': form})

from django.shortcuts import redirect
from django.urls import reverse

def Add_to_basket(request, pk):
    print(f"Received pk: {pk}")  # بررسی مقدار pk
    basket = request.session.get('basket', {})  # سبد خرید از session

    try:
        product = ProductModel.objects.get(id=pk)

        if str(pk) in basket:
            basket[str(pk)] += 1  # اگر محصول قبلاً موجود است، تعداد آن را افزایش می‌دهیم
        else:
            basket[str(pk)] = 1  # اگر محصول جدید است، آن را به سبد اضافه می‌کنیم

        request.session['basket'] = basket  # ذخیره مجدد سبد خرید در session
        return redirect(reverse('product_detail', kwargs={'pk': pk}))

    except ProductModel.DoesNotExist:
        return redirect('product_list')





def view_basket(request):
    basket = request.session.get('basket', {})  # دریافت سبد خرید از session
    basket_items = []
    total_price = 0

    for product_id, quantity in basket.items():
        try:
            product = ProductModel.objects.get(id=product_id)
            total_price += product.price * quantity  # محاسبه قیمت کل
            basket_items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
        except ProductModel.DoesNotExist:
            continue

    return render(request, 'basket/basket.html', {'basket_items': basket_items, 'total_price': total_price})



@csrf_exempt
def remove_from_basket(request, pk):
    if request.method == 'POST':
        basket = request.session.get('basket', {})

        if str(pk) in basket:
            item_total_price = basket[str(pk)] * ProductModel.objects.get(id=pk).price
            del basket[str(pk)]  # حذف محصول از سبد خرید
            request.session['basket'] = basket  # ذخیره مجدد سبد خرید

            total_price = sum(ProductModel.objects.get(id=product_id).price * quantity for product_id, quantity in basket.items())

            return JsonResponse({
                'status': 'success',
                'item_total_price': item_total_price,
                'total_price': total_price,
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})



def Checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        return redirect('basket')  # اگر سبد خالی بود به صفحه سبد خرید برگرد

    # نمایش صفحه چک‌اوت با اطلاعات سبد خرید
    basket_items = []
    total_price = 0

    for product_id, quantity in basket.items():
        product = ProductModel.objects.get(id=product_id)
        basket_items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
        total_price += product.price * quantity

    return render(request, 'checkout/checkout.html', {'basket_items': basket_items, 'total_price': total_price})



def Payment_success(request):
    return render(request,'payment_success/payment_success.html')


@login_required
def profile(request):
    return render(request, 'profile/profile.html', {'user': request.user})



@login_required
def orders(request):
    try:
        basket = request.user.basket  # سبد خرید کاربر را بگیر
        items = basket.items.all()  # تمامی آیتم‌های سبد خرید را بگیر
    except Basket.DoesNotExist:
        basket = None
        items = []

    return render(request, 'orders/orders.html', {'basket': basket, 'items': items})

