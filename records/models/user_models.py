from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator

"""
Note on 'backward' properties
To anyone looking at this code, I recommend reading the following docs:
https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects
"""

class UserType(models.TextChoices):
    """
    Defines the types of user that a derrived type could be.
    """
    CLIENT= "CLIENT"

class AvailabilityPeriod(models.TextChoices):
    """
    Defines when a client is available
    """

    MONDAY = 'MONDAY', 'Monday'
    TUESDAY = 'TUESDAY', 'Tuesday'
    WEDNESDAY = 'WEDNESDAY', 'Wednesday'
    THURSDAY = 'THURDSAY', 'Thursday'
    FRIDAY = 'FRIDAY', 'Friday'
    SATURDAY = 'SATURDAY', 'Saturday'
    SUNDAY = 'SUNDAY', 'Sunday'

DURATION_CHOICES = (
        (15, "15 minutes"),
        (30, "30 minutes"),
        (45, "45 minutes"),
        (60, "60 minutes")
    )

INTERVAL_CHOICES = (
    (1, "Every week"),
    (2, "Every two weeks"),
    (3, "Every three weeks"),
    (4, "Every four weeks")
)

class User(AbstractUser):
    """
    Base user from which all types of user are derrived from.
    Model is used for authentication purposes.
    """

    username = models.EmailField(unique=True, blank=False)
    type = models.CharField(max_length=50, choices=UserType.choices, default=UserType.CLIENT)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

    def full_name(self):
        """
        Returns the user's full name
        """
        return f"{ self.first_name } { self.last_name }"

    """
    Overridden methods
    """

    def clean(self):
        """
        Perform model validation checks that occur across multiple fields
        Docs for model validation: https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.clean
        """
        
        """
        This validation check will only occur if both the email and username fields have been populated.
        This is to prevent the a form.is_valid() calling clean too early, resulting in a crash
        """
        if (self.username and self.email and self.username != self.email):
            raise ValidationError("Username field must be equal to email field at all times")

        if (self.type is None):
            raise ValidationError("A user must be associated to a user type")

class ClientProfile(models.Model):
    """
    Represents a client with privileges to request lessons, access invoices, and other basic tasks.
    Guests can register as a client via public site.
    """

    # Represents the unique client identifer number
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")

