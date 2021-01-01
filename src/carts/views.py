from django.shortcuts import render, redirect

from .models import Cart
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
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
    billing_address_form = AddressForm()
    guest_email_id = request.session.get('guest_email_id')
    print("guest_email_id:{}".format(guest_email_id))

    # checkout.html에선 billing_profile 존재여부로 분기처리한다.
    # 즉, billing_profile이 존재한다는 뜻은, cart가 있고, cart에 products가 1개이상 있으며, 그 cart로 order가 생성과고, user가 인증되었다는 뜻이다.
    if user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass

    # 위에서 billing profile을 만들었다. 그리고 order객체를 생성하는데 billing_profile과 같이 만든다.
    # 즉, 없겠지만, 해당 cart_obj로 order객체를 검색해서 있으면 active=False로 설정한다.
    # 없다면 해당 cart_obj와 billing_profile로 order객체를 하나 만든다.
    # 아래는 하지만 로직에 문제가 있다. 체크아웃에서 리프레시를 하면 order가 계속 바뀐다.
    # if billing_profile is not None:
    #     order_qs = Order.objects.filter(cart=cart_obj, active=True)
    #     if order_qs.exists():
    #         # update 이거 save대신 쓴건데... 좋은지 모르겠다.
    #         print("Waring1 update -{}".format(order_qs.first()))
    #         order_qs.update(active=False)
    #         print("Waring2 update -{}".format(order_qs.first()))
    #         # 아래와 같이 찍힌다. 이것은. order_qs에 있다가, active를 False로 바꾸니 order_qs first가 None으로 나온것이다.
    #         # 즉, order_qs는 active=True 조건이 붙어 있는 쿼리셋이다. 이게 바뀌면 당연히 데이터가 안나온다.
    #         # Waring1 - rimzvk48hu
    #         # Waring2 - None
    #         # 아래 save와 같은 결과이다. save는 개별instance에 저장하는 것이고,
    #         # update는 한번에 하는 것인데, order_qs 쿼리셋의 결과는 동일하다.
    #
    #         # print("Waring1 save -{}".format(order_qs.first()))
    #         # order_qs.active=False
    #         # for instance in order_qs:
    #         #     instance.active=False
    #         #     instance.save()
    #         # print("Waring2 save -{}".format(order_qs.first()))
    #
    #     else:
    #         order_obj = Order.objects.create(
    #             billing_profile = billing_profile,
    #             cart=cart_obj
    #         )

    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "billing_address_form": billing_address_form,
    }

    return render(request, "carts/checkout.html", context)
