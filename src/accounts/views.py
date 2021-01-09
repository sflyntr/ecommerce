from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from .signals import user_logged_in


# Create your views here.
def guest_login_view(request):

    print("hellow....guetsview")
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post_ = request.POST.get('next')
    redirect_path = next_ or next_post_ or None
    print("guest form good?")

    if form.is_valid():
        print("before email check")
        email = form.cleaned_data.get("email")
        print(email)
        print("after email check")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            print("it is safe")
            return redirect(redirect_path)
        else:
            print(1)
            print(redirect_path)
            print(2)
            print(request.get_host())
            print("it is not safe")
            return redirect("/register/")
    print("i dont know its safe or not")
    return redirect("/register/")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    # print('User Logged In')
    # print(request.user.is_authenticated())

    next_ = request.GET.get('next')
    next_post_ = request.POST.get('next')
    redirect_path = next_ or next_post_ or None

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated())
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)

            # 사이트 방문하고 logout 상태의 session에서 guest로 checkout을 하면,
            # guest_email_id가 session에 남아 있다.
            # 이 상태에서 login을 하면 이 session에 로그인정보를 담는데, guest_email_id가 남아 있으므로,
            # 삭제한다. 참고로 session은 set_expiry설정 또는 logout시 없어지고 새로 만들어 진다.

            try:
                del request.session['guest_email_id']
            except:
                pass

            # Redirect to a success page
            # context['form'] = LoginForm()
            print(request.get_host())
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Login Error")
    return render(request, "accounts/login.html", context)


User = get_user_model()


class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = "/"

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post_ = request.POST.get('next')
        redirect_path = next_ or next_post_ or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = '/login/'


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }

    if form.is_valid():
        # username = form.cleaned_data.get("username")
        # email = form.cleaned_data.get("email")
        # password = form.cleaned_data.get("password")
        # new_user = User.objects.create_user(username, email, password)
        # print(new_user)
        form.save()

    return render(request, "accounts/register.html", context)


def guest_register_view(request):
    pass