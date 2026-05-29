import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from customer.forms import CustomerForm, CustomerAdminForm, ProjectForm, DocumentsForm, TicketMessageForm
from customer.models import Customer, MyProject, Documents, Fonctions, Ticket
from site_bds.models import Contact
from site_bds.views import is_superuser
from yourproject.models import Question


@login_required(login_url='sign_in')
def add_profil_customer(request):
    user = request.user

    # Vérifier si le profil existe déjà
    if Customer.objects.filter(user=user).exists():
        messages.warning(request, "Vous avez déjà un profil.")
        return redirect('account')

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = user
            customer.email = user.email
            customer.register_web = True
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.save()
            customer.save()

            messages.success(request, 'Votre profil a été créé avec succès.')
            return redirect('account')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifiez vos informations.")
    else:
        form = CustomerForm()

    context = {'form': form}
    return render(request, 'add-profil-customer.html', context)


@login_required(login_url='sign_in')
def edit_profil_customer(request, user_id):
    user = request.user
    customer_id = user.customer.id
    try:
        customer = Customer.objects.get(id=customer_id, user=user)
    except Customer.DoesNotExist:
        raise Http404("Profil introuvable ou non autorisé.")

    customer = get_object_or_404(Customer, id=customer_id)
    old_image = customer.image.path if customer.image and customer.image.name else None
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():

            # Vérifier si une nouvelle image est uploadée et supprimer l'ancienne
            if 'image' in request.FILES:
                if old_image and os.path.exists(old_image):
                    os.remove(old_image)

            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            customer.email = user.email
            user.save()
            customer.save()
            form.save()

            messages.success(request, 'Votre profil a été modifié avec succès.')
            return redirect('account')
        else:
            messages.error(request, "Erreur lors de la modification du profil.")

    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'customer': customer
    }

    return render(request, 'edit-profil-customer.html', context)


# ----------------- administration for dmin ----------------------

@user_passes_test(is_superuser)
def administration(request):
    messages_clients = Contact.objects.filter(checked=False).order_by('-created_at')
    messages_clients_checked = Contact.objects.all().order_by('-created_at')
    messages_clients_count = messages_clients.count()
    messages_clients_checked_count = messages_clients_checked.count()

    tickets = Ticket.objects.all().order_by('-created_at')
    tickets_count = Ticket.objects.filter(
        status=Ticket.IN_PROGRESS
    ).count()

    devis = Question.objects.filter(checked=False).order_by('-created_at')
    devis_checked = Question.objects.all().order_by('-created_at')
    devis_count = devis.count()

    context = {
        'messages_clients': messages_clients,
        'messages_clients_count': messages_clients_count,
        'devis': devis,
        'devis_count': devis_count,
        'messages_clients_checked': messages_clients_checked,
        'messages_clients_checked_count': messages_clients_checked_count,
        'devis_checked': devis_checked,
        'tickets': tickets,
        'tickets_count': tickets_count,
    }
    return render(request, "admin-customer/administration.html", context)


# ----------------- dashboard for dmin ----------------------

@user_passes_test(is_superuser)
def dashboard_partial(request):
    customers = Customer.objects.all().order_by('last_name')
    customers_count = customers.count()

    messages_clients = Contact.objects.filter(checked=False)
    messages_clients_checked = Contact.objects.all().order_by('-created_at')
    messages_clients_count = messages_clients.count()
    messages_clients_checked_count = messages_clients_checked.count()

    projects = MyProject.objects.all().order_by('-created_at')[:5]
    projects_count = projects.count()

    documents = Documents.objects.all().order_by('-created_at')
    documents_count = documents.count()

    context = {
        'customers_count': customers_count,
        'customers': customers,

        'projects': projects,
        'projects_count': projects_count,

        'documents': documents,
        'documents_count': documents_count,

        'messages_clients': messages_clients,
        'messages_clients_count': messages_clients_count,
        'messages_clients_checked': messages_clients_checked,
        'messages_clients_checked_count': messages_clients_checked_count,
    }
    return render(request, "admin-customer/partials/_dashboard.html", context)


# ----------------- Customer for dmin ----------------------

@user_passes_test(is_superuser)
def members_partial(request):
    customers = Customer.objects.all().order_by('-last_name')

    customers_count = customers.count()

    if request.method == "POST":
        form = CustomerAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client est bien enregistré")
            return redirect("customer:administration")
        else:
            messages.error(request, "Ce client existe déjà")
    else:
        form = CustomerAdminForm()

    context = {
        "customers": customers,
        "customers_count": customers_count,
        "form": form,
    }

    return render(request, "admin-customer/partials/_members.html", context)


@user_passes_test(is_superuser)
def members_table(request):
    q = request.GET.get("q", "").strip()
    page_number = request.GET.get("page", 1)

    qs = Customer.objects.filter().order_by("-last_name")

    if q:
        qs = qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(mail__icontains=q) |
            Q(phone__icontains=q) |
            Q(entreprise__icontains=q)
        )

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "q": q,
    }

    return render(request, "admin-customer/partials/_members_table_block.html", context)


