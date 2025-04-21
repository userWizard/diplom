import logging

from django.http import HttpRequest
from django.core.cache import cache
from datetime import timedelta
from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

from app.application.api.customers.schemas import (
    AuthOutSchema,
    ChangePasswordSchema,
    CustomerOutSchema,
    LoginSchema,
    MeOutShema,
    RegisterSchema
)
from app.customers.models import Customers

router = Router(tags=['Customers'])

logger = logging.getLogger('customers')  # Получаем логгер

@router.post('/register', response=AuthOutSchema, operation_id='registration')
def register(request: HttpRequest, payload: RegisterSchema) -> AuthOutSchema:
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

        return {
            'user': user
        }
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        cache.set(ip_key, reg_attempts + 1, timeout=timedelta(hours=1).total_seconds())
        raise HttpError(500, f'Ошибка при создании пользователя: {str(e)}')


@router.post('/login', response=AuthOutSchema, operation_id='login')
def login(request: HttpRequest, payload: LoginSchema) -> AuthOutSchema:
    try:
        cache_key = f"login_attempts:{payload.email}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 20:
            logger.warning(f"Too many login attempts for email: {payload.email}")
            raise HttpError(429, "Слишком много попыток входа. Попробуйте позже.")

        try:
            user = Customers.objects.get(email=payload.email)
        except Customers.ObjectDoesNotExist:
            logger.warning(f"User not found: {payload.email}")
            raise HttpError(404, "Пользователь не найден")
        
        if user is None:
            cache.set(cache_key, attempts + 1, timeout=900)  # 15 минут
            logger.warning(f"Failed login for email: {payload.email}. Attempts: {attempts + 1}")
            raise HttpError(401, "Неверный email или пароль")

        if payload.password != user.password:
            logger.warning(f"Invalid password for user: {payload.email}")
            raise HttpError(401, "Неверный пароль")

        return {
            "user": CustomerOutSchema.from_orm(user)
        }
    except HttpError:
        raise  HttpError(401, "Неверные учетные данные.")
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HttpError(500, "Ошибка сервера")

@router.get('/me', response=MeOutShema, operation_id='me')
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


@router.delete('/logout', operation_id='logout')
def logout(request: HttpRequest):
    try:
        email = request.user.email
        logout(request)
        logger.info(f"User {email} logged out successfully")
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
        raise HttpError(500, "Logout failed")


@router.post('/change_password', response=AuthOutSchema, operation_id='change_password')
def change_password(request: HttpRequest, payload: ChangePasswordSchema) -> AuthOutSchema:
    try:
        user = request.user
        logger.info(f"Password change requested for {user.email}")
        
        if not user.is_authenticated:
            raise HttpError(401, "Требуется авторизация")
        
        # Проверка старого пароля
        if not payload.password:
            logger.warning(f"Invalid old password for {user.email}")
            raise HttpError(400, "Неверный текущий пароль")
        
                
        if payload.new_password != payload.current_password:
            raise HttpError('Пароли не совпадают. Повторите попытку еще раз!')
        
        # Установка нового пароля
        user.set_password(payload.new_password)
        user.save()
        
        logger.info(f"Password changed successfully for {user.email}")
        return {
            "user": user,
            "message": "Пароль успешно изменен"
        }
        
    except HttpError:
        raise
    except Exception as e:
        logger.error(f"Password change error for {user.email}: {str(e)}", exc_info=True)
        raise HttpError(500, "Ошибка при изменении пароля")
