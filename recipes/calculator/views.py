from django.shortcuts import render
from django.http import HttpRequest

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
#---------------------------------------------------------------------------
#Для нормального вывода имени рецепта введём словарь «слаг → красивое имя»
RECIPE_TITLES = {
    'omlet': 'Омлет',
    'pasta': 'Паста',
    'buter': 'Бутерброд',
}

#Корневая страница
def home(request: HttpRequest):
    # пресеты для быстрых ссылок
    presets = [1, 2, 3, 4]

    # опционально можно подставить servings ко всем ссылкам со страницы
    servings = request.GET.get('servings')
    try:
        if servings is not None:
            s = int(servings)
            servings = str(max(1, s))
    except ValueError:
        servings = None

    context = {
        'recipes': sorted(DATA.keys()),
        'presets': presets,
        'servings': servings,  # строка или None
    }
    return render(request, 'calculator/home.html', context)


def recipe_view(request: HttpRequest, recipe: str):
    base = DATA.get(recipe)
    servings_str = request.GET.get('servings', '1')

    try:
        servings = int(servings_str)
        if servings < 1:
            servings = 1
    except ValueError:
        servings = 1

    context = {
        'recipe': {},                       # всегда есть ключ recipe
        'title': RECIPE_TITLES.get(recipe), # None, если рецепт неизвестен
        'servings': servings,               # удобно показать в заголовке
    }

    if base:
        scaled = {}
        for ingredient, amount in base.items():
            value = amount * servings
            if isinstance(value, float):
                value = round(value, 3)
            scaled[ingredient] = value
        context['recipe'] = scaled

    return render(request, 'calculator/index.html', context)