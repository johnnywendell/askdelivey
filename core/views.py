# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash,authenticate
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView
from django.views.generic.edit import UpdateView
from django.utils.encoding import force_str
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import Permission

from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader

from django.db import transaction, DatabaseError
from .forms import UserCreateForm, UsuarioForm, ClienteForm, EnderecoForm, RestauranteForm, EntregadorForm
from askdelivery.settings import DEFAULT_FROM_EMAIL

import operator
from functools import reduce
from .custom_views import CustomView, CustomDetailView
from .models import Usuario, Cliente, Restaurante, Entregador

DEFAULT_PERMISSION_MODELS = []

DEFAULT_PERMISSION_MODELS_STAFF = []
                               
CUSTOM_PERMISSIONS = []


class LoginView(View):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core:index')
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=email,   # porque você salva username = email
            password=password
        )
        if user:
            login(request, user)
            return redirect(self.success_url)
        context = {
            'error': 'Email ou senha inválidos.'
        }
        return render(request, self.template_name, context)

class IndexView(CustomView):

    template_name = 'accounts/index.html'

    def get(self, request, *args, **kwargs):

        context = {
            'page_title': 'Home Page'
        }
        return render(request, self.template_name, context)



class ClienteCreateView(CustomView):

    template_name = 'accounts/cliente_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get(self, request, *args, **kwargs):

        context = {
            'user_form': UserCreateForm(),
            'usuario_form': UsuarioForm(),
            'cliente_form': ClienteForm(),
            'endereco_form': EnderecoForm(),
            'is_update': False,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user_form = UserCreateForm(request.POST)

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES
        )

        cliente_form = ClienteForm(request.POST)

        endereco_form = EnderecoForm(request.POST)
        print("POST:", request.POST)
        print("FILES:", request.FILES)
        
        print("CLIENTE VALID:", user_form.is_valid())
        print("CLIENTE ERRORS:", user_form.errors)

        print("CLIENTE VALID:", cliente_form.is_valid())
        print("CLIENTE ERRORS:", cliente_form.errors)

        print("USUARIO VALID:", usuario_form.is_valid())
        print("USUARIO ERRORS:", usuario_form.errors)

        print("USUARIO VALID:", endereco_form.is_valid())
        print("USUARIO ERRORS:", endereco_form.errors)

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and cliente_form.is_valid()
            and endereco_form.is_valid()
        ):

            # salva User
            user = user_form.save(commit=False)
            user.set_password(
                user_form.cleaned_data['password']
            )
            user.username = user.email
            user.save()

            # salva Usuario
            usuario = usuario_form.save(commit=False)

            print("FOTO FORM:", usuario_form.cleaned_data.get('foto'))

            usuario.user = user
            usuario.tipo = 'CLIENTE'

            if usuario_form.cleaned_data.get('foto'):
                usuario.foto = usuario_form.cleaned_data['foto']

            usuario.save()

            # salva Cliente
            cliente = cliente_form.save(commit=False)
            cliente.usuario = usuario
            cliente.save()

            # salva Endereco
            endereco = endereco_form.save(commit=False)
            endereco.usuario = usuario
            endereco.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'cliente_form': cliente_form,
            'endereco_form': endereco_form,
            'is_update': False,
        }

        return render(request, self.template_name, context)

class ClienteUpdateView(CustomView):

    template_name = 'accounts/cliente_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get_object(self):
        return Cliente.objects.select_related(
            'usuario__user'
        ).get(pk=self.kwargs['pk'])

    def get_endereco(self, cliente):
        return cliente.usuario.enderecos.filter(principal=True).first()

    def get(self, request, *args, **kwargs):

        cliente = self.get_object()
        endereco = self.get_endereco(cliente)

        context = {
            'user_form': UserCreateForm(
                instance=cliente.usuario.user
            ),
            'usuario_form': UsuarioForm(
                instance=cliente.usuario
            ),
            'cliente_form': ClienteForm(
                instance=cliente
            ),
            'endereco_form': EnderecoForm(
                instance=endereco
            ),
            'object': cliente,
            'is_update': True,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        cliente = self.get_object()
        endereco = self.get_endereco(cliente.usuario)

        user_form = UserCreateForm(
            request.POST,
            instance=cliente.usuario.user
        )

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES,
            instance=cliente.usuario
        )

        cliente_form = ClienteForm(
            request.POST,
            instance=cliente
        )

        endereco_form = EnderecoForm(
            request.POST,
            instance=endereco
        )

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and cliente_form.is_valid()
            and endereco_form.is_valid()
        ):

            # USER
            user = user_form.save(commit=False)
            user.username = user.email
            user.save()

            # USUARIO
            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            # CLIENTE
            cliente = cliente_form.save(commit=False)
            cliente.usuario = usuario
            cliente.save()

            # ENDERECO
            endereco = endereco_form.save(commit=False)
            endereco.usuario = usuario
            endereco.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'cliente_form': cliente_form,
            'endereco_form': endereco_form,
            'object': cliente,
            'is_update': True,
        }

        return render(request, self.template_name, context)


