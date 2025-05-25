import logging

from django.http import HttpRequest
from django.core.cache import cache
from datetime import timedelta
from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from app.application.api.customers.schemas import (
    ChangePasswordSchema,
    LoginSchema,
    MeOutShema,
    RegisterSchema,
    RegisterOutSchema,
    RegisterInSchema,
    LoginOutSchema,
    LoginInSchema,
    ChangePasswordOutSchema,
    ChangePasswordInSchema
)
from app.customers.models import Customers

router = Router(tags=['Customers'])

logger = logging.getLogger('customers')  # Получаем логгер

@router.post('register/', response=RegisterInSchema, operation_id='registration')
def register(request: HttpRequest, payload: RegisterSchema) -> RegisterOutSchema:
    try:
        ip_key = f"reg_attempts:{request.META.get('REMOTE_ADDR')}"
        reg_attempts = cache.get(ip_key, 0)
        
        if reg_attempts >= 20:
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
        
        user = Customers.objects.create(
            username=payload.username,
            email=payload.email,
            phone_number=payload.phone_number,
            password=make_password(payload.password)
        )

        cache.delete(ip_key)
        logger.info(f"New user registered: {user.email} (ID: {user.id})")

        return RegisterInSchema(
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            password=user.password
        )
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        cache.set(ip_key, reg_attempts + 1, timeout=timedelta(hours=1).total_seconds())
        raise HttpError(500, f'Ошибка при создании пользователя: {str(e)}')


@router.post('login/', response=LoginInSchema, operation_id='login')
def login(request: HttpRequest, payload: LoginSchema) -> LoginOutSchema:
    try:
        cache_key = f"login_attempts:{payload.email}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 20:
            logger.warning(f"Too many login attempts for email: {payload.email}")
            raise HttpError(429, "Слишком много попыток входа. Попробуйте позже.")

        user = get_object_or_404(Customers, email=payload.email)
        
        if user is None:
            cache.set(cache_key, attempts + 1, timeout=900)  # 15 минут
            logger.warning(f"Failed login for email: {payload.email}. Attempts: {attempts + 1}")
            raise HttpError(401, "Неверный email или пароль")

        if not check_password(payload.password, user.password):
            cache.set(cache_key, attempts + 1, timeout=900)  # 15 минут
            logger.warning(f"Failed login for email: {payload.email}. Attempts: {attempts + 1}")
            raise HttpError(401, "Неверный email или пароль")

        cache.delete(cache_key)
        logger.info(f"User logged in: {user.email} (ID: {user.id})")

        return LoginInSchema(
            email=user.email,
            password=user.password
        )

    except HttpError:
        raise  HttpError(401, "Неверные учетные данные.")
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HttpError(500, "Ошибка сервера")


@router.get('me/', response=MeOutShema, operation_id='me')
def me(request: HttpRequest) -> MeOutShema:
    try:
        user = request.user
        
        if not user.is_authenticated:
            raise HttpError(401, "Требуется авторизация")

        logger.info(f"User info requested for {request.user.email}")        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    except Exception as e:
        logger.error(f"Error in me endpoint: {str(e)}", exc_info=True)
        raise HttpError(500, "Internal server error")


@router.delete('logout/', operation_id='logout')
def logout(request: HttpRequest):
    try:
        email = request.user.email
        logout(request)
        logger.info(f"User {email} logged out successfully")
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
        raise HttpError(500, "Logout failed")


@router.post('change_password/', response=ChangePasswordInSchema, operation_id='change_password')
def change_password(request: HttpRequest, payload: ChangePasswordSchema) -> ChangePasswordOutSchema:
    try:
        user = request.user
        logger.info(f"Password change requested for {user.email}")
        
        if not user.is_authenticated:
            raise HttpError(401, "Требуется авторизация")
        
        # Проверка старого пароля
        if not payload.password:
            logger.warning(f"Invalid old password for {user.email}")
            raise HttpError(400, "Неверный текущий пароль")
        
                
        if not check_password(payload.new_password, payload.current_password):
            logger.warning(f"The passwords don't match. Make sure that the data is entered correctly: {payload.new_password}:{payload.current_password}")
            raise HttpError('Пароли не совпадают. Повторите попытку еще раз!')
        
        # Установка нового пароля
        user.set_password(payload.new_password)
        user.save()
        
        logger.info(f"Password changed successfully for {user.email}")
        return ChangePasswordInSchema(password=payload.password, new_password=payload.new_password, current_password=payload.current_password)
        
    except HttpError:
        raise
    except Exception as e:
        logger.error(f"Password change error for {user.email}: {str(e)}", exc_info=True)
        raise HttpError(500, "Ошибка при изменении пароля")
