from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    # ----------------------------Ajout et modif client#-------------------------

    path('add-profil-customer', views.add_profil_customer, name='add_profil_customer'),
    path('edit-profil-customer/<int:user_id>/', views.edit_profil_customer, name='edit_profil_customer'),
    # administration bds
    path('administration', views.administration, name='administration'),

    # -----------------------------------------------------------------------------
    # ----------------------------------Partials----------------------------------
    # -----------------------------------------------------------------------------

    path("administration/dashboard", views.dashboard_partial, name="dashboard"),

    # ----------------------------------Customers----------------------------------
    path("administration/members", views.members_partial, name="members"),
    path("administration/members/table", views.members_table, name="members_table"),
    path("administration/members/<int:customer_id>/edit", views.edit_members_partial, name="edit_members"),
    path("administration/members/<int:customer_id>/delete", views.delete_member, name="delete_member"),
    path("administration/members/<int:customer_id>/details", views.details_client_admin, name="details_client_admin"),

    path("administration/modal-close", views.modal_close, name="modal_close"),

    # --------------------------------Project customer----------------------------------

    path("administration/project/", views.project_partial, name="project"),
    path("project/<int:project_id>/edit/", views.edit_project, name="project_edit"),
    path("project/<int:project_id>/", views.details_project, name="details_project"),
    path("project/<int:project_id>/delete/", views.delete_project, name="delete_project"),

    # --------------------------------Document customer----------------------------------
    path(
        "administration/documents-clients/",
        views.add_documents_clients_partial,
        name="add_documents_clients_partial"
    ),
    path(
        "documents/<int:document_id>/edit/",
        views.edit_documents_clients_partial,
        name="edit_documents_clients_partial",
    ),
    path("documents/<int:document_id>/delete/", views.delete_document, name="delete_document"),

    # --------------------------------Messages reçus----------------------------------
    path("administration/messages/", views.messages_clients_partial, name="messages_clients_partial"),
    path(
        "messages-clients/<int:message_client_id>/details/",
        views.message_clients_details_partial,
        name="message_clients_details_partial"
    ),
    path(
        "messages/<int:message_client_id>/checked/",
        views.checked_message,
        name="checked_message"
    ),
    path("message/<int:message_client_id>/delete/", views.delete_message, name="delete_message"),

    # ----------------------------------Devis reçus----------------------------------

    path("administration/devis/", views.devis_clients_partial, name="devis_clients_partial"),
    path(
        "devis/<int:devi_id>/details/",
        views.devis_details_partial,
        name="devis_details_partial"
    ),

    path(
        "devis/<int:devi_id>/checked/",
        views.checked_devis,
        name="checked_devis"
    ),

    path("devis/<int:devi_id>/delete/", views.delete_devis, name="delete_devis"),

    # ----------------------------------Tickets  reçus----------------------------------

    path("administration/tikets/", views.tickets_partial, name="tickets_partial"),
    path("details-ticket/tikets/<int:ticket_id>/", views.tickets_details, name="tickets_details"),
    path(
        "tickets/<int:ticket_id>/message/add/",
        views.add_ticket_message,
        name="add_ticket_message"
    ),
    path(
        "tickets/<int:ticket_id>/close/",
        views.close_ticket,
        name="close_ticket"
    ),

    path(
        "tickets/<int:ticket_id>/delete/",
        views.delete_ticket,
        name="delete_ticket"
    ),
]
