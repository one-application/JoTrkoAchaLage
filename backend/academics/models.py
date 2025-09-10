from django.db import models


class Program(models.Model):
	code = models.CharField(max_length=16, unique=True)
	name = models.CharField(max_length=128)

	def __str__(self) -> str:
		return self.code


class Course(models.Model):
	code = models.CharField(max_length=16, unique=True)
	title = models.CharField(max_length=256)
	credits = models.DecimalField(max_digits=4, decimal_places=1)
	program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name="courses")

	def __str__(self) -> str:
		return self.code


class CourseRegistration(models.Model):
	student = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="registrations")
	course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="registrations")
	term = models.CharField(max_length=16)
	status = models.CharField(max_length=16, default="enrolled")

	class Meta:
		unique_together = ("student", "course", "term")


class Attendance(models.Model):
	student = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	faculty = models.ForeignKey("hr.Employee", on_delete=models.PROTECT)
	date = models.DateField()
	status = models.CharField(max_length=8) 