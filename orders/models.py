from django.db import models
from django.conf import settings
from core.models import Entregador, Restaurante, Cliente


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = 'created', 'Criado'
        APPROVED = 'approved', 'Aprovado pelo restaurante'
        ACCEPTED = 'accepted', 'Aceito pelo entregador'
        PICKING = 'picking', 'Em coleta'
        IN_TRANSIT = 'in_transit', 'Em rota'
        DELIVERED = 'delivered', 'Entregue'
        CANCELED = 'canceled', 'Cancelado'


    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    address = models.TextField()

    latitude = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )
    restaurante = models.ForeignKey(
        Restaurante,
        related_name='orders_restaurante',
        on_delete=models.CASCADE,
    )

    entregador = models.ForeignKey(
        Entregador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_name}"
    
