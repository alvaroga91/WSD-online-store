from django.db import models
from django.forms import ModelForm
from onlinestore.models import User

class LoginForm(ModelForm):
	class Meta:
		model = User;
		fields = ['username','password'];
		
