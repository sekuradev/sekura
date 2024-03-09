from django.urls import path

from . import views

app_name = "vendor"
urlpatterns = [
    path("", views.VendorListView.as_view(), name="index"),
    path("<int:pk>/", views.VendorDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.VendorEditView.as_view(), name="edit"),
    path("create/", views.VendorCreateView.as_view(), name="create"),
]
