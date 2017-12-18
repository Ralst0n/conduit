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

    # Following a person doesn't mean they follow back
    # Thus symmetrical = False
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    favorites = models.ManyToManyField(
        'articles.Article',
        related_name='favorited_by'
    )

    def __str__(self):
        return self.user.username

    def favorite(self, article):
        """Favorite `article` if we haven't already favorited it."""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Unfavorite `article` if we've already favorited it."""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Returns True if we have favorited `article`; else False"""
        return self.favorites.filter(pk=article.pk).exists()

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        return self.followed_by.filter(pk=profile.pk).exists()
