from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Livre
from .forms import LivreForm

def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'livres/liste.html', {'livres': livres})

def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm()
    return render(request, 'livres/ajouter.html', {'form': form})

def modifier_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'livres/modifier.html', {'form': form, 'livre': livre})

def supprimer_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == 'POST':
        livre.delete()
        return redirect('liste_livres')
    return render(request, 'livres/supprimer.html', {'livre': livre})

def rechercher_livre(request):
    query = request.GET.get('q', '')
    if query:
        livres = Livre.objects.filter(
            models.Q(titre__icontains=query) | 
            models.Q(auteur__icontains=query)
        )
    else:
        livres = Livre.objects.all()
    return render(request, 'livres/liste.html', {'livres': livres, 'query': query})