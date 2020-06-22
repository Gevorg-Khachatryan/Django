from django.shortcuts import render, HttpResponse
import re
import os

from .forms import File_input_form
from .models import Data, Files


def choose_file(request):
    if request.POST:
        documents = Files.objects.all()

        for document in documents:
            os.remove(document.file.name)
            document.delete()

        csv_file = request.FILES['file']
        data = csv_file.read().decode('UTF-8')
        rows = re.split('\n', data)
        for i in range(len(rows)):
            rows[i] = rows[i].split(',')
        cols = rows[0]
        cols = list(map(lambda i: i.replace('\r', ''), cols))
        rows = rows[1:]
        save_file = Files()
        save_file.file = csv_file
        save_file.save()
        return render(request, 'map.html', {'data': rows, 'cols': cols})
    form = File_input_form()
    return render(request, 'index.html', {'form': form})


def save_data(request):
    file_obj = Files.objects.first()
    file = file_obj.file
    data = file.read().decode('UTF-8')
    rows = re.split('\n', data)
    for i in range(len(rows)):
        rows[i] = rows[i].split(',')
    cols = rows[0]
    cols = list(map(lambda i: i.replace('\r', ''), cols))

    rows = rows[1:]
    ind = {}
    for i in cols:
        ind.update({i: int(request.POST[i])})
    if request.POST:
        for i in rows:
            if len(i) > 1:
                if len(i[0]) > 0:
                    data = Data()
                    data.series_reference = i[ind['Series_reference']]
                    data.period = i[ind['Period']]
                    data.data_value = i[ind['Data_value']]
                    data.status = i[ind['STATUS']]
                    data.units = i[ind['UNITS']]
                    data.subject = i[ind['Subject']]
                    data.group = i[ind['Group']]
                    data.save()
        return HttpResponse("Success  <a href='http://127.0.0.1:8000/admin/app/data/'>Look in admin panel </a>")
    return render(request, 'map.html')
