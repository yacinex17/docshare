from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Optional: for icon class or path

    def __str__(self):
        return self.name

class SubSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subsubjects')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Document(models.Model):
    file = models.FileField(upload_to='documents/', blank=True, null=True, help_text="Upload a file or provide a link below.")
    link = models.URLField(blank=True, null=True, help_text="Paste a link to an external document (e.g., Google Drive)")
    corrected_file = models.FileField(upload_to='documents/', blank=True, null=True, help_text="Upload a corrected file if available.")
    corrected_link = models.URLField(blank=True, null=True, help_text="Paste a link to a corrected document if available.")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='documents')
    subsubject = models.ForeignKey(SubSubject, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=10,
        choices=[
            ("Cours", "Cours"),
            ("TD", "TD"),
            ("Exam", "Exam"),
            ("DS", "DS"),
            ("TP", "TP"),
            ("Resume", "Resume"),
            ("Other", "Other"),
        ],
        default="TD",
        help_text="Type of document (Exam, TD, DS, TP)"
    )
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    has_correction = models.BooleanField(default=False, help_text="Check if a corrected version is provided.")

    def __str__(self):
        return self.title
