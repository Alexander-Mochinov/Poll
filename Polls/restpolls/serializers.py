from rest_framework import serializers
from question.models import Polls, Question, Answers, Statistic

class PollsSerializer(serializers.ModelSerializer):
    """Сериализация модели опроса"""

    class Meta:
        model = Polls
        fields = '__all__'

    def create(self, validated_data):
        return Polls.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализация модели вопроса"""
    poll = PollsSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['questiontext', 'poll', 'countanswers', 'countanswersmaxсhoice']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class AnswersSerializer(serializers.ModelSerializer):
    """Сериализация модели ответа"""
    question = QuestionSerializer( read_only=True)
    class Meta:
        model = Answers
        fields = ['answerstext','question']

    def create(self, validated_data):
        return Answers.objects.create(**validated_data)


class StatisticSerializer(serializers.ModelSerializer):
    """Сериализация модели статистики"""
    answers = AnswersSerializer(read_only=True)
    class Meta:
        model = Statistic
        fields = ['user', 'answers']

class StatisticSetSerializer(serializers.ModelSerializer):
    """Сериализация модели статистики"""
    class Meta:
        model = Statistic
        fields = ['user', 'answers']
