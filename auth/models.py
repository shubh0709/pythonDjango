import uuid
from typing import Any, Type

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.manager import Manager  # Import the Manager type


class StudentTeacherChoice(models.TextChoices):
    STUDENT = 'student', 'Student'
    TEACHER = 'teacher', 'Teacher'
    PROFESSIONAL = 'professional', 'Professional'
    REST = "rest", "REST"


class StudentTeacherField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['choices'] = StudentTeacherChoice.choices
        kwargs['default'] = StudentTeacherChoice.STUDENT
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=6)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)  # Validators should be a list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: Manager['OTP']


class CustomUser(models.Model):
    # userId
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=17, default=None)
    type = StudentTeacherField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: Manager['CustomUser']


class LoginToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    token = models.CharField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: Manager['LoginToken']
