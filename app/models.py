from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProfileManager(models.Manager):
    def get_best_members(self):
        return self.all()[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_popular(self):
        return self.all()[:5]


class QuestionManager(models.Manager):
    def get_best_questions(self):
        return self.order_by('-answer_count')[:5]

    def get_new_questions(self):
        return self.order_by('-date_asked')[:5]

    def get_question(self, question_id):
        return self.filter(id=question_id)

    def get_by_tag(self, tag_name):
        tag = get_object_or_404(Tag, tag_name=tag_name)
        return self.filter(tags=tag)


class AnswerManager(models.Manager):
    def get_by_question_id(self, question_id):
        question = Question.objects.get(id=question_id)
        return self.filter(question=question)


class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question_text = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True)
    answer_count = models.IntegerField(default=0)

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

    def str(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    answer_text = models.TextField()
    date_answered = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'{self.user.username} to "{self.question.title}": "{self.answer_text}"'

    def str(self):
        return self.answer_text[:50]


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)



    class Meta:
        unique_together = (('question', 'user'),)

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('answer', 'user'),)

def get_base_layout_context():
    return {"popular_tags": Tag.objects.get_popular(),
            "best_members": Profile.objects.get_best_members(),
            "is_authorized": True,
            "user": Profile.objects.first()}