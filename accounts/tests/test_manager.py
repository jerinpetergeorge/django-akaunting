from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase as DjangoTestCase

User = get_user_model()


class TestAuthManager(DjangoTestCase):
    def test_unique_email(self):
        User.objects.create_user(
            email="villanelle@test.com", is_verified=True, is_staff=True
        )
        with self.assertRaises(IntegrityError) as ctx:
            User.objects.create_user(email="villanelle@test.com")
        self.assertTrue(
            "Key (email)=(villanelle@test.com) already exists" in str(ctx.exception)
        )

    def test_create_user__extra_kwargs(self):
        user = User.objects.create_user(
            email="villanelle@test.com", is_verified=True, is_staff=True
        )
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, "villanelle@test.com")

    def test_create_user(self):
        user = User.objects.create_user(email="villanelle@test.com", is_verified=True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, "villanelle@test.com")

    def test_create_superuser__is_staff_false(self):
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_superuser(
                email="villanelle@test.com", is_verified=True, is_staff=False
            )
        self.assertEqual(str(ctx.exception), "Superuser must have is_staff=True.")

    def test_create_superuser__is_superuser_false(self):
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_superuser(
                email="villanelle@test.com", is_verified=True, is_superuser=False
            )
        self.assertEqual(str(ctx.exception), "Superuser must have is_superuser=True.")

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="villanelle@test.com", is_verified=True
        )
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, "villanelle@test.com")
