import random
from faker import Faker


def generate(count: int) -> list:

    """Generates a list of games to be populated into the database

    Parameters:
        count (int): number of games to be created

    Returns (list): list of randomly generated games
    """
    fake = Faker()
    return [
        {
            "name": f"{fake.user_name()} {fake.word()}".title(),
            "price": round(random.SystemRandom().uniform(2, 1000), 2),
            "space": random.randint(100, 10737418240),
        }
        for i in range(count)
    ]
