import os

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from customer.forms import CustomerForm
from customer.models import Customer


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
            return redirect('site:account')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifiez vos informations.")
    else:
        form = CustomerForm()

    context = {'form': form}
    return render(request, 'add-profil-customer.html', context)


@login_required(login_url='sign_in')
def edit_profil_customer(request, customer_id):
    user = request.user
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