import pytest

# from create_table import create_table, seed_table, create_app, db
from ..utils.generate_games import generate
from ..app import create_app, db


def create_table(database):
    """
    Create game table with name, price and space
    """

    database.engine.execute(
        """
        CREATE TABLE game (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            price DECIMAL(65 , 5) NOT NULL,   
            space BIGINT NOT NULL
        );
        """
    )  # AUTOINCREMENT for id for other databases

    print("game table created successfully")


def seed_table(database, count=1000):
    """
    Insert randomly generated games into the database
    """

    for game in generate(count):
        try:
            database.engine.execute(
                f"""
                INSERT INTO game(name, price, space) VALUES 
                ('{game["name"]}', {game["price"]}, {game["space"]});
                """
            )
            print(f"{game} inserted successfully")
        except:
            print("\n")
            print(f">>>>>>>>>>>>>>>>>>>>>>>database insert failed for {game}")
            print("\n")


@pytest.fixture(scope="module")
def flask_connection():
    flask_app = create_app()
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="module")
def flask_connection_with_db():
    app = create_app()

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        db.init_app(app)
        create_table(database=db)

        for game in generate(10):
            try:

                seed_table(database=db, count=10)
            except:
                print("\n")
                print(f">>>>>>>>>>>>>>>>>>>>>>>DB insert failed for {game}")
                print("\n")

    yield client


@pytest.fixture(scope="session")
def get_games():
    games = [
        {"name": "FIFA22", "price": 500.92, "space": 2390222111},
        {"name": "FIFA21", "price": 100.99, "space": 4392221110},
        {"name": "Vanguard", "price": 600.12, "space": 2390232111},
        {"name": "Last of Us", "price": 50.92, "space": 1024678290},
        {"name": "Ghost", "price": 400.42, "space": 3290212191},
        {"name": "MarkTrip", "price": 71.722, "space": 1073741824},
        {"name": "Airforce One", "price": 71.722, "space": 973741824},
        {"name": "Diablo 112", "price": 71.722, "space": 2073741824},
    ]
    return games


@pytest.fixture(scope="session")
def get_pen_drive_space(get_games):
    pen_drive_space = sum([x["space"] for x in get_games])
    return pen_drive_space
