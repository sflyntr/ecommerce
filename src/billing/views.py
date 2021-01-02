from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.http import is_safe_url


# Create your views here.

import stripe

stripe.api_key = 'sk_test_51HputmGYYMq5YiSWSw3vJVfkEkMcmXlolnJ2deRBAcxlAlvPvDG1m6VZcE4hTQjA7senoikZ8L3UEu2FMBVjCkg100gmneW7aT'
STRIPE_PUB_KEY = 'pk_test_51HputmGYYMq5YiSWF1KdXYFZuNIgziD9NS6Vxjx3gK6bAGwXukemgwe7iTH7Bqv7NNC2iZO3HaXE70wkq9XX1JnA00hvSlOlSD'

def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "done"})
    return HttpResponse("error", status_code=401)
