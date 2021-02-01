from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Demanda
# Register your models here.

@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ("endereco_de_entrega", "anunciante", "status_svg")