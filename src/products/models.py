import random
import os

from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse

from ecommerce.utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    print(name)
    print(ext)
    return name, ext


def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1, 393829328239)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        # self는 QuerySet이므로 filter를 바로 self에 쓸수 있다.
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query) |
                   Q(tag__slug__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    # 위에서 만든 CustomQuerySet을 ProductManager에서 사용하게 해야 한다.
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def features(self): # Product.objects.features()
        return self.get_queryset().featured()

    def featured(self): # Product.objects.featured()
        return self.get_queryset().filter(featured=True, active=True)

    # ModelManager의 get_by_id를 override함.
    # Product.objects.all() 여기서 Product.objects는 ModelManager임.
    # 필요하다면 all() 도 재정의 할수 있음.
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)



# Create your models here.
class Product(models.Model): # CamelCase로 작성하며, 단수로 처리하는것이 Convention임. 즉 Products 이렇게 하지 않는다.
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99) # 또는 null=True로 해도 됨.
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # 요거는 override는 아니고 그냥 extending이라고 얘기하는데..
    # 내 생각엔 변수를 덮어쓴거라 override랑 비슷한거 같다.
    # 따라서 기존에 Product.objects 하면 models.Manager가 나오는데, 이렇게 하면 ProductManager가 나온다.
    # (물론 기존 models.Manager를 상속받은 것이니 기존 기능 다 사용가능하다.)
    objects = ProductManager()

    # for reverse. -> html에서 사용될 것임.
    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):  # python3
        return self.title

    def __unicode__(self):  # this is 하위호환성. python2에서는 이렇게 사용해야함.
        return self.title

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = 'abc'
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
