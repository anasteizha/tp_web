import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askme.settings")

django.setup()

from django.contrib.auth.models import User
from django.db.models import Sum
from app.models import *

total_answers = 0
total_questions = 0

def generate_tags(num_records_per_query):
    for i in range(num_records_per_query):
        yield Tag(name=f"tag {i + 1}")

def create_tags():
    print("Creating tags")
    Tag.objects.bulk_create(generate_tags(10001))

def generate_profiles(num_records_per_query):
    for i in range(num_records_per_query):
        yield Profile(user_id=i + 1, nickname=f"Nick {i + 1}")

def generate_users():
    for i in range(1, 10002):
        yield User(username=f'user_{i}')


def create_profiles():
    print("Creating profiles")
    User.objects.bulk_create(generate_users())

    Profile.objects.bulk_create(generate_profiles(10001))

count_questions = 0
count_answers = 0

def generate_rating_question(num_records_per_query):
    for i in range(num_records_per_query):
        yield RatingQuestion(grade=1, question_id=(count_questions % 100010) + 1, profile_id=i + 1)
        count_questions += 1

def create_rating_question():
    print("Creating ratings questions")
    for j in range(0, 2000000, 10001):
        RatingQuestion.objects.bulk_create(generate_rating_question(10001))

def generate_rating_answer(num_records_per_query):
    for i in range(num_records_per_query):
        yield RatingAnswer(grade=1, answer_id=(count_answers % 1000100) + 1, profile_id=i + 1)
        count_answers += 1

def create_rating_answer():
    print("Creating ratings answers")
    for j in range(0, 2000000, 10001):
        RatingAnswer.objects.bulk_create(generate_rating_answer(10001))

def generate_answers(num_records_per_query):
    for i in range(num_records_per_query):
        yield Answer(text=f"This is text for answer №{total_answers + 1}",
        profile_id=i + 1,
        question_id=(count_questions % 100010) + 1)
        count_questions += 1
        total_answers += 1

def create_answers():
    print("Creating answers")
    for j in range(0, 1000000, 10001):
        Answer.objects.bulk_create(generate_answers(10001))
    count_questions %= count_questions

def generate_questions(num_records_per_query):
    for i in range(num_records_per_query):
        yield Question(title=f"Title №{total_questions + 1}",
        text=f"This is text for question №{total_questions + 1}",
        profile_id=i + 1)
        total_questions += 1

def change_questions():
    for i in range(10001):
        #Question.objects.all().get(id=i + 1).tags.add(Tag.objects.get(id=i % 10001 + 3))
        #Question.objects.all().get(id=i + 1).tags.add(Tag.objects.get(id=i % 10000 + 2))
        yield Question.objects.all().get(id=i + 1).tags.add(Tag.objects.get(id=i % 9999 + 1))

def create_questions():
    print("Creating questions")
    for j in range(0, 100000, 10001):
        Question.objects.bulk_create(generate_questions(10001))

    for j in range(0, 100000, 10001):
        Question.objects.bulk_update(change_questions(), ['tags'])

def count_rating_questions():
    print("Count rating questions")
    Question.objects.annotate(rating=Sum('RatingQuestion__grade'))

def count_rating_answers():
    print("Count rating answers")
    Answer.objects.annotate(rating=Sum('RatingAnswer__grade'))


def create_records():
    create_tags()
    create_profiles()
    create_questions()
    create_answers()
    create_rating_question()
    create_rating_answer()
    count_rating_questions()
    count_rating_answers()
    


if (__name__ == "__main__"):
    create_records()

