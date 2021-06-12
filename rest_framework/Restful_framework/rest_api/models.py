from django.db import models


# Create your models here.


class BUser(models.Model):  # 사용자관리
    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.CharField(db_column='user_id', max_length=50)
    user_nm = models.CharField(db_column='user_nm', max_length=50, blank=True, null=True)
    psswd = models.CharField(db_column='psswd', max_length=255)
    email = models.CharField(db_column='email', max_length=255, blank=True, null=True)
    phoneno = models.CharField(db_column='phoneno', max_length=20, blank=True, null=True)
    insrt_id = models.IntegerField(db_column='insrt_id', blank=True, null=True)
    insrt_dt = models.DateTimeField(db_column='insrt_dt', blank=True, null=True, auto_now_add=True)
    updt_id = models.IntegerField(db_column='updt_id', blank=True, null=True)
    updt_dt = models.DateTimeField(db_column='updt_dt', blank=True, null=True, auto_now=True)
    usage_fg = models.CharField(db_column='usage_fg', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b_user'


class Review(models.Model):  # 방탈출 기록
    id = models.AutoField(db_column='id', primary_key=True)
    visited_day = models.CharField(db_column='visited_day', max_length=50, blank=True, null=True)
    region = models.CharField(db_column='region', max_length=50, blank=True, null=True)
    cafe_name = models.CharField(db_column='cafe_name', max_length=50, blank=True, null=True)
    theme_name = models.CharField(db_column='theme_name', max_length=50, blank=True, null=True)
    participant_num = models.IntegerField(db_column='participant_num', blank=True, null=True, default=2)
    escape_flag = models.CharField(db_column='escape_flag', max_length=1, blank=True, null=True, default='O')
    r_time = models.CharField(db_column='r_time', max_length=50, blank=True, null=True)
    content = models.CharField(db_column='content', max_length=300, blank=True, null=True)
    updt_dt = models.DateTimeField(db_column='updt_dt', auto_now=True)
    insrt_dt = models.DateTimeField(db_column='insrt_dt', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'review'
