from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
import uuid

class Command(BaseCommand):
    help = "Generates dummy data for db"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Adding Users
        users = []
        for i in range(ratio):
            user = User.objects.create_user(
                username=f'username_{uuid.uuid4().hex[:10]}',
                email=f"user{i}@example.com",
                password="superpass"
            )
            users.append(user)

        # Adding Profiles
        profiles = []
        for user in users:
            profile = Profile.objects.create(user=user)
            profiles.append(profile)

        # Adding tags
        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(name=f"tag{i}")
            tags.append(tag)

        # Adding Questions
        questions = []
        for i in range(ratio):
            for j in range(10):
                question = Question.objects.create(
                    title=f'This is a question #{i * 10 + j}',
                    question_text='This is a content for a question',
                    user=profiles[i]
                )
                questions.append(question)

        # Adding answers
        answers = []
        for i in range(ratio):
            for j in range(100):
                answer = Answer.objects.create(
                    answer_text=f"Answer {i * ratio + j}",
                    user=profiles[i],
                    question=questions[(i * 100 + j) % len(questions)]
                )
                answers.append(answer)

        # Adding tags to questions
        for i, question in enumerate(questions):
            question.tags.add(tags[i % len(tags)], tags[(i + 1) % len(tags)], tags[(i + 2) % len(tags)])

        # Adding likes to questions
        for i in range(ratio):
            for question in questions:
                QuestionLike.objects.create(question=question, user=profiles[i])

        # Adding likes to answers
        for i in range(ratio):
            for answer in answers:
                AnswerLike.objects.create(answer=answer, user=profiles[i])

