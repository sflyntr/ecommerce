from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post_ = request.POST.get('next')
    redirect_path = next_ or next_post_ or None
    print(redirect_path)
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id:" + str(instance.id))
        else:
            print("Error here")
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("cart:checkout")


def checkout_address_reuse_view(request):
    print("action_url:checkout_address_reuse_view")
    if request.user.is_authenticated():
        context = {}
        next_ = request.GET.get('next')
        next_post_ = request.POST.get('next')
        redirect_path = next_ or next_post_ or None
        print(redirect_path)
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                print("shipping_address is not None")
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                    print(address_type + "_address_id")
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout")
