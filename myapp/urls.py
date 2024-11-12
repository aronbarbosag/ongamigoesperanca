from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("sobre-nos/", views.sobre, name="sobre"),
    path("transparencia/", views.transparencia, name="transparencia"),
    path("voluntariado/", views.voluntariado, name="voluntariado"),
    path("contato/", views.contato, name="contato"),
    path("doacao/", views.doacao, name="doacao"),
    path("eventos/", views.eventos, name="eventos"),
    path("area-restrita/", views.area_restrita, name="area-restrita"),
    path("sucesso/<str:id_loc>/", views.sucesso, name="sucesso"),


]
handler404 = views.custom_404
