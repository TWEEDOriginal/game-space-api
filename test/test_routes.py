import json


def test_page_404(flask_connection):
    response = flask_connection.get(
        "/random_route",
    )
    assert response.status_code == 404


def test_homepage_redirect(flask_connection):
    response = flask_connection.get(
        "/",
    )
    assert response.status_code == 302


def test_swagger_url(flask_connection):
    response = flask_connection.get(
        "/static/swagger.json",
    )
    assert response.status_code == 200


def test_docs_redirect(flask_connection):
    response = flask_connection.get(
        "/docs",
    )
    assert response.status_code == 308


def test_status(flask_connection_with_db):
    response = flask_connection_with_db.get(
        "/api/v1/status",
    )
    assert response.status_code == 200


def test_games(flask_connection_with_db, get_games):
    game = get_games[0]
    response = flask_connection_with_db.post(
        "/api/v1/games",
        data=json.dumps(game),
        content_type="application/json",
    )
    assert response.status_code == 201


def test_best_value_games(flask_connection_with_db, get_games):
    pen_drive_space = 9827128972
    response = flask_connection_with_db.post(
        f"/api/v1/best_value_games?pen_drive_space={pen_drive_space}",
        content_type="application/json",
    )
    res = response.json
    assert response.status_code == 200
    assert len(res) > 0
    assert pen_drive_space >= res["total_space"]
