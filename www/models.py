from django.db import models
from django.contrib.auth.models import User
MAN = 'M'
WOMAN = 'W'

SEX_CHOICES = (
    (MAN, 'Man'),
    (WOMAN, 'Woman'),
)

class Characters(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=100, blank=True, null=True)
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=MAN)
	taken = models.BooleanField(default=False)
	picture = models.CharField(max_length=300, blank=True, null=True)
	def __unicode__(self):
		return self.name

class Profiles(models.Model):
	user = models.OneToOneField(User)
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=MAN)
	character = models.OneToOneField(Characters, blank=True, null=True)
	def __unicode__(self):
		return self.user.username