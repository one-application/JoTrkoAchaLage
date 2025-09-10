from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	role = models.CharField(max_length=32, db_index=True)
	phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	student_id = models.CharField(max_length=32, blank=True, null=True, unique=True)
	employee_id = models.CharField(max_length=32, blank=True, null=True, unique=True)

	def __str__(self) -> str:
		return f"Profile({self.user_id})" 