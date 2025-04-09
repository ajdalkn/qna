from django.db import models

from users.models import User


# Create your models here.
class AbstractDateBase(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractUserBase(models.Model):
    created_by = models.ForeignKey(User,
                                   related_name='%(class)s_createdby',
                                   blank=True, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User,
                                    related_name='%(class)s_modifiedby',
                                    null=True, blank=True,
                                    on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Question(AbstractDateBase, AbstractUserBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='questions')
    question = models.TextField()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question[:400]


class Answer(AbstractDateBase, AbstractUserBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')
    answer = models.TextField()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        unique_together = ('user', 'question')

    def __str__(self):
        return self.answer[:400]


class Like(AbstractDateBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,
                             related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')
