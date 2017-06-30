import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from geonode.layers.models import Layer

from .models import Chart, ChartForm
from wfs_harvest.utils import get_fields


class ChartDetailView(DetailView):
    model = Chart


class ChartCreate(CreateView):
    form_class = ChartForm
    template_name = 'charts_app/chart_form.html'

    def get_initial(self):
        layer_id = self.kwargs['layer_id']
        initial = self.initial.copy()
        initial['layer'] = layer_id
        return initial

    def get_context_data(self, **kwargs):
        layer_id = self.kwargs['layer_id']
        layer = Layer.objects.get(pk=layer_id)
        fieldnames, num_fieldnames = get_fields(layer_id)
        ctx = super(ChartCreate, self).get_context_data(**kwargs)
        ctx['fieldnames'] = fieldnames
        ctx['num_fieldnames'] = num_fieldnames
        ctx['layer'] = layer
        return ctx


class ChartUpdate(UpdateView):
    model = Chart
    fields = '__all__'
    template_name_suffix = '_update_form'


class ChartDelete(DeleteView):
    model = Chart
    success_url = '/'


def pie_chart_v1(request):
    return render(request, 'pie_chart_v1.html')


def donut_chart_v1(request):
    return render(request, 'donut_chart_v1.html')


def pie_chart_v2(request):
    qdict = request.GET
    typename = qdict['lyrname']
    category_field = qdict['category']
    quantity_field = qdict['quantity']
    context = {
        'lyrname': typename,
        'category': category_field,
        'quantity': quantity_field
    }
    return render(request, 'pie_chart_v2.html', context)


def donut_chart_v2(request):
    return render(request, 'donut_chart_v2.html')
