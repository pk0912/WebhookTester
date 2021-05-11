import random
import json

from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, redirect, render

from endpoints.models import UniqueEndpoints, Endpoint, EndpointHits
from endpoints.serializers import EndpointSerializer, EndpointHitSerializer


# class EndpointViewSet(ModelViewSet):
#     queryset = Endpoint.objects.all()
#     serializer_class = EndpointSerializer
#
#     def create(self, request, *args, **kwargs):
#         all_names = list(UniqueEndpoints.objects.all())
#
#         while 1:
#             endpoint_name = random.choice(all_names)
#             all_names.remove(endpoint_name)
#             try:
#                 endpoint_name.delete()
#             except AssertionError:
#                 continue
#             else:
#                 request.data["name"] = endpoint_name.name
#                 break
#         return super(EndpointViewSet, self).create(request, *args, **kwargs)
#
#     def list(self, request, *args, **kwargs):
#         alive_endpoints = EndpointSerializer(Endpoint.objects.all(), many=True).data
#         alive_endpoints = [e for e in alive_endpoints if e is not None]
#         return Response(alive_endpoints, status=status.HTTP_200_OK)


# class IndexView(TemplateView):
#     template_name = "index.html"
#
#     def get_context_data(self, **kwargs):
#         kwargs["data"] = EndpointSerializer(Endpoint.objects.all(), many=True).data
#         kwargs["data"] = [d for d in kwargs["data"] if d is not None]
#         return kwargs
#
#     def get(self, request, *args, **kwargs):
#         return self.render_to_response(self.get_context_data(**kwargs))


class EndpointApiView(APIView):
    parser_classes = (JSONParser, )

    def post(self, request, *args, **kwargs):
        all_names = list(UniqueEndpoints.objects.all())
        while 1:
            endpoint_name = random.choice(all_names)
            all_names.remove(endpoint_name)
            try:
                endpoint_name.delete()
            except AssertionError:
                continue
            else:
                break
        endpoint = Endpoint()
        endpoint.name = endpoint_name
        endpoint.save()
        return Response({"message": "Endpoint successfully created!!!"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        alive_endpoints = EndpointSerializer(Endpoint.objects.all(), many=True).data
        alive_endpoints = [e for e in alive_endpoints if e is not None]
        return Response(alive_endpoints, status=status.HTTP_200_OK)


# class EndpointView(TemplateView):
#     template_name = "endpoint.html"
#
#     def get_context_data(self, **kwargs):
#         endpoint_obj = get_object_or_404(Endpoint, name=kwargs.get("endpoint", ""))
#         endpoint = EndpointSerializer(endpoint_obj).data
#         kwargs["endpoint"] = endpoint
#         endpoint_hit = EndpointHitSerializer(EndpointHits.objects.filter(name=endpoint_obj), many=True).data
#         kwargs["hits"] = endpoint_hit
#         return kwargs
#
#     def get(self, request, *args, **kwargs):
#         try:
#             data = self.get_context_data(**kwargs)
#         except Http404:
#             raise Http404("")
#         except TypeError:
#             raise Http404("")
#         return render(request, self.template_name, data)
#
#     def post(self, request, *args, **kwargs):
#         try:
#             endpoint = get_object_or_404(Endpoint, name=kwargs.get("endpoint", ""))
#             endpoint.clicked()
#             endpoint_hit = EndpointHits()
#             endpoint_hit.name = endpoint
#             endpoint_hit.raw_body = json.loads(request.body)
#             endpoint_hit.query_params = [request.content_params]
#             endpoint_hit.headers = dict(request.headers)
#             endpoint_hit.save()
#         except Http404 as e:
#             return HttpResponse({"message": str(e)}, content_type="application/json")
#         return HttpResponse({"message": "Hit done!!!"}, content_type="application/json")


class EndpointHitApiView(APIView):
    parser_classes = (JSONParser, )

    def post(self, request, *args, **kwargs):
        try:
            endpoint = get_object_or_404(Endpoint, name=kwargs.get("endpoint", ""))
            if endpoint.is_expired():
                return Response({"message": "No such endpoint exist!!!"}, status=status.HTTP_404_NOT_FOUND)
            endpoint.clicked()
            endpoint_hit = EndpointHits()
            endpoint_hit.name = endpoint
            endpoint_hit.raw_body = request.data
            endpoint_hit.query_params = [request.query_params] if len(request.query_params) > 0 else None
            endpoint_hit.headers = ["Accept: " + request.META.get("HTTP_ACCEPT", ""),
                                    "Cache-Control: " + request.META.get("HTTP_CACHE_CONTROL", "")]
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
            endpoint_hit = EndpointHitSerializer(EndpointHits.objects.filter(name=endpoint_obj), many=True).data
            kwargs["hits"] = endpoint_hit
            return Response(kwargs, status=status.HTTP_200_OK)
        except TypeError:
            return Response({"message": "No such endpoint exists."}, status=status.HTTP_404_NOT_FOUND)
