# firebase_auth/views.py
from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import auth
from .Firebase import initialize_firebase  # Importeer de initialize_firebase-functie
from django.contrib.auth import authenticate, login
import requests

# Initialiseer Firebase bij de eerste import van views
initialize_firebase()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verzend het aanmeldingsverzoek naar Firebase Authentication REST API
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBXTn-ByCNA6utmMsWiOZfWINSXNd-_Bmw'
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        response = requests.post(url, json=data)

        # Verwerk de Firebase-response
        if response.status_code == 200:
            firebase_response = response.json()
            id_token = firebase_response.get('idToken')
            # Hier kun je het JWT-token gebruiken om de gebruiker in te loggen in je Django-applicatie
            return JsonResponse({'success': True, 'id_token': id_token})
        else:
            # Behandel fouten
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            return JsonResponse({'success': False, 'error_message': error_message}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Method not allowed'}, status=405)

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        # Controleer of de gebruiker al bestaat
        try:
            user = auth.get_user_by_email(email)
            return JsonResponse({'success': False, 'error_message': 'User with provided email already exists'})
        except auth.UserNotFoundError:
            # De gebruiker bestaat nog niet, dus maak een nieuwe gebruiker aan
            try:
                new_user = auth.create_user(email=email, password=password)
                print(new_user.uid)  # Controleren of de nieuwe gebruiker correct is gemaakt
                return JsonResponse({'success': True, 'user_id': new_user.uid})
            except auth.AuthError as e:
                return JsonResponse({'success': False, 'error_message': str(e)})

    return render(request, 'FirebaseAuth/register.html')


def logout_view(request):
    # Implementeer de afmelding functionaliteit, zoals sessie-invalide of token-invalide.
    # Voorbeeld:
    # auth.revoke_refresh_tokens(uid)
    # auth.create_session_cookie(...)
    return JsonResponse({'success': True})
