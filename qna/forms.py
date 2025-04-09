from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question',]


class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['answer',]

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.question:
            already_answered = Answer.objects.filter(
                user=self.user, question=self.question).exists()
            if already_answered:
                raise ValidationError(
                    "You have already answered this question.")
        return cleaned_data
