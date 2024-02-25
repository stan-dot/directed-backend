from random import random
import re
from passlib.context import CryptContext
from sqlalchemy.orm import Session


crpt_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(string: str):
    return crpt_contex.hash(string)

def clean_string(text: str) -> str:
    print(text)
    text = re.sub('\s', '', text)
    return text.lower()

parts_2 = ["Smart", "Red", "Blue", "Green", "Mint"]
parts_3 = [
    "Rabbit",
    "Duck",
    "Shrimp",
    "Pig",
    "Bee",
    "Goat",
    "Crab",
    "Deer",
    "Turkey",
    "Dove",
    "Sheep",
    "Fish",
    "Chicken",
    "Horse",
    "Dog",
    "Cat",
    "Goose",
    "Llama",
    "Ostrich",
    "Camel",
    "Ox",
    "Reindeer",
    "Cow",
    "Tiger",
    "Lion",
    "Elephant",
    "Cheetah",
    "Gorilla",
    "Zebra",
    "Penguin",
]

def generate_pseudonym(user_part: str) -> str:
    # Randomly select from the constant parts
    part_2 = random.choice(parts_2)
    part_3 = random.choice(parts_3)

    # Combine the parts to form the pseudonym
    pseudonym = f"{user_part}{part_2}{part_3}"

    return pseudonym
