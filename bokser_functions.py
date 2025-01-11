def get_data_from_user():
    age = get_input("\nAge: ", validate_age, "Are you sure it is correct age?")
    height = get_input("\nHeight(cm): ", validate_height, "Are you sure it is correct height(cm)?")
    weight = get_input("\nWeight(kg): ", validate_weight, "Are you sure it is correct weight(kg)?")
    weight_class = check_weight_class(weight)
    style_num = get_input("\nStyle:\n1 - Outfighter.\n2 - Infighter.\n3 - Boxer.\n4 - Brawler.\n", validate_style_number, "Please choose from the list.")
    style = validate_style(style_num)
    ranking = get_input("\nRanking: ", validate_ranking, "Please choose between 1 and 25 000.")
    wins = get_input("\nWins: ", validate_fights, "Are you sure this is correct?")
    losses = get_input("\nLosses: ", validate_fights, "Are you sure this is correct?")
    draws = get_input("\nDraws: ", validate_fights, "Are you sure this is correct?")
    no_contest = get_input("\nNo contest: ", validate_fights, "Are you sure this is correct?")
        
    new_boxer_list = [age, height, weight, weight_class, style, ranking, wins, losses, draws, no_contest]
    return new_boxer_list


def get_input(promt, validation_func, error_message):
    """Validates input from a user."""
    while True:
        value = input(promt)
        if validation_func(value):
            return value
        else:
            print(error_message)


def validate_name(name: str) -> bool:
    return len(name) <= 40 and not name.isnumeric() and name != ""


def validate_age(age: str) -> bool:
    if not age.isnumeric():
        return False
    return 15 <= int(age) <= 65


def validate_fights(fights: str) -> bool:
    if not fights.isnumeric():
        return False
    return 0 <= int(fights) <= 1000


def validate_height(height: str) -> bool:
    try:
        return 100.0 <= float(height) <= 300.0
    except:
        return False
    

def validate_weight(weight: float) -> bool:
    try:
        return 48.0 <= float(weight) <= 300.0
    except:
        return False


def validate_style_number(value: str) -> str:
    if not value.isnumeric():
        return False
    return 1 <= int(value) <= 4


def check_weight_class(weight):
    weight_class_dict = {
        (48.0, 50.8): "Flyweight",
        (50.9, 53.5): "Bantamweight",
        (53.6, 57.2): "Featherweight",
        (57.3, 61.2): "Lightweight",
        (61.3, 66.7): "Welterweight",
        (66.8, 76.2): "Middleweight",
        (76.3, 90.7): "Light heavyweight",
        (90.8, 300.0): "Heavyweight",
    }

    for (min_weight, max_weight), weight_cat in weight_class_dict.items():
        if min_weight <= float(weight) <= max_weight:
            return weight_cat


def validate_style(style: int) -> str:
    menu_style = {
        '1': 'Outfighter',
        '2': 'Infighter',
        '3': 'Boxer',
        '4': 'Brawler',
    }

    if style in menu_style:
        print (menu_style[style])
        return menu_style[style]


def validate_ranking(ranking: str) -> bool:
    if not ranking.isnumeric():
        return False
    return 1 <= int(ranking) <= 25000
