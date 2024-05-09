from typing import Iterable

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model"""

    created_at = models.DateTimeField(
        verbose_name=_("creation date"),
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("last update date"),
        default=timezone.now,
    )

    class Meta:
        abstract = True

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.updated_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)
