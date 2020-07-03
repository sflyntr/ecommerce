from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# 이렇게 해도 된다. generic에 init.py에 shortcut이 있으므로,
# from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product


# Create your views here.
class ProductListView(ListView):
    queryset = Product.objects.all()
    # 참고로 Class based view 에서 default view 이름은 product(모델명소문자)_list.html이다.
    # 따라서 template_name = "products/list.html" 로 하고 아무것도 안만들면,
    # product_list.html, list.html 2개의 template이 없다는 에러가 나온다. (Tip!!)
    # 실제 ListView 소스를 보면 template을 못찾는 경우, get_template_names 를 호출해서 default template을 찾는다.
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailView(DetailView):
    # get_object_or_404 안해도 DetailView나온다.즉, 어떤모델의 queryset을 사용하는지만 지정해도 된다.
    # 그리고 queryset 이름도 지정된거 써야한다. queryset = 말고 qs = 이런식으로 하면 안된다.
    # 즉, queryset이라는 변수에 반드시 model queryset을 지정해줘야 parent에서 그걸 참조한 함수들을 사용할 수 있다.
    queryset = Product.objects.all()
    # 참고로 Class based view 에서 default view 이름은 product(모델명소문자)_list.html이다.
    # 따라서 template_name = "products/list.html" 로 하고 아무것도 안만들면,
    # product_list.html, list.html 2개의 template이 없다는 에러가 나온다. (Tip!!)
    # 실제 ListView 소스를 보면 template을 못찾는 경우, get_template_names 를 호출해서 default template을 찾는다.
    template_name = "products/detail.html"
    hello_words = "Hello, World welcome to django world."

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk)

    # 아래도 동일한 기능을 수행한다.
    # instance = get_object_or_404(Product, pk=pk)

    # 이것도 동일한 기능을 수행한다.
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExists:
    #     print('no product here')
    # except:
    #     print("huh?")

    qs = Product.objects.filter(id=pk)

    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist")


    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)

