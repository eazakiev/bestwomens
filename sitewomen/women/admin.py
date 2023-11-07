from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Women, Category

# from django.template.defaultfilters import slugify


class MarriedFilter(admin.SimpleListFilter):
    """Админ класс MarriedFilter, кастомный фильтр для админки
    Args:
        admin (class): _description_
    """

    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        """Возвращает список, из возможных значений параметра статус"""
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request, queryset):
        """Возвращает набор записей, для отбора фильтра"""
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    """Админ класс WomenAdmin для модели Women.
    Args:
        admin (class): _description_
    """

    list_display = (
        "title",
        "post_photo",
        "time_create",
        "is_published",
        "cat",
    )  # 'get_html_photo'
    list_display_links = ("title",)
    ordering = ["time_create", "title"]
    search_fields = ("title", "content", "cat__name")
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    list_filter = (MarriedFilter, "cat__name", "is_published", "time_create")
    # 'time_create', 'time_update' 'photo','get_html_photo'
    fields = [
        "title",
        "slug",
        "content",
        "photo",
        "post_photo",
        "cat",
        "is_published",
        "husband",
        "tags",
    ]
    readonly_fields = ("time_create", "time_update", "post_photo")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    # filter_vertical = ['tags']
    save_on_top = True

    @admin.display(description="Изображение", ordering="content")
    def post_photo(self, women: Women):
        """Возвращает HTML-код фотографии."""
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(
            request, f"{count} записей снято с публикации!", messages.WARNING
        )

    # def get_html_photo(self, object):
    #     """Возвращает HTML-код фотографии."""
    #     if object.photo:
    #         return mark_safe(f"<img src='{object.photo.url}' width=50>")

    # get_html_photo.short_description = "Миниатюра"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ класс CategoryAdmin для модели Category.
    Args:
        admin (class): _description_
    """

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# admin.site.register(Women, WomenAdmin)
# admin.site.register(Category, CategoryAdmin)

admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Админка сайта о женщинах"
admin.site.index_title = "Известные женщины мира"
