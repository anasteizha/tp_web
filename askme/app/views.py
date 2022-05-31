from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from app.models import *
from pagination import paginate

from app.forms import LoginForm, SignupForm, SettingsForm, QuestionForm, AnswerForm

from askme.settings import DEFAULT_AVATAR

def index(request):
    context = {"page_obj": paginate(Question.objects.all_with_num_answers(), request),
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

def login(request):
    if request.method == 'GET':
        user_form = LoginForm()

    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
            else:
                user_form.add_error(None, "User not found")
                
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "form": user_form}
    return render(request, "login.html", context)

def signup(request):
    if request.method == "GET":
        user_form = SignupForm()
    else:
        user_form = SignupForm(data=request.POST)
        if user_form.is_valid():
            try:
                User.objects.get(username=user_form.cleaned_data['username'], email=user_form.cleaned_data['email'])
            except User.DoesNotExist:
                user_form.cleaned_data.pop("password_repeat")
                user_avatar = user_form.cleaned_data.pop("avatar")
                if not user_avatar:
                    user_avatar = DEFAULT_AVATAR
                user = User.objects.create_user(**user_form.cleaned_data)
                Profile.objects.create(user=user, avatar=user_avatar)
                return redirect(reverse("index"))
            else:
                user_form.add_error(None, "User exist")

    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "form":user_form}
    return render(request, "signup.html", context)

@login_required
def settings(request):
    if request.method == "GET":
        _profile = Profile.objects.get(user=request.user)
        _data = {"username": _profile.user.username, "email": _profile.user.email,
                 "nickname": _profile.user.first_name}
        form = SettingsForm(initial=_data)
    else:
        form = SettingsForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("settings"))

    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "form": form}

    return render(request, 'settings.html', context)

def page_not_found(request, exception):
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members()}
    return render(request, "page_not_found.html", context, status=404)

@login_required
def ask(request):
    if request.method == "GET":
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.profile = Profile.objects.get(user=request.user)
            question.save()
            for tag in form.cleaned_data['tags'].split():
                new = Tag.objects.get_or_create(name=tag)[0]
                question.tags.add(new)
            question.save()
            return redirect("question", question.id)
        form.save()
    context = {"popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "form": form}
    return render(request, "ask.html", context)

def question(request, i):
    if request.method == 'GET':
        form = AnswerForm()
    else:
        if not request.user.is_authenticated:
            return redirect("login")
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            question = Question.objects.get(id=i)
            ans.profile = profile
            ans.question = question
            ans.save()
            return redirect("question", i)

    context = {"question": Question.objects.get_by_id(i),
            "popular_tags": Tag.objects.popular_tags(),
            "best_members": Profile.objects.best_members(),
            "page_obj": paginate(Answer.objects.order_by_popularity(i), request),
            "form": form}
    return render(request, "question.html", context)

