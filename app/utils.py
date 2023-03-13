import re
from passlib.context import CryptContext

crpt_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(string: str):
    return crpt_contex.hash(string)

def clean_string(text: str) -> str:
    print(text)
    text = re.sub('\s', '', text)
    return text.lower()