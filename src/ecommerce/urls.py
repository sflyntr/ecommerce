"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin

# Good Tip for intellij
# 만약에 from products.views 에서 오류표시가 보인다면, src 디렉토리로 가서 mark as source root 체크하면 오류표기 없어진다.
# from products.views import (
                            # ProductListView,
                            # product_list_view,
                            # ProductDetailView,
                            # product_detail_view,
                            # ProductFeaturedDetailView,
                            # ProductFeaturedListView,
                            # ProductDetailSlugView,
                           # )

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^about/', about_page, name='about'),
    url(r'^contact/', contact_page, name='contact'),
    url(r'^login/', login_page, name='login'),
    url(r'^register/', register_page, name='register'),
    url(r'^products/', include("products.urls", namespace='products')),
    # url(r'^featured/$', ProductFeaturedListView.as_view()),
    # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    # url(r'^products/$', ProductListView.as_view()),
    # url(r'^products-fbv/$', product_list_view),
    # # url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    # url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    # url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    # 기존 urlpatterns 에 append해서 추가한다는것이다.
    # settings.STATIC_URL은 /static/ 이다. 즉 r'^static/' 정도 되겠다. 그리고 STATIC_ROOT 는 프로젝트 외부에 존재하는 경로이다.
    # 따라서 static url이 들어오면 그 위치를 참조한다는 뜻이다.
    # production에서는 절대 이렇게 하면 안된다. 이것때문에 DEBUG를 해두었고, settings.py 에 DEBUG는 현재 True로 되어 있다.
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
