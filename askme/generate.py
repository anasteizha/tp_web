import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askme.settings")

django.setup()

from django.contrib.auth.models import User
from django.db.models import Sum
from app.models import *

from random import randint

ANSWERS = 1000000
RATING = 1000000
QUESTIONS = 100000
TAGS = 10000
PROFILES = 10000

MIN_BUF_SIZE = 10001

def generate_tags(num_records_per_query):
    for i in range(num_records_per_query):
        yield Tag(name=f"tag {i + 1}")

def create_tags():
    Tag.objects.bulk_create(generate_tags(TAGS + 1))

def generate_profiles():
    for i in range(PROFILES + 1):
        yield Profile(user_id=i + 1, nickname=f"Nick {i + 1}")

def generate_users():
    for i in range(1, 10002):
        yield User(username=f'user_{i}')

def create_profiles():
    User.objects.bulk_create(generate_users())

    Profile.objects.bulk_create(generate_profiles())

def generate_rating_question():
    ListQuestionProfile = []
    i = 0
    while (i < MIN_BUF_SIZE):
        q_id = randint(1, QUESTIONS + 10)
        p_id = randint(1, PROFILES + 1)

        if not RatingQuestion.objects.filter(grade=1, question_id=q_id, profile_id=p_id).exists() \
                    and ListQuestionProfile.count((q_id, p_id)) == 0:
            ListQuestionProfile.append((q_id, p_id))
            i += 1
            yield RatingQuestion(grade=1, question_id=q_id, profile_id=p_id)

def create_rating_question():
    for i in range(0, RATING, MIN_BUF_SIZE):
        RatingQuestion.objects.bulk_create(generate_rating_question())

def generate_rating_answer():
    ListAnswerProfile = []
    i = 0
    while (i < MIN_BUF_SIZE):
        a_id = randint(1, ANSWERS + 100)
        p_id = randint(1, PROFILES + 1)

        if not RatingAnswer.objects.filter(grade=1, answer_id=a_id, profile_id=p_id).exists() \
                    and ListAnswerProfile.count((a_id, p_id)) == 0:
            ListAnswerProfile.append((a_id, p_id))
            i += 1
            yield RatingAnswer(grade=1, answer_id=a_id, profile_id=p_id)

def create_rating_answer():
    for i in range(0, RATING, MIN_BUF_SIZE):
        RatingAnswer.objects.bulk_create(generate_rating_answer())

def generate_answers(count):
    for i in range(MIN_BUF_SIZE):
        yield Answer(text=f"This is text for answer №{MIN_BUF_SIZE * count + i + 1}",
        profile_id=i + 1,
        question_id=(MIN_BUF_SIZE * count + i) % (QUESTIONS + 10) + 1)

def create_answers():
    for i in range(0, ANSWERS, MIN_BUF_SIZE):
        Answer.objects.bulk_create(generate_answers(i // MIN_BUF_SIZE))

def generate_questions(count):
    for i in range(MIN_BUF_SIZE):
        yield Question(title=f"Title №{MIN_BUF_SIZE * count + i + 1}",
        text=f"This is text for question №{MIN_BUF_SIZE * count + i + 1}",
        profile_id=i + 1)

def create_questions():
    for i in range(0, QUESTIONS, MIN_BUF_SIZE):
        Question.objects.bulk_create(generate_questions(MIN_BUF_SIZE, i // MIN_BUF_SIZE))

    for i in range(0, QUESTIONS + 10):
        Question.objects.get(id=i + 1).tags.add(Tag.objects.get(id=i % (TAGS - 1) + 3))
        Question.objects.get(id=i + 1).tags.add(Tag.objects.get(id=i % TAGS + 2))
        Question.objects.get(id=i + 1).tags.add(Tag.objects.get(id=i % (TAGS + 1) + 1))

def update_questions(count):
    for i in range(MIN_BUF_SIZE):
        question = Question.objects.get(id=MIN_BUF_SIZE * count + i + 1)
        ratingQuestionObjects = RatingQuestion.objects.filter(question_id=question.id)
        if (ratingQuestionObjects.exists()):
            question.rating = ratingQuestionObjects.aggregate(total_rating=Sum('grade')).get("total_rating")
        yield question

def count_rating_questions():
    for i in range(0, QUESTIONS, MIN_BUF_SIZE):
        Question.objects.bulk_update(update_questions(i // MIN_BUF_SIZE), ['rating'])

def update_answers(count):
    for i in range(MIN_BUF_SIZE):
        answer = Answer.objects.get(id=MIN_BUF_SIZE * count + i + 1)
        ratingAnswerObjects = RatingAnswer.objects.filter(answer_id=answer.id)
        if (ratingAnswerObjects.exists()):
            answer.rating = ratingAnswerObjects.aggregate(total_rating=Sum('grade')).get("total_rating")
        yield answer

def count_rating_answers():
    for i in range(0, ANSWERS, MIN_BUF_SIZE):
        Answer.objects.bulk_update(update_answers(i // MIN_BUF_SIZE), ['rating'])

def create_records():
    create_tags()
    create_profiles()
    create_questions()
    create_answers()
    create_rating_question()
    create_rating_answer()
    count_rating_answers()
    count_rating_questions()

if __name__ == "__main__":
    create_records()

