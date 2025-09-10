from rest_framework import serializers
from .models import Applicant, Application


class ApplicantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Applicant
		fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Application
		fields = "__all__" 