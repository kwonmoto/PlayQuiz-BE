from rest_framework import serializers
from quiz.models import Quiz, QuizSet, Library

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSet
        fields = ("setTitle", "pulickYn")