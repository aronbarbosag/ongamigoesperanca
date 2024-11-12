from django.db import models

# Create your models here.
class Evento(models.Model):
  nome = models.CharField(max_length=200)
  data = models.DateField()
  hora = models.TimeField()
  imagem = models.ImageField(upload_to='eventos/')
  link_postagem = models.CharField(max_length=300)
  info = models.TextField()
  
  def __str__(self):
    return self.nome
  
class Voluntario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    comentario = models.TextField()
    
    def __str__(self):
        return self.nome
  