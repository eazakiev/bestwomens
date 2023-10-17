from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """ Описывает пользовательский менеджер записей для моделей.
    Args:
        models (class): _description_
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    """Класс, описывающий модель Women.
    Args:
        models (class): _description_
    """
    class Status(models.IntegerChoices):
        """Формирует, автоматизирует процесс создания перечислений (0/1)
        определяет осмысленные имена, в которых они будут созданы.
        Args:
            models (int): _description_
        """
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(
        auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Публикация')
    cat = models.ForeignKey(  # внешний ключ, хранит идентификатор категории, с которым связана запись
        'Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField(
        'TagPost', blank=True, related_name='tags', verbose_name='Теги')
    husband = models.OneToOneField(
        'Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman', verbose_name='Муж')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        """Возвращает строковое представление модели Women."""
        return self.title

    def get_absolute_url(self):
        """Возвращает путь до модели Women."""
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        """Метаданные модели Women, устанавливает название модели."""
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']
        indexes = [
            models.Index(fields=['time_create'])
        ]


class Category(models.Model):
    """Класс, описывающий модель Category.
    Args:
        models (class): _description_
    """
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        """Возвращает строковое представление модели Category."""
        return self.name

    def get_absolute_url(self):
        """ Формирует адрес для каждой конкретной записи (slug/id). """
        return reverse("category", kwargs={"cat_slug": self.slug})

    class Meta:
        """Метаданные модели Category, устанавливает название модели."""
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class TagPost(models.Model):
    """Класс, описывающий модель TagPost. Реализация функционала
    тегирования записей.
    Args:
        models (class): _description_
    """
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Тег')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """Возвращает строковое представление модели TagPost."""
        return self.tag

    def get_absolute_url(self):
        """Формирует адрес для каждой конкретной записи тега"""
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Husband(models.Model):
    """Класс, описывающий модель Husbands.
    Args:
        models (class): _description_
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        """Возвращает строковое представление модели Husbands."""
        return self.name
