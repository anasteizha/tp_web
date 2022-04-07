from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

QUESTION_TAGS = ["Python", "MySQL", "C++", "PHP"]

QUESTIONS = [
    {
        "title": f"Title №{i + 1}",
        "text": f"This is text for question №{i + 1}",
        "number": i,
        "tags": QUESTION_TAGS
    } for i in range(100)
]

ANSWERS = [
    {
        "title": f"Title №{i + 1}",
        "text": f"This is text for answer №{i + 1}"
    } for i in range(20)
]

POPULAR_TAGS = ["MySQL", "Python", "C#", "C++", "Java", "C", "HTML", "Android", "PHP", "CSS", "JavaScript", "Django"]

BEST_MEMBERS = ["Masha", "Sasha", "Petya", "Ivan"]

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return page_obj

def index(request):
    context = {"page_obj": paginate(QUESTIONS, request),
            "popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS,}

    return render(request, "index.html", context)

def hot(request):
    context = {"page_obj": paginate(QUESTIONS, request),
            "popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "hot.html", context)

def tag(request, tag_name: str):
    context = {"tag": tag_name,
            "page_obj": paginate(QUESTIONS, request),
            "popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "tag.html", context)

def question(request, i: int):
    context = {"question": QUESTIONS[i],
            "popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS,
            "page_obj": paginate(ANSWERS, request)}
    return render(request, "question.html", context)

def login(request):
    context = {"popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "login.html", context)

def signup(request):
    context = {"popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "signup.html", context)

def ask(request):
    context = {"popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "ask.html", context)

def settings(request):
    context = {"popular_tags": POPULAR_TAGS,
            "best_members": BEST_MEMBERS}
    return render(request, "settings.html", context)

