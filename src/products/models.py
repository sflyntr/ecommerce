from django.db import models


# Create your models here.
class Product(models.Model): # CamelCase로 작성하며, 단수로 처리하는것이 Convention임. 즉 Products 이렇게 하지 않는다.
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.00) # 또는 null=True로 해도 됨.
