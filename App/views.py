from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name: str = 'index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)


class LegalNoticeView(View):
    template_name: str = 'legal_notice.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)
