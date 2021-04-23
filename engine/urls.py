from django.urls import path

from .views import *

urlpatterns = [
    path('database/', database, name='database_url'),
    path('ticket-open/', ticket_list_open, name='ticket_list_open_url'),
    path('ticket-resolved/', ticket_list_resolved, name='ticket_list_resolved_url'),
    path('ticket-closed/', ticket_list_closed, name='ticket_list_closed_url'),
    path('ticket/create/', TicketCreate.as_view(), name='ticket_create_url'),
    path('ticket/<str:slug>/resolute/', TicketResolute.as_view(), name='ticket_resolute_url'),
    path('ticket/<str:slug>/', TicketDetail.as_view(), name='ticket_detail_url'),
    path('ticket/<str:slug>/update/', TicketUpdate.as_view(), name='ticket_update_url'),
    path('ticket/<str:slug>/delete/', TicketDelete.as_view(), name='ticket_delete_url'),
    path('ticket-stats/', ticket_stats, name='ticket_stats_url'),
]
