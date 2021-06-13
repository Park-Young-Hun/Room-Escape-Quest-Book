import os
from urllib.error import HTTPError

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import datetime

import urllib.request as req

import pymysql
from django.conf import settings

board_path = "board/"


# Basic views
def home(request):  # 홈 화면.
    context = {}

    if request.session.has_key('id'):  # 로그인 되어있는 상태인지 체크.
        member_no = request.session['id']
        member_id = request.session['user_id']
    else:
        member_no = None
        member_id = None

        return redirect('/')

    context["id"] = member_no
    context["user_id"] = member_id

    return render(request, 'home.html', context)


# User Register

def member_register(request):  # 회원가입 화면.
    return render(request, "registration/member_register.html")


@csrf_exempt
def member_id_check(request):  # 아이디 중복체크 기능.
    context = {}

    member_id = request.GET['user_id']
    rs = BUser.objects.filter(user_id=member_id).exists()

    if rs:
        context['flag'] = '1'
        context['result_msg'] = '이미 존재하는 아이디입니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용가능한 아이디입니다.'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def member_insert(request):  # 회원등록 기능.
    context = {}

    member_id = request.GET['user_id']
    member_pwd = request.GET['psswd']
    member_name = request.GET['user_nm']
    member_phone_num = request.GET['phoneno']
    member_email = request.GET['email']

    rs = BUser.objects.create(user_id=member_id,
                              psswd=member_pwd,
                              user_nm=member_name,
                              email=member_email,
                              phoneno=member_phone_num,
                              usage_fg='1', )

    context['result_msg'] = '회원가입이 완료되었습니다.'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def member_login(request):  # 로그인 기능.
    context = {}

    member_id = request.GET['user_id']
    member_pwd = request.GET['psswd']

    if 'id' in request.session:
        context['flag'] = "1"
        context['result_msg'] = '이미 로그인 되어있는 아이디가 있습니다.'
    else:
        rs = BUser.objects.filter(user_id=member_id, psswd=member_pwd).exists()

        if rs:
            member = BUser.objects.get(user_id=member_id, psswd=member_pwd)
            member_no = member.id
            member.save()

            request.session['id'] = member_no
            request.session['user_id'] = member_id

            context['flag'] = "0"
            context['result_msg'] = '로그인이 완료되었습니다.'
        else:
            context['flag'] = "1"
            context['result_msg'] = '아이디 혹은 비밀번호가 일치하지 않습니다.'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def member_logout(request):  # 로그아웃 기능.
    context = {}

    request.session.flush()

    return redirect('main')


def member_check(request):  # 비밀번호 확인 화면.
    context = {}
    if request.session.has_key('id'):  # 로그인 되어있는 상태인지 체크.
        member_no = request.session['id']
        member_id = request.session['user_id']
    else:
        member_no = None
        member_id = None

        return redirect('/')

    context["id"] = member_no
    context["user_id"] = member_id

    return render(request, "registration/member_check.html", context)


@csrf_exempt
def member_pwd_check(request):  # 비밀번호 확인 기능.
    context = {}

    member_pwd = request.GET['psswd']

    if 'id' in request.session:
        rs = BUser.objects.filter(psswd=member_pwd).exists()

        if rs:
            context['flag'] = "0"
            context['result_msg'] = '비밀번호가 확인되었습니다.'
        else:
            context['flag'] = "1"
            context['result_msg'] = '비밀번호가 일치하지 않습니다.'
    else:
        context['flag'] = "1"
        context['result_msg'] = '로그인 페이지로 이동합니다.'

    return JsonResponse(context, content_type="application/json")


def member_edit(request):  # 회원정보 변경화면.
    context = {}

    if 'id' in request.session:
        member_no = request.session['id']
        member = BUser.objects.get(id=member_no)

        context['id'] = member.id
        context['user_id'] = member.user_id
        context['user_nm'] = member.user_nm
        context['phoneno'] = member.phoneno
        context['email'] = member.email

        context['flag'] = "0"
        context['result_msg'] = '회원정보 수정가능합니다.'

        return render(request, "registration/member_edit.html", context)

    else:
        return redirect('/')


@csrf_exempt
def member_update(request):  # 회원정보 변경 기능.
    context = {}

    member_req = request.GET
    member_id = member_req.get('user_id')  # url에 포함되어있지 않으면 None 반환.
    member_pwd = member_req.get('psswd')
    member_name = member_req.get('user_nm')
    member_phone_num = member_req.get('phoneno')
    member_email = member_req.get('email')

    member = BUser.objects.get(user_id=member_id)

    if member_pwd is not None:
        member.psswd = member_pwd

    if member_name is not None:
        member.user_nm = member_name

    if member_phone_num is not None:
        member.phoneno = member_phone_num

    if member_email is not None:
        member.email = member_email

    member.save()

    context['result_msg'] = '회원정보 변경이 완료되었습니다.'

    return JsonResponse(context, content_type="application/json")


def review_list(request):  # review list
    context = {}

    if request.session.has_key('id'):  # 로그인 되어있는 상태인지 체크.
        member_no = request.session['id']
        member_id = request.session['user_id']
    else:
        member_no = None
        member_id = None

        return redirect('board:home')

    context["id"] = member_no
    context["user_id"] = member_id

    rv = Review.objects.all()
    p_num = ['O', 'X']
    star_num = ['★', '★★', '★★★', '★★★★', '★★★★★']
    context["rsCo"] = rv
    context["p_num"] = p_num
    context["range"] = range(1, 7)
    context["star_num"] = star_num
    print(rv.values('star_num'))

    context["title"] = "해결한 퀘스트 목록"
    context["result_msg"] = "해결한 퀘스트 목록"

    return render(request, board_path + "review.html", context)


def review_detail(request, pk):  # review detail
    context = {}

    if request.session.has_key('id'):  # 로그인 되어있는 상태인지 체크.
        member_no = request.session['id']
        member_id = request.session['user_id']
    else:
        member_no = None
        member_id = None

        return redirect('board:home')

    context["id"] = pk
    context["user_id"] = member_id

    obj = Review.objects.get(id=pk).content
    print(obj)

    context["obj"] = obj

    return render(request, board_path + "review_detail.html", context)


def b_item(request):
    context = {}
    return render(request, board_path + "b_item.html", context)
