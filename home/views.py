from unicodedata import category

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category, Images


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:1]
    category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts': randomproducts
               }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)

    context = {'setting': setting, 'page': 'aboutus', 'category': category}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category}
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderildi. Teşekkür ederiz")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contact.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    category_data = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'category_data': category_data
               }
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images= Images.objects.filter(product_id=id)
    context = {
        'product': product,
        'category': category,
        'images': images
    }
    return render(request, 'product_detail.html', context)
