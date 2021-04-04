from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from src.finances.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('<int:year>/<int:month>/', MonthView.as_view(), name='month'),
]
