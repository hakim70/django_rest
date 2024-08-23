from django.db import models

class data(models.Model):

    username = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name