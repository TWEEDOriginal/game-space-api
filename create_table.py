import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from app import create_app

from utils.generate_games import generate


def check_database_status(database):
    """
    Check database connection
    """

    try:
        database.session.execute(text("SELECT 1"))
        print("<h1>It works.</h1>")
    except:
        print("<h1>Something is broken.</h1>")
        sys.exit()


def drop_table(database):
    """
    Delete table if it already exists
    """

    database.engine.execute(
        """
        DROP TABLE IF EXISTS game;
        """
    )


def create_table(database):
    """
    Create game table with name, price and space
    """

    database.engine.execute(
        """
        CREATE TABLE game (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            price DECIMAL(65 , 2) NOT NULL,   
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


def select_table(database, limit=1):
    for record in database.engine.execute(f"SELECT * FROM game LIMIT {limit};"):
        print(record)


if __name__ == "__main__":
    db = SQLAlchemy(create_app())
    check_database_status(database=db)
    drop_table(database=db)
    create_table(database=db)
    seed_table(database=db)
    select_table(database=db)
