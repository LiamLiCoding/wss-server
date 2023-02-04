from django.db import models
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import ASCIIUsernameValidator


class UserCustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class Users(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters only.",
        validators=[username_validator],
    )

    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    email = models.EmailField("email address", unique=True,
                              error_messages={"unique": "A user with that email already exists.", },)
    is_staff = models.BooleanField("staff status", default=False, help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField("active", default=True,
                                    help_text="Designates whether this user should be treated as active. "
                                              "Unselect this instead of deleting accounts.",)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    avatar = models.ImageField(upload_to='accounts/avatar', max_length=200, null=True, blank=True)
    oauth_id = models.PositiveIntegerField('Oauth-id', unique=True, null=True, blank=True)
    oauth_page_url = models.CharField('Oauth-Page-Url', max_length=255, null=True, blank=True)

    is_verified = models.BooleanField("Is verified", default=False)

    date_joined = models.DateTimeField("date joined", default=timezone.now)

    objects = UserCustomManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    class Meta:
        abstract = False
        ordering = ["-create_time"]
        verbose_name = "users"
        verbose_name_plural = "users"



