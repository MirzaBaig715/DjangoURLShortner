from django.db import models

# Create your models here.


class WordList(models.Model):
    word = models.CharField(max_length=100)
    last_used = models.DateTimeField(blank=True, null=True)
    last_url = models.URLField(blank=True, null=True, max_length=400)

    class Meta:
        ordering = ["-last_used"]

    def __str__(self):
        return self.word


class WordRecord(models.Model):
    used_word = models.CharField(max_length=100)

    def __str__(self):
        return self.used_word

