from django.db import models
from django.contrib.auth.models import User
from django.db.models import DO_NOTHING

from .utils import generate_ref_code
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class SubscriptionType(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    TYPE = (
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    )
    name = models.CharField(max_length=12, default=BASIC, choices=TYPE)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=False)
    date_changed = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


class Subscription(models.Model):
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=DO_NOTHING)
    user = models.ForeignKey(Profile,  on_delete=DO_NOTHING) # on_delete=models.SET_NULL
    date_changed = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.user.username}"
