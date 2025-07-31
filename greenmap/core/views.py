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
from .models import Agent, Citoyen, Reclamation


def home(request):
    return render(request, 'core/reclamation.html')



@csrf_exempt
def save_point(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            citoyen_id = data.get('citoyen_id')
            type_reclamation = data.get('type_reclamation')
            description = data.get('description')
            localisation = data.get('localisation')
            code_postale_id = data.get('code_postale_id')  # Optionnel
            priorite = data.get('priorite', 1)

            if not all([citoyen_id, type_reclamation, localisation]):
                return JsonResponse({'status': 'error', 'message': 'Champs requis manquants'}, status=400)

            citoyen = Citoyen.objects.get(id=citoyen_id)
            code_postale = CodePostale.objects.get(id=code_postale_id) if code_postale_id else None

            reclamation = Reclamation.objects.create(
                citoyen=citoyen,
                type_reclamation=type_reclamation,
                description=description,
                localisation=localisation,
                code_postale=code_postale,
                priorite=priorite
            )

            return JsonResponse({'status': 'success', 'reclamation_id': reclamation.id}, status=201)

        except Citoyen.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Citoyen introuvable'}, status=404)
        except CodePostale.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Code postal introuvable'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url='login')
def HomePage(request):
    return render (request,'core/reclamation.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Vérifie si le nom d'utilisateur existe déjà
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
            return redirect('signup')

        # Vérifie que les mots de passe correspondent
        if pass1 != pass2:
            return HttpResponse("Votre mot de passe et la confirmation ne correspondent pas !")

        # Crée l'utilisateur correctement avec create_user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

        messages.success(request, "Votre compte a été créé avec succès. Connectez-vous.")
        return redirect('login')

    return render(request, 'core/signup.html')


def LoginPage(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type == 'citoyen':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homecitoyen')
            else:
                messages.error(request, "Identifiants invalides pour citoyen")
                return redirect('login')

        elif user_type == 'agent':
            cin = request.POST.get('cin')
            try:
                agent = Agent.objects.get(cin=cin)  # suppose que tu as un modèle Agent
                # Ici pas de login Django, juste session manuelle
                request.session['agent_id'] = agent.id
                return redirect('home_agent')
            except Agent.DoesNotExist:
                messages.error(request, "CIN invalide pour agent")
                return redirect('login')

        else:
            messages.error(request, "Veuillez sélectionner un type d'utilisateur")
            return redirect('login')

    return render(request, 'core/login.html')


@login_required(login_url='login')
def homecitoyen(request):
    
    return render(request, 'core/homecitoyen.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

