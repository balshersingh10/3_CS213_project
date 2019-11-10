from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Fac_Courses(models.Model):
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=20)
    department = models.CharField(max_length=5)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.f_name} - {self.course_code}-{self.department}"

class Stud_Course(models.Model):
    rollno = models.CharField(max_length=10)
    course = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.rollno}"

class Attendence(models.Model):
    rollno = models.CharField(max_length=10)
    course_code = models.CharField(max_length=5)
    present = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)
    t = models.DateTimeField()


    def __str__(self):
        return f"{self.rollno} {self.present} on {self.date}"
