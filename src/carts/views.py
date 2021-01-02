from django.shortcuts import render, redirect

from .models import Cart
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product


def cart_create(user=None):
    cart_obj = Cart.objects.create(user=user)
    print('New Cart created')
    return cart_obj


def cart_home(request):
    # # del request.session['cart_id']
    # cart_id = request.session.get("cart_id", None)
    #
    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     print('cart id exists')
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated() and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     cart_obj = Cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    # products = cart_obj.products.all()
    # print(cart_obj.id)

    # total = 0
    # for x in products:
    #     total += x.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            print("try to find product")
            product_obj = Product.objects.get(id=product_id)

        except Product.DoesNotExists:
            print("Show message to user, product is gone?")
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            print(product_obj)
            cart_obj.products.remove(product_obj)
        else:
            print("no data")
            cart_obj.products.add(product_obj)

        request.session['cart_items'] = cart_obj.products.count()

    # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")




def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    # cart로 부터 먼저 order객체를 만들지 말자.
    # else:
    #     # billing_profile없이 order부터 만든다.
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)

    user = request.user
    print("어나니머스?:{}".format(user))
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    guest_email_id = request.session.get('guest_email_id')
    print("guest_email_id:{}".format(guest_email_id))
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "some check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            # 이것을 넣지 않으니 checkout 끝나도 계속 남아있다.
            if request.session.get('guest_email_id', None):
                del request.session['guest_email_id']
        return redirect("cart:success")


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }

    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
