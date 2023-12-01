from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from women.forms import RegisterUserForm, ContactForm
from .utils import DataMixin
from django.core.paginator import Paginator
from women.forms import AddPostForm, LoginUserForm
from .models import Category, Women
from .utils import *


class WomenHome(DataMixin, ListView):
    """Класс для получения главной страницы сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """

    template_name = "women/index.html"
    context_object_name = "posts"
    cat_selected = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для главной страницы сайта"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Главная страница")

    def get_queryset(self):
        """Получение объектов для постов"""
        return Women.objects.filter(is_published=True).select_related("cat")


# def index(request):
#     posts = Women.objects.filter(is_published=True)
#     # posts = Women.objects.all()
#     context = {
#         "posts": posts,
#         "menu": menu,
#         "title": "Главная страница",
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=context)


# @login_required(login_url=reverse_lazy("users:login"))
def about(request):
    """О сайте"""
    contact_list = Women.published.all()
    # paginator = Paginator(contact_list, 3)  # Show 3 contacts per page.
    page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number) 'page_obj': page_obj,
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Класс для добавления статьи
    Args:
        LoginRequiredMixin (class): _description_
        DataMixin (class): _description_
        CreateView (class): _description_
    """

    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = 'Добавление статьи'
    success_url = reverse_lazy("home")
    # login_url = reverse_lazy("home")
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для добавления статьи"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Добавление статьи")

    def form_valid(self, form):
        """Обработка формы добавления статьи"""
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    # extra_context = {
    #     "menu": menu,
    #     "title": "Редактирование статьи",
    # }


class ContactFormView(DataMixin, FormView):
    """Класс для представления формы контактов
    Args:
        DataMixin (class): _description_
        FormView (class): Стандартный базовый класс для форм,
        не привязанных к моделям, не работает с БД
    """

    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для шаблона, формы контактов"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Обратная связь")

    def form_valid(self, form):
        """
        Обработка формы контактов, вызывается если пользователь
        корректно заполнил все поля контактной формы
        """
        print(form.cleaned_data)
        return redirect("home")


def pageNotFound(request, exception):
    """Получение сообщения страница не найдена"""
    return HttpResponseNotFound("<h1>Страница не найдена (Боевой сервер!)</h1>")


class ShowPost(DataMixin, DetailView):
    """Класс для представления статьи
    Args:
        DataMixin (class): _description_
        DetailView (class): _description_
    """

    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"  # pk_url_kwarg = 'post_pk'
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для представления статьи"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    """Класс для получения списка категорий сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """

    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        """Получение объектов для списка категорий"""
        return Women.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, **kwargs):
        """Получение контекста для списка категорий"""
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug=self.kwargs["cat_slug"])
        return self.get_mixin_context(
            context, title="Категория - " + cat.name, cat_selected=cat.pk
        )


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

#     def form_valid(self, form):
#         """
#         Обработка формы регистрации пользователя, вызывается если
#         пользователь корректно заполнил все поля контактной формы
#         """
#         user = form.save()
#         login(self.request, user)
#         return redirect("home")


class LoginUser(DataMixin, LoginView):
    """Класс для авторизации пользователя
    Args:
        DataMixin (class): _description_
        LoginView (class): _description_
    """

    form_class = LoginUserForm
    template_name = "women/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для авторизации пользователя"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Авторизация")

    def get_success_url(self):
        """Получение страницы после авторизации пользователя"""
        return reverse_lazy("home")


def logout_user(request):
    """Получение перенаправления после авторизации пользователя"""
    logout(request)
    return redirect("login")


class TagPostList(DataMixin, ListView):
    """Класс получение списка постов по тегу
    Args:
        DataMixin (class): _description_
        LoginView (class): _description_
    """

    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")


def confidential(request):
    """О политике конфиденциальности"""
    return render(
        request, "women/confidential.html", {"title": "О сайте", "menu": menu}
    )


def terms(request):
    """О пользовательском соглашении"""
    return render(request, "women/terms.html", {"title": "О сайте", "menu": menu})
