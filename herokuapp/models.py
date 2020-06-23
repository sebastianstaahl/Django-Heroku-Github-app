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

class UserName(models.Model):
	username = models.CharField(max_length=100)

	def __str__(self):
		return self.username

class PayLoad(models.Model):
	payload = models.CharField(max_length=1000000)

	def __str__(self):
		return self.payload