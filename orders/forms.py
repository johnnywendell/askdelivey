from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'latitude',
            'longitude',
            'restaurante',
            'entregador',
            'cliente',
            'status',
            'cep',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do cliente',
            }),

            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
            }),

            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0000000001',
            }),

            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0000000001',
            }),

            'restaurante': forms.Select(attrs={
                'class': 'form-select',
            }),

            'entregador': forms.Select(attrs={
                'class': 'form-select',
            }),

            'cliente': forms.Select(attrs={
                'class': 'form-select',
            }),

            'status': forms.Select(attrs={
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
        }

