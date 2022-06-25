from celery.result import AsyncResult
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .forms import FakeDataForm
from .tasks import generate_fake_data, make_csv


class HomeView(FormView):
    template_name = "index.html"
    form_class = FakeDataForm

    def form_valid(self, form):
        total_by_user = self.request.session.get("total_by_user", 0)
        self.request.session["total_by_user"] = total_by_user + form.cleaned_data.get(
            "total"
        )
        task = generate_fake_data.delay(form.cleaned_data.get("total"))
        messages.success(
            self.request,
            f"Data generation started. You've made {self.request.session.get('total_by_user')} "
            f"rows in total in this session. <a href='result/{task.id}'>here</a>",
        )
        return redirect("home")


def task_result_view(request, task_id):
    task = AsyncResult(id=task_id)
    context = {
        "task": task,
        "task_state": task.state,
        "task_result": task.get(),
    }
    return render(request, "result.html", context)
