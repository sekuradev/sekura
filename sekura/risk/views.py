from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic
from guardian.mixins import PermissionListMixin  # PermissionRequiredMixin,

from . import forms, models


class ListView(LoginRequiredMixin, PermissionListMixin, generic.ListView):
    model = models.Risk
    template_name = "risk_list.html"
    context_object_name = "risks"
    paginate_by = 10
    permission_required = models.RiskPermissions.VIEW

    def get_queryset(self):
        m = models.Risk.get_for_user(self.request.user)
        filter_val = self.request.GET.get("q")
        order = self.request.GET.get("orderby", "title")
        if filter_val:
            m = m.filter(title__icontains=filter_val)
        return m.order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["orderby"] = self.request.GET.get("orderby", "title")
        return context


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
            obj = form.save(commit=False)
            if obj.owner is None:
                obj.owner = request.owner
            obj.save()
            messages.add_message(request, messages.INFO, "Risk created.")
            return redirect(reverse("risk:detail", kwargs={"pk": obj.pk}))

        return render(request, "risk_edit.html", {"form": form})


class EditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        risk = models.Risk.objects.get(pk=pk)
        form = forms.Risk(instance=risk)

        return render(request, "risk_edit.html", {"form": form, "risk": pk})

    def post(self, request, pk):
        risk = models.Risk.objects.get(pk=pk)
        form = forms.Risk(request.POST, instance=risk)
        if form.is_valid():
            risk = form.save()
            messages.add_message(request, messages.INFO, "Risk updated.")
            return redirect(reverse("risk:detail", kwargs={"pk": pk}))

        return render(request, "risk_edit.html", {"form": form, "risk": pk})