class ClienteDetailView(CustomDetailView):

    model = Cliente
    template_name = 'accounts/cliente_detail.html'

    def get_queryset(self):
        return Cliente.objects.select_related(
            'usuario__user'
        ).prefetch_related(
            'usuario__enderecos'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.object

        context['endereco'] = cliente.usuario.enderecos.filter(
            principal=True
        ).first()

        return context


class RestauranteCreateView(CustomView):

    template_name = 'accounts/restaurante_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get(self, request, *args, **kwargs):

        context = {
            'user_form': UserCreateForm(),
            'usuario_form': UsuarioForm(),
            'restaurante_form': RestauranteForm(),
            'endereco_form': EnderecoForm(),
            'is_update': False,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user_form = UserCreateForm(request.POST)

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES
        )

        restaurante_form = RestauranteForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        
        print("POST:", request.POST)
        print("FILES:", request.FILES)
        
        print("CLIENTE VALID:", user_form.is_valid())
        print("CLIENTE ERRORS:", user_form.errors)

        print("CLIENTE VALID:", restaurante_form.is_valid())
        print("CLIENTE ERRORS:", restaurante_form.errors)

        print("USUARIO VALID:", usuario_form.is_valid())
        print("USUARIO ERRORS:", usuario_form.errors)

        print("USUARIO VALID:", endereco_form.is_valid())
        print("USUARIO ERRORS:", endereco_form.errors)

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and restaurante_form.is_valid()
            and endereco_form.is_valid()
        ):

            # USER
            user = user_form.save(commit=False)
            user.set_password(
                user_form.cleaned_data['password']
            )
            user.username = user.email
            user.save()

            # USUARIO
            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.tipo = 'RESTAURANTE'

            if usuario_form.cleaned_data.get('foto'):
                usuario.foto = usuario_form.cleaned_data['foto']

            usuario.save()

            # RESTAURANTE
            restaurante = restaurante_form.save(commit=False)
            restaurante.usuario = usuario
            restaurante.save()
            
            # salva Endereco
            endereco = endereco_form.save(commit=False)
            endereco.usuario = usuario
            endereco.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'restaurante_form': restaurante_form,
            'endereco_form': endereco_form,
            'is_update': False,
        }

        return render(request, self.template_name, context)

class RestauranteUpdateView(CustomView):

    template_name = 'accounts/restaurante_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get_object(self):
        return Restaurante.objects.select_related(
            'usuario__user'
        ).get(pk=self.kwargs['pk'])
    def get_endereco(self, restaurante):
        return restaurante.usuario.enderecos.filter(principal=True).first()

    def get(self, request, *args, **kwargs):

        restaurante = self.get_object()
        endereco = self.get_endereco(restaurante)

        context = {
            'user_form': UserCreateForm(
                instance=restaurante.usuario.user
            ),
            'usuario_form': UsuarioForm(
                instance=restaurante.usuario
            ),
            'restaurante_form': RestauranteForm(
                instance=restaurante
            ),
            'endereco_form': EnderecoForm(
                instance=endereco
            ),
            'object': restaurante,
            'is_update': True,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        restaurante = self.get_object()
        endereco = self.get_endereco(restaurante)

        user_form = UserCreateForm(
            request.POST,
            instance=restaurante.usuario.user
        )

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES,
            instance=restaurante.usuario
        )

        restaurante_form = RestauranteForm(
            request.POST,
            instance=restaurante
        )

        endereco_form = EnderecoForm(
            request.POST,
            instance=endereco
        )

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and restaurante_form.is_valid()
            and endereco_form.is_valid()
        ):

            # USER
            user = user_form.save(commit=False)
            user.username = user.email
            user.save()

            # USUARIO
            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            # RESTAURANTE
            restaurante = restaurante_form.save(commit=False)
            restaurante.usuario = usuario
            restaurante.save()

            # salva Endereco
            endereco = endereco_form.save(commit=False)
            endereco.usuario = usuario
            endereco.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'restaurante_form': restaurante_form,
            'endereco_form': endereco_form,
            'object': restaurante,
            'is_update': True,
        }

        return render(request, self.template_name, context)

