from pydantic import BaseModel
from pydantic import EmailStr, field_validator
import re

from app.customers.models import Customers

class RegisterSchema(BaseModel):
    """Валидация формы данных регистрации."""
    username: str
    email: str
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


class RegisterOutSchema(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    password: str


class RegisterInSchema(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str


class LoginSchema(BaseModel):
    """Валидация формы данных авторизации."""
    email: str
    password: str
    
    @field_validator('password')
    def password_valid(cls, v):
        if not v:
            raise ValueError('Пароль не может быть пустым')
        return v

class LoginOutSchema(BaseModel):
    id: int
    username: str
    email: str

class LoginInSchema(BaseModel):
    email: str
    password: str


class MeOutShema(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    password: str


class ChangePasswordSchema(BaseModel):
    """Валидация формы данных смены пароля."""
    password: str
    new_password: str
    current_password: str
    
    @field_validator('password')
    def password_valid(cls, v):
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


class ChangePasswordOutSchema(BaseModel):
    id: MeOutShema
    password: str
    new_password: str
    current_password: str

 
class ChangePasswordInSchema(BaseModel):
    password: str
    new_password: str
    current_password: str

    
