from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    # correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    # is_correct = models.BooleanField(default=False)
    is_correct = models.CharField(max_length=255)

    def __str__(self):
        return self.text
