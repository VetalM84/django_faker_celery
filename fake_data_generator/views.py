from celery.result import AsyncResult
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .forms import FakeDataForm
from .tasks import generate_fake_data


class HomeView(FormView):
    template_name = "index.html"
    form_class = FakeDataForm

    def form_valid(self, form):
        # TODO add links to generated files to session
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


def task_result_view(request, task_id):
    task = AsyncResult(id=task_id)
    return render(request, "result.html", context={"task": task})
