import json

from django.http import HttpResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.views import View


class ApiTest(View):

    def get(self, request):
        return render(request, "test.html")

    def put(self, request):
        # json.loads(request.body)
        print(QueryDict(request.body)["file-name"])
        return HttpResponse(123)

    def post(self, request):
        # print(dir(request))
        print(request.FILES)
        # print(QueryDict(request.body))
        return HttpResponse(123)
