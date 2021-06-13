import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Blog


class BlogModelTests(TestCase):

    def test_was_published_recently_with_future_blog(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_blog = Blog(pub_date=time)
        self.assertIs(future_blog.was_published_recently(), False)

    def test_was_published_recently_with_old_blog(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_blog = Blog(pub_date=time)
        self.assertIs(old_blog.was_published_recently(), False)

    def test_was_published_recently_with_recent_blog(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_blog = Blog(pub_date=time)
        self.assertIs(recent_blog.was_published_recently(), True)


def create_blog(title, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Blog.objects.create(title=title, pub_date=time)


class BlogIndexViewTests(TestCase):
    def test_past_blog(self):
        blog = create_blog(title="Past blog.", days=-30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_blog_list'],
            [blog],
        )

    def test_future_blog_and_past_blog(self):
        title = create_blog(title="Past blog.", days=-30)
        create_blog(title="Future blog.", days=30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_blog_list'],
            [title],
        )

    def test_two_past_blogs(self):
        blog1 = create_blog(title="Past blog 1.", days=-30)
        blog2 = create_blog(title="Past blog 2.", days=-5)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_blog_list'],
            [blog2, blog1],
        )
