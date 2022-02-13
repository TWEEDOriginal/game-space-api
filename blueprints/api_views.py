from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from jsonschema import validate as json_validate

try:
    from app import db
    from utils.game_schema import validator, game_schema
    from utils.game_combination import get_game_combination
except ImportError:
    from ..app import db
    from ..utils.game_schema import validator, game_schema
    from ..utils.game_combination import get_game_combination

main = Blueprint("main", __name__, url_prefix="/api/v1")


@main.route("/status", methods=["GET", "HEAD"])
def status():
    """
    Checks if the web server can connect to the database

    Returns
        - (json): database connection status if it is a get request
        - appropriate status code
    """
    try:
        db.session.execute(text("SELECT 1"))
        health_status = {"database": "healthy"}
        status = 200
    except:
        health_status = {"database": "unhealthy"}
        status = 502

    return jsonify(health_status), status


@main.route("/games", methods=["POST"])
def save_game():
    """Upload game to the database

    Request body:
        (json): name, price and space

    Requirements:
        - Name must not be an empty string and it must be unique(no two games can have the same name)
        - Price must be a positive Floating point number
        - Space must be a positive integer in bytes

    Database Operations:
        Inserts a validated game into the database

    Returns:
        - (json):
            - Created game if the game was created successfully
                                OR
            - Error message if the game does not meet one or more requirements
        - appropriate status code
    """
    data = request.json

    if not data:
        return (
            jsonify(
                {"status": "error", "message": "please input a valid request body"}
            ),
            403,
        )

    try:
        json_validate(instance=data, schema=game_schema)
    except Exception as e:
        return (
            jsonify({"status": "error", "data": data, "message": str(e.message)}),
            400,
        )

    try:
        validator(data)
        name, price, space = data["name"], data["price"], data["space"]

    except Exception as e:
        return jsonify({"status": "error", "data": data, "message": str(e)}), 400

    try:
        db.engine.execute(
            f"""
        INSERT INTO game(name, price, space) VALUES 
        ('{name}', {price}, {space});
        """
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "status": "error",
                    "data": data,
                    "message": "A game with that name already exists in the database",
                }
            ),
            400,
        )

    return jsonify(data), 201


@main.route("/best_value_games", methods=["POST"])
def get_best_value_games():

    """Get the best combination of games that can fit into the pendrive

    Query Parameters:
        pen_drive_space(int): space in bytes

    Conditions:
        - Combination of games must have the highest total value of all possible game combinations and also fit the given pen-drive space
        - pen_drive_space query parameter must be a positive integer

    Database Operations:
        Get all games that have a space less than or equal to the pen drive space

    Returns:
        - (json):
            - A list of games, total_space of the game comnbination, remaining space left on the pen_drive and total value of the game combination
                                OR
            - Error message if the pen_drive_space is not a positive integer
        - appropriate status code
    """
    pen_drive_space = request.args.get("pen_drive_space")
    try:
        pen_drive_space = int(str(pen_drive_space))

        if pen_drive_space < 0:
            raise ValueError("Negative integer")
    except ValueError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Pen drive space of {pen_drive_space} bytes is not a positive integer",
                }
            ),
            400,
        )

    records = db.engine.execute(
        f"""
        SELECT * FROM game
        WHERE space <= {pen_drive_space}
        ORDER BY space ASC;
    """
    )
    # print([record for record in db.engine.execute("SELECT * FROM game;")])
    # print("\n")
    game_list = [
        {"name": record[1], "price": record[2], "space": record[3]}
        for record in records
    ]
    print(game_list)

    return jsonify(get_game_combination(game_list, pen_drive_space)), 200
