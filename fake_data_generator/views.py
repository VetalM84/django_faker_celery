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


def result_view(request, task_id):
    task = AsyncResult(id=task_id)
    context = {
        "task": task,
        "task_state": task.state,
        "task_result": task.get(),
    }
    return render(request, "result.html", context)


# def get_model_info(request, model_id):
#     """получаем информацию о конкретной модели авто"""
#     car_model = CarModel.objects.get(pk=model_id)
#     car_brand = CarBrand.objects.get(pk=car_model.brand_id)
#     # отображаем только уникальные запчасти у которых есть отзыв к этой модели
#     spare_parts = (
#         Review.objects.filter(car_model_id=model_id)
#         .order_by("spare_part__name")
#         .distinct("spare_part__name", "spare_part__brand", "spare_part__number")
#         .select_related("spare_part")
#     )
#     context = {
#         "spare_parts": spare_parts,
#         "car_model": car_model,
#         "car_brand": car_brand,
#         "title": f"Все для {car_brand.brand} {car_model.model_name}",
#     }
#     return render(request, "mileage/model_info.html", context)
