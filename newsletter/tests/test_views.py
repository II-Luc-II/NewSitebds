from uuid import uuid4
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from newsletter.models import NewsletterSubscriber


class NewsletterSubscribeTests(TestCase):

    def test_subscribe_requires_post(self):
        response = self.client.get(
            reverse(
                "newsletter:subscribe",
            )
        )

        self.assertEqual(
            response.status_code,
            405,
        )

    def test_invalid_email_does_not_create_subscriber(self):
        response = self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "adresse-invalide",
                "next": "/",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            NewsletterSubscriber.objects.exists()
        )

    def test_valid_email_creates_unconfirmed_subscriber(self):
        response = self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "Test@Example.com",
                "next": "/",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        subscriber = NewsletterSubscriber.objects.get(
            email="test@example.com",
        )

        self.assertFalse(
            subscriber.is_confirmed
        )

        self.assertFalse(
            subscriber.is_active
        )

    def test_valid_subscription_sends_confirmation_email(self):
        self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "test@example.com",
                "next": "/",
            },
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        email = mail.outbox[0]

        self.assertEqual(
            email.to,
            ["test@example.com"],
        )

        self.assertIn(
            "Confirmez votre inscription",
            email.subject,
        )

        subscriber = NewsletterSubscriber.objects.get(
            email="test@example.com",
        )

        confirmation_url = reverse(
            "newsletter:confirm",
            kwargs={
                "token": subscriber.confirmation_token,
            },
        )

        self.assertIn(
            confirmation_url,
            email.body,
        )

    def test_existing_unconfirmed_subscriber_receives_new_email(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        old_token = subscriber.confirmation_token

        response = self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "test@example.com",
                "next": "/",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            NewsletterSubscriber.objects.filter(
                email="test@example.com",
            ).count(),
            1,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        subscriber.refresh_from_db()

        # Ton code actuel ne renouvelle pas le token,
        # il renvoie simplement un mail avec le token existant.
        self.assertEqual(
            subscriber.confirmation_token,
            old_token,
        )

    def test_already_confirmed_active_subscriber_does_not_receive_email(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        subscriber.confirm()

        response = self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "test@example.com",
                "next": "/",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            len(mail.outbox),
            0,
        )

    def test_subscribe_redirects_to_next(self):
        response = self.client.post(
            reverse(
                "newsletter:subscribe",
            ),
            {
                "email": "test@example.com",
                "next": "/ma-page/",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            response.url,
            "/ma-page/",
        )


class NewsletterConfirmationTests(TestCase):

    def test_valid_token_confirms_subscription(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        response = self.client.get(
            reverse(
                "newsletter:confirm",
                kwargs={
                    "token": subscriber.confirmation_token,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

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

    def test_already_confirmed_subscription_stays_active(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        subscriber.confirm()

        confirmed_at = subscriber.confirmed_at

        response = self.client.get(
            reverse(
                "newsletter:confirm",
                kwargs={
                    "token": subscriber.confirmation_token,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        subscriber.refresh_from_db()

        self.assertTrue(
            subscriber.is_confirmed
        )

        self.assertTrue(
            subscriber.is_active
        )

        self.assertEqual(
            subscriber.confirmed_at,
            confirmed_at,
        )

    def test_invalid_confirmation_token_returns_404(self):
        response = self.client.get(
            reverse(
                "newsletter:confirm",
                kwargs={
                    "token": uuid4(),
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )


class NewsletterUnsubscribeTests(TestCase):

    def setUp(self):
        self.subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
        )

        self.subscriber.confirm()

        self.url = reverse(
            "newsletter:unsubscribe",
            kwargs={
                "token": self.subscriber.unsubscribe_token,
            },
        )

    def test_get_displays_unsubscribe_confirmation_page(self):
        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "unsubscribe_confirm.html",
        )

        self.assertEqual(
            response.context["subscriber"],
            self.subscriber,
        )

    def test_post_unsubscribes_active_subscriber(self):
        response = self.client.post(
            self.url
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.subscriber.refresh_from_db()

        self.assertFalse(
            self.subscriber.is_active
        )

        self.assertIsNotNone(
            self.subscriber.unsubscribed_at
        )

    def test_second_unsubscribe_keeps_subscriber_inactive(self):
        self.subscriber.unsubscribe()

        unsubscribed_at = (
            self.subscriber.unsubscribed_at
        )

        response = self.client.post(
            self.url
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.subscriber.refresh_from_db()

        self.assertFalse(
            self.subscriber.is_active
        )

        self.assertEqual(
            self.subscriber.unsubscribed_at,
            unsubscribed_at,
        )

    def test_invalid_unsubscribe_token_returns_404(self):
        response = self.client.get(
            reverse(
                "newsletter:unsubscribe",
                kwargs={
                    "token": uuid4(),
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )