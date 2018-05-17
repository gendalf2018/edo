from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
from django.http import QueryDict

from django.contrib.auth.models import Group

from edoprofile.models import EdoUser
from dochistory.models import DocHistory
from .models import Doc

class EditorNewView(TemplateView):
    template_name = "editor/editor.html"
    def get_context_data(self, *args, **kwargs):
        context = super(EditorNewView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] =EdoUser.objects.all()
        return context

class EditorView(DetailView):
    template_name = "editor/editor.html"
    model = Doc
    context_object_name = 'doc'
    def get_context_data(self, *args, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] =EdoUser.objects.all()
        return context


class DocListView(TemplateView):
    template_name="editor/docs.html"
    def get_context_data(self, *args, **kwargs):
        context = super(DocListView, self).get_context_data(**kwargs)
        user = self.request.user
        groups = user.groups.all()
        group_docs = Doc.objects.filter(u_group__in=groups)
        user_docs = Doc.objects.filter(user__id=user.pk)
        context['group_docs'] = group_docs
        context['user_docs'] = user_docs
        return context

class EditorSaveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EditorSaveView, self).dispatch(request, *args, **kwargs)
    def post(self, request):
        print(request.user)
        doc_id = request.POST.get('doc_id')
        doc = request.POST.get('html')
        name = request.POST.get('name')
        if not doc_id:
            new_doc = Doc.objects.create(name=name, html=doc)
            new_doc.user.add(request.user)
            return JsonResponse({'success': True, 'doc_id': new_doc.pk})
        else:
            rewritten_doc = Doc.objects.get(pk=int(doc_id))
            rewritten_doc.html = doc
            rewritten_doc.name = name
            rewritten_doc.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': True})

class EditorGroupView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EditorGroupView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        doc_id = request.POST.get('doc')
        gid = request.POST.get('group')
        doc = Doc.objects.get(pk=int(doc_id))
        group = Group.objects.get(pk=int(gid))
        doc.u_group.add(group)
        return JsonResponse({'success': True})

    def delete(self, request):
        delete = QueryDict(request.body)
        # print(dict(request).keys())
        doc_id = delete.get('doc')
        gid = delete.get('group')
        doc = Doc.objects.get(pk=int(doc_id))
        group = Group.objects.get(pk=int(gid))
        doc.u_group.remove(group)
        return JsonResponse({'success': True})

class EditorUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EditorUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        doc_id = request.POST.get('doc')
        uid = request.POST.get('user')
        doc = Doc.objects.get(pk=int(doc_id))
        user = Group.objects.get(pk=int(uid))
        doc.user.add(user)
        return JsonResponse({'success': True})

    def delete(self, request):
        delete = QueryDict(request.body)
        doc_id = delete.get('doc')
        uid = delete.get('user')
        doc = Doc.objects.get(pk=int(doc_id))
        user = Group.objects.get(pk=int(uid))
        doc.user.remove(user)
        return JsonResponse({'success': True})
