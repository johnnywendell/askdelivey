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
            'cliente',
            'address',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do cliente',
            }),

            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control phone-mask',
                'placeholder': 'Telefone',
            }),

            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),

            'cliente': forms.Select(attrs={
                'class': 'form-select',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o endereço',
                'id': 'address-search',
                'autocomplete': 'off',
            }),

        }

