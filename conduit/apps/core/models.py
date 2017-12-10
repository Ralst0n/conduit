from django.db import models

class TimestampedModel(models.Model):
    # timestamp representing object created
    created_at = models.DateTimeField(auto_now_add=True)

    # timestamp representing object last update
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # reverse-chronological order
        ordering = ['-created_at', '-updated_at']

        
