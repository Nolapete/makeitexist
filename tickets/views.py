# tickets/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm, TicketUpdateForm


@login_required
def ticket_list(request):
    status_filter = request.GET.get('status', 'active')
    
    if status_filter == 'all':
        tickets = Ticket.objects.filter(created_by=request.user).order_by("-created_at")
    elif status_filter == 'resolved':
        tickets = Ticket.objects.filter(created_by=request.user, status='resolved').order_by("-created_at")
    elif status_filter == 'closed':
        tickets = Ticket.objects.filter(created_by=request.user, status='closed').order_by("-created_at")
    else:  # active (default)
        tickets = Ticket.objects.filter(created_by=request.user).exclude(status__in=['resolved', 'closed']).order_by("-created_at")
    
    context = {
        'tickets': tickets,
        'current_status': status_filter,
        'status_choices': [
            ('active', 'Active'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
            ('all', 'All'),
        ]
    }
    
    if request.headers.get('HX-Request'):
        return render(request, "tickets/ticket_list_partial.html", context)
    
    return render(request, "tickets/ticket_list.html", context)


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            print(f"\n--- DEBUGGING FORM ERRORS ---\n{form.errors}\n---------------------------\n")
            return redirect("ticket_list")
        else:
            print("form is not valid")
    else:
        form = TicketForm()
    return render(request, "tickets/create_ticket.html", {"form": form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        form = TicketUpdateForm(instance=ticket)
    return render(request, "tickets/update_ticket.html", {"form": form, "ticket": ticket})


@login_required
def resolve_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    ticket.status = "resolved"
    ticket.save()
    return redirect("ticket_detail", pk=ticket.pk)


@login_required
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    ticket.status = "closed"
    ticket.save()
    return redirect("ticket_detail", pk=ticket.pk)
