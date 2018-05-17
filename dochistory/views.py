from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
from .models import DocHistory
from editor.models import Doc
# Create your views here.
class HistoryView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HistoryView, self).dispatch(request, *args, **kwargs)
    def post(self, request):
        html = request.POST.get('html')
        doc_id = request.POST.get('doc_id')
        doc = Doc.objects.get(pk=int(doc_id))
        hist = DocHistory.objects.create(user=request.user, previous_version=html, doc=doc)
        return JsonResponse({'success': True})
