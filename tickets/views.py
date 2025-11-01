# tickets/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


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
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "tickets/update_ticket.html", {"form": form, "ticket": ticket})


@login_required
def resolve_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    ticket.status = "resolved"
    ticket.save()
    return redirect("ticket_detail", pk=ticket.pk)
