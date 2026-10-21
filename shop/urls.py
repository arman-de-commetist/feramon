from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import SITEMAPS

urlpatterns = [
    path('', views.index, name='index'),
    # shop
    path('aromaty/', views.catalog, name='catalog'),
    path('aromat/<slug:slug>/', views.product_detail, name='product'),
    path('obemy/', views.compare, name='compare'),
    path('test/', views.quiz, name='quiz'),
    path('zakaz/', views.order, name='order'),
    path('korzina/', views.cart, name='cart'),
    path('korzina/dobavit/', views.cart_add, name='cart_add'),
    path('oformlenie/', views.checkout, name='checkout'),
    path('spasibo/<uuid:token>/', views.thanks, name='thanks'),
    # gifts & offers
    path('akcii/', views.promotions, name='promotions'),
    path('dyson-airwrap/', views.dyson, name='dyson'),
    path('podarki/', views.gifts, name='gifts'),
    path('podarki/<slug:slug>/', views.gift_perfume, name='gift_perfume'),
    # community
    path('otzyvy/', views.reviews, name='reviews'),
    path('galereya/', views.gallery, name='gallery'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.article, name='article'),
    # info
    path('o-brende/', views.about, name='about'),
    path('feromony/', views.page('shop/pheromones.html'), name='pheromones'),
    path('sertifikaty/', views.page('shop/certificates.html'), name='certificates'),
    path('dostavka-i-oplata/', views.page('shop/delivery.html'), name='delivery'),
    path('oplata/', views.page('shop/payment.html'), name='payment'),
    path('garantiya-i-vozvrat/', views.page('shop/returns.html'), name='returns'),
    path('voprosy/', views.page('shop/faq.html'), name='faq'),
    path('kontakty/', views.page('shop/contacts.html'), name='contacts'),
    path('politika-konfidencialnosti/', views.page('shop/privacy.html'), name='privacy'),
    path('oferta/', views.page('shop/offer.html'), name='offer'),
    path('napisat/', views.write_to_manager, name='write'),
    path('lang/<str:code>/', views.set_language, name='set_lang'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
]
