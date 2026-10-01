from pydantic import BaseModel, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Электронная почта пользователя",
        examples=["student@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Пароль (минимум 8 символов)",
        examples=["password123"],
    )
    password_confirm: str = Field(
        ...,
        description="Повтор пароля для подтверждения",
        examples=["password123"],
    )

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"