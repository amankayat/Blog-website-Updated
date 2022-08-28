
from django.http import HttpResponse, HttpResponseRedirect


from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
def index(requests):
    return HttpResponseRedirect(reverse('blog_list'))