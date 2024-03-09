from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic

from . import forms, models


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = "risk_list.html"
    context_object_name = "risks"

    def get_queryset(self):
        return models.Risk.objects.order_by("title")


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Risk
    template_name = "risk_detail.html"


class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.Risk()
        return render(request, "risk_edit.html", {"form": form})

    def post(self, request):
        form = forms.Risk(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(reverse("risk:detail", kwargs={"pk": obj.pk}))

        return render(request, "risk_edit.html", {"form": form})


class EditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk is None:
            return redirect(reverse("risk:create"))
        risk = models.Risk.objects.get(pk=pk)
        form = forms.Risk(instance=risk)

        return render(request, "risk_edit.html", {"form": form, "risk": pk})

    def post(self, request, pk):
        if pk is None:
            return redirect(reverse("risk:create"))
        risk = models.Risk.objects.get(pk=pk)
        form = forms.Risk(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            return redirect(reverse("risk:detail", kwargs={"pk": pk}))

        return render(request, "risk_edit.html", {"form": form, "risk": pk})
