from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from product.models import Category, Product
from rent.models import RentForm, Rent, RentProduct


def index(request):

    return HttpResponse("rent App")


@login_required(login_url='/login')  # Check login
def rentproduct(request, id):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    current_user = request.user


    if request.method == 'POST':  # if there is a post
        form = RentForm(request.POST)
        if form.is_valid():
            data = Rent()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.start_date = form.cleaned_data['start_date']
            data.end_date = form.cleaned_data['end_date']
            data.user_id = current_user.id
            data.ip = request.META.get('REMOTE_ADDR')
            rentcode = get_random_string(5).upper()
            data.code = rentcode
            data.save()
            total=(data.end_date-data.start_date)*product.price

            rentproduct = RentProduct()
            rentproduct.order = data
            rentproduct.price = total
            rentproduct.user = current_user
            rentproduct.product = product
            rentproduct.save()

            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Rent_Completed.html', {'rentcode': rentcode, 'category': category})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/rent/rentproduct/" + str(id))

    form = RentForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'form': form,
               'profile': profile,
               'product': product,

               }
    return render(request, 'Rent_Form.html', context)
