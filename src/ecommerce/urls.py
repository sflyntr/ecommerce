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

from django.conf.urls import url
from django.contrib import admin

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
    url(r'^$', home_page),
    url(r'^about/', about_page),
    url(r'^contact/', contact_page),
    url(r'^login/', login_page),
    url(r'^register/', register_page),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    # 기존 urlpatterns 에 append해서 추가한다는것이다.
    # settings.STATIC_URL은 /static/ 이다. 즉 r'^static/' 정도 되겠다. 그리고 STATIC_ROOT 는 프로젝트 외부에 존재하는 경로이다.
    # 따라서 static url이 들어오면 그 위치를 참조한다는 뜻이다.
    # production에서는 절대 이렇게 하면 안된다. 이것때문에 DEBUG를 해두었고, settings.py 에 DEBUG는 현재 True로 되어 있다.
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
