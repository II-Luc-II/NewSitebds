from django.test import TestCase

from newsletter.models import (
    Newsletter,
    NewsletterSubscriber,
)


class NewsletterSubscriberModelTests(TestCase):

    def test_string_representation(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        self.assertEqual(
            str(subscriber),
            "test@example.com",
        )

    def test_confirm_activates_subscriber(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        self.assertFalse(
            subscriber.is_confirmed
        )

        self.assertFalse(
            subscriber.is_active
        )

        self.assertIsNone(
            subscriber.confirmed_at
        )

        subscriber.confirm()

        subscriber.refresh_from_db()

        self.assertTrue(
            subscriber.is_confirmed
        )

        self.assertTrue(
            subscriber.is_active
        )

        self.assertIsNotNone(
            subscriber.confirmed_at
        )

        self.assertIsNone(
            subscriber.unsubscribed_at
        )

    def test_unsubscribe_deactivates_subscriber(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        subscriber.confirm()
        subscriber.unsubscribe()

        subscriber.refresh_from_db()

        self.assertTrue(
            subscriber.is_confirmed
        )

        self.assertFalse(
            subscriber.is_active
        )

        self.assertIsNotNone(
            subscriber.unsubscribed_at
        )


class NewsletterModelTests(TestCase):

    def test_string_representation(self):
        newsletter = Newsletter.objects.create(
            subject="Actualités",
            content="<p>Bonjour</p>",
        )

        self.assertEqual(
            str(newsletter),
            "Actualités",
        )

    def test_default_status_is_draft(self):
        newsletter = Newsletter.objects.create(
            subject="Actualités",
            content="<p>Bonjour</p>",
        )

        self.assertEqual(
            newsletter.status,
            Newsletter.Status.DRAFT,
        )