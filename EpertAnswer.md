ОТВЕТ ЭКСПЕРТА НЕТОЛОГИИ, НО ОНО КАКОЕ_ТО ДЫРЯВОЕ

Рецепты
urls.py
```python
"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from calculator.views import recipes

urlpatterns = [
    path('<str:name>/', recipes)
]
```
Пагинация
views.py
```python
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv


with open(settings.BUS_STATION_CSV, newline='', encoding="utf-8") as f:
    csv_data = csv.DictReader(f)
    bus_stations_list = []
    for row in csv_data:
        bus_stations_list.append(row)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stations_list, 10)
    page = paginator.get_page(current_page)
    context = {
        'bus_stations': page.object_list,
        'page': page
    }
    return render(request, 'stations/index.html', context)
```

