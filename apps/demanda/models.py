from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Anunciante(User):
     
    nome = models.CharField(_("Nome Completo"), max_length=240)
    cpf = models.CharField(_("CPF"), max_length=15)
    telefone = models.CharField(_("Telefone"), max_length=50)
    
    class Meta:
        verbose_name = _('anunciante')
        verbose_name_plural = _('anunciantes')

    def __str__(self):
        return self.nome


class Endereco(models.Model):

    rua = models.CharField(_("Rua"), max_length=100)
    numero = models.CharField(_("Número"), max_length=10)
    bairro = models.CharField(_("Bairro"), max_length=100)
    cidade = models.CharField(_("Cidade"), max_length=100)
    estado = models.CharField(_("Estado"), max_length=50)
    cep = models.CharField(_("CEP"), max_length=10)
    complemento = models.TextField(_("Complemento"), blank=True)
    anunciante = models.ForeignKey(Anunciante, verbose_name=_("endereco"), on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = _('endereco')
        verbose_name_plural = _('enderecos')

    def __str__(self):
        return self.rua
