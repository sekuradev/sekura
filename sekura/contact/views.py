from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic

from . import forms, models


class ContactListView(LoginRequiredMixin, generic.ListView):
    template_name = "index.html"
    context_object_name = "contacts"

    def get_queryset(self):
        return models.Contact.objects.order_by("name")


class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Contact
    template_name = "detail.html"
    context_object_name = "contact"


class ContactCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.Contact()
        return render(request, "edit.html", {"form": form})

    def post(self, request):
        form = forms.Contact(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(reverse("contact:detail", kwargs={"pk": contact.pk}))

        return render(request, "edit.html", {"form": form})


class ContactEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk is None:
            return redirect(reverse("contact:create"))
        contact = models.Contact.objects.get(pk=pk)
        form = forms.Contact(instance=contact)

        return render(request, "edit.html", {"form": form, "contact_id": pk})

    def post(self, request, pk):
        if pk is None:
            return redirect(reverse("contact:create"))
        contact = models.Contact.objects.get(pk=pk)
        form = forms.Contact(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(reverse("contact:detail", kwargs={"pk": pk}))
        return render(request, "edit.html", {"form": form, "contact_id": pk})
