from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string


def index(request):
    return render(request, 'women/index.html')


def about(request):
    return render(request, 'women/about.html')


def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")


def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('sport',))
        return HttpResponsePermanentRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>year: {year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена (на боевом сервере!)</h1>")
