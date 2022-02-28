"""Taxonomy model."""

# Third Party
from django.db import models

from .category import Category


class Taxonomy(models.Model):
    """Taxonomy model."""

    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        """Display name value in admin view."""
        return self.name
