"""Document model."""

# Third Party
from django.db import models


class Document(models.Model):
    """Document model."""

    name = models.CharField(max_length=255)
    related_documents = models.ManyToManyField('Document')
    related_entities = models.ManyToManyField('Entity')
    content = models.TextField()

    def __str__(self):
        """Display name value in admin view."""
        return self.name
