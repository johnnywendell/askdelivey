from django.db import models
from django.utils import timezone
from core.models import Entregador


class EntregadorLocalizacao(models.Model):
    entregador = models.OneToOneField(
        Entregador,
        on_delete=models.CASCADE,
        related_name='localizacao'
    )

    latitude = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)

    velocidade = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)

    disponivel = models.BooleanField(default=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.entregador} ({self.latitude}, {self.longitude})"

class SessaoRastreamento(models.Model):
    entregador = models.ForeignKey(
        Entregador,
        on_delete=models.CASCADE,
        related_name='sessoes_rastreamento'
    )

    online = models.BooleanField(default=False)

    iniciado_em = models.DateTimeField(default=timezone.now)

    finalizado_em = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.entregador} - {'Online' if self.online else 'Offline'}"
    
class HistoricoLocalizacao(models.Model):
    entregador = models.ForeignKey(
        Entregador,
        on_delete=models.CASCADE,
        related_name='historico_localizacao'
    )
    latitude = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)
    velocidade = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['registrado_em']
