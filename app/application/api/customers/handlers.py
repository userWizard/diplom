import jwt
import logging

from django.http import HttpRequest
from django.core.cache import cache
from datetime import timedelta
from ninja import Router
from ninja.security import django_auth
from ninja.errors import HttpError
from django.contrib.auth import authenticate, login, logout

from app.application.api.customers.schemas import (
    AuthOutSchema,
    ChangePasswordSchema,
    LoginSchema,
    MeOutShema,
    RegisterSchema
)
from app.customers.models import Customers

router = Router(tags=['Customers'])

logger = logging.getLogger('customers')  # Получаем логгер

@router.post('/register', response=AuthOutSchema, auth=None)
def register(request: HttpRequest, payload: RegisterSchema) -> AuthOutSchema:
    try:
        ip_key = f"reg_attempts:{request.META.get('REMOTE_ADDR')}"
        reg_attempts = cache.get(ip_key, 0)
        
        if reg_attempts >= 3:
            logger.warning(f"Too many registration attempts from IP: {request.META.get('REMOTE_ADDR')}")
            raise HttpError(429, "Слишком много попыток регистрации. Попробуйте позже.")
        
        if Customers.objects.filter(email=payload.email).exists():
            cache.set(ip_key, reg_attempts + 1, timeout=timedelta(hours=1).total_seconds())
            logger.warning(f"Registration attempt with existing email: {payload.email}")
            raise HttpError(400, 'Пользователь с таким email уже существует')
        
        if Customers.objects.filter(phone_number=payload.phone_number).exists():
            cache.set(ip_key, reg_attempts + 1, timeout=timedelta(hours=1).total_seconds())
            logger.warning(f"Registration attempt with existing phone: {payload.phone_number}")
            raise HttpError(400, 'Пользователь с таким телефоном уже существует')
        
        user = Customers.objects.create_user(
            username=payload.username,
            email=payload.email,
            phone_number=payload.phone_number,
            password=payload.password
        )

        cache.delete(ip_key)
        logger.info(f"New user registered: {user.email} (ID: {user.id})")
        
        token = jwt.encode(
            {'id': user.id, 'email': user.email},
            algorithm='HS256'
        )

        return {
            'token': token,
            'user': user
        }
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        cache.set(ip_key, reg_attempts + 1, timeout=timedelta(hours=1).total_seconds())
        raise HttpError(500, f'Ошибка при создании пользователя: {str(e)}')


@router.post('/login', response=AuthOutSchema, auth=None)
def login(request: HttpRequest, payload: LoginSchema) -> AuthOutSchema:
    try:
        cache_key = f"login_attempts:{payload.email}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 3:
            logger.warning(f"Too many login attempts for email: {payload.email}")
            raise HttpError(429, "Слишком много попыток входа. Попробуйте позже.")
        
        user = authenticate(email=payload.email, password=payload.password)
        
        if user is not None and user.is_active:
            cache.delete(cache_key)
            login(request, user)
            token = jwt.encode(
                {
                    'id': user.id, 'email': user.email
                },
                algorithm='HS256'
            )
            logger.info(f"Successful login for user: {user.email}")
            return {
                'token': token,
                'user': user
            }
        
        cache.set(cache_key, attempts + 1, timeout=timedelta(minutes=15).total_seconds())
        logger.warning(f"Failed login attempt for email: {payload.email}. Attempts: {attempts + 1}")
        raise HttpError(401, "Неверные учетные данные. Осталось попыток: {}".format(2 - attempts))
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HttpError(500, "Внутренняя ошибка сервера")


@router.get('/me', response=MeOutShema, auth=django_auth)
def me(request: HttpRequest) -> MeOutShema:
    try:
        logger.info(f"User info requested for {request.user.email}")
        return request.user
    except Exception as e:
        logger.error(f"Error in me endpoint: {str(e)}", exc_info=True)
        raise HttpError(500, "Internal server error")


@router.delete('/logout', auth=django_auth)
def logout(request: HttpRequest):
    try:
        email = request.user.email
        logout(request)
        logger.info(f"User {email} logged out successfully")
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
        raise HttpError(500, "Logout failed")


@router.post('/change_password', response=AuthOutSchema, auth=django_auth)
def change_password(request: HttpRequest, payload: ChangePasswordSchema) -> AuthOutSchema:
    try:
        user = request.user
        logger.info(f"Password change requested for {user.email}")
        
        # Проверка старого пароля
        if not user.check_password(payload.old_password):
            logger.warning(f"Invalid old password for {user.email}")
            raise HttpError(400, "Неверный текущий пароль")
        
        # Установка нового пароля
        user.set_password(payload.new_password)
        user.save()
        
        # Генерация нового токена
        token = jwt.encode(
            {
                'id': user.id, 'email': user.email
            },
                algorithm='HS256'
        )
        
        logger.info(f"Password changed successfully for {user.email}")
        return {
            "token": token,
            "user": user,
            "message": "Пароль успешно изменен"
        }
        
    except HttpError:
        raise
    except Exception as e:
        logger.error(f"Password change error for {user.email}: {str(e)}", exc_info=True)
        raise HttpError(500, "Ошибка при изменении пароля")
