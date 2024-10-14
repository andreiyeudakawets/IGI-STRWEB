import logging

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def room_list(request):
    user = request.user
    us_gr = ''

    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    logging.info(f'Вызвана страница всех помещений')
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms, 'user': user, 'us_gr': us_gr})


def add_room(request):

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logging.info(f'Комната добавлена')
            return redirect('/rooms/')
        else:
            logging.warning(f'Form is not valid')
    else:
        form = RoomForm()
    return render(request, 'rooms/add_room.html', {'form': form})


def delete_room(request, id):
    try:
        room = Room.objects.get(id=id)
        room.delete()
        logging.info(f'Комната {id} удалена')
        return redirect("/rooms/")
    except Room.DoesNotExist:
        logging.error(f'Room doesnt exist')
        return HttpResponseNotFound("<h2>Animal not found</h2>")


def edit_room(request, id):
    try:
        room = Room.objects.get(id=id)
        if request.method == 'POST':
            form = RoomForm(request.POST, request.FILES, instance=room)
            if form.is_valid():
                form.save()
                logging.info(f'Комната {id} изменена')
                return redirect('/rooms/')
        else:
            form = RoomForm(instance=room)
        return render(request, 'rooms/edit_room.html', {'form': form})
    except Room.DoesNotExist:
        logging.error(f'Room doesnt exist')
        return HttpResponseNotFound("<h2>Room not found</h2>")
