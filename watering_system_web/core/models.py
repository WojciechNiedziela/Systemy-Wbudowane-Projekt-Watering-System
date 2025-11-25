from django.db import models

class Pomiar(models.Model):
    wilgotnosc = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.wilgotnosc}%"

class Log(models.Model):
    akcja = models.CharField(max_length=50)
    szczegoly = models.CharField(max_length=200, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.akcja} {self.szczegoly}"

class Ustawienia(models.Model):
    auto = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ustawienia(auto={self.auto})"
