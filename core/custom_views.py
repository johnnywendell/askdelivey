# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from .views_mixins import CheckPermissionMixin

class CustomView(View, CheckPermissionMixin):
    pass


class CustomTemplateView(TemplateView, CheckPermissionMixin):
    pass


class CustomDetailView(DetailView, CheckPermissionMixin):
    pass

class CustomCreateView(CreateView, CheckPermissionMixin):

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class CustomListView(ListView, CheckPermissionMixin):

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, self.model):

            ids = [
                key for key, value in request.POST.items()
                if value == "on" and key.isdigit()
            ]

            if ids:
                self.model.objects.filter(id__in=ids).delete()

        return redirect(self.get_success_url())


class CustomUpdateView(UpdateView, CheckPermissionMixin):

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)