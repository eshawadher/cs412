from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(r'', views.quote_page, name='quote_page'),
    path(r'about', views.about, name='about_page'),
    path(r'all', views.all, name='show_all_page')
] 
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
