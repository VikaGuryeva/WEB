from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data population')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        fake = Faker()

        # Создание пользователей
        existing_usernames = set(User.objects.values_list('username', flat=True))
        for _ in range(max(10, ratio)):
            username = fake.user_name()
            while username in existing_usernames:
                username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(username=username, email=email, password=password)
            existing_usernames.add(username)

        # Создание вопросов, ответов, тегов и оценок пользователей
        for _ in range(max(10, ratio * 10)):
            # Создание вопроса
            user = User.objects.order_by('?').first()
            title = fake.sentence()
            question_text = fake.text()
            question = Question.objects.create(user=user, title=title, question_text=question_text)

            # Создание ответов
            for _ in range(max(10, ratio)):
                answer_user = User.objects.order_by('?').first()
                answer_text = fake.text()
                answer = Answer.objects.create(user=answer_user, question=question, answer_text=answer_text)

                # Обновление поля answer_count
                question.answer_count = question.answer_set.count()
                question.save()

                # Создание оценок пользователей для ответов
                for _ in range(max(2, ratio)):
                    like_user = User.objects.order_by('?').first()
                    try:
                        AnswerLike.objects.create(user=like_user, answer=answer)
                    except IntegrityError:
                        pass

            # Создание оценок пользователей для вопросов
            for _ in range(max(20, ratio * 2)):
                like_user = User.objects.order_by('?').first()
                try:
                    QuestionLike.objects.create(user=like_user, question=question)
                except IntegrityError:
                    pass

        # Создание тегов
        for _ in range(max(100, ratio)):
            tag_name = fake.word()
            Tag.objects.create(tag_name=tag_name)

        self.stdout.write(self.style.SUCCESS('Database successfully filled with test data'))
