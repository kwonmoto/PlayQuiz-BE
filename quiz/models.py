from django.db import models
from users.models import User
# Create your models here.

class Set_Library(models.Model):
    set = models.CharField("세트ID", max_length=20)
    libID = models.CharField("라이브러리ID", max_length=20)
    regDate = models.DateTimeField("등록일자", auto_now_add=True)
    chgData = models.DateTimeField("변경일자", auto_now=True)
    
class Set(models.Model):
    user = models.CharField("사용자ID", max_length=20)
    setTitle = models.CharField("퀴즈 세트 타이틀", max_length=50)
    publicYn = models.CharField("공개여부", max_length=1)
    regDate = models.DateTimeField("등록일자", auto_now_add=True)
    regUser = models.CharField("등록 유저", max_length=20)
    regUserIP = models.CharField("등록 유저IP", max_length=20)
    chgDate = models.DateTimeField("변경일자", auto_now=True)
    chgUser = models.CharField("변경 유저", max_length=20)
    chgUserIP = models.CharField("변경 유저IP", max_length=20)

class Quiz(models.Model):
    user = models.CharField("사용자ID", max_length=20)
    quizTitle = models.CharField("퀴즈 제목", max_length=200)
    quizDetail = models.CharField("퀴즈 지문", max_length=500)
    quizSet = models.ManyToManyField(Set, verbose_name="퀴즈 세트ID", related_name="set_quiz")
    quizTime = models.IntegerField("풀이시간")
    category = models.CharField("퀴즈 카테고리", max_length=8)
    quizChar = models.CharField("퀴즈 캐릭터", max_length=2)
    quizNo = models.CharField("퀴즈 넘버", max_length=4)
    quizType = models.CharField("퀴즈 타입", max_length=1)
    answerCount = models.IntegerField("정답 개수")
    quizValue1 = models.CharField("퀴즈 값1", max_length=50)
    quizValue2 = models.CharField("퀴즈 값2", max_length=50)
    quizValue3 = models.CharField("퀴즈 값3", max_length=50)
    quizValue4 = models.CharField("퀴즈 값4", max_length=50)
    quizValue5 = models.CharField("퀴즈 값5", max_length=50)
    regDate = models.DateTimeField("등록일자", auto_now_add=True)
    chgDate = models.DateTimeField("변경일자", auto_now=True)

