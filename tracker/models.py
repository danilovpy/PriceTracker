from django.db import models

from .utils import get_link_data
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username: username})


class User(AbstractUser):
    objects = CustomUserManager()


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    name = models.CharField(max_length=220, blank=True)
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('price_difference', '-created')

    def save(self, *args, **kwargs):
        name, price = get_link_data(self.url)
        if price == "unavailable":
            self.delete()
            return 0
        old_price = self.current_price
        if self.current_price:
            self.price_difference = round(old_price - price, 2)
            self.old_price = old_price
        else:
            self.old_price = 0
            self.price_difference = 0
        self.name, self.current_price = name, price
        super().save(*args, **kwargs)
