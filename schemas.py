from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор сообщения")
    secret_key: str = Field(..., description="Секретный ключ по которому можно получить сообщение")
    password: str = Field(..., description="Пароль для получения сообщения")
    content: bytes = Field(..., description="Содержимое сообщения")


class MessageCreate(BaseModel):
    password: str = Field(..., description="Пароль для получения сообщения")
    content: str = Field(..., description="Содержимое сообщения")