from datetime import datetime, date

from django.test import TestCase
from django.utils import timezone
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact, Newsletter


class SiteBdsModelTest(TestCase):

    def test_model_gallery_fields(self):
        time = timezone.now()
        gallery = Gallery(
            name='Test Name',
            description='Test Description',
            image='bg-hero.png',
            is_published=True,
            created_at=time
        )

        self.assertEqual(gallery.name, 'Test Name')
        self.assertEqual(gallery.description, 'Test Description')
        self.assertEqual(gallery.image, 'bg-hero.png')
        self.assertEqual(gallery.is_published, True)
        self.assertEqual(gallery.created_at, time)

    def test_model_gallery_default_is_published(self):
        gallery = Gallery()
        self.assertEqual(gallery.is_published, False)

    def test_model_testimonials_fields(self):
        time = timezone.now()
        testimonials = Testimonials(
            name='Test Name',
            job='Test Job',
            description='Test Description',
            image='bg-hero.png',
            is_published=True,
            created_at=time
        )

        self.assertEqual(testimonials.name, 'Test Name')
        self.assertEqual(testimonials.job, 'Test Job')
        self.assertEqual(testimonials.description, 'Test Description')
        self.assertEqual(testimonials.image, 'bg-hero.png')
        self.assertEqual(testimonials.is_published, True)
        self.assertEqual(testimonials.created_at, time)

    def test_model_testimonials_default_is_published(self):
        testimonials = Testimonials()
        self.assertEqual(testimonials.is_published, False)

    def test_model_team_fields(self):
        time = timezone.now()
        team = Team(
            name='Test Name',
            function='Test Function',
            description='Test Description',
            facebook='Test Facebook',
            twitter='Test Twitter',
            linkedin='Test Linkedin',
            instagram='Test Instagram',
            image='Test Image',
            is_published=True,
            created_at=time
        )

        self.assertEqual(team.name, 'Test Name')
        self.assertEqual(team.function, 'Test Function')
        self.assertEqual(team.description, 'Test Description')
        self.assertEqual(team.facebook, 'Test Facebook')
        self.assertEqual(team.twitter, 'Test Twitter')
        self.assertEqual(team.linkedin, 'Test Linkedin')
        self.assertEqual(team.instagram, 'Test Instagram')
        self.assertEqual(team.image, 'Test Image')
        self.assertEqual(team.is_published, True)
        self.assertEqual(team.created_at, time)

    def test_team_default_at_model_ask_is_published(self):
        team = Team()
        self.assertEqual(team.is_published, False)

    def test_at_model_ask_initialization(self):
        # Test d'initialisation avec ask
        q = Ask(ask='Question')
        self.assertEqual(q.ask, 'Question')

        # Test d'initialisation avec response
        q = Ask(response='Response')
        self.assertEqual(q.response, 'Response')

        # Test d'initialisation avec is_published
        q = Ask(is_published=True)
        self.assertEqual(q.is_published, True)

    def test_created_at_model_ask_direct_assignment(self):
        # Test d'initialisation avec created_at
        time = timezone.now()
        q = Ask(created_at=time)
        self.assertEqual(q.created_at, time)

    def test_created_at_model_ask_default(self):
        # Test de la valeur par défaut de created_at
        q = Ask()
        q.save()  # Nécessaire pour générer la date actuelle
        self.assertTrue(timezone.now() - q.created_at < timezone.timedelta(seconds=1))

    def test_model_contact(self):
        time = timezone.now()
        contact = Contact(
            name='Test Name',
            email='Test Email',
            subject='Test subject',
            message='message',
            checked=True,
        )

        self.assertEqual(contact.name, 'Test Name')
        self.assertEqual(contact.email, 'Test Email')
        self.assertEqual(contact.subject, 'Test subject')
        self.assertEqual(contact.message, 'message')
        self.assertEqual(contact.checked, True)

    def test_created_at_model_contact_direct_assignment(self):
        # Test d'initialisation avec created_at
        time = timezone.now()
        q = Contact(created_at=time)
        self.assertEqual(q.created_at, time)

    def test_created_at_model_contact_default(self):
        # Test de la valeur par défaut de created_at
        q = Contact()
        q.save()  # Nécessaire pour générer la date actuelle
        self.assertTrue(timezone.now() - q.created_at < timezone.timedelta(seconds=1))

    def test_madel_newsletter(self):
        time = timezone.now()
        newsletter = Newsletter(
            email='Test Email',
        )

        self.assertEqual(newsletter.email, 'Test Email')

    def test_created_at_model_newsletter_direct_assignment(self):
        # Test d'initialisation avec created_at
        time = timezone.now()
        q = Newsletter(created_at=time)
        self.assertEqual(q.created_at, time)

    def test_created_at_model_newsletter_default(self):
        # Test de la valeur par défaut de created_at
        q = Newsletter()
        q.save()  # Nécessaire pour générer la date actuelle
        self.assertTrue(timezone.now() - q.created_at < timezone.timedelta(seconds=1))

