def validator(data: dict):

    """Validate upload game request payload

    Conditions:
        - game name must not an empty string
        - game price and game space must be positive

    Parameters:
        data (dict): request payload dictionary

    Raises an error if none of the conditions are met
    """
    for key, value in data.items():
        if type(value) == str:
            if not value.strip():
                raise Exception(f"Please input a valid game {key}")
        else:
            if value < 0.0:
                raise Exception(f"Game {key} can only be a positive value")


"""
JSON SCHEMA for post game request payload
Ensures the request payload has valid properties
"""
game_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [{"name": "Diablo 112", "price": 71.722, "space": 1073741824}],
    "required": ["name", "price", "space"],
    "properties": {
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["Diablo 112"],
        },
        "price": {
            "$id": "#/properties/price",
            "type": "number",
            "title": "The price schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0.0,
            "examples": [71.722],
        },
        "space": {
            "$id": "#/properties/space",
            "type": "integer",
            "title": "The space schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [1073741824],
        },
    },
    "additionalProperties": False,
}
