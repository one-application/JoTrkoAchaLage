from django.db import models


class Applicant(models.Model):
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, db_index=True)
	user = models.OneToOneField("users.User", null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self) -> str:
		return self.email


class Application(models.Model):
	applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="applications")
	program = models.ForeignKey("academics.Program", on_delete=models.PROTECT)
	stage = models.CharField(max_length=32, default="draft")
	payment_status = models.CharField(max_length=16, default="unpaid")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Application({self.id})" 