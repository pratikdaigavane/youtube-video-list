from django.db import models


# Model to store API Keys
class APIKey(models.Model):
    key = models.TextField()
