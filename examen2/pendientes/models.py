# pendientes/models.py
from django.db import models
from django.urls import reverse

class Todo(models.Model):
    """
    Representa un pendiente (ToDo) sincronizado desde la API externa.
    """
    user_id = models.IntegerField(
        verbose_name="ID de Usuario (API)",
        help_text="El ID del usuario propietario del pendiente según la API."
    )
    api_id = models.IntegerField(
        verbose_name="ID del Pendiente (API)",
        unique=True,
        help_text="El ID único del pendiente proveniente de la API."
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Título",
        help_text="El título o descripción del pendiente."
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Completado",
        help_text="Indica si el pendiente ha sido completado."
    )

    class Meta:
        ordering = ['api_id']
        verbose_name = "Pendiente"
        verbose_name_plural = "Pendientes"

    def __str__(self):
        return f"ID:{self.api_id} - {self.title}"

    def get_absolute_url(self):
        """
        Devuelve la URL para ver el detalle de este objeto.
        """
        return reverse('todo-detail', kwargs={'pk': self.pk})