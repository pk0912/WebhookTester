from datetime import datetime

from celery import shared_task

from endpoints.models import Endpoint, UniqueEndpoints


@shared_task()
def delete_expired_endpoints():
    endpoints = Endpoint.objects.all()
    endpoints = [e for e in endpoints if e.is_expired()]
    for endpoint in endpoints:
        u = UniqueEndpoints()
        u.name = endpoint.name
        u.save()
        endpoint.delete()
