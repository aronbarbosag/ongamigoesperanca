from django.contrib import admin
from .models import Evento
# Register your models here.
class EventoAdmin(admin.ModelAdmin):
  list_display = ('nome','data','hora','imagem','link_postagem','info')
  
admin.site.register(Evento,EventoAdmin)