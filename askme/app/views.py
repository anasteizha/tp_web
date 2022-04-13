from django.shortcuts import render

from app.models import *
from pagination import paginate

# Create your views here.

def index(request):
    context = {"page_obj": paginate(Question.objects.all(), request),
            "popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}

    return render(request, "index.html", context)


def hot(request):
    context = {"page_obj": paginate(Question.objects.hot_questions(), request),
            "popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "hot.html", context)

def tag(request, tag_name: str):
    context = {"tag": tag_name,
            "page_obj": paginate(Question.objects.tag_questions(tag_name), request),
            "popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "tag.html", context)

def question(request, i: int):
    context = {"question": Question.objects.get_by_id(i),
            "popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "page_obj": paginate(Answer.objects.order_by_popularity(i), request)}
    return render(request, "question.html", context)

def login(request):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "login.html", context)

def signup(request):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "signup.html", context)

def ask(request):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "ask.html", context)

def settings(request):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "settings.html", context)

def page_not_found(request, exception):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "page_not_found.html", context, status=404)

