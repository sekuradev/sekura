from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic

from . import forms, models


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = "archive_list.html"
    context_object_name = "archives"

    def get_queryset(self):
        return models.Archive.objects.order_by("name")


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Archive
    template_name = "archive_detail.html"


class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.Archive()
        return render(request, "archive_edit.html", {"form": form})

    def post(self, request):
        form = forms.Archive(request.POST, request.FILES)
        if form.is_valid():
            archive = form.save()
            return redirect(reverse("archive:detail", kwargs={"pk": archive.pk}))
        return render(request, "archive_edit.html", {"form": form})


class EditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        archive = models.Archive.objects.get(pk=pk)
        form = forms.Archive(instance=archive)

        return render(request, "archive_edit.html", {"form": form, "archive_id": pk})

    def post(self, request, pk):
        archive = models.Archive.objects.get(pk=pk)
        form = forms.Archive(request.POST, request.FILES, instance=archive)
        if form.is_valid():
            form.save()
            return redirect(reverse("archive:detail", kwargs={"pk": pk}))

        return render(request, "archive_edit.html", {"form": form, "archive_id": pk})
