import random

try:
    from utils.generate_games import generate
except ImportError:
    from ..utils.generate_games import generate


def test_generate_game():
    games = generate(10)
    assert len(games) == 10
    assert type(games[random.randint(0, 9)]["space"]) == int
    assert type(games[random.randint(0, 9)]["name"]) == str
    assert type(games[random.randint(0, 9)]["price"]) == float