class RestauranteDetailView(CustomDetailView):

    model = Restaurante
    template_name = 'accounts/restaurante_detail.html'

    def get_queryset(self):
        return Restaurante.objects.select_related(
            'usuario__user'
        ).prefetch_related(
            'horarios'
        )

class EntregadorCreateView(CustomView):

    template_name = 'accounts/entregador_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get(self, request, *args, **kwargs):

        context = {
            'user_form': UserCreateForm(),
            'usuario_form': UsuarioForm(),
            'entregador_form': EntregadorForm(),
            'is_update': False,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user_form = UserCreateForm(request.POST)

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES
        )

        entregador_form = EntregadorForm(request.POST)

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and entregador_form.is_valid()
        ):

            user = user_form.save(commit=False)
            user.set_password(
                user_form.cleaned_data['password']
            )
            user.username = user.email
            user.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.tipo = 'ENTREGADOR'

            if usuario_form.cleaned_data.get('foto'):
                usuario.foto = usuario_form.cleaned_data['foto']

            usuario.save()

            entregador = entregador_form.save(commit=False)
            entregador.usuario = usuario
            entregador.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'entregador_form': entregador_form,
            'is_update': False,
        }

        return render(request, self.template_name, context)    

class EntregadorUpdateView(CustomView):

    template_name = 'accounts/entregador_form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get_object(self):
        return Entregador.objects.select_related(
            'usuario__user'
        ).get(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):

        entregador = self.get_object()

        context = {
            'user_form': UserCreateForm(
                instance=entregador.usuario.user
            ),
            'usuario_form': UsuarioForm(
                instance=entregador.usuario
            ),
            'entregador_form': EntregadorForm(
                instance=entregador
            ),
            'object': entregador,
            'is_update': True,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        entregador = self.get_object()

        user_form = UserCreateForm(
            request.POST,
            instance=entregador.usuario.user
        )

        usuario_form = UsuarioForm(
            request.POST,
            request.FILES,
            instance=entregador.usuario
        )

        entregador_form = EntregadorForm(
            request.POST,
            instance=entregador
        )

        if (
            user_form.is_valid()
            and usuario_form.is_valid()
            and entregador_form.is_valid()
        ):
            user = user_form.save(commit=False)
            user.username = user.email
            user.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            entregador = entregador_form.save(commit=False)
            entregador.usuario = usuario
            entregador.save()

            return redirect(self.success_url)

        context = {
            'user_form': user_form,
            'usuario_form': usuario_form,
            'entregador_form': entregador_form,
            'object': entregador,
            'is_update': True,
        }

        return render(request, self.template_name, context)
    
class EntregadorDetailView(CustomDetailView):

    model = Entregador
    template_name = 'accounts/entregador_detail.html'

    def get_queryset(self):
        return Entregador.objects.select_related(
            'usuario__user'
        ).prefetch_related(
            'documentos'
        )
        
        

class UsuarioListView(CustomView, ListView):
    model = Usuario
    template_name = 'accounts/usuarios_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Usuario.objects.select_related('user').all().order_by('-id')

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        return queryset

    def get_tipo_badge(self, tipo):
        badges = {
            'CLIENTE': 'primary',
            'RESTAURANTE': 'success',
            'ENTREGADOR': 'warning',
            'ADMIN': 'dark',
        }
        return badges.get(tipo, 'secondary')

    def get_urls(self, usuario):
        """
        Retorna urls corretas dependendo do tipo
        """

        if usuario.tipo == 'CLIENTE' and hasattr(usuario, 'cliente'):
            return {
                'detail': reverse('core:cliente_detail', kwargs={'pk': usuario.cliente.pk}),
                'update': reverse('core:cliente_update', kwargs={'pk': usuario.cliente.pk}),
            }

        elif usuario.tipo == 'RESTAURANTE' and hasattr(usuario, 'restaurante'):
            return {
                'detail': reverse('core:restaurante_detail', kwargs={'pk': usuario.restaurante.pk}),
                'update': reverse('core:restaurante_update', kwargs={'pk': usuario.restaurante.pk}),
            }

        elif usuario.tipo == 'ENTREGADOR' and hasattr(usuario, 'entregador'):
            return {
                'detail': reverse('core:entregador_detail', kwargs={'pk': usuario.entregador.pk}),
                'update': reverse('core:entregador_update', kwargs={'pk': usuario.entregador.pk}),
            }

        return {
            'detail': '#',
            'update': '#',
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuarios = context['usuarios']

        for usuario in usuarios:
            usuario.urls = self.get_urls(usuario)
            usuario.badge = self.get_tipo_badge(usuario.tipo)

        context['page_title'] = 'Usuários'
        context['search'] = self.request.GET.get('search', '')

        return context










