from django.db import models


class Department(models.Model):
	code = models.CharField(max_length=16, unique=True)
	name = models.CharField(max_length=128)

	def __str__(self) -> str:
		return self.code


class Employee(models.Model):
	user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="employee")
	employee_code = models.CharField(max_length=32, unique=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)
	designation = models.CharField(max_length=128)

	def __str__(self) -> str:
		return self.employee_code


class LeaveApplication(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	type = models.CharField(max_length=32)
	status = models.CharField(max_length=16, default="pending")
	created_at = models.DateTimeField(auto_now_add=True) 