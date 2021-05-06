from django.contrib import admin
from django import forms
from .models import Question, Answers, Polls, Statistic


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    pass

@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    pass

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    pass