import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Question")
    pub_date = models.DateTimeField(default=timezone.now(), verbose_name="Published date")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return f'/polls/{self.id}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question")
    choice_text = models.CharField(max_length=200, verbose_name="Choice")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def get_absolute_url(self):
        return f'/polls/'
