from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    front_file = models.FileField(
        upload_to="uploads/"
    )

    back_file = models.FileField(
        upload_to="uploads/",
        null=True,
        blank=True
    )

    front_text = models.TextField(
        blank=True,
        default=""
    )

    back_text = models.TextField(
        blank=True,
        default=""
    )

    extracted_text = models.TextField(
        blank=True,
        default=""
    )

    structured_data = models.JSONField(
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title