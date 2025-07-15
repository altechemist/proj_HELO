from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from .models import SupportTicket, TicketMessage, Feedback, Ticket

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'tickets': tickets
    }
    return render(request, 'support/ticket_list.html', context)

@login_required
def create_ticket(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        Ticket.objects.create(
            subject=subject,
            description=description,
        )
        return redirect("support:ticket_list")
    return render(request, "support/create_ticket.html")

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    ticket_messages = ticket.messages.all().order_by('created_at')
    context = {
        'ticket': ticket,
        'messages': ticket_messages
    }
    return render(request, 'support/ticket_detail.html', context)

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        # Handle ticket update form submission
        # This will be implemented with proper form handling
        pass
    return render(request, 'support/update_ticket.html', {'ticket': ticket})

@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.status = 'closed'
        ticket.save()
        messages.success(request, 'Ticket has been closed successfully.')
        return redirect('support:ticket_list')
    return render(request, 'support/close_ticket.html', {'ticket': ticket})

@login_required
def add_message(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        # Handle message form submission
        # This will be implemented with proper form handling
        pass
    return redirect('support:ticket_detail', ticket_id=ticket.id)

@login_required
def download_attachment(request, ticket_id, message_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    message = get_object_or_404(TicketMessage, id=message_id, ticket=ticket)
    if message.attachment:
        try:
            return FileResponse(message.attachment.open(), as_attachment=True)
        except FileNotFoundError:
            raise Http404()
    raise Http404()

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'support/feedback_list.html', context)

@login_required
def create_feedback(request):
    if request.method == 'POST':
        # Handle feedback form submission
        # This will be implemented with proper form handling
        pass
    return render(request, 'support/create_feedback.html')

@login_required
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, user=request.user)
    return render(request, 'support/feedback_detail.html', {'feedback': feedback})
