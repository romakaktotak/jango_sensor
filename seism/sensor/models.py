from django.db import models
from django.contrib.auth.models import User

class Sens(models.Model):
    name = models.CharField(max_length=30)
    ownuser = models.ForeignKey(User, on_delete = models.CASCADE, db_constraint=False)

    def __str__(self):
        return self.name
