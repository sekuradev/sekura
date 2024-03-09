from django.urls import path

from . import views

app_name = "risk"
urlpatterns = [
    path("", views.ListView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditView.as_view(), name="edit"),
    path("create/", views.CreateView.as_view(), name="create"),
]
