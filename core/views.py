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
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader

from django.db import transaction, DatabaseError
from .forms import UserCreateForm, UsuarioForm, ClienteForm, EnderecoForm
from askdelivery.settings import DEFAULT_FROM_EMAIL

import operator
from functools import reduce
from .custom_views import CustomView, CustomDetailView
from .models import Usuario, Cliente

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


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class IndexView(CustomView):

    template_name = 'accounts/index.html'

    def get(self, request, *args, **kwargs):

        context = {
            'page_title': 'Dashboard'
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
            endereco.cliente = cliente
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
        return cliente.enderecos.filter(principal=True).first()

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
        endereco = self.get_endereco(cliente)

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

            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)

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
            endereco.cliente = cliente
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
            'enderecos'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.object

        context['endereco'] = cliente.enderecos.filter(
            principal=True
        ).first()

        return context



class UsuarioListView(CustomView, ListView):
    model = Usuario
    template_name = 'accounts/usuarios_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Usuario.objects.all().order_by('-id')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Usuários'
        context['search'] = self.request.GET.get('search', '')

        return context










