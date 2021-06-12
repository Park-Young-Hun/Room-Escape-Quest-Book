from .models import *
from rest_framework import serializers


#  CRUD API


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('visited_day', 'region', 'cafe_name', 'theme_name', 'participant_num', 'escape_flag', 'r_time')


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content',)


