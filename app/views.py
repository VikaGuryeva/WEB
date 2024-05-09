
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
    context = get_basecontext()
    page_obj = paginate(request, questions, 5)

    # Добавление дополнительного контекста
    extra_context = {
        "current": "New Questions",
        "other": "Hot Questions",
        "questions": page_obj,
    }
    context.update(extra_context)

    return render(request, "index.html", context)



def hot(request):
    questions = Question.objects.get_best_questions()
    context = get_basecontext()
    page_obj = paginate(request, questions, 5)

    # Добавление дополнительных переменных контекста
    extra_context = {
        "current": "Hot Questions",
        "other": "New Questions",
        "questions": page_obj,
    }
    context.update(extra_context)

    return render(request, "hot.html", context)


def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = Answer.objects.get_by_question_id(question_id)
    context = get_basecontext()
    page_obj = paginate(request, answers, 5)

    # Добавление дополнительных переменных контекста
    extra_context = {
        "question": question[0],
        "answers": page_obj,
    }
    context.update(extra_context)

    return render(request, "question_detail.html", context)


def tag(request, tag_name):
    context = get_basecontext()
    questions = Question.objects.get_by_tag(tag_name)
    page_obj = paginate(request, questions, 5)

    # Добавление дополнительных переменных контекста
    extra_context = {
        "questions": page_obj,
        "tag": tag_name,
    }
    context.update(extra_context)

    return render(request, "tag.html", context)


def ask(request):
    context = get_basecontext()
    if not context['is_authorized']:
        return HttpResponseRedirect(reverse('login'))
    context['tag_err'] = False
    return render(request, "ask.html", context)



def settings(request):
    context = get_basecontext()
    return render(request, "settings.html", context)



def register(request, profile_id, tag_name):
    context = get_basecontext()
    profile = get_object_or_404(Profile, pk=profile_id)
    tag = Tag.objects.get(name=tag_name)
    return render(request, "register.html", context)


def login(request):
    context = get_basecontext()
    return render(request, "login.html", context)


def signup(request):
    context = get_basecontext()
    return render(request, "signup.html", context)


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
