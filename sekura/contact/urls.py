from django.urls import path

from . import views

app_name = "contact"
urlpatterns = [
    path("", views.ContactListView.as_view(), name="index"),
    path("<int:pk>/", views.ContactDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ContactEditView.as_view(), name="edit"),
    path("create/", views.ContactCreateView.as_view(), name="create"),
]
