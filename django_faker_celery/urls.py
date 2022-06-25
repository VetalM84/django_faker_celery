"""
django_faker_celery URL Configuration.
"""

from django.contrib import admin
from django.urls import path

from fake_data_generator.views import HomeView, task_result_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("result/<str:task_id>/", task_result_view, name="result"),
]
