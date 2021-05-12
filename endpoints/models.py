from datetime import timedelta

from django.db import models
from django.utils import timezone


class UniqueEndpoints(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        """
        :return:
        """
        return self.name


class Endpoint(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        """
        :return:
        """
        return self.name

    def is_expired(self):
        """
        :return:
        """
        return self.created_at + timedelta(hours=1) < timezone.now()

    def clicked(self):
        """
        :return:
        """
        self.clicks += 1
        self.save()


class EndpointHits(models.Model):
    name = models.ForeignKey(to=Endpoint, on_delete=models.CASCADE)
    query_params = models.JSONField(default=None, null=True)
    raw_body = models.JSONField(default=dict)
    headers = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
