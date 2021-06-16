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
    path('<int:year>/<int:month>/root/', MonthRootView.as_view(), name='month-root'),
    path('<int:year>/<int:month>/root/<int:category_id>/', MonthRootView.as_view(), name='month-root-detail'),
    path('<int:year>/<int:month>/detail/', MonthDetailView.as_view(), name='month-detail'),
    path('<int:year>/<int:month>/detail/<int:category_id>/', MonthDetailView.as_view(), name='month-detail-category'),
]
