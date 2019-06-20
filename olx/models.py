from django.db import models

# Create your models here.

class OlxRequest(models.Model):
    url = models.URLField(verbose_name='Url for analis', max_length=2000)
    email = models.EmailField(verbose_name='Yor email')
    datetime_add_request = models.DateTimeField(auto_now_add=True)

class OlxLinks(models.Model):
    request = models.ForeignKey(OlxRequest, on_delete=models.CASCADE)
    link = models.URLField()
    datetime = models.DateTimeField()
