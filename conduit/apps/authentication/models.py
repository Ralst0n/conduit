import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):
    """
    Django suggest defining a custom manager for custom user model

    We inherit from BaseUserManager to get much of the functionality
    of Django's default User

    We override the 'create_user' function
    """
    def create_user(self, username, email, password=None):
        """Create 'USER' with a username, email * password"""

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must provide an email address.')

        user = self.model(
            username=username,
            email= self.normalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create a 'User' with admin permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    #Each 'User' needs a human-readable unique identifier
    #to represent said 'User' in the UI.
    # Index this column in db to improve lookup performance
    username = models.CharField(db_index=True, max_length=225, unique=True)

    #We need a way to contact a user and for a user to identify
    #themselves when logging in
    #email is a common way to handle both
    email = models.EmailField(db_index=True, unique=True)

    #Deleting data is bad for business, therefore we can
    #give an option to deactivate an account so it doesn't show
    #anymore, but we still get to use it for our data deeds
    is_active = models.BooleanField(default=True)

    #The 'is_staff' flag is EXPECTED by Django to determine
    #who can and cannot log into the Django admin site.
    #most users won't/shouldn't have access to it
    is_staff = models.BooleanField(default=False)

    #timestamp for when 'User' object created
    created_at = models.DateTimeField(auto_now_add=True)

    #timestamp representing when 'User' was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    #More fields required by Django when creating a custom user model.

    #The 'USERNAME_FIELD' property tells which field we
    #use to log in.
    #recall, that was the email field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #Tells Django that the UserManager class defined above
    #should manage objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        return string repr of 'User'
        """
        return self.email

    @property
    def token(self):
        """
        call token to get value from 'user.generate_jwt_token()'
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
