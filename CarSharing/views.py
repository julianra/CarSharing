# views.py in de juiste app
from django.shortcuts import render,redirect
from django.contrib import messages

def home(request):
    display_name = request.session.get('display_name')  # Haal de gebruikersnaam op uit de sessie
    if display_name:
        return render(request, 'FirebaseAuth/home.html', {'display_name': display_name})
    else:
        # Gebruiker is niet ingelogd, doorsturen naar de loginpagina
        messages.error(request, 'Je moet ingelogd zijn om toegang te krijgen tot deze pagina.')
        return redirect('login')
