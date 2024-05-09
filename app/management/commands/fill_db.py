from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
from django.db.utils import IntegrityError
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
        for _ in range(max(100, ratio)):
            email = self.generate_unique_email()
            username = fake.user_name()  # Создаем случайное имя пользователя, даже если оно не будет использоваться
            password = fake.password()
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, avatar=None)

        # Create Questions, Answers, Tags, and User Likes
        print("Creating questions, answers, tags, and user likes...")
        profiles = Profile.objects.all()
        tags = Tag.objects.all()
        for _ in range(max(100, ratio * 10)):
            # Get a random user
            user = random.choice(profiles)

            title = fake.sentence()
            question_text = fake.text()
            question = Question.objects.create(user=user, title=title, question_text=question_text,
                                               date_asked=timezone.now())

            # Assign Tags to Questions
            question_tags = random.sample(list(tags), min(3, len(tags)))  # Assign up to 3 random tags to the question
            question.tags.add(*question_tags)

            # Create Answers
            for _ in range(max(100, ratio * 10)):
                answer_user = random.choice(profiles)
                text = fake.text()
                answer = Answer.objects.create(user=answer_user, question=question, text=text,
                                               date_answered=timezone.now())

                # Update answer_count field
                question.answer_count = question.answer_set.count()
                question.save()

                # Create user likes for answers
                for _ in range(max(20, ratio * 20)):
                    like_user = random.choice(profiles)
                    try:
                        AnswerLike.objects.create(user=like_user, answer=answer)
                    except IntegrityError:
                        pass

            # Create user likes for questions
            for _ in range(max(200, ratio * 20)):
                like_user = random.choice(profiles)
                try:
                    QuestionLike.objects.create(user=like_user, question=question)
                except IntegrityError:
                    pass



        print("Database successfully filled with test data")

    def generate_unique_email(self):
        fake = Faker()
        email = fake.email()
        while User.objects.filter(email=email).exists():
            email = fake.email()
        return email
