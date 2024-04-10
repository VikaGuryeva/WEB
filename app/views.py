from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
from django.shortcuts import get_object_or_404
from django.http import Http404
# Create your views here.

from django.http import HttpResponse
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(200)
]
POPULAR = {
    "tags": [f"tag{i+1}" for i in range(5)],
    "users": [f"user{i+1}" for i in range(5)]
}


def index(request):
    questions = Question.objects.order_by('-date_asked')
    page_obj = paginator(questions, request)
    return render(request, "index.html", {"current": "New Questions",
                                          "other": "Hot Questions",
                                          "questions": page_obj,
                                          "popular": POPULAR})


def hot(request):
    questions = Question.objects.order_by('-questionlike')[:10]
    page_obj = paginator(questions, request)
    return render(request,"hot.html", {"current": "Hot Questions",
                                            "other": "New Questions",
                                            "questions": page_obj,
                                            "popular": POPULAR})


def question(request, question_id):
    questions = get_object_or_404(Question, pk=question_id)
    answers = questions.answer_set.all()

    return render(request,"question_detail.html", {"question": questions, 'answers': answers})

def question_detail(request, question_id):

    return render(request, "question_detail.html", {"question": question, 'answers': answers})

def ask(request):

    return render(request, "ask.html", {"page_title": "Ask", "popular": POPULAR})


def settings(request):
    context = {
        "page_title": "Settings",
        "settings": {
            "current_login": "Dr. Pepper",
            "current_email": "example@mail.com",
            "current_NickName": "VIKA_Guryeva"
        },
        "popular": POPULAR
    }
    return render(request, 'settings.html', context)


def register(request, profile_id, tag_name):
    profile = get_object_or_404(Profile, pk=profile_id)
    tag = Tag.objects.get(name=tag_name)
    return render(request, "register.html", {"page_title": profile, "popular": POPULAR})


def login(request):
    return render(request, 'login.html', {"page_title": "Login", "popular": POPULAR})


def tag(request, tag_name):
    tags = get_object_or_404(Tag, tag_name=tag_name)
    page_obj = paginator(tags, request)

    return render(request, "tag.html", {"page_title": tags,
                                        "questions": page_obj})


def paginator(objects_list, request, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    return paginator.page(page_num)