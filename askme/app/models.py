from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import IntegerField

GRADE = [
    (1, 'Like'),
    (-1, "Dislike"),
]

class TagManager(models.Manager):
    def popular_tags(self):
        return self.annotate(num_questions=Count('question')).order_by('-num_questions')[:12]

class AnswerManager(models.Manager):
    def order_by_popularity(self, id):
        return self.filter(question__id=id).order_by('-rating')

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.all_with_num_answers().order_by('-published_date')

    def hot_questions(self):
        return self.all_with_num_answers().order_by('-rating')[:50]

    def all_with_num_answers(self):
        return self.annotate(num_answers=Count('answer'))

    def tag_questions(self, tag_name):
        return self.all_with_num_answers().filter(tags__name=tag_name)

    def get_by_id(self, question_id):
        return self.all_with_num_answers().get(id=question_id)

class ProfileManager(models.Manager):
    def best_members(self):
        return self.annotate(answers=Count('answer')).order_by('-answers')[:10]

class Tag(models.Model):
    name = models.CharField(max_length=20)

    objects = TagManager()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(upload_to="%Y/%m/%d/", default="static/img/picture.png")
    nickname = models.CharField(max_length=256)

    objects = ProfileManager()

    def __str__(self):
        return self.nickname

class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(Profile, models.CASCADE)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(Profile, models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)

    objects = AnswerManager()

class RatingQuestion(models.Model):
    grade = models.IntegerField(choices=GRADE)
    question = models.ForeignKey(Question, models.CASCADE)
    profile = models.ForeignKey(Profile, models.CASCADE)

class RatingAnswer(models.Model):
    grade = models.IntegerField(choices=GRADE)
    answer = models.ForeignKey(Answer, models.CASCADE)
    profile = models.ForeignKey(Profile, models.CASCADE)

