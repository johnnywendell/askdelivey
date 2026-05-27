from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'address',
            'latitude',
            'longitude',
            'restaurante',
            'entregador',
            'cliente',
            'status',
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

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo',
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
        }

