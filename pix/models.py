from django.db import models

class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    # Informações do devedor
    cpf = models.CharField(max_length=11, verbose_name="CPF do Devedor")
    nome = models.CharField(max_length=255, verbose_name="Nome do Devedor")

    # Informações sobre o pagamento
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Cobrança")

    # Dados do Pix
    txid = models.CharField(max_length=255, null=True, blank=True, verbose_name="Txid do Pagamento")
    id_loc = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID da Localização")
    qr_code = models.TextField(max_length=255, null=True, blank=True, verbose_name="QR Code")
    link_visualizacao = models.URLField(null=True, blank=True, verbose_name="Link de Visualização")
    imagem_qrcode = models.TextField(null=True, blank=True, verbose_name="Imagem do QR Code")
    email = models.EmailField(default='ongamigo@esperanca')
    mensagem = models.TextField(blank=True, null=True)
    
    # Status do pagamento
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status do Pagamento")
    
    # Campos para rastreamento (como data de criação e última atualização)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def __str__(self):
        return f"Pagamento {self.id} - {self.nome} - {self.valor}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-created_at']