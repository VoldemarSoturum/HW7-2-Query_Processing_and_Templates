import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    # Читаем данные из CSV файла, путь берем из settings.py
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';', quotechar='"')
        bus_stations_list = list(csv_reader)

#Получаем названия полей
    available_fields = list(bus_stations_list[0].keys()) if bus_stations_list else []

    # Отладочная информация
    if bus_stations_list:
        print("=== ДОСТУПНЫЕ ПОЛЯ В CSV ===")
        for i, field in enumerate(bus_stations_list[0].keys()):
            print(f"{i + 1}. {field}")
        print("=== ПЕРВАЯ ЗАПИСЬ ===")
        print(bus_stations_list[0])

    paginator = Paginator(bus_stations_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
         'bus_stations': page_obj.object_list,
         'page': page_obj,
         'available_fields': available_fields,
    }
    return render(request, 'stations/index.html', context)
