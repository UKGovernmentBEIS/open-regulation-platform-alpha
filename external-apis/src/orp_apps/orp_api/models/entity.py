"""Entity model."""

# Third Party
from django.db import models


class Entity(models.Model):
    """Entity model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Display name value in admin view."""
        return self.name

    def related_documents(self):
        """Return all Documents related to current entity."""
        return self.document_set.filter(related_entity=self)  # noqa
