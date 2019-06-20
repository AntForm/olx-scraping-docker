from django.shortcuts import render
from olx.forms import RequestForm
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from olx.tasks import get_request
from django.views import View
from django.shortcuts import render
from olx.models import OlxRequest
import gviz_api

from django.http import HttpResponse


# Create your views here.

class RequestView(SuccessMessageMixin, FormView):
    template_name = 'olx/request_form.html'
    form_class = RequestForm
    success_url = reverse_lazy('olx')
    success_message = "The result will be sent to your email."

    def form_valid(self, form):
        model = form.save()
        get_request.delay(model.pk)

        return super().form_valid(form)

class PopularTime(View):
    def get(self, request, pk):
        description={"hour" : ("number", "Time"), "quantity" : ("number", "Quantity")}
        data = []
        context = {}
        obj = OlxRequest.objects.get(pk = pk)

        for x in range(24):
            dic={}
            dic['hour'] = x
            dic['quantity'] = obj.olxlinks_set.filter(datetime__hour=x).count()
            data.append(dic)

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        context['gviz_data'] = data_table.ToJSon()

        return render(request, 'olx/p_time.html', context)

class PopularDay(View):
    def get(self, request, pk):
        description={"weekday" : ("number", "Weekday"), "quantity" : ("number", "Quantity")}
        data = []
        context = {}
        obj = OlxRequest.objects.get(pk = pk)

        for x in range(1, 8):
            dic={}
            dic['weekday'] = x
            dic['quantity'] = obj.olxlinks_set.filter(datetime__week_day=x).count()
            data.append(dic)

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        context['gviz_data'] = data_table.ToJSon(columns_order=("weekday", "quantity"))

        return render(request, 'olx/p_weekday.html', context)
