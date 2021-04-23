from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import View, DeleteView
from django.utils import timezone
from django.conf import settings

from .forms import *
from .utils import *
from .models import *


from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def ticket_list_open(request):
    tickets = Ticket.objects.filter(status="Open").order_by("-modified")
    search_query = request.GET.get('search', '')
    if search_query:
        tickets = Ticket.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    paginator = Paginator(tickets, 16)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'tickets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'ServiceDesk/index.html', context=context)


def ticket_list_resolved(request):
    tickets = Ticket.objects.filter(status="Resolved").order_by("-created")
    paginator = Paginator(tickets, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'tickets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render(request, 'ServiceDesk/index2.html', context=context)


def ticket_list_closed(request):
    tickets = Ticket.objects.filter(status="Closed").order_by("id")
    paginator = Paginator(tickets, 1)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'tickets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'ServiceDesk/index3.html', context=context)


def ticket_stats(request):
    ticket = Ticket.objects.filter(status='Closed')
    tickets = Ticket.objects.all().count()
    tickets_open = Ticket.objects.filter(status="Open").count()
    tickets_resolved = Ticket.objects.filter(status="Resolved").count()
    tickets_closed = Ticket.objects.filter(status="Closed").count()
    metric_hours: int = 0
    for ticket in ticket:
        metric_hours += (ticket.created - ticket.modified).total_seconds()
        # print(metric_hours)
    metric_hours /= tickets_closed
    metric_hours /= (60 * 60)
    metric_minutes = metric_hours * 60
    return render(request, 'ServiceDesk/ticket_stats.html', context={'tickets_open': tickets_open,
                                                                     'tickets_closed': tickets_closed,
                                                                     'tickets_resolved': tickets_resolved,
                                                                     'tickets': tickets,
                                                                     'metric_hours': metric_hours,
                                                                     'metric_minutes': metric_minutes})


class TicketDetail(ObjectDetailMixin, View):
    model = Ticket
    template = 'ServiceDesk/ticket_detail.html'


class TicketCreate(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'ServiceDesk/ticket_create_form.html', context={'form': form})

    def post(self, request):
        bound_form = TicketForm(request.POST)

        if bound_form.is_valid():
            new_ticket = bound_form.save()
            send_mail('Ваша проблема принята',
                      new_ticket.description,
                      settings.EMAIL_HOST_USER,
                      [new_ticket.email_address])
            return redirect(new_ticket)

        return render(request, 'ServiceDesk/ticket_create_form.html', context={'form': bound_form})


class TicketResolute(LoginRequiredMixin, View):
    def get(self, request, slug):
        ticket = Ticket.objects.get(slug__exact=slug)
        bound_form2 = TicketForm(instance=ticket)
        bound_form = TicketForm2(instance=ticket)
        return render(request, 'ServiceDesk/ticket_resolution.html', context={'form2': bound_form, 'ticket': ticket, 'form': bound_form2})

    def post(self, request, slug):
        ticket = Ticket.objects.get(slug__exact=slug)
        ticket.modified = ticket.created
        ticket.created = timezone.now()
        ticket.status = 'Closed'
        ticket.save()
        bound_form = TicketForm2(request.POST, instance=ticket)
        if bound_form.is_valid():
            ticket = bound_form.save()
            send_mail('Решение проблемы:',
                      ticket.resolution,
                      settings.EMAIL_HOST_USER,
                      [ticket.email_address],
                      fail_silently=True)

            return redirect(ticket)

        return render(request, 'ServiceDesk/ticket_resolution.html', context={
            'form2': bound_form,
            'ticket': ticket,
            }
        )

    raise_exception = True


class TicketUpdate(LoginRequiredMixin, View):
    def get(self, request, slug):
        ticket = Ticket.objects.get(slug__exact=slug)
        bound_form = TicketForm(instance=ticket)
        return render(request, 'ServiceDesk/ticket_update_form.html', context={'form': bound_form, 'ticket': ticket})

    def post(self, request, slug):
        ticket = Ticket.objects.get(slug__exact=slug)
        ticket.modified = ticket.created
        ticket.created = timezone.now()
        ticket.save()
        bound_form = TicketForm(request.POST, instance=ticket)
        if bound_form.is_valid():
            ticket = bound_form.save()
            send_mail('Ваша проблема обновлена',
                      ticket.description,
                      settings.EMAIL_HOST_USER,
                      [ticket.email_address])
            return redirect(ticket)

        return render(request, 'ServiceDesk/ticket_update_form.html', context={
            'form': bound_form,
            'ticket': ticket,
            }
        )

    raise_exception = True


class TicketDelete(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = '/'
    template_name = 'ServiceDesk/ticket_delete_form.html'

    raise_exception = True


def database(request):
    tickets = Ticket.objects.filter(status="Closed").order_by("-modified")
    return render(request, 'ServiceDesk/index3.html', context={'tickets': tickets})
