from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
import string
import random
from django.conf import settings
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def home(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        password = request.POST.get('password')
        expiration = request.POST.get('expiration')
        
        short_code = generate_short_code()
        
        # Encrypt the URL
        f = Fernet(settings.FERNET_KEY)
        encrypted_url = f.encrypt(original_url.encode())
        
        url_instance = URL(original_url=encrypted_url.decode(), short_code=short_code)
        
        if password:
            url_instance.password = make_password(password)
        
        if expiration:
            url_instance.expires_at = timezone.now() + timedelta(minutes=int(expiration))

        url_instance.save()
        
        short_url = request.build_absolute_uri('/') + short_code
        return render(request, 'shortener/success.html', {'short_url': short_url})
        
    return render(request, 'shortener/home.html')

def redirect_url(request, short_code):
    try:
        url_instance = URL.objects.get(short_code=short_code)
    except URL.DoesNotExist:
        return render(request, 'shortener/not_found.html')

    if url_instance.expires_at and url_instance.expires_at < timezone.now():
        return render(request, 'shortener/expired.html')
    
    if url_instance.password:
        if request.method == 'POST':
            password = request.POST.get('password')
            if check_password(password, url_instance.password):
                # Decrypt the URL before redirecting
                f = Fernet(settings.FERNET_KEY)
                decrypted_url = f.decrypt(url_instance.original_url.encode()).decode()
                return redirect(decrypted_url)
            else:
                return render(request, 'shortener/password.html', {'error': 'Incorrect password'})
        return render(request, 'shortener/password.html')
        
    # Decrypt the URL before redirecting
    f = Fernet(settings.FERNET_KEY)
    decrypted_url = f.decrypt(url_instance.original_url.encode()).decode()
    return redirect(decrypted_url)
