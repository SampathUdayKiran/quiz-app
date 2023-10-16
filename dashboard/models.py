from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class QuestionsModel(models.Model):
    question = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()


class UserAccuracyModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_tests = models.IntegerField()
    accuracy = models.FloatField()


class UserTestDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    test_number = models.IntegerField()
    total_test_questions = models.IntegerField()
    attempted_questions = models.IntegerField()
    correct_answered = models.IntegerField()
    wrong_answered = models.IntegerField()
    total_marks = models.IntegerField()
    marks_secured = models.IntegerField()
    percentage = models.FloatField()

class QuizConfiguration(models.Model):
    number_of_questions = models.PositiveIntegerField()
    marks_per_question = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"Quiz Configuration {self.pk}"
