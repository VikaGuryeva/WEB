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

        # Создание пользователей и профилей
        for _ in range(max(10, ratio)):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, avatar=None)

        # Создание вопросов, ответов, тегов и оценок пользователей
        for _ in range(max(10, ratio * 10)):
            # Получаем случайного пользователя
            user = random.choice(Profile.objects.all().prefetch_related('user'))

            title = fake.sentence()
            question_text = fake.text()
            question = Question.objects.create(user=user, title=title, question_text=question_text,
                                               date_asked=timezone.now())

            # Создание ответов
            for _ in range(max(10, ratio)):
                answer_user = random.choice(Profile.objects.all().prefetch_related('user'))
                answer_text = fake.text()
                answer = Answer.objects.create(user=answer_user, question=question, answer_text=answer_text,
                                               date_answered=timezone.now())

                # Обновление поля answer_count
                question.answer_count = question.answer_set.count()
                question.save()

                # Создание оценок пользователей для ответов
                for _ in range(max(2, ratio)):
                    like_user = random.choice(Profile.objects.all().prefetch_related('user'))
                    try:
                        AnswerLike.objects.create(user=like_user, answer=answer)
                    except IntegrityError:
                        pass

            # Создание оценок пользователей для вопросов
            for _ in range(max(20, ratio * 2)):
                like_user = random.choice(Profile.objects.all().prefetch_related('user'))
                try:
                    QuestionLike.objects.create(user=like_user, question=question)
                except IntegrityError:
                    pass

        # Создание тегов
        for _ in range(max(100, ratio)):
            tag_name = fake.word()
            Tag.objects.create(tag_name=tag_name)

        self.stdout.write(self.style.SUCCESS('Database successfully filled with test data'))

