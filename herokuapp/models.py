from django.db import models


# Create your models here.
class SelectedRepository(models.Model):
	name = models.CharField(max_length=10000)

	def __str__(self):
		return self.name


class AccessToken(models.Model):
	token = models.CharField(max_length=100)

	def __str__(self):
		return self.token

