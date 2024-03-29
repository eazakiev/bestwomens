from django import template
from women.models import Category, TagPost
import women.views as views
from django.db.models import Count
from women.utils import menu

register = template.Library()


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected=0):
    """Показать список категорий."""
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("women/list_tags.html")
def show_all_tags():
    """Показать список тегов."""
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}


@register.simple_tag(name="getcats")
def get_categories(filter=None):
    """Получение списка категорий."""
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.simple_tag
def get_menu():
    """Получение меню."""
    return menu


# @register.inclusion_tag("women/list_categories.html")
# def show_categories(sort=None, cat_selected=0):
#     """Показать список категорий."""
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)

#     return {"cats": cats, "cat_selected": cat_selected}
