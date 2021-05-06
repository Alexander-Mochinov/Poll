from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from question.models import Polls, Question, Answers, Statistic
from .serializers import PollsSerializer, AnswersSerializer, QuestionSerializer, StatisticSerializer, StatisticSetSerializer

class PollsView(APIView):
    def get(self, request):
        polls = Polls.objects.all()
        serializer = PollsSerializer(polls, many=True)
        return Response({"polls": serializer.data})

    def post(self, request):
        polls = request.data.get('polls')
        serializer = PollsSerializer(data=polls)
        if serializer.is_valid(raise_exception=True):
            polls_saved = serializer.save()
            return Response({
                "success": "Опрос '{}' успешно создан".format(polls_saved.namepolls)
            })
        else:
            return Response({
                "error" : "Что то пошло не так, проверьте установленные вами значения"
            })

    def put(self, request, pk):
        saved_polls = get_object_or_404(Polls.objects.all(), pk=pk)
        data = request.data.get('polls')
        serializer = PollsSerializer(instance=saved_polls, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            polls_saved = serializer.save()
            return Response({
                "success": "Опрос '{}' успешно обновлен".format(polls_saved.namepolls)
            })
        else:
            return Response({
                "error" : "Что то пошло не так, проверьте установленные вами значения"
            })

    def delete(self, request, pk):
        polls = get_object_or_404(Polls.objects.all(), pk=pk)
        polls.delete()
        return Response({
            "message": "Опрос с id `{}` был удалён.".format(pk)
        }, status=204)

class AnswerView(APIView):
    def get(self, request):
        answers = Answers.objects.all()
        serializer = AnswersSerializer(answers, many=True)
        return Response({"answers": serializer.data})

    def post(self, request):
        answers = request.data.get('answers')
        serializer = AnswersSerializer(data=answers)
        if serializer.is_valid(raise_exception=True):
            answers_saved = serializer.save()
            return Response({"success": "Ответ на вопрос '{}' успешно создан".format(answers_saved.answerstext)})
        else:
            return Response({"error" : "Что то пошло не так, проверьте установленные вами значения"})

    def put(self, request, pk):
        saved_answers = get_object_or_404(Answers.objects.all(), pk=pk)
        data = request.data.get('answers')
        serializer = AnswersSerializer(instance=saved_answers, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            answers_saved = serializer.save()
            return Response({
                "success": "Ответ на вопрос '{}' успешно обновлен".format(answers_saved.answerstext)
            })
        else:
            return Response({
                "error" : "Что то пошло не так, проверьте установленные вами значения"
            })

    def delete(self, request, pk):
        answers = get_object_or_404(Answers.objects.all(), pk=pk)
        answers.delete()
        return Response({
            "message": "Ответ на вопрос с id `{}` был удалён.".format(pk)
        }, status=204)



class QuestionView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response({"questions": serializer.data})

    def post(self, request):
        questions = request.data.get('questions')
        getpoll = Polls.objects.get(id = questions['poll'])
        if getpoll.datestart:
            serializer = QuestionSerializer(data=questions)
            if serializer.is_valid(raise_exception=True):
                questions_saved = serializer.save()
                return Response({"success": "Вопрос '{}' успешно создан".format(questions_saved.questiontext)})
            else:
                return Response({"error" : "Что то пошло не так, проверьте установленные вами значения"})
        else:
            return Response({
                "error" : "Для текущего опроса нельзя создать новый вопрос, превышен временной лимит"
            })
    def put(self, request, pk):
        saved_questions = get_object_or_404(Question.objects.all(), pk=pk)
        data = request.data.get('questions')
        if saved_questions.poll.datestart: 
            serializer = QuestionSerializer(instance=saved_questions, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                questions_saved = serializer.save()
                return Response({
                    "success": "Вопрос '{}' успешно обновлен".format(questions_saved.questiontext)
                })
            else:
                return Response({
                    "error" : "Что то пошло не так, проверьте установленные вами значения"
                })
        else:
            return Response({
                "error" : "Для текущего опроса нельзя обновлять данные, превышен временной лимит"
            })

    def delete(self, request, pk):
        answers = get_object_or_404(Question.objects.all(), pk=pk)
        if answers.poll.datestart: 
            answers.delete()
            return Response({
                "message": "Вопрос с id `{}` был удалён.".format(pk)
            }, status=204)
        else:
            return Response({
                "error" : "Для текущего опроса нельзя удалить данные, превышен временной лимит"
            })

class StatisticView(APIView):
    def get(self, request, pk = None):
        if pk:
            statistic = Statistic.objects.filter(user__id = pk)
        else:
            statistic = Statistic.objects.all()

        serializer = StatisticSerializer(statistic, many=True)
        return Response({"statistic": serializer.data})

    def post(self, request):
        statistic = request.data.get('statistic')
        if statistic['user']:
            serializer = StatisticSerializer(data=statistic)
        else:
            serializer = StatisticSetSerializer(data=statistic)
        if serializer.is_valid(raise_exception=True):
            statistic_saved = serializer.save()
            return Response({"success": "Статистика '{}' успешно создан".format(statistic_saved.answers)})
        else:
            return Response({"error" : "Что то пошло не так, проверьте установленные вами значения"})
            
    def put(self, request, pk):
        saved_statistic = get_object_or_404(Question.objects.all(), pk=pk)
        data = request.data.get('statistic')
        serializer = StatisticSerializer(instance=saved_statistic, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            statistic_saved = serializer.save()
            return Response({
                "success": "Статистика '{}' успешно обновлен".format(statistic_saved.answers)
            })
        else:
            return Response({
                "error" : "Что то пошло не так, проверьте установленные вами значения"
            })

    def delete(self, request, pk):
        statistic = get_object_or_404(Statistic.objects.all(), pk=pk)
        statistic.delete()
        return Response({
            "message": "Статистика с id `{}` был удалён.".format(pk)
        }, status=204)
