from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProfileManager(models.Manager):
    def get_best_members(self):
        return self.all()[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', default="no_avatar.jpg", null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.name


class TagManager(models.Manager):
    def get_popular(self):
        return self.all()[:5]


class QuestionManager(models.Manager):
    def get_best_questions(self):
        return self.order_by('-rating')[:100]




    def get_new_questions(self):
        return self.order_by('-date_asked')[:100]

    def get_question(self, question_id):
        return self.filter(id=question_id)

    def get_by_tag(self, category):
        return self.filter(tags__name=category)

class AnswerManager(models.Manager):
    def get_by_question_id(self, question_id):
        question = Question.objects.get(id=question_id)
        return self.filter(question=question)



class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    COLORS = [
        'text-bg-primary',
        'text-bg-warning',
        'text-bg-secondary',
        'text-bg-success',
        'text-bg-danger',
        'text-bg-info',
    ]

    objects = TagManager()

    def __str__(self):
        return self.name

    def random_color(self):
        from random import randint
        return self.COLORS[randint(0, len(self.COLORS) - 1)]


class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question_text = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("question", kwargs={"question_id": self.id})

    def answer_number(self):
        return Answer.objects.filter(question=self).count()

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def update_rating(self):
        self.update(rating=QuestionLike.objects.filter(question=self).count())

    class Meta:
        ordering = ["-date_asked"]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    text = models.TextField()
    date_answered = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'{self.user.name} to "{self.question.title}": "{self.text}"'

    def str(self):
        return self.text[:50]


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = [["user", "question"]]


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["user", "answer"]]


def get_basecontext():
    return {"popular_tags": Tag.objects.get_popular(),
            "best_members": Profile.objects.get_best_members(),
            "is_authorized": True,
            "user": Profile.objects.first()
            }