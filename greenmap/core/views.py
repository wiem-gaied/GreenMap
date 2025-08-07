from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Reclamation, Citoyen, CodePostale
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Agent, Citoyen, Reclamation
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CitoyenRegisterForm
from .forms import ReclamationForm
from .forms import AgentRegisterForm




#def home(request):
#   return render(request, 'core/reclamation.html')


def choisir(request):
    return render(request, 'core/choisir.html')


def login_agent(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                # Vérifier si un objet Agent est lié à l'utilisateur
                agent = Agent.objects.get(user=user)
                login(request, user)
                request.session['agent_id'] = agent.id
                return redirect('AgentReclamations')  # <- Redirection vers la page principale agent
            except Agent.DoesNotExist:
                messages.error(request, "Ce compte n'est pas enregistré comme agent.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'core/login_agent.html')

def login_citoyen(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                citoyen = Citoyen.objects.get(user=user)
                login(request, user)
                request.session['citoyen_id'] = citoyen.id  # Stocke l'ID du citoyen en session
                return redirect('mesreclamations')  # Redirige vers la page des réclamations du citoyen
            except Citoyen.DoesNotExist:
                messages.error(request, "Ce compte n'est pas enregistré comme citoyen.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'core/login_citoyen.html')
    
def signup_citoyen(request):
    if request.method == 'POST':
        form = CitoyenRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_citoyen')  # ou la page de connexion
    else:
        form = CitoyenRegisterForm()
    return render(request, 'core/signup_citoyen.html', {'form': form})

def signup_agent(request):
    if request.method == 'POST':
        form = AgentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_agent')
    else:
        form = AgentRegisterForm()
    return render(request, 'core/signup_agent.html', {'form': form})



@csrf_exempt  # À retirer si tu passes bien le CSRF token dans ton JS
@login_required
def save_point(request):
    if request.method == 'POST':
        type_reclamation = request.POST.get('reclamation_type')
        description = request.POST.get('description')
        localisation = request.POST.get('localisation')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        code_postale = request.POST.get('postal_code')
        image = request.FILES.get('image')
        
        # Récupérer l'utilisateur connecté
        user = request.user

        # Trouver le citoyen correspondant
        try:
            citoyen = Citoyen.objects.get(user=user)
        except Citoyen.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profil citoyen introuvable pour cet utilisateur.'})

        # Récupérer l'objet CodePostale
        try:
            code_postale = CodePostale.objects.get(num=code_postale)
        except CodePostale.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Code postal introuvable'})

        # Créer la réclamation
        reclamation = Reclamation.objects.create(
            citoyen=citoyen,
            type_reclamation=type_reclamation,
            description=description,
            localisation=localisation,
            latitude=latitude,
            longitude=longitude,
            code_postale=code_postale,
            image=image
        )

        return JsonResponse({'status': 'success', 'message': 'Réclamation enregistrée avec succès !'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required
def ADDreclamation(request):
    try:
        citoyen = Citoyen.objects.get(user=request.user)
    except Citoyen.DoesNotExist:
        # Rediriger si le profil Citoyen n'existe pas
        return redirect('signup_citoyen')  # Assure-toi que cette URL est bien définie dans tes urls.py

    if request.method == 'POST':
        form = ReclamationForm(request.POST, request.FILES)
        if form.is_valid():
            reclamation = form.save(commit=False)
            reclamation.citoyen = citoyen
            reclamation.save()
            return redirect('mesreclamations')
    else:
        form = ReclamationForm()

    return render(request, 'core/ADDreclamation.html', {'form': form})


@login_required
def mesreclamation(request):
    try:
        citoyen = Citoyen.objects.get(user=request.user)

        # Associer les anciennes réclamations non liées (si possible)
        reclamations_sans_citoyen = Reclamation.objects.filter(citoyen__isnull=True, localisation__icontains=citoyen.nom)

        for r in reclamations_sans_citoyen:
            r.citoyen = citoyen
            r.save()

        # Récupérer toutes les réclamations de ce citoyen
        mes_reclamations = Reclamation.objects.filter(citoyen=citoyen)

        return render(request, 'core/mesreclamations.html', {
            'reclamations': mes_reclamations
        })

    except Citoyen.DoesNotExist:
        return render(request, 'erreur.html', {
            'message': 'Aucun profil citoyen trouvé pour cet utilisateur.'
        })

@login_required
def modifier_reclamation(request, id):
    reclamation = get_object_or_404(Reclamation, id=id, citoyen__user=request.user)

    if request.method == 'POST':
        reclamation.type_reclamation = request.POST.get('type_reclamation')
        reclamation.localisation = request.POST.get('localisation')
        reclamation.description = request.POST.get('description')
        reclamation.latitude = request.POST.get('latitude')
        reclamation.longitude = request.POST.get('longitude')

        if request.FILES.get('image'):
            reclamation.image = request.FILES['image']

        reclamation.save()
        return redirect('mesreclamations')

    type_choices = Reclamation._meta.get_field('type_reclamation').choices
    return render(request, 'core/modifier.html', {
        'reclamation': reclamation,
        'type_choices': type_choices,
    })

@login_required
@csrf_exempt  # Nécessaire si tu ne passes pas le token CSRF correctement en AJAX
def supprimer_reclamation(request, id):
    if request.method == "POST":
        reclamation = get_object_or_404(Reclamation, id=id, citoyen__user=request.user)
        if reclamation.etat == 'En attente':
            reclamation.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': "Réclamation déjà traitée."}, status=403)
    return JsonResponse({'error': "Méthode non autorisée"}, status=405)
    


def LogoutPage(request):
    logout(request)
    return redirect('choisir')
    

def AgentReclamations(request):
    # Vérifie si l'agent est connecté via la session
    agent_id = request.session.get('agent_id')
    if not agent_id:
        return redirect('login_agent')

    try:
        agent = Agent.objects.get(id=agent_id)
        reclamations = Reclamation.objects.filter(code_postale=agent.code_postale)
    except Agent.DoesNotExist:
        reclamations = []
        agent = None

    context = {
        'agent': agent,
        'reclamations': reclamations,
    }
    return render(request, 'core/reclamations_par_code_postale.html', context)

@csrf_exempt
@login_required
def modifier_etat_reclamation(request, reclamation_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nouvel_etat = data.get('etat')
            reclamation = Reclamation.objects.get(id=reclamation_id)
            reclamation.etat = nouvel_etat
            reclamation.save()
            return JsonResponse({"message": "Statut mis à jour"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


@login_required
def reclamation_detail(request, reclamation_id):
    reclamation = get_object_or_404(Reclamation, id=reclamation_id)

    if request.method == 'POST':
        new_etat = request.POST.get('etat')
        if new_etat in ['En attente', 'Acceptée', 'Rejetée']:
            reclamation.etat = new_etat
            reclamation.save()
            return redirect('reclamation_detail', reclamation_id=reclamation.id)

    return render(request, 'core/reclamation_detail.html', {'reclamation': reclamation})