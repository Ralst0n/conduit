from django.db import models

from conduit.apps.core.models import TimestampedModel

class Profile(TimestampedModel):
    # each user has 1 & only 1 profile
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)

    # each user may have a profile image
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
