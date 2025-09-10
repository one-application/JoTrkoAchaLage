from django.db import models


class FeePlan(models.Model):
	program = models.ForeignKey("academics.Program", on_delete=models.PROTECT)
	term = models.CharField(max_length=16)
	description = models.CharField(max_length=255, blank=True)

	class Meta:
		unique_together = ("program", "term")


class Invoice(models.Model):
	student = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
	term = models.CharField(max_length=16)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=16, default="unpaid")
	created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
	gateway_ref = models.CharField(max_length=64)
	status = models.CharField(max_length=16)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True) 