import os
import random
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import OTP, CustomUser, LoginToken
from .serializers import CustomUserSerialzer, OTPSerialzer
from .utils import generate_token, send_sms


@csrf_exempt
@api_view(['POST'])
def send_otp(request: Request) -> Response:
    serializer = OTPSerialzer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        phone_number: str = data['phone_number']

        # Generate a random 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save the OTP to the database
        OTP.objects.create(otp=otp, phone_number=phone_number)

        # Send the OTP via SMS
        message = f'Your OTP is: {otp}'
        send_sms(phone_number, message)

        return Response({'message': 'OTP sent successfully'})

    print("serializer.errors: ", serializer.errors)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
def verify_otp(request: Request) -> Response:
    serializer = OTPSerialzer(data=request.data)
    if serializer.is_valid():
        data: dict[str, Any] = request.data
        otp = str(data['otp'])
        phone_number = str(data['phone_number'])
        try:
            db_otp = OTP.objects.get(phone_number=phone_number)

            if db_otp.otp == otp:
                login(request, phone_number=phone_number)
                try:

                    user = CustomUser.objects.get(phone_number=phone_number)
                    token = generate_token(user.id)
                    # type: ignore

                    loginToken = LoginToken.objects.create(
                        user_id=user.id, token=token, is_active=True)
                    loginToken.save()

                    return Response({'message': 'OTP verification success', 'newUser': False, 'loginToken': token})
                except ObjectDoesNotExist:
                    return Response(data={'message': 'OTP verification success', 'newUser': True})
            else:
                return Response({'message': 'Invalid OTP'})
        except Exception as exc:
            # print(e)
            # the number sent in request never got its otp triggered
            return Response({'message': f'Invalid OTP, {exc}'})

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def create_user(request: Request) -> Response:
    serializer = CustomUserSerialzer(data=request.data)
    if serializer.is_valid():
        data: dict[str, Any] = request.data
        name: str = data['name']
        email: str = data['email']
        age: str = data['age']
        phone_number: str = data['phone_number']
        try:
            user = CustomUser.objects.create(
                name=name, email=email, age=age, phone_number=phone_number)
            token: str = generate_token(user.id)
            LoginToken.objects.create(
                user_id=user, token=token, is_active=True)
            return Response({'message': 'User created', 'token': token})
        except BaseException as exc:
            print("got error in creating the user")
            return Response({f"user creation failure: {exc}"}, status=564)
    return Response(serializer.errors, status=400)


def middleware_authenticateUser(request: Request):
    # jwt.decode(token, jwt_token_secret, algorithms=['HS256'])
    pass


def login(request: Request, phone_number: str):
    try:
        LoginTokenObj = LoginToken.objects.get(phone_number=phone_number)

        return JsonResponse({'message': 'Logged in'})
    except Exception as exc:
        return JsonResponse({'message': f'Invalid token {exc}'})
