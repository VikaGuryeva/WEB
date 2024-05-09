from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
from django.db import transaction
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data population')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        # Create Users and Profiles
        print("Creating users and profiles...")
        users = []
        profiles = []
        for _ in range(max(100, ratio)):
            username = self.generate_unique_username()
            email = fake.email()
            password = fake.password()
            user = User(username=username, email=email)
            users.append(user)
            profile = Profile(user=user, avatar=None)
            profiles.append(profile)

        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)

        # Create Questions, Answers, Tags, and User Likes
        print("Creating questions, answers, tags, and user likes...")
        questions = []
        answers = []
        question_likes = []
        answer_likes = []
        for _ in range(max(100, ratio * 10)):
            user = random.choice(profiles)

            title = fake.sentence()
            question_text = fake.text()
            question = Question(user=user, title=title, question_text=question_text, date_asked=timezone.now())
            questions.append(question)

            # Create Answers
            for _ in range(max(100, ratio * 10)):
                answer_user = random.choice(profiles)
                text = fake.text()
                answer = Answer(user=answer_user, question=question, text=text, date_answered=timezone.now())
                answers.append(answer)

            # Create user likes for questions
            for _ in range(max(200, ratio * 20)):
                like_user = random.choice(profiles)
                question_like = QuestionLike(user=like_user, question=question)
                question_likes.append(question_like)

        Question.objects.bulk_create(questions)
        Answer.objects.bulk_create(answers)
        QuestionLike.objects.bulk_create(question_likes)

        with transaction.atomic():
            for _ in range(max(100, ratio)):
                tag_name = fake.word()
                tag = Tag(name=tag_name)
                tag.save()

            for _ in range(max(20, ratio * 20)):
                answer_like_user = random.choice(profiles)
                answer_like = AnswerLike(user=answer_like_user, answer=random.choice(answers))
                answer_likes.append(answer_like)

            AnswerLike.objects.bulk_create(answer_likes)

        print("Database successfully filled with test data")

    def generate_unique_username(self):
        fake = Faker()
        username = fake.user_name()
        while User.objects.filter(username=username).exists():
            username = fake.user_name()
        return username
