
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from app.models import Question, Answer, Profile, Tag, get_basecontext

from django.http import Http404
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
# Create your views here.

from django.http import HttpResponse



def index(request):
    questions = Question.objects.get_new_questions()
    page_obj = paginate(request, questions, 5)
    return render(request, "index.html", {"current": "New Questions",
                                          "other": "Hot Questions",
                                          "questions": page_obj})


def hot(request):
    questions = Question.objects.get_best_questions()
    page_obj = paginate(request, questions, 5)
    return render(request,"hot.html", {"current": "Hot Questions",
                                            "other": "New Questions",
                                            "questions": page_obj})


def question(request, question_id):
    questions = Question.objects.get_question(question_id)
    answer = Answer.objects.get_by_question_id(question_id)
    page_obj = paginate(request, answer, 5)
    return render(request, "question_detail.html", {"question": questions[0], "answers": page_obj})


def tag(request, tag_name):
    que = Question.objects.get_by_tag(tag_name)

    page_obj = paginate(request, que, 5)
    return render(request, "tag.html", {"questions": page_obj, "tag": tag_name})





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




def paginate(request, objects_list, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        obj = paginator.page(page_num)

    except PageNotAnInteger:
        obj = paginator.page(1)

    except EmptyPage:
        obj = paginator.page(paginator.num_pages)

    return obj
