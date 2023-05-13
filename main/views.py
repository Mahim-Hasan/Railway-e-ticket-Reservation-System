import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import auth
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import redirect, render

from main.models import *


def home(request):
    if "action" in request.GET and request.is_ajax:
        id = request.GET.get('id')
        ends = End.objects.filter(start_id=id).values()
        ends_list = list(ends)
        return JsonResponse(ends_list, safe=False)

    elif request.method == "POST":
        start_id = request.POST["from"]
        end_id = request.POST["to"]
        date = request.POST["date"]
        class_type = request.POST["class"]
        adult = int(request.POST["adult"])
        child = int(request.POST["child"])

        end = End.objects.get(id=end_id)
        end_distance = end.distance

        total_passengers = adult + (child/2)
        costs = 0

        if class_type == "ac_b":
            costs = end_distance * 8 * total_passengers
        elif class_type == "ac_s":
            costs = end_distance * 6 * total_passengers
        elif class_type == "snigdha":
            costs = end_distance * 4 * total_passengers
        elif class_type == "s_chair":
            costs = end_distance * 2 * total_passengers

        start_name = Start.objects.get(id=start_id)
        end_name = end.name
        trains = Train.objects.filter(end__id=end_id)


        ticket = request.session.get('ticket')
        if ticket:
            ticket.clear()
            ticket['start_id'] = start_id
            ticket['end_id'] = end_id
            ticket['date'] = date
            ticket['class_type'] = class_type
            ticket['adult'] = adult
            ticket['child'] = child
        else:
            ticket = {}
            ticket['start_id'] = start_id
            ticket['end_id'] = end_id
            ticket['date'] = date
            ticket['class_type'] = class_type
            ticket['adult'] = adult
            ticket['child'] = child
        request.session['ticket'] = ticket

        print(request.session['ticket'])
        ticket_test = request.session['ticket']
        print(ticket_test['start_id'])

        context = {
            'trains': trains,
            'from': start_name,
            'to': end_name,
            'date': date,
            'class': class_type,
            'adult': adult,
            'child': child,
            'costs': costs
        }

        return render(request, 'dashboard.html', context)

    elif request.method == "GET":
        starts = Start.objects.all()
        context = {
            'starts': starts
        }
        return render(request, 'index.html', context)


@login_required(login_url='/user/login')
def purchase(request, id):
    if request.method == "POST":
        train = Train.objects.get(id=id)
        ticket = request.session['ticket']
        start = Start.objects.get(id=ticket['start_id']).name
        end_obj = End.objects.get(id=ticket['end_id'])
        end = end_obj.name
        class_type = ticket['class_type']
        date = ticket['date']
        adult = ticket['adult']
        child = ticket['child']
        seats = adult + child
        ticket_no = uuid.uuid4().hex[:15]
        trans_id = request.POST["trans_id"]


        end_distance = end_obj.distance
        total_passengers = adult + (child/2)
        costs = 0

        if class_type == "ac_b":
            costs = end_distance * 8 * total_passengers
        elif class_type == "ac_s":
            costs = end_distance * 6 * total_passengers
        elif class_type == "snigdha":
            costs = end_distance * 4 * total_passengers
        elif class_type == "s_chair":
            costs = end_distance * 2 * total_passengers

        book_ticket = Ticket(ticket_no=ticket_no, start=start, end=end, total_seats=seats, class_type=class_type, cost=costs, travel_time=date, is_active=True, train=train, passenger=request.user)
        book_ticket.save()

        train.seats = train.seats - seats
        train.save()


        return redirect('/profile/')

    elif request.method == "GET":
        return render(request, 'purchase.html')



@login_required(login_url='/user/login')
def profile(request):
    tickets = Ticket.objects.filter(passenger=request.user)
    context = {
        'tickets': tickets
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/user/login')
def cancel_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.user.id == ticket.passenger_id:
        ticket.delete()
        messages.success(request, 'Ticket cancelled successfully!')
        return redirect("/profile/")
    else:
        return render(request, "404.html")


def verify(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        ticket = Ticket.objects.filter(passenger__username=phone)
        if ticket:
            messages.success(request, 'Your ticket was found in database!')
            return redirect('/verify/')
        else:
            messages.error(request, 'Your ticket was not found in database!')
            return redirect('/verify/')
    else:
        return render(request, 'verify.html')



def contact(request):
    return render(request, 'contact.html')

def error_page(request):
    return render(request, '404.html')
