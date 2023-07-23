from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # Your custom user model fields and methods go here
    is_wsadmin = models.BooleanField(default=False)