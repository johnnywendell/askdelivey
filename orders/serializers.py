from rest_framework import serializers
from .models import Order
from tracking.models import Entregador


class OrderSerializer(serializers.ModelSerializer):

    restaurante_nome = serializers.CharField(
        source='restaurante.nome_fantasia',
        read_only=True
    )
    entregador_nome = serializers.CharField(
        source='entregador.usuario.user.first_name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    class Meta:
        model = Order

        fields = [
            'id',

            'customer_name',
            'customer_phone',
            'address',

            'latitude',
            'longitude',

            'status',
            'status_display',

            'restaurante',
            'restaurante_nome',

            'entregador',
            'entregador_nome',

            'cliente',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'status',
            'entregador',
            'created_at',
            'updated_at',
        ]


class AssignOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    entregador_id = serializers.IntegerField()