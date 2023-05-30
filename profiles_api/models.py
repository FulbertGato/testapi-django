from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        # Normalize email address
        email = self.normalize_email(email)
        # Create a new user model
        user = self.model(email=email, name=name)

        # Set the password
        user.set_password(password)
        # Save the user model
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""

        # Create a new user model
        user = self.create_user(email, name, password)

        # Set the user as a superuser
        user.is_superuser = True
        user.is_staff = True

        # Save the user model
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # is_active is required for custom user model
    is_staff = models.BooleanField(default=False)  # is_staff is required for custom user model

    # Create a model manager for our custom user model
    objects = UserProfileManager()

    # Set the USERNAME_FIELD to email
    USERNAME_FIELD = 'email'
    # Set the REQUIRED_FIELDS to name
    REQUIRED_FIELDS = ['name']

    # Helper functions
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email
