from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from .forms import FakeDataForm
from .tasks import generate_fake_data


class HomeView(FormView):
    template_name = "index.html"
    form_class = FakeDataForm

    def form_valid(self, form):
        total_by_user = self.request.session.get("total_by_user", 0)
        self.request.session["total_by_user"] = total_by_user + form.cleaned_data.get(
            "total"
        )
        generate_fake_data.delay(form.cleaned_data.get("total"))
        messages.success(
            self.request,
            f"Data generation started. You've made {self.request.session.get(total_by_user)} rows in total in this "
            f"session",
        )
        return redirect("home")
