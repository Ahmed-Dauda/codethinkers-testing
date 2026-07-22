from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from .models import Quiz, Question, Answer, StudentScore


class QuizListView(ListView):
    model = Quiz
    template_name = "quiz_list.html"
    paginate_by = 25


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quiz_detail.html"

    def get_queryset(self):
        return Quiz.objects.prefetch_related("questions")


class SubmitAnswerView(View):
    template_name = "quiz_detail.html"

    def post(self, request, quiz_id):
        quiz = get_object_or_404(
            Quiz.objects.prefetch_related("questions"),
            pk=quiz_id
        )

        correct_answers = 0

        for question in quiz.questions.all():
            selected_option = request.POST.get(f"question_{question.id}")

            if selected_option in ["A", "B", "C", "D"]:
                Answer.objects.create(
                    question=question,
                    selected_option=selected_option
                )

                if selected_option == question.correct_option:
                    correct_answers += 1

        StudentScore.objects.create(
            quiz=quiz,
            score=correct_answers
        )

        return redirect("cbt:quiz_detail", pk=quiz.pk)
        

class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"
    paginate_by = 25
    ordering = ["-id"]