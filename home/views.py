from tkinter import Menu
#from unicodedata import category


from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from home.forms import SignUpForm, SearchForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile, FAQ
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:3]
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
    category = Category.objects.all()

    context = {'setting': setting, 'page': 'aboutus', 'category': category}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}
    return render(request, 'references.html', context)


def contact(request):
    category = Category.objects.all()
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
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
    }

    return render(request, 'product_detail.html', context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # get data from form
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)  # select * from where title like query
            else:
                products = Product.objects.filter(title__icontains=query,
                                                  category_id=catid)  # select * from where title like query

            context = {
                'products': products,
                'category': category,
            }
            return render(request, 'product_search.html', context)
    return HttpResponseRedirect('/')


def product_search_auto(request):
    messages.success(request, "deneme")
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş yapılamadı! Kullanıcı adı ya da şifre yanlış!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Hoş Geldiniz.. Kayıt işleminiz başarılı ile gerçekleşti")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {'category': category,
               'faq': faq,

               }
    return render(request, 'faq.html', context)
