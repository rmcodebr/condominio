from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from . managers import UserManager
from autoslug import AutoSlugField
from common.models import TimeStampedModel
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Avg





def get_user_username(instance: "Profile") -> str:
    return instance.user.username


class UsernameValidator(validators.RegexValidator):
  regex = r"^[\w.@+_]+z"
  message = _('Your username is not valid')
  flag = 0


class User(AbstractUser):
  pkid = models.BigAutoField(primary_key=True, editable=False)
  id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  first_name = models.CharField(max_length=60, verbose_name=_('First Name'))
  last_name = models.CharField(max_length=60, verbose_name=_('Last Name'))
  email = models.EmailField(verbose_name=_('Email Address'), unique=True, db_index=True)
  username = models.CharField(verbose_name=_('Username'), max_length=60, unique=True, validators=[UsernameValidator])

  EMAIL_FIELD = "email"
  USERNAME_FIELD = "email"

  REQUIRED_FIELDS = [
    'username', 'first_name', 'last_name'
  ]

  objects = UserManager()

  class Meta:
    verbose_name = _("User")
    verbose_name_plural = _("Users")
    ordering = ["-date_joined"]


  @property
  def get_full_name(self) -> str:
    full_name = f'{self.first_name} {self.last_name}'
    return full_name.strip()





class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = ("male", _("Male"),)
        FEMALE = ("female", _("Female"),)
        OTHER = ("other", _("Other"),)

    class Occupation(models.TextChoices):
        Mason = ("mason", _("Mason"),)
        Carpenter = ("carpenter", _("Carpenter"),)
        Plumber = ("plumber", _("Plumber"),)
        Roofer = ("roofer", _("Roofer"),)
        Painter = ("painter", _("Painter"),)
        Electrician = ("electrician", _("Electrician"),)
        HVAC = ("hvac", _("HVAC"),)
        TENANT = ("tenant", _("Tenant"),)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatar/", verbose_name=_("Avatar"), blank=True, null=True)
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True)
    occupation = models.CharField(
        verbose_name=_("Occupation"),
        max_length=20,
        choices=Occupation.choices,
        default=Occupation.TENANT,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+551198181"
    )
    country_of_origin = CountryField(verbose_name=_("Country"), default="BR")
    city_of_origin = models.CharField(
        verbose_name=_("City"), max_length=180, default="São Paulo"
    )
    report_count = models.IntegerField(verbose_name=_("Report Count"), default=0)
    reputation = models.IntegerField(verbose_name=_("Reputation"), default=100)
    slug = AutoSlugField(populate_from=get_user_username, unique=True)

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"

    @property
    def is_banned(self) -> bool:
        return self.report_count >= 5

    def update_reputation(self):
        self.reputation = max(0, 100 - self.report_count * 20)

    def save(self, *args, **kwargs):
        self.update_reputation()
        super().save(*args, **kwargs)

    def get_average_rating(self):
        average = self.user.received_ratings.aggregate(Avg("rating"))["rating__avg"]
        return average if average is not None else 0.0

