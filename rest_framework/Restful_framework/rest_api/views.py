
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import exceptions
from openpyxl import Workbook
import pymysql
from django.conf import settings


@api_view(['GET', 'POST'])
@csrf_exempt
def review_list(request):
    if request.method == 'GET':
        query_set = Review.objects.all()
        serializer = ReviewSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        serializer = ReviewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def review_detail(request, pk):
    obj = Review.objects.get(id=pk)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        serializer = ReviewDetailSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReviewSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)
