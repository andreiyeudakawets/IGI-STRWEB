import logging

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import AnimalForm
from .models import Animal, Country, AnimalClass
from django.http import HttpResponseRedirect, HttpResponseNotFound


from django.views.generic.edit import CreateView, UpdateView, DeleteView

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def animal_list(request):
    logging.info(f'Вызвана страница всех животных')
    current_date = ''
    us_gr = ''
    current_date = timezone.localtime(timezone.now()).strftime('%d/%m/%Y')
    animals = Animal.objects.all()

    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    context = {
        'animals': animals, 'current_date': current_date,
        'us_gr': us_gr
    }

    return render(request, "animals/showall.html", context)


def search_animals(request):
    logging.info(f'Вызвана функция поиска')
    if request.method == 'GET':
        search_query = request.GET.get('q')

        if search_query:
            animals = Animal.objects.filter(name__icontains=search_query)
        else:
            animals = Animal.objects.all()

        return render(request, 'animals/showall.html', {'animals': animals, 'search_query': search_query})

    return redirect('/animals/')


def sort_animals(request):
    logging.info(f'Вызвана функция сортировки')
    if request.method == 'GET':
        sort_param = request.GET.get('sort_param')

        if sort_param == 'name':
            animals = Animal.objects.order_by('name')
        elif sort_param == 'age':
            animals = Animal.objects.order_by('age')
        elif sort_param == 'amount_of_feed':
            animals = Animal.objects.order_by('amount_of_feed')
        else:
            animals = Animal.objects.all()

        return render(request, 'animals/showall.html', {'animals': animals})

    return redirect('/animals/')

@permission_required(perm='animals.add_animal', raise_exception=True)
def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logging.info(f'Животное добавлено')
            return redirect('/animals/')  # Redirect to the animal list view
        else:
            logging.warning('Form isnt valid')
    else:
        form = AnimalForm()
    return render(request, 'animals/add_animal.html', {'form': form})


@permission_required(perm='animals.delete_animal', raise_exception=True)
def delete_animal(request, id):
    try:
        animal = Animal.objects.get(id=id)
        animal.delete()
        logging.info(f'Животное удалено')
        return redirect("/animals/")
    except Animal.DoesNotExist:
        logging.error(f'Animal not found')
        return HttpResponseNotFound("<h2>Animal not found</h2>")


@permission_required(perm='animals.change_animal', raise_exception=True)
def edit_animal(request, id):
    try:
        animal = Animal.objects.get(id=id)
        if request.method == 'POST':
            form = AnimalForm(request.POST, request.FILES, instance=animal)
            if form.is_valid():
                form.save()
                logging.info(f'Животное изменено')
                return redirect('/animals/')  # Redirect to the animal list view
            else:
                logging.warning('Form isnt valid')
        else:
            form = AnimalForm(instance=animal)
        return render(request, "animals/edit_animal.html", {'form': form})

    except Animal.DoesNotExist:
        logging.error(f'Animal not found')
        return HttpResponseNotFound("<h2>Animal not found</h2>")

def animal_family_population(request):
    families = AnimalClass.objects.all()
    selected_family = request.GET.get('family')

    logging.info(f'Вызвана страница популяции по семейству')

    if selected_family:
        animal_family = Animal.objects.filter(animal_class__name=selected_family)
        total_animals_count = animal_family.count()
    else:
        total_animals_count = 0

    return render(request, 'animals/animal_family_population.html',
                  {'families': families, 'selected_family': selected_family,
                   'total_animals_count': total_animals_count})

