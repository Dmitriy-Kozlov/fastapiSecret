from fastapi import FastAPI, Body
from schemas import MessageCreate
from crud import SecretCRUD

app = FastAPI(
    title="One Secret"
)


@app.post("/generate")
async def generate_secret_key(message_data: MessageCreate):
    secret_key = await SecretCRUD.add(
        password=message_data.password,
        content=message_data.content,
    )
    return secret_key


@app.post("/secrets/{secret_key}")
async def get_secret(secret_key: str, password: str = Body()):
    secret = await SecretCRUD.find_one_or_none_by_secret_key_and_password(secret_key, password)
    return secret if secret else "None"
