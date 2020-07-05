from tags.models import Tag

qs = Tag.objects.all()
print(qs)
black = Tag.objects.last()
black.title
black.slug

black.products.all()

black.products.all().first()

exit()

from products.models import Product

qs = Product.objects.all()
print(qs)
tshirt = qs.first()
tshirt.title
tshirt.description

tshirt.tag
tshirt.tags

tshirt.tag_set

tshirt.tag_set.all()

#
# ecommerce ❯ python manage.py shell
# Python 3.6.1 (v3.6.1:69c0db5050, Mar 21 2017, 01:21:04)
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# (InteractiveConsole)
# >>> from tags.models import Tag
# >>> qs = Tag.objects.all()
# >>> qs
# <QuerySet [<Tag: T shirt>, <Tag: red>, <Tag: black>]>
# >>> print(qs)
# <QuerySet [<Tag: T shirt>, <Tag: red>, <Tag: black>]>
# >>> black = Tag.objects.last()
# >>> black.title
# 'black'
# >>> black.slug
# 'black'
# >>> black.products.all()
# <ProductQuerySet [<Product: T-shirts>, <Product: Hat>, <Product: supercomputer>, <Product: T-shirts>]>
# >>>
# >>> from products.models import Product
# >>> qs = Product.objects.all()
# >>> qs
# <ProductQuerySet [<Product: T-shirts>, <Product: Hat>, <Product: supercomputer>, <Product: T-shirts>, <Product: Lorem ipsum>, <Product: SmartPhone>]>
# >>> tshirt = qs.first()
# >>> tshirt.title
# 'T-shirts'
# >>> tshirt.description
# 'This is awesome T-shirts. buy it :)'
# >>> tshirt.tag
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'Product' object has no attribute 'tag'
# >>> tshirt.tags
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'Product' object has no attribute 'tags'
# >>> tshirt.tag_set
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x106ea8cc0>
# >>> tshirt.tag_set.all()
# <QuerySet [<Tag: T shirt>, <Tag: red>, <Tag: black>]>
# >>>