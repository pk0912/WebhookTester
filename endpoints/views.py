import logging
import random

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from endpoints.models import UniqueEndpoints, Endpoint, EndpointHits
from endpoints.serializers import EndpointSerializer, EndpointHitSerializer

log = logging.getLogger(__name__)


class EndpointApiView(APIView):
    """
    This APIView allows to create unique Endpoints by retrieving the already populated Unique endpoints and
    randomly picking one of them to avoid collision. After picking up it deletes the endpoint name from the
    UniqueEndpoint table and creating a new Endpoint for one hour. This script will try a limited number of
    times to perform the creation. If creation does not happen within the allotted count of tries, creation fails.
    This could be made more efficient by using Redis Queue.
    The get method retrieves the list of alive endpoints and returns them.
    """

    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        all_names = list(UniqueEndpoints.objects.all())
        creation_try = 0
        while creation_try < settings.MAX_ENDPOINT_CREATION_TRY:
            endpoint_name = random.choice(all_names)
            all_names.remove(endpoint_name)
            try:
                endpoint_name.delete()
            except AssertionError:
                creation_try += 1
                continue
            else:
                endpoint = Endpoint()
                endpoint.name = endpoint_name
                endpoint.save()
                return Response(
                    {"message": "Endpoint successfully created!!!"}, status=status.HTTP_200_OK
                )
        return Response(
            {"message": "Endpoint creation failed!!!"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        alive_endpoints = EndpointSerializer(Endpoint.objects.all(), many=True).data
        alive_endpoints = [e for e in alive_endpoints if e is not None]
        return Response(alive_endpoints, status=status.HTTP_200_OK)


class EndpointHitApiView(APIView):
    """
    This APIView inserts the data received from the endpoints hit made by webhooks in the Endpoint Hits table.
    This also increases the click counter of the Endpoint record over which the hit was done.
    The get method returns the Endpoint related info from Endpoint table like the expiry time and the name.
    It also includes the data sent while making post request on the endpoints.
    It returns the full-fledged url of the endpoint which needs to be used by webhooks for testing.
    """
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        try:
            endpoint = get_object_or_404(Endpoint, name=kwargs.get("endpoint", ""))
            if endpoint.is_expired():
                return Response(
                    {"message": "No such endpoint exist!!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            endpoint.clicked()
            endpoint_hit = EndpointHits()
            endpoint_hit.name = endpoint
            endpoint_hit.raw_body = request.data
            endpoint_hit.query_params = (
                [request.query_params] if len(request.query_params) > 0 else None
            )
            endpoint_hit.headers = [
                "Accept: " + request.META.get("HTTP_ACCEPT", ""),
                "Cache-Control: " + request.META.get("HTTP_CACHE_CONTROL", ""),
            ]
            endpoint_hit.save()
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Hit done!!!"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        endpoint_obj = get_object_or_404(Endpoint, name=kwargs.get("endpoint", ""))
        try:
            endpoint = EndpointSerializer(endpoint_obj).data
            kwargs["endpoint"] = endpoint
            kwargs["endpoint"]["name"] = request.build_absolute_uri()
            endpoint_hit = EndpointHitSerializer(
                EndpointHits.objects.filter(name=endpoint_obj).order_by("-id"),
                many=True,
            ).data[: settings.MAX_HITS_DISPLAY_COUNT]
            kwargs["hits"] = endpoint_hit
            return Response(kwargs, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {"message": "No such endpoint exists."},
                status=status.HTTP_404_NOT_FOUND,
            )
