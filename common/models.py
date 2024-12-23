from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django_countries.fields import CountryField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    country = CountryField(blank_label='(Select country)', null=True, blank=True)  # 출신 국가
    address = models.CharField(max_length=255, null=True, blank=True)  # 거주지
    birth_date = models.DateField(null=True, blank=True)  # 생년월일
    age = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 생년월일로 나이를 계산
        if self.birth_date:
            today = date.today()
            self.age = (
                    today.year - self.birth_date.year -
                    ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username