import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# shortcut function tool
def create_question(question_text, days=0):
    """

    :param question_text:given question text for creation question.
    :param days: offset to now
    :return:Question instance
    """
    time = timezone.now() + datetime.timedelta(days)
    q = Question.objects.create(question_text=question_text, pub_date=time)
    return q


# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# View Test
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # view home index
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)  # normal response code
        self.assertContains(response, "No Home are available.")  # no item result.
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("home:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: Past question.>"])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("home:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: Past question.>"])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("home:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        old_question = create_question(question_text="Old question.", days=-30)
        url = reverse("home:detail", args=(old_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # successfully request context.
        self.assertContains(response, "Old question.")
