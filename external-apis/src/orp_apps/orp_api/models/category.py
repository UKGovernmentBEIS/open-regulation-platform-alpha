"""Category model."""

# Third Party
from django.db import models


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=255)
    related_categories = models.ManyToManyField('Category')
    related_documents = models.ManyToManyField('Document')

    def __str__(self):
        """Display name value in admin view."""
        return self.name
