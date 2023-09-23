from django.urls import path, re_path, register_converter
from . import converters
from . import views

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),

    # path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    # path("archive/<year4:year>/", views.archive, name='archive'),
]
