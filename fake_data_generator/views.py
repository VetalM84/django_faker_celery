"""View functions to render frontend."""

from celery.result import AsyncResult
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from django_faker_celery.settings import AWS_S3_CUSTOM_DOMAIN

from .forms import FakeDataForm
from .tasks import generate_fake_data


class HomeView(FormView):
    """Main page. Get session variables. Check form and start generate data task."""

    template_name = "index.html"
    form_class = FakeDataForm

    def form_valid(self, form):
        total_by_user = self.request.session.get("total_by_user", 0)
        self.request.session["total_by_user"] = total_by_user + form.cleaned_data.get(
            "total"
        )
        task = generate_fake_data.delay(form.cleaned_data.get("total"))
        messages.info(
            self.request,
            f"Data generation started. You've made {total_by_user} rows in total in this session.",
        )
        return redirect("result", task_id=task.id)


def task_result_view(request, task_id: str):
    """
    Get task status and result.
    Get session data with list of created files."""

    # Get task status
    task = AsyncResult(id=task_id)

    # Get session data, put items in list
    if "saved_list" not in request.session or not request.session["saved_list"]:
        request.session["saved_list"] = [task_id]
    else:
        saved_list = request.session["saved_list"]
        if task_id not in saved_list:
            saved_list.append(task_id)
        request.session["saved_list"] = saved_list

    return render(
        request,
        "result.html",
        context={
            "task": task,
            "saved_list": request.session["saved_list"],
            "aws": AWS_S3_CUSTOM_DOMAIN + "/uploads/",
        },
    )
