from rest_framework import serializers
from student.models import Student

class SerializeStudent(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
