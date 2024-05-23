from __future__ import annotations
from django.db import models


class BaseModel(models.Model):
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True