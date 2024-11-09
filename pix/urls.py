from django.urls import path
from . import views

app_name = 'pix'

urlpatterns = [
    path('gerar-pix/', views.processar_cobranca_pix, name='gerar_pix'),
    path('sucesso/<str:id_loc>/', views.sucesso, name='sucesso'),
]   
