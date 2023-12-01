from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from women.forms import RegisterUserForm
from django.contrib.auth import logout
from django.urls import reverse_lazy

from users.forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    # def get_success_url(self):
    #     """Получение страницы после авторизации пользователя"""
    #     return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "users/register_done.html")
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html", {"form": form})


# class RegisterUser(DataMixin, CreateView):
#     """Класс для регистрации пользователя
#     Args:
#         DataMixin (class): _description_
#         CreateView (class): _description_
#     """

#     form_class = RegisterUserForm
#     template_name = "women/register.html"
#     success_url = reverse_lazy("login")

#     def get_context_data(self, *, object_list=None, **kwargs):
#         """Получение контекста для регистрации пользователя"""
#         context = super().get_context_data(**kwargs)
#         return self.get_mixin_context(context, title="Регистрация")

# def form_valid(self, form):
#     """
#     Обработка формы регистрации пользователя, вызывается если
#     пользователь корректно заполнил все поля контактной формы
#     """
#     user = form.save()
#     login(self.request, user)
#     return redirect("home")
