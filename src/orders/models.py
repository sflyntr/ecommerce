from django.db import models
from django.db.models.signals import pre_save, post_save

from ecommerce.utils import unique_order_id_generator

from carts.models import Cart
from billing.models import BillingProfile


# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refuned', 'Refuned'),
)

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=20, blank=True)
    # billing_profile =?
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    # 호출된 order객체의 cart를 가져와서 cart의 정보중에 total을 가져온뒤 거기에 shipping_total을 더해 전체 total을 구해서 update한다.
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        import math
        new_total = math.fsum([cart_total, shipping_total])
        formatted_new_total = format(new_total, '.2f')
        # new_total = cart_total + shipping_total
        # self.total = new_total
        self.total = formatted_new_total
        self.save()
        return new_total

# signal 처리되면 호출할 함수 정의.(order를 저장하기 전에 주문id를 만든다.)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    print("this def runs when order is created at first befor save")
    if not instance.order_id:
        print("this def runs when order is created at first befor save - run!!!")
        instance.order_id = unique_order_id_generator(instance)

# order에 대해 save하기 전에는 자동으로 signal 처리됨.
pre_save.connect(pre_save_create_order_id, sender=Order)


# cart가 저장된 후에 signal에 의해 호출될 함수 정의
# post_save든 pre_save든 save의 종류는 update와 create가 있다. created가 그 의미이다.
# update인 경우에만 수행되도록 if not created가 들어감.
# cart가 update되면, 그 cart_id와 연관있는 order를 찾아서 update_total을 호출한다.
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    print("this def runs when order is updated everytime")
    if not created:
        print("this def runs when order is updated everytime - run!!!")
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

# Cart가 save된후에 singal처리된다.
post_save.connect(post_save_cart_total, sender=Cart)

# order가 저장되면 다시 이것을 호출하는데 신규생성일때만 호출한다.
# 즉 update될땐느 위에 정의했고, 새로만들때는 기존cart에 있던 정보로 초기화 해야 하는데 그런 역할을 한다.
# 참고로 2번 호출된다. 즉 사용자가 화면에서 저장을 눌를때 호출되고,
# signal에 의해 update_total()이 호출되어 save가 되면 또 다시 한번 호출된다.
# 하지만 마지막에는 저장할게 없으니 더이상 수행되지 않는다.
def post_save_order(sender, instance, created, *args, **kwargs):
    print("this def runs after order is created at first")
    if created:
        print("this def runs after order is created at first - run!!!")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)