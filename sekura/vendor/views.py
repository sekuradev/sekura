from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic

from . import forms, models


class VendorListView(LoginRequiredMixin, generic.ListView):
    template_name = "vendor_list.html"
    context_object_name = "vendors"

    def get_queryset(self):
        return models.Vendor.objects.order_by("name")


class VendorDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Vendor
    template_name = "vendor_detail.html"


class VendorCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.Vendor()
        return render(request, "vendor_edit.html", {"form": form})

    def post(self, request):
        form = forms.Vendor(request.POST)
        if form.is_valid():
            vendor = form.save()
            return redirect(reverse("vendor:detail", kwargs={"pk": vendor.pk}))

        return render(request, "vendor_edit.html", {"form": form})


class VendorEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk is None:
            return redirect(reverse("vendor:create"))
        vendor = models.Vendor.objects.get(pk=pk)
        form = forms.Vendor(instance=vendor)

        return render(request, "vendor_edit.html", {"form": form, "vendor_id": pk})

    def post(self, request, pk):
        if pk is None:
            return redirect(reverse("vendor:create"))
        vendor = models.Vendor.objects.get(pk=pk)
        form = forms.Vendor(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect(reverse("vendor:detail", kwargs={"pk": pk}))

        return render(request, "vendor_edit.html", {"form": form, "vendor_id": pk})
