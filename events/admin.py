from django.contrib import admin
from .models import Evento, Voluntario
# Register your models here.
class EventoAdmin(admin.ModelAdmin):
  list_display = ('nome','data','hora','imagem','link_postagem','info')
  
  
class VoluntarioAdmin(admin.ModelAdmin):
  list_display = ('nome','email','comentario')
  
   
admin.site.register(Evento,EventoAdmin)
admin.site.register(Voluntario,VoluntarioAdmin)