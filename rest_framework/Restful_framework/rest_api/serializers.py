from .models import *
from rest_framework import serializers


# 1단계 기준정보 CRUD API


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('visited_day', 'region', 'cafe_name', 'theme_name', 'participant_num', 'escape_flag', 'r_time', 'content')
