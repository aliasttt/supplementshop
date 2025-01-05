from django.shortcuts import render , HttpResponse ,redirect
from .models import *
from .serializers import Productserializer
from rest_framework import viewsets
from rest_framework.response import Response
from .forms import *
from django.core.mail import send_mail


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
                return redirect('vpsapp:contactus')  # ریدایرکت به صفحه موفقیت
            except Exception as e:
                status = 500  # در صورت بروز خطا در ارسال ایمیل
                print("Error sending email:", e)

    return render(request, 'contactus/contactus.html', {'form': form, 'status': status})




def Aboutus(request):
    return render(request,'aboutus/aboutus.html')

def Product_detail(request):
    return render(request,'product_detail/product_detail.html')







