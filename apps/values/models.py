from django.db import models
from apps.items.models import Item


class Value(models.Model):
    item_id = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        db_index=True
    )

    name = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default='value'
    )

    value_number = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    value_text = models.TextField(
        null=True,
        blank=True,
        max_length=200
    )

    def __str__(self) -> str:
        return f"Item ID: {self.item_id.id} - Value: {self.value_text}"
