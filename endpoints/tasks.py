from celery import shared_task

from endpoints.models import Endpoint, UniqueEndpoints


@shared_task()
def delete_expired_endpoints():
    """
    This background task deletes all the expired Endpoints and
    insert it back into UniqueEndpoint table for the re-usability.
    :return: None
    """
    endpoints = Endpoint.objects.all()
    endpoints = [e for e in endpoints if e.is_expired()]
    for endpoint in endpoints:
        u = UniqueEndpoints()
        u.name = endpoint.name
        u.save()
        endpoint.delete()
