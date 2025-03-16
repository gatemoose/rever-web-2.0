from django.db import models
from django.utils.html import format_html

class Request(models.Model):
    prompt = models.TextField(verbose_name='Prompt')
    file = models.FileField(upload_to='api/files/', verbose_name='Vídeo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['prompt']
        verbose_name = 'Requisição'
        verbose_name_plural = 'Requisições'

    def __str__(self):
        return self.prompt
    

class Response(models.Model):
    prompt = models.ForeignKey(Request, on_delete=models.CASCADE,
                               related_name='responses', verbose_name='Prompt')
    ai_response = models.TextField(verbose_name='Resposta do Gemini')
    tokens_used = models.IntegerField(verbose_name='Tokens Usados', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['ai_response', 'prompt']
        verbose_name = 'Resposta'

    def __str__(self):
        return self.ai_response
    
    def ai_response_html(self):
        return format_html(self.ai_response)
    
    ai_response_html.short_description = 'Resposta do Gemini'
    