@user_passes_test(is_superuser)
def edit_members_partial(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        form = CustomerAdminForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Le membre a bien été modifié.")

            resp = HttpResponse("")
            resp["HX-Trigger"] = "memberUpdated"
            return resp
    else:
        form = CustomerAdminForm(instance=customer)

    context = {
        "customer": customer,
        "form": form,
    }

    return render(request, "admin-customer/partials/_edit_member_modal.html", context)


@user_passes_test(is_superuser)
def delete_member(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        try:
            customer.delete()
            messages.success(request, "L’adhérent a bien été supprimé.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer le client : il est lié à des applications."
            )

        return redirect("customer:administration")

    return redirect("customer:administration")


@user_passes_test(is_superuser)
def modal_close(request):
    return HttpResponse("")


@user_passes_test(is_superuser)
def details_client_admin(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    projects = MyProject.objects.filter(user=customer)
    documents = Documents.objects.filter(user=customer)

    documents_dict = {doc.document_name: doc for doc in documents}

    context = {
        "customer": customer,
        "projects": projects,
        "documents_dict": documents_dict,
        "DOCS_CHOICES": dict(Documents.DOCS_CHOICES)
    }

    return render(request, "admin-customer/details-client-admin.html", context)


# ----------------- Projects for dmin ----------------------

@user_passes_test(is_superuser)
def project_partial(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Projet enregistré.")
            return redirect("customer:administration")
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        project_form = ProjectForm()

    projects = MyProject.objects.all().order_by('-created_at')

    context = {
        "project_form": project_form,
        "projects": projects,
    }

    return render(request, "admin-customer/partials/_project.html", context)


@user_passes_test(is_superuser)
def edit_project(request, project_id):
    project = get_object_or_404(MyProject, id=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Le projet a bien été modifié.")
            return redirect("customer:administration")
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = ProjectForm(instance=project)

    context = {
        "form": form,
        "project": project,
    }
    return render(request, "admin-customer/edit_project.html", context)


@user_passes_test(is_superuser)
def details_project(request, project_id):
    project = MyProject.objects.get(id=project_id)

    documents = Documents.objects.filter(user=project.user)
    documents_dict = {doc.document_name: doc for doc in documents}
    functions = Fonctions.objects.filter(project=project)

    context = {
        'project': project,
        'documents': documents,
        "documents_dict": documents_dict,
        "DOCS_CHOICES": dict(Documents.DOCS_CHOICES),
        "functions": functions,
    }

    return render(request, "admin-customer/details-project.html", context)


@user_passes_test(is_superuser)
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(MyProject, id=project_id)

    try:
        project.delete()
        messages.success(request, "Le projet a bien été supprimé.")
        return redirect("customer:administration")

    except ProtectedError:
        messages.error(
            request,
            "Impossible de supprimer ce projet : il contient encore des fonctions liées."
        )
        return redirect("customer:details_project", project_id)


# ----------------- Ajout doc clients----------------------

@user_passes_test(is_superuser)
def add_documents_clients_partial(request):
    if request.method == "POST":
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Les document sont bien enregistrés')
            return redirect("customer:administration")
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = DocumentsForm()

    context = {
        "form": form,

    }
    return render(request, 'admin-customer/partials/_add-client-doc.html', context)


@user_passes_test(is_superuser)
def edit_documents_clients_partial(request, document_id):
    document = get_object_or_404(Documents, id=document_id)

    if request.method == "POST":
        form = DocumentsForm(request.POST, request.FILES, instance=document)
        old_document = document.document.path if document.document else None

        if form.is_valid():

            # Nouveau fichier uploadé
            if 'document' in request.FILES:
                if old_document and os.path.exists(old_document):
                    os.remove(old_document)

            form.save()
            messages.success(request, 'Les document sont bien enregistrés')
            return redirect("customer:administration")
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = DocumentsForm(instance=document)

    context = {
        "form": form,
        "document": document,
    }
    return render(request, 'admin-customer/partials/_edit-client-doc.html', context)


@user_passes_test(is_superuser)
@require_POST
def delete_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    project = get_object_or_404(MyProject, user=document.user)

    document.delete()

    messages.success(request, "Le document a bien été supprimé.")

    return redirect("customer:details_project", project.id)


# ----------------- Messages clients----------------------

@user_passes_test(is_superuser)
def messages_clients_partial(request):
    messages_clients = Contact.objects.filter(checked=False)
    messages_clients_checked = Contact.objects.all().order_by('-created_at')

    context = {
        "messages_clients": messages_clients,
        "messages_clients_checked": messages_clients_checked,
    }
    return render(request, 'admin-customer/partials/_messages.html', context)


@user_passes_test(is_superuser)
def message_clients_details_partial(request, message_client_id):
    message_client = get_object_or_404(Contact, id=message_client_id)

    context = {
        "message_client": message_client,
    }
    return render(request, 'admin-customer/partials/_message-client-details.html', context)


@user_passes_test(is_superuser)
@require_POST
def delete_message(request, message_client_id):
    message_client = get_object_or_404(Contact, id=message_client_id)

    message_client.delete()

    messages.success(request, "Le message a bien été supprimé.")

    return redirect(reverse("customer:administration") + "?section=messages")


@user_passes_test(is_superuser)
@require_POST
def checked_message(request, message_client_id):
    message_client = get_object_or_404(Contact, id=message_client_id)

    message_client.checked = request.POST.get("checked") == "on"
    message_client.save()

    messages.success(request, "Le statut du message a bien été mis à jour.")

    return redirect(reverse("customer:administration") + "?section=messages")

# ----------------- Devis clients----------------------

@user_passes_test(is_superuser)
def devis_clients_partial(request):
    devis = Question.objects.all().order_by('-created_at')

    context = {
        "devis": devis,
    }
    return render(request, 'admin-customer/partials/_devis.html', context)


@user_passes_test(is_superuser)
def devis_details_partial(request, devi_id):
    devi = get_object_or_404(Question, id=devi_id)

    context = {
        "devi": devi,
    }
    return render(request, 'admin-customer/partials/_devis-details.html', context)


@user_passes_test(is_superuser)
@require_POST
def delete_devis(request, devi_id):
    devi = get_object_or_404(Question, id=devi_id)

    devi.delete()

    messages.success(request, "Le devi a bien été supprimé.")

    return redirect("customer:administration")


@user_passes_test(is_superuser)
@require_POST
def checked_devis(request, devi_id):
    devi = get_object_or_404(Question, id=devi_id)

    devi.checked = request.POST.get("checked") == "on"
    devi.save()

    messages.success(request, "Le statut du devis a bien été mis à jour.")

    return redirect(reverse("customer:administration") + "?section=devis")


# ----------------- Projects for dmin ----------------------

@user_passes_test(is_superuser)
def tickets_partial(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    tickets_count = Ticket.objects.filter(
        status=Ticket.IN_PROGRESS
    ).count()

    context = {
        "tickets": tickets,
        'tickets_count': tickets_count,
    }

    return render(request, "admin-customer/partials/_ticket.html", context)


@login_required(login_url='sign_in')
def tickets_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    messages_ticket = ticket.messages.all()
    message_form = TicketMessageForm()

    context = {
        "ticket": ticket,
        "messages_ticket": messages_ticket,
        "message_form": message_form,
    }

    return render(request, "admin-customer/details-ticket.html", context)

@login_required
def add_ticket_message(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = TicketMessageForm(request.POST, request.FILES)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.author = request.user
            msg.save()

            # Statut automatique
            if request.user.is_superuser:
                ticket.status = Ticket.WAITING_CLIENT
            else:
                ticket.status = Ticket.IN_PROGRESS

            ticket.save()

            # Notification mail simple
            if request.user.is_superuser:
                recipient = ticket.customer.mail
            else:
                recipient = "contact@bds38.com"

            if recipient:
                EmailMessage(
                    subject=f"Nouvelle réponse ticket : {ticket.title}",
                    body=f"Une nouvelle réponse a été ajoutée au ticket : {ticket.title}",
                    from_email="BDS <contact@bds38.com>",
                    to=[recipient],
                ).send(fail_silently=True)

            messages_ticket = ticket.messages.all()

            html = render_to_string(
                "admin-customer/partials/_ticket-conversation.html",
                {
                    "ticket": ticket,
                    "messages_ticket": messages_ticket,
                    "message_form": TicketMessageForm(),
                },
                request=request
            )

            return HttpResponse(html)

    messages_ticket = ticket.messages.all()

    html = render_to_string(
        "admin-customer/partials/_ticket-conversation.html",
        {
            "ticket": ticket,
            "messages_ticket": messages_ticket,
            "message_form": form,
        },
        request=request
    )

    return HttpResponse(html)


@login_required
@require_POST
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # sécurité client
    if not request.user.is_superuser:
        customer = get_object_or_404(Customer, user=request.user)
        if ticket.customer != customer:
            return HttpResponseForbidden()

    ticket.status = Ticket.CLOSED
    ticket.closed_at = timezone.now()
    ticket.save()

    messages.success(request, "Le ticket a bien été clôturé.")

    return redirect("customer:tickets_details", ticket.id)


@login_required
@require_POST
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # sécurité client
    if not request.user.is_superuser:
        customer = get_object_or_404(Customer, user=request.user)

        if ticket.customer != customer:
            return HttpResponseForbidden()

    ticket.delete()

    messages.success(request, "Le ticket a bien été supprimé.")

    if request.user.is_superuser:
        return redirect("customer:administration")

    return redirect("customer:tickets_client")