import random
import os

from django.db import models


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


class ProductManager(models.Manager):
    # ModelManager의 get_by_id를 override함.
    # Product.objects.all() 여기서 Product.objects는 ModelManager임.
    # 필요하다면 all() 도 재정의 할수 있음.
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


# Create your models here.
class Product(models.Model): # CamelCase로 작성하며, 단수로 처리하는것이 Convention임. 즉 Products 이렇게 하지 않는다.
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99) # 또는 null=True로 해도 됨.
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    # 요거는 override는 아니고 그냥 extending이라고 얘기하는데..
    # 내 생각엔 변수를 덮어쓴거라 override랑 비슷한거 같다.
    # 따라서 기존에 Product.objects 하면 models.Manager가 나오는데, 이렇게 하면 ProductManager가 나온다.
    # (물론 기존 models.Manager를 상속받은 것이니 기존 기능 다 사용가능하다.)
    objects = ProductManager()

    def __str__(self):  # python3
        return self.title

    def __unicode__(self):  # this is 하위호환성. python2에서는 이렇게 사용해야함.
        return self.title

