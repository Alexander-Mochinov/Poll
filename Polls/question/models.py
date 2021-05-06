# -*- coding=utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from datetime import timedelta, datetime
from django.urls import reverse
from django.forms.models import model_to_dict
from django.utils import timezone




class Polls(models.Model):
    """Модель опроса"""
    namepolls = models.CharField(verbose_name='Название опроса', max_length=255, blank=False)
    datestart = models.DateTimeField(verbose_name='Дата начала опроса', default=timezone.now)
    dateend = models.DateTimeField(verbose_name='Дата конца опроса', default=timezone.now)
    descriptions = models.TextField(verbose_name='Описание опроса', null=True)
    def __str__(self):
        return self.namepolls

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        db_table = 'polls'

class Question(models.Model):
    """Модель вопроса для опроса"""
    questiontext = models.CharField(verbose_name='Вопрос', max_length=255, blank=False)
    poll = models.ForeignKey(Polls, verbose_name='Вопрос', null=True, on_delete=models.SET_NULL)
    countanswers = models.PositiveIntegerField(verbose_name='Кол-во ответор для вопроса', null=False)
    countanswersmaxсhoice = models.PositiveIntegerField(verbose_name='Кол-во ответор для вопроса', null=False, default=1)

    def __str__(self):
        return self.questiontext

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'question'


class Answers(models.Model):
    """Модель ответа для опроса"""
    answerstext = models.CharField(verbose_name='Ответ для вопроса', max_length=255, null=False)
    question = models.ForeignKey(Question, verbose_name='Вопрос', null=True, on_delete=models.SET_NULL)


    def CreatePollAnswer(poll_id, answerstext):
        poll = Polls.objects.get(id = poll_id)
        if poll.annotate(created_count=Count('id')) < poll.question.countanswers:
            answer = Answers.objects.create(
                answerstext = answerstext,
                question = poll.question
            )
            return answer
        else:
            return 'Нельзя создать ещё ответ для данного вопроса !'


    def __str__(self):
        return 'ID Question: ' + str(self.question.questiontext) + ' Question: ' + str(self.question) + ', ' + str(self.answerstext)

    def CountOfAnswer(id_answer) -> int:
        return Statistic.objects.filter(answers__id = id_answer).count

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        db_table = 'answers'


class Statistic(models.Model):
    """Статистика опросов"""
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete = models.SET_NULL, null=True)
    answers = models.ForeignKey(Answers, verbose_name='Ответ', related_name='answers_options', on_delete=models.SET_NULL, null=True)

    # views = models.IntegerField('Просмотры', default=0) 
    def __str__(self):
        return str(self.user) + ' ' + str(self.answers)

    class Meta:
        verbose_name = 'Статистика опросов'
        verbose_name_plural = 'Статистика опроса'
        db_table = 'statistic'

