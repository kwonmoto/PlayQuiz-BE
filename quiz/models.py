from django.db import models
from users.models import User
# Create your models here.

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class QuizSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setTitle = models.CharField(max_length=50)
    publicYn = models.CharField(max_length=1)
    quizLibrary = models.ForeignKey(Library, on_delete=models.CASCADE)

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quizSet = models.ManyToManyField(QuizSet, related_name="set_quiz")
    quizTime = models.IntegerField()
    category = models.CharField(max_length=8)
    quizChar = models.CharField(max_length=2)
    quizNo = models.CharField(max_length=4)
    quizType = models.CharField(max_length=1)
    answerCount = models.IntegerField()
    quizValue1 = models.CharField(max_length=50)
    quizValue2 = models.CharField(max_length=50)
    quizValue3 = models.CharField(max_length=50)
    quizValue4 = models.CharField(max_length=50)
    quizValue5 = models.CharField(max_length=50)