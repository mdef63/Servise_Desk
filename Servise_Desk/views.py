from django.shortcuts import redirect


def redirect_block(request):
    return redirect('ticket_list_open_url', permanent=True)