from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question_text = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True)
    answer_count = models.IntegerField(default=0)  # Новое поле
    tags = models.ManyToManyField('Tag', related_name='questions')  # Многие ко многим

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()
    date_answered = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text[:50]

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('question', 'user'),)

    @classmethod
    def like_question(cls, question, user):
        try:
            objs = [cls(question=question, user=user) for _ in range(100)]
            cls.objects.bulk_create(objs)
        except IntegrityError:
            pass

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('answer', 'user'),)

    @classmethod
    def like_answer(cls, answer, user):
        try:
            objs = [cls(answer=answer, user=user) for _ in range(100)]
            cls.objects.bulk_create(objs)
        except IntegrityError:
            pass
