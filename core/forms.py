# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from .models import User, Usuario, Cliente, Endereco, Restaurante, HorarioFuncionamento, Entregador, DocumentoEntregador

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma senha',
        })
    )

    confirm_password = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha',
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # se existe instance com pk => UPDATE
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'telefone',
        ]


        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com',
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
            }),
    
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        # só valida se alguma senha foi digitada
        if password or confirm:
            if password != confirm:
                raise forms.ValidationError(
                    'As senhas não coincidem.'
                )

        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = [
            'foto',
        ]

        widgets = {
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class ClienteForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Cliente
        fields = [
            'cpf',
            'data_nascimento',
            'aceita_marketing',
            'sexo',
        ]


        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
            }),

            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'aceita_marketing': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control',
            }),

        }


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Endereco
        fields = [
            'tipo',
            'cep',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'principal',
        ]

        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
            }),

            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
            }),

            'rua': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua / Avenida',
            }),

            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número',
            }),

            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, bloco, referência...',
            }),

            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro',
            }),

            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
            }),

            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'maxlength': '2',
            }),

            'principal': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

class RestauranteForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = [
            'nome_fantasia',
            'razao_social',
            'cnpj',
            'descricao',
            'telefone_comercial',
            'taxa_entrega',
            'tempo_preparo_min',
            'aceita_retirada',
            'ativo',
        ]

        widgets = {
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome Fantasia',
            }),

            'razao_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razão Social',
            }),

            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do restaurante',
            }),

            'telefone_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
            }),

            'taxa_entrega': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),

            'tempo_preparo_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
            }),

            'aceita_retirada': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

class HorarioFuncionamentoForm(forms.ModelForm):

    class Meta:
        model = HorarioFuncionamento
        fields = [
            'dia_semana',
            'hora_abertura',
            'hora_fechamento',
            'fechado',
        ]

        widgets = {
            'dia_semana': forms.Select(attrs={
                'class': 'form-select',
            }),

            'hora_abertura': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),

            'hora_fechamento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),

            'fechado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        
class EntregadorForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Entregador
        fields = [
            'cpf',
            'cnh',
            'tipo_veiculo',
            'placa',
            'disponivel',
            'aprovado',
            'data_nascimento',
            'sexo',
        ]

        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
            }),

            'cnh': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da CNH',
            }),

            'tipo_veiculo': forms.Select(attrs={
                'class': 'form-select',
            }),

            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234',
            }),

            'disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'aprovado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
             'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
             'sexo': forms.Select(attrs={
                'class': 'form-control',
            }),
             
        }
        
class DocumentoEntregadorForm(forms.ModelForm):

    class Meta:
        model = DocumentoEntregador
        fields = [
            'tipo',
            'arquivo',
            'aprovado',
        ]

        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
            }),

            'arquivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'aprovado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }