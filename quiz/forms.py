# quiz/forms.py
from django import forms
from .models import Question


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['question'] = forms.CharField(widget=forms.HiddenInput(), initial=question.id)
        self.fields['answer'] = forms.ChoiceField(
            choices=[(answer.id, answer.answer_text) for answer in question.answers.all()],
            widget=forms.RadioSelect
        )

    def save(self, user):
        cleaned_data = self.cleaned_data
        question_id = cleaned_data['question']
        selected_answer_id = cleaned_data['answer']
        question = Question.objects.get(id=question_id)
        selected_answer = question.answers.get(id=selected_answer_id)
        is_correct = (selected_answer.answer_text == question.correct_answer)

        user_response = UserResponse.objects.create(
            user=user,
            question=question,
            selected_answer=selected_answer,
            is_correct=is_correct
        )
        return user_response
