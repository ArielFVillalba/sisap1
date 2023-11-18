
from django.urls import path
from inicio import views

urlpatterns = [
   # path('login/', views.login, name="login"),
    path('logoini/', views.logoini, name="logoini"),
    path('menuini/', views.menuini, name="menuini"),
    path('menu/', views.menu, name="menu"),
    path('buscar_usuario/', views.buscar_usuario, name="buscar_usuario"),
    path('base/', views.base, name="base"),
    path('sisa/', views.sisa, name="sisa"),
    path('login2/', views.login2, name="login2"),
    path('login/', views.loginc, name='login'),
    path('pagcofirmacion/', views.pagcofirmacion, name='pagcofirmacion'),
    path('accounts/login/', views.error, name='error'),


]
handler404 = views.error_404
