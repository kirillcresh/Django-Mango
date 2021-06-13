from django.forms import ModelForm, TextInput, Textarea, DateTimeField
from .models import Question, Choice
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']


class CreateChoice(ModelForm):
     class Meta:
        model = Choice
        fields = ['choice_text', 'question']
