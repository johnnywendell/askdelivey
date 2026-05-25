
from django.urls import path
from . import views as v


app_name = 'core'
urlpatterns = [
    path('', v.IndexView.as_view(), name='index'),
    path('login/', v.LoginView.as_view(), name='login'),
    path('logout/', v.LogoutView.as_view(), name='logout'),
    path(r'criarcliente/',
        v.ClienteCreateView.as_view(), name='criarcliente'),
    path(r'editarcliente/<int:pk>/',
        v.ClienteUpdateView.as_view(), name='usuario_update'),
    path(r'detailcliente/<int:pk>/',
        v.ClienteDetailView.as_view(), name='usuario_detail'),
    path('usuarios/', v.UsuarioListView.as_view(), name='usuario_list'),

]

