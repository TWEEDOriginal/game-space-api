from decimal import Decimal


def get_game_combination(game_list: list, pen_drive_space: int) -> dict:

    """Get the best combination of games that can fit into the pen drive

    Conditions:
        - total space of combination has to be less than or equal to pen drive space
        - total value has to be the highest total value of all possible game combinations

    Parameters:
        - pen_drive_space (int): space of the pen drive in bytes
        - game_list (list): list of all games that have a space less than or equal to pen drive space

    Returns (dict): game combination with the highest total value
    """
    total_value = 0.0
    best_game_combination = {
        "games": [],
        "total_space": 0,
        "remaining_space": pen_drive_space,
        "total_value": total_value,
    }

    for i in range(len(game_list) + 1):
        for j in range(i):
            sub_list = game_list[j:i]

            if (
                pen_drive_space - sum([x["space"] for x in sub_list]) >= 0
                and sum([Decimal(str(x["price"])) for x in sub_list]) > total_value
            ):
                total_value = sum([Decimal(str(x["price"])) for x in sub_list])

                best_game_combination = {
                    "games": game_list[j:i],
                    "total_space": sum([x["space"] for x in sub_list]),
                    "remaining_space": pen_drive_space
                    - sum([x["space"] for x in sub_list]),
                    "total_value": float(total_value),
                }

    return best_game_combination
