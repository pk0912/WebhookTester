from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from endpoints.models import Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = "__all__"

    def to_representation(self, instance):
        if not instance.is_expired():
            expires_in = instance.created_at + timedelta(hours=1) - timezone.now()
            expires_in = expires_in.seconds // 60
            expires_in = str(expires_in) + " mins"
            return {"name": instance.name, "clicks": instance.clicks, "expires_in": expires_in}


class EndpointHitSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        hit_time = timezone.now() - instance.created_at
        hit_time = hit_time.seconds
        if hit_time < 60:
            hit_time = str(hit_time) + " seconds ago"
        else:
            hit_time = hit_time // 60
            hit_time = str(hit_time) + " minutes ago"
        return {"query_param": instance.query_params, "raw_body": instance.raw_body,
                "headers": instance.headers, "last_hit": hit_time}
