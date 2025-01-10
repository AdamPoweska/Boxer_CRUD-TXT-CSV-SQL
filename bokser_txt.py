# CRUD - list of boxers -> saving to txt

import sys

FILE_PATH = r'C:\Users\Projects\Bokser\\'
FILE_NAME = 'bokser_data_txt.txt'
FULL_FILE_PATH = FILE_PATH + FILE_NAME

class Boxer:
    def __init__(self, name="", age=0, height = 0, weight="", weight_class="", style="", ranking=0):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.weight_class = weight_class
        self.style = style
        self.ranking = ranking

        self.ATTRS_ORDER = [key for key in self.__dict__] # pobiera klucze dla self i zwraca je w formie listy - do napisania nagłówków w pliku
    
    def __str__(self):
        values = ",".join(str(getattr(self, attr)) for attr in self.ATTRS_ORDER) # getattr "wyciąga" wartości dla self a następnie szereguje je w kolejności takiej jak w self.ATTRS_ORDER - czyli tak jak wpisaliśmy oryginalnie w klasę
        return f"{values}"
    
    def __repr__(self):
        return f"Boxer(name={self.name!r}, age={self.age!r}, height={self.height!r} weight={self.weight!r}, weight_class={self.weight_class!r}, style={self.style!r}, ranking={self.ranking!r})"

    def read_file_str(self):
        with open(FULL_FILE_PATH, 'r', encoding='utf-8') as file_read:
            content = file_read.read()
            return content
    
    def read_file_list(self):
        with open(FULL_FILE_PATH, 'r', encoding='utf-8') as file_read:
            content = file_read.readlines()
            return content
        
    def append_to_file(self, new_boxer_str):
        with open(FULL_FILE_PATH, 'a', encoding='utf-8') as file_append:
            file_append.write(new_boxer_str)
            
    def add_boxer(self):
        """Adds Boxer class instance."""
        file_lines = self.read_file_list()

        name = get_input("\nName: ", validate_name, "There can not be only numbers in names! Max. 40 signs!")
        
        for line in file_lines:
            name_check = line.split(',')[0]
            if name_check.lower() == name.lower():
                print("There is already boxer with such name. Please check or add a number to a name.")
                return # w funkcji, gdzie występuje return bez żadnej wartości (jak w tym przykładzie), jest to jednoznaczne z return None. Zakończenie funkcji w ten sposób przerywa jej działanie natychmiast.

        age = get_input("\nAge: ", validate_age, "Are you sure it is correct age?")
        height = get_input("\nHeight(cm): ", validate_height, "Are you sure it is correct height(cm)?")
        weight = get_input("\nWeight(kg): ", validate_weight, "Are you sure it is correct weight(kg)?")
        weight_class = check_weight_class(weight)
        style_num = get_input("\nStyle:\n1 - Outfighter.\n2 - Infighter.\n3 - Boxer.\n4 - Brawler.\n", validate_style_number, "Please choose from the list.")
        style = validate_style(style_num)
        ranking = get_input("\nRanking: ", validate_ranking, "Please choose between 1 and 25 000.")
        
        new_boxer = Boxer(name, age, height, weight, weight_class, style, ranking)

        new_boxer_str = str(new_boxer) + '\n'
        
        self.append_to_file(new_boxer_str)

    def remove_boxer(self, delete_person):
        """Removes boxer from database."""
        file_lines = self.read_file_list() # Reads database file as a list of strings.
        boxer_name_pos = self.file_name_check(delete_person) # Returns position (int) of given name.

        if boxer_name_pos == None:
            print(f"No such name on the list: '{delete_person}'.")
            return
        
        file_lines.pop(boxer_name_pos)

        with open(FULL_FILE_PATH, 'w', encoding='utf=8') as file:
            file.writelines(file_lines)
        
        print(f"Boxer deleted: '{delete_person}'.")
        

    def update_boxer(self, name_to_update):
        """Updates data for a boxer"""
        file_lines = self.read_file_list()
        boxer_name_pos = self.file_name_check(name_to_update)
        
        if boxer_name_pos == None:
            print(f"No such name on the list: '{name_to_update}'.")
            return
        
        print(f"Updating data for: '{name_to_update}'.")

        age = get_input("\nAge: ", validate_age, "Are you sure it is correct age?")
        height = get_input("\nHeight(cm): ", validate_height, "Are you sure it is correct height(cm)?")
        weight = get_input("\nWeight(kg): ", validate_weight, "Are you sure it is correct weight?")
        weight_class = check_weight_class(weight)
        style_num = get_input("\nStyle:\n1 - Outfighter.\n2 - Infighter.\n3 - Boxer.\n4 - Brawler.\n", validate_style_number, "Please choose from the list.")
        style = validate_style(style_num)
        ranking = get_input("\nRanking: ", validate_ranking, "Please choose between 1 and 25 000.")
        
        update_boxer = Boxer(name_to_update, age, height, weight, weight_class, style, ranking)

        update_boxer_str = str(update_boxer) + '\n'

        file_lines[boxer_name_pos] = update_boxer_str

        with open(FULL_FILE_PATH, 'w', encoding='utf=8') as file:
            file.writelines(file_lines)
        
        print(f"Data updated for: '{name_to_update}.")


    def file_name_check(self, name_to_update):
        """Returns position of given name."""
        data_lines = self.read_file_list()
        boxer_position = None
        for num, line in enumerate(data_lines):
            line_split = line.split(',')
            if line_split[0].lower() == name_to_update.lower():
                boxer_position = num
                return boxer_position

        
    def boxer_list_headings(self: list) -> None:
        """Prints headings of Boxer class into file (only at first run of program)."""
        file_lines = self.read_file_list()

        if file_lines == []:
            names = ",".join(attr for attr in self.ATTRS_ORDER) # łączy (join) listę każdy jej element przedzielając "|" i centrując na "max_width"
            names_str = str(names) + '\n'
            self.append_to_file(names_str)
        else:
            return


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
    age_int = int(age)
    return 15 <= age_int <= 60


