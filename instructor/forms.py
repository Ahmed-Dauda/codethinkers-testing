# instructor/forms.py
from django import forms
from sms.models import Courses
from quiz.models import QuestionAssessment, TopicsAssessment
from sms.models import Topics


class TopicsAssessmentForm(forms.ModelForm):
    class Meta:
        model = TopicsAssessment
        fields = '__all__'
        widgets = {
            'course_name': forms.Select(attrs={
                'class': 'form-control select2'
            })
        }


class TopicsForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = [
            'categories',
            'courses',
            'title',
            'desc',
            'transcript',
            'img_topic',
            'video',
            'topics_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic Title'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Topic Description'}),
            'transcript': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Transcript'}),
            'topics_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional URL'}),
        }


class QuestionAssessmentForm(forms.ModelForm):

    class Meta:
        model = QuestionAssessment
        fields = [
            'course',
            'marks',
            'question',
            'img_quiz',
            'option1',
            'option2',
            'option3',
            'option4',
            'answer',
        ]

        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'option1': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'option2': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'option3': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'option4': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'answer': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional UX polish
        self.fields['course'].empty_label = "Select Topic / Assessment"
        self.fields['img_quiz'].required = False



class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = [
            'img_course',
            'course_logo',
            'title',
            # 'course_owner',
            'course_type',
            'status_type',
            'price',
            'cert_price',
            'categories',
            'prerequisites',
            'desc',
            'is_programming',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course title'
            }),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'status_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cert_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'prerequisites': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Course description'
            }),
            'is_programming': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from quiz.models import Course  # Make sure this is the correct import path

class CourseQuizForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'categories',
            'room_name',
            'schools',
            'course_name',
            'question_number',
            'course_pay',
            'full_screen',
            'total_marks',
            'session',
            'term',
            'exam_type',
            'num_attemps',
            'show_questions',
            'pass_mark',
            'duration_minutes',
        ]

        widgets = {
            'categories': forms.Select(attrs={'class': 'form-select'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room name'}),
            'schools': forms.Select(attrs={'class': 'form-select'}),
            'course_name': forms.Select(attrs={'class': 'form-select'}),
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_pay': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'full_screen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
            'term': forms.Select(attrs={'class': 'form-select'}),
            'exam_type': forms.Select(attrs={'class': 'form-select'}),
            'num_attemps': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_questions': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
        }


