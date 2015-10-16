# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render


def test_view(request):
    return HttpResponse("It´ works !")


def mapping_generator(imported_product_csv):
    """Return a generator who yield mapping csv data line by line"""
    pass
