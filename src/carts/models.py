from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL

# Create your models here.
class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id

        # return cart_obj, True
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        print(user_obj)
        # login안되어 있을때 user는 request.user 정보에 AnonymousUser 들어가 있다.
        print(user)
        if user is not None:
            # login 안되어 있을때 AnonymousUser 이므로 여기를 탄다.
            print("here?")
            if user.is_authenticated():
                # 하지만 여기는 안탄다.
                print("or here?")
                user_obj = user
        # 즉 로긴 안되어 있을때는, user_obj = None, user = AnonymousUser 이다.
        # 따라서, self.model.objects.create(user=user) 이렇게 호출하면 AnonymousUser 즉, User Object가 아니라서 오류난다.
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)



def m2m_save_cart_receiver(sender, instance, action, *args, **kwargs):
    print(action)
    if action in ('post_add', 'post_remove', 'post_clear'):
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        print(total)
        instance.subtotal = total
        instance.save()

m2m_changed.connect(m2m_save_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10 # No Error
        # instance.total = instance.subtotal * 1.08 # 8% tax  --> Error
        instance.total = float(instance.subtotal) * float(1.08)
        # from decimal import Decimal  # --> OK. Decimal 이지만 instance의 field가 decimal_places=2로 되어 있어 문제 없음.
        # instance.total = Decimal(instance.subtotal) * Decimal(1.08)
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)