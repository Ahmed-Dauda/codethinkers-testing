# tests.py
from django.test import TestCase
from .models import Quiz, Question

class QuizModelTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='Sample Quiz', description='A sample quiz for testing.')

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, 'Sample Quiz')
        self.assertEqual(self.quiz.description, 'A sample quiz for testing.')

class QuestionModelTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='Sample Quiz', description='A sample quiz for testing.')
        self.question = Question.objects.create(quiz=self.quiz, question_text='What is 2 + 2?', option_a='3', option_b='4', option_c='5', option_d='6', correct_option='B')

    def test_question_creation(self):
        self.assertEqual(self.question.question_text, 'What is 2 + 2?')
        self.assertEqual(self.question.correct_option, 'B')