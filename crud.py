import string
import random
from cryptography.fernet import Fernet
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from database import async_session_maker
from models import Secret
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

key = b'Kscw3eVnLxB_j5vlfaV3wTuGnamYmzIVi7wNqN9zvSU='
# key = Fernet.generate_key()
# print(key)
cipher_suite = Fernet(key)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_encript(content: str):
    return cipher_suite.encrypt(content.encode('utf-8'))


def get_decript(content: bytes):
    return cipher_suite.decrypt(content).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class SecretCRUD:
    model = Secret

    @classmethod
    async def find_one_or_none_by_secret_key_and_password(cls, data_secret_key: str, data_password: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(secret_key=data_secret_key)
            result = await session.execute(query)
            plain_result = result.scalar_one_or_none()
            if plain_result and verify_password(data_password, plain_result.password):
                return get_decript(plain_result.content)

    @classmethod
    async def add(cls, **values):

        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                hash_password = get_password_hash(new_instance.password)
                encript_content = get_encript(new_instance.content)
                new_instance.content = encript_content.decode('utf-8')
                new_instance.password = hash_password
                secret_key = random_string()
                new_instance.secret_key = secret_key
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return secret_key
