import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askme.settings")

django.setup()

from django.contrib.auth.models import User
from django.db.models import Sum
from app.models import *

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

def generate_rating_question(num_records_per_query, count):
    for i in range(num_records_per_query):
        yield RatingQuestion(grade=1, question_id=(num_records_per_query * count + i) % 100010 + 1, profile_id=i + 1)

def create_rating_question():
    print("Creating ratings questions")
    for i in range(0, 1000000, 10001):
        RatingQuestion.objects.bulk_create(generate_rating_question(10001, i // 10001))

def generate_rating_answer(num_records_per_query, count):
    for i in range(num_records_per_query):
        yield RatingAnswer(grade=1, answer_id=(num_records_per_query * count + i) % 1000100 + 1, profile_id=i + 1)

def create_rating_answer():
    print("Creating ratings answers")
    for i in range(0, 1000000, 10001):
        RatingAnswer.objects.bulk_create(generate_rating_answer(10001, i // 10001))

def generate_answers(num_records_per_query, count):
    for i in range(num_records_per_query):
        yield Answer(text=f"This is text for answer №{num_records_per_query * count + i + 1}",
        profile_id=i + 1,
        question_id=(num_records_per_query * count + i) % 100010 + 1)

def create_answers():
    print("Creating answers")
    for i in range(0, 1000000, 10001):
        Answer.objects.bulk_create(generate_answers(10001, i // 10001))

def generate_questions(num_records_per_query, count):
    for i in range(num_records_per_query):
        yield Question(title=f"Title №{num_records_per_query * count + i + 1}",
        text=f"This is text for question №{num_records_per_query * count + i + 1}",
        profile_id=i + 1)

def create_questions():
    for i in range(0, 100000, 10001):
        Question.objects.bulk_create(generate_questions(10001, i // 10001))

    for i in range(100010):
        #Question.objects.all().get(id=i + 1).tags.add(Tag.objects.get(id=i % 9999 + 3))
        #Question.objects.all().get(id=i + 1).tags.add(Tag.objects.get(id=i % 10000 + 2))
        Question.objects.get(id=i + 1).tags.add(Tag.objects.get(id=i % 10001 + 1))

def count_rating_questions():
    Question.objects.annotate(rating=Sum('RatingQuestion__grade'))

def count_rating_answers():
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

if __name__ == "__main__":
    create_records()

