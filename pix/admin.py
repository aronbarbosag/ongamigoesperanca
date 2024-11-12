from django.contrib import admin
from .models import Pagamento
# Register your models here.
class PagamentoAdmin(admin.ModelAdmin):
  list_display=('nome','email','valor','status')
  list_filter=('status',)
  list_editable =('status',)
  list_per_page = (15)
  
  
admin.site.register(Pagamento,PagamentoAdmin)