def validate_height(height: str) -> bool:
    try:
        return 120 <= float(height) <= 300.0
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
    value_int = int(value)
    return 1 <= value_int <= 4


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
    ranking_int = int(ranking)
    return 1 <= ranking_int <= 25000


def show_menu():
    """Program menu - allows user only to provide '1', '2', '3', '4' or '5' answers and returns the user choice."""
    while True:
        print("\nMenu:\n1 - Add boxer.\n2 - Remove boxer.\n3 - Show all boxers.\n4 - Update boxer.\n5 - End.")
        user_reply = input("Type: 1, 2, 3, 4 or 5: ")
        
        if user_reply.isnumeric() and 1 <= int(user_reply) <= 5:
            return user_reply
        else:
            print('Only 1, 2, 3, 4 or 5!')
            continue


def main():
    boxer_manager = Boxer() # MUSZĘ STWORZYĆ ZMIENNĄ KTÓRA JEST INSTANCJĄ KLASY BY MÓC NA NIEJ OPEROWAĆ - NIE MOGĘ ODWOŁAĆ SIĘ BEZPOŚREDNIO DO KLASY. KLASA MUSI MIEĆ WARTOŚCI DOMYŚLNE ABY NIE POJAWIŁ SIĘ NA TYM ETAPIE BŁĄD WYWOŁANIA KLASY. PRZYPISANIE WARTOŚCI DOMYŚLNYCH JAKO "NONE" MOŻE POWODOWAĆ PROBLEMY I NIE JEST REKOMENDOWANE.

    boxer_manager.boxer_list_headings()
    
    menu_actions = {
        '1': boxer_manager.add_boxer, # nie ma tu nawiasów gdyż gdyby były to od razu na tym etapie wywoływalibyśmy funkcję "add_crew_member" - my natomiast chcemy jedynie PRZECHOWAĆ ODWOŁANIE DO FUNKCJI A NIE JĄ WYWOŁAĆ
        '2': lambda: boxer_manager.remove_boxer(input("Which boxer do you wish to remove from the database? Type name: ")), # w przypadku gdy mamy lambdę - zwraca ona wartość (wbudowana funkcja return) i nic nie wywołuje
        '3': lambda: print(boxer_manager.read_file_str()),
        '4': lambda: boxer_manager.update_boxer(input("Which boxer do you wish to update? Type name: ")),
        '5': lambda: print("\nGoodbye!") or sys.exit(0), # "or" w pythonie zwraca wartość pierwszego wyrażenia, które ocenia się jako True. Pierwszy jest print(), który zwraca None - a None jest traktowany jako False. Dlatego wykonywane jest drugie wyrażenie: sys.exit. Gdybyśmy użyli "and" python oczekiwałby, że oba wyrażenia muszą być True żeby wykonać sys.exit(0).
    }

    while True:
        question = show_menu() # zwraca 1-5
        action = menu_actions.get(question) # ".get" pobiera wartość dla danego klucza (z danego słownika)

        if action:
            action() # tutaj używamy już nawiasów, więc funkcja jest wywoływana dopiero na tym etapie
        else:
            print('1, 2, 3, 4 or 5 answers!')

if __name__ == "__main__":
    main()