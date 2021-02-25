from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

#
# class SubscriptionType(models.Model):
#     name = models.CharField(max_length=50)
#     price = models.FloatField(null=True)
#     description = models.CharField(max_length=200, null=True)  # add blank=True
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#
#     def __str__(self):
#         return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

#
# class Subscription(models.Model):
#     STATUS = (
#         ('Active', 'Active'),
#         ('Cancelled', 'Cancelled'),
#     )
#
#     customer = models.ForeignKey(Profile, on_delete=models.SET_NULL)
#     subscription_type = models.ForeignKey(SubscriptionType, on_delete=DO_NOTHING)
#     status = models.CharField(max_length=30, null=True, blank=True, choices=STATUS)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)

