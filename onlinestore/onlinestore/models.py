from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission

class Developer(models.Model):
	user = models.OneToOneField(User)
	

class Game(models.Model):
	name = models.CharField(max_length=70, unique=True)
	source_URL = models.URLField(max_length=200, unique=True, default='default_url')
	developer = models.ForeignKey(Developer, related_name='developed_games', default=0)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	description = models.TextField(max_length=200, blank=True)
	category = models.TextField(default="Adventure")
	def __str__(self):
		return self.name


class Save(models.Model):
	player = models.ForeignKey(User, related_name="saves")
	game = models.ForeignKey(Game, related_name="saves")
	gameState = models.TextField()


class HighScore(models.Model):
	player = models.ForeignKey(User, related_name="highScores")
	game = models.ForeignKey(Game, related_name="highScores")
	score = models.IntegerField()
	def __str__(self):
		return self.game.name + " " + self.player.username + " " + self.score

	description = models.TextField()


class Sales (models.Model):
	user = models.ForeignKey(User, related_name="purchases")
	game = models.ForeignKey(Game)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	date = models.DateTimeField(auto_now=True)
	success = models.BooleanField(default=False)
	

