from .models import *
from django.db.models import Count
from django.core.cache import cache


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
]


class DataMixin:
    title_page = None
    cat_selected = None
    extra_context = {}
    paginate_by = 5

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

        if self.cat_selected is not None:
            self.extra_context["cat_selected"] = self.cat_selected

        # if "menu" not in self.extra_context:
        #     self.extra_context["menu"] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context["title"] = self.title_page

        # context["menu"] = menu
        context["cat_selected"] = None
        context.update(kwargs)
        return context


# class DataMixin:
#     """Класс добавления функционала для модели данных."""

#     paginate_by = 3

#     def get_mixin_context(self, **kwargs):
#         """Получение контекста пользователя."""
#         context = kwargs
#         cats = Category.objects.annotate(Count("id"))


# user_menu = menu.copy()
# if not self.request.user.is_authenticated:
#     user_menu.pop(1)

# context["menu"] = user_menu

# context["cats"] = cats
# if "cat_selected" not in context:
#     context["cat_selected"] = 0
# return context
