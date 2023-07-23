from django.db import models
from django.conf import settings
from .validators import validate_file_size
from core.models import User

# Create your models here.
class Workspaces(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.image = models.ImageField(
        upload_to="software/images",
        validators=[validate_file_size])
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_admin')

class WorkspacesUsers(models.Model):
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE, related_name="workspace")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_user')

# class Tasks(models.Model):
#     title = models.CharField(max_length=250, null=False, blank=False)
#     description = models.TextField(null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     duration = models.DurationField(null=True, blank=True)
#     user = models.ForeignKey(WorkspacesUsers, on_delete=models.CASCADE, related_name='workspace_user')
