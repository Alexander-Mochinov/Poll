from django.urls import path
from .views import PollsView, AnswerView, QuestionView, StatisticView

app_name = "restpolls"



urlpatterns = [
    path('polls/', PollsView.as_view()),
    path('polls/<int:pk>/', PollsView.as_view()),


    path('answers/', AnswerView.as_view()),
    path('answers/<int:pk>/', AnswerView.as_view()),

    path('question/', QuestionView.as_view()),
    path('question/<int:pk>/', QuestionView.as_view()),

    path('statistic/', StatisticView.as_view()),
    path('statistic/<int:pk>/', StatisticView.as_view()),
]