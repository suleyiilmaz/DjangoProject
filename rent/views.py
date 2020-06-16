from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from product.models import Category, Product
from rent.models import RentForm, Rent, RentProduct, ShopCartForm, ShopCart


def index(request):

    return HttpResponse("rent App")


@login_required(login_url='/login')  # Check login
def rentproduct(request, id):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    current_user = request.user
    url=request.META.get('HTTP_REFERER')
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        total = (rs.end_date-rs.start_date).days*rs.price

    if request.method == 'POST':  # if there is a post
        form1 = RentForm(request.POST)
        form2 = ShopCartForm(request.POST)

        if form2.is_valid():
            current_user=request.user
            data=ShopCart()
            data.user_id=current_user.id
            data.product_id=id
            data.total=total
            data.start_date=form2.cleaned_data['start_date']
            data.end_date=form2.cleaned_data['end_date']
            data.save()
            messages.success(request,"Günleriniz başarılı bir şekilde kaydedildi")

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            total = 0
            for rs in shopcart:
                total = (rs.end_date - rs.start_date).days * rs.price

            return render(request, 'Rent_Form.html', {'category': category,
               'form1': form1,
               'form2': form2,
               'profile': profile,
               'product': product,
               'total': total,
               })


        if form1.is_valid():
            data = Rent()
            data.first_name = form1.cleaned_data['first_name']
            data.last_name = form1.cleaned_data['last_name']
            data.address = form1.cleaned_data['address']
            data.city = form1.cleaned_data['city']
            data.phone = form1.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            rentcode = get_random_string(5).upper()
            data.code = rentcode
            data.save()

            shopcart=ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail=RentProduct()
                detail.rent_id=data.id
                detail.product_id=rs.product_id
                detail.user_id=current_user.id
                detail.start_date=rs.start_date
                detail.end_date=rs.end_date

                product = Product.objects.get(id=rs.product_id)

                detail.price=rs.product.price
                detail.amount=rs.amount.days
                detail.save()



            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0

            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html', {'rentcode': rentcode, 'category': category})

        else:
            messages.warning(request, form1.errors)
            return HttpResponseRedirect("/rent/rentproduct/" + str(id))

    form1 = RentForm()
    form2 = ShopCartForm()
    context = {'category': category,
               'form1': form1,
               'form2': form2,
               'profile': profile,
               'product': product,

               }
    return render(request, 'Rent_Form.html', context)
