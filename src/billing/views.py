from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile, Card


import stripe

stripe.api_key = 'sk_test_51HputmGYYMq5YiSWSw3vJVfkEkMcmXlolnJ2deRBAcxlAlvPvDG1m6VZcE4hTQjA7senoikZ8L3UEu2FMBVjCkg100gmneW7aT'
STRIPE_PUB_KEY = 'pk_test_51HputmGYYMq5YiSWF1KdXYFZuNIgziD9NS6Vxjx3gK6bAGwXukemgwe7iTH7Bqv7NNC2iZO3HaXE70wkq9XX1JnA00hvSlOlSD'


def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status=401)
        print(request.POST)
        token = request.POST.get("token")
        print(billing_profile.customer_id)
        print(token)
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id, expand=['sources',])
            # print(dir(customer))
            # card_response = customer.sources.create(source=token)
            # print(card_response)
            new_card_obj = Card.objects.add_new(billing_profile, token)
            return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status=401)

