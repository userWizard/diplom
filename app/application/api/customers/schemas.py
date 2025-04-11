from ninja import Schema, ModelSchema
from pydantic import EmailStr, field_validator
import re

from app.customers.models import Customers

class RegisterSchema(Schema):
    """Валидация формы данных регистрации."""
    username: str
    email: EmailStr
    phone_number: str
    password: str
    
    @field_validator('username')
    def username_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Имя не может быть пустым')
        return v.strip()
    
    @field_validator('phone_number')
    def phone_number_valid(cls, v):
        if not v.strip():
            raise ValueError('Телефон не может быть пустым')
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Номер должен быть в формате +7XXXXXXXXXX")
        return v.strip()
    
    @field_validator('password')
    def password_valid(cls, v):
        if not v:
            raise ValueError('Пароль не может быть пустым')
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        
        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        
        # Проверка на наличие хотя бы одного специального символа
        special_chars = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_chars, v):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ: !@#$%^&*(),.?":{}|<>')
        
        return v

class LoginSchema(Schema):
    """Валидация формы данных авторизации."""
    email: EmailStr
    password: str
    
    @field_validator('password')
    def password_valid(cls, v):
        if not v:
            raise ValueError('Пароль не может быть пустым')
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        
        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        
        # Проверка на наличие хотя бы одного специального символа
        special_chars = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_chars, v):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ: !@#$%^&*(),.?":{}|<>')
        
        return v

class CustomerOutSchema(ModelSchema):
    class Config:
        model = Customers
        model_fields = ['id', 'username', 'email', 'phone_number']

class AuthOutSchema(Schema):
    token: str
    user: CustomerOutSchema

class MeOutShema(Schema):
    id: int
    name: str
    email: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str
    
    @field_validator('old_password')
    def old_password_valid(cls, v):
        if not v:
            raise ValueError('Старый пароль не может быть пустым')
        return v
    
    @field_validator('new_password')
    def new_password_valid(cls, v):
        if not v:
            raise ValueError('Новый пароль не может быть пустым')
        if len(v) < 8:
            raise ValueError('Новый пароль должен содержать минимум 8 символов')
        
        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(char.isupper() for char in v):
            raise ValueError('Новый пароль должен содержать хотя бы одну заглавную букву')
        
        special_chars = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_chars, v):
            raise ValueError('Новый пароль должен содержать хотя бы один специальный символ: !@#$%^&*(),.?\":{}|<>')
        return v