from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Category, Women


menu = [{'title': "О сайте", 'url_name': "about"},
        {'title': "Добавить статью", 'url_name': "add_page"},
        {'title': "Обратная связь", 'url_name': "contact"},
        {'title': "Войти", 'url_name': "login"},
        ]


data_db = [
    {'id': 1, 'title': 'Анджелина Джоли',
        'content': '<h1>англ. Angelina Jolie</h1>, при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН. Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': '(англ. Margot Elise Robbie; род. 2 июля 1990, Дэлби, Квинсленд, Австралия) — австралийская актриса и кинопродюсер. Двукратная номинантка на премию «Оскар», пятикратная номинантка на премию BAFTA, пятикратная номинантка на премию Гильдии киноактёров США, трёхкратная номинантка на премию «Золотой глобус» и семикратная номинантка на премию Critics Choice Movie Award».', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': '(англ. Julia Fiona Roberts; род. 28 октября 1967, Смирна, Джорджия)— американская актриса кино и телевидения, продюсер. Первый прорыв в карьере Робертс произошёл после выхода фильмов «Мистическая пицца» и «Стальные магнолии», за последний из которых она была удостоена «Золотого глобуса» и первой номинации на премию «Оскар».', 'is_published': True},
]


def index(request):
    posts = Women.published.all()

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


def about(request):
    """О сайте"""
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'women/about.html', context=data)


def addpage(request):
    return HttpResponse(f"Добавление статьи")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    """Получение сообщения страница не найдена"""
    return HttpResponseNotFound("<h1>Страница не найдена (на боевом сервере!)</h1>")
