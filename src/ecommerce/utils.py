import random
import string

from django.utils.text import slugify

def unique_order_id_generator(instance):
    new_order_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    # string.ascii_lowercase = "abcd....xyz", string.digits = '01234..89'
    return ''.join(random.choice(chars) for _ in range(size))