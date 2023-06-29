# views.py

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from twilio.rest import Client
from .models import CustomUser


def send_otp(phone_number, otp):
    account_sid = settings.OTP_TWILIO_ACCOUNT_SID
    auth_token = settings.OTP_TWILIO_AUTH_TOKEN
    from_phone_number = settings.OTP_TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=from_phone_number,
        to=phone_number
    )


def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'is_staff': user.is_staff
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        # Verify OTP
        stored_otp = request.session.get('otp')
        if otp != stored_otp:
            return JsonResponse({'error': 'Invalid OTP'})

        # Create user
        employment_history = request.POST.get('employment_history')
        education = request.POST.get('education')
        skills = request.POST.get('skills')

        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            employment_history=employment_history,
            education=education,
            skills=skills
        )

        # Generate JWT
        jwt_token = generate_jwt(user)

        # Clear OTP from session
        del request.session['otp']

        return JsonResponse({'token': jwt_token})

    return JsonResponse({'error': 'Invalid request method'})


def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        # Verify OTP
        stored_otp = request.session.get('otp')
        if otp != stored_otp:
            return JsonResponse({'error': 'Invalid OTP'})

        # Authenticate user
        user = authenticate(request, phone_number=phone_number)
        if user is None:
            return JsonResponse({'error': 'Invalid phone number'})

        # Generate JWT
        jwt_token = generate_jwt(user)

        # Clear OTP from session
        del request.session['otp']

        return JsonResponse({'token': jwt_token})

    return JsonResponse({'error': 'Invalid request method'})
