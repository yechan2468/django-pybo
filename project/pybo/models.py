from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='author_question')
    content = models.TextField()
    voter = models.ManyToManyField(User, related_name='voter_question')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.subject

    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='author_answer')
    content = models.TextField()
    voter = models.ManyToManyField(User, related_name='voter_answer')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return 'A) ' + self.question.subject

class Comment(models.Model):
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
    