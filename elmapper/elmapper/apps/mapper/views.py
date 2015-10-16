# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render


def test_view(request):
    return HttpResponse("It´ works !")
