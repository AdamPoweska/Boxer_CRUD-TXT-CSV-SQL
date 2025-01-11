# CRUD - lista bokserów -> zapisywanie do sql
# napisz jedną funkcję, która zmienia dane do nowego boksera i do updatu starego - DRY

import sqlite3
import sys
import os

from bokser_functions import get_input, validate_name, get_data_from_user

FULL_FILE_PATH = 'bokser_data_sql.db'
CONNECTION_TO_DB = sqlite3.connect(FULL_FILE_PATH) # łączy do bazy danych i tworzy ją jeśli plik jeszcze nie istnieje
COURSOR_SQL = CONNECTION_TO_DB.cursor() # musimy ustawić zmienną która pozwoli nam na zmiany w badzie danych do której jesteśmy połączeni

class Boxer:
    def __init__(self, name="", age=0, height = 0, weight="", weight_class="", style="", ranking=0, wins=0, losses=0, draws=0, no_contest=0):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.weight_class = weight_class
        self.style = style
        self.ranking = ranking
        self.wins = wins
        self.losses = losses
        self.draws = draws
        self.no_contest = no_contest

        self.ATTRS_ORDER = [key for key in self.__dict__] # pobiera klucze dla self i zwraca je w formie listy - do napisania nagłówków w pliku
        
        self.ATTRS_TYPES = { # słownik służy do dynamicznego wpisywania nagłówków przy pierwszym uruchomieniu programu, w przypadku zmian w klasie należy też dokonać zmian w słowniku
            "name": "text",
            "age": "integer",
            "height": "real",
            "weight": "real",
            "weight_class": "text",
            "style": "text",
            "ranking": "integer",
            "wins": "integer",
            "losses": "integer",
            "draws": "integer",
            "no_contest": "integer"
        }

    def __str__(self):
        values = [getattr(Boxer, attr) for attr in self.ATTRS_ORDER] # getattr "wyciąga" wartości dla self a następnie szereguje je w kolejności takiej jak w self.ATTRS_ORDER - czyli tak jak wpisaliśmy oryginalnie w klasę
        return f"{values}"
    
    def __repr__(self):
        return f"Boxer(name={self.name!r}, age={self.age!r}, height={self.height!r} weight={self.weight!r}, weight_class={self.weight_class!r}, style={self.style!r}, ranking={self.ranking!r}, wins={self.wins!r}, losses={self.losses!r}, draws={self.draws}, no_contest={self.no_contest!r})"
    
    def read_file_list(self):
        COURSOR_SQL.execute("SELECT * FROM boxer_database")
        all_results = COURSOR_SQL.fetchall()
        return all_results
    
    def print_by_line(self, full_list):
        COURSOR_SQL.execute("PRAGMA table_info(boxer_database)")
        columns = COURSOR_SQL.fetchall()
        columns_headers = [desc[1] for desc in columns]
        print(columns_headers)
        for short_list in full_list:
            print(short_list)

    def add_boxer(self):
        """Adds Boxer class instance."""
        name_list = COURSOR_SQL.execute("SELECT name FROM boxer_database")
        actual_list_type = [row[0] for row in name_list.fetchall()]
        
        name = get_input("\nName: ", validate_name, "There can not be only numbers in names! Max. 40 signs!")
        
        for item in actual_list_type:
            if item.lower() == name.lower():
                print("There is already boxer with such name. Please check or add a number to a name.")
                return
        
        new_boxer_list = get_data_from_user()
        new_boxer_list.insert(0, name)
        question_marks_for_sql = ", ".join(["?" for _ in range(len(new_boxer_list))])
        upload_for_db = f"INSERT INTO boxer_database VALUES({question_marks_for_sql})"
        COURSOR_SQL.execute(upload_for_db, new_boxer_list)
        CONNECTION_TO_DB.commit()

    def remove_boxer(self, delete_person):
        """Removes boxer from database."""        
        name_list = COURSOR_SQL.execute("SELECT name FROM boxer_database")
        actual_list_type = [row[0] for row in name_list.fetchall()]

        name_check = False
        for item in actual_list_type:
            if item == delete_person:
                name_check = True
                break

        upload_for_db = f"DELETE FROM boxer_database WHERE name = ?"
        if name_check:
            COURSOR_SQL.execute(upload_for_db, (delete_person,))
            CONNECTION_TO_DB.commit()
            print(f"Boxer deleted: '{delete_person}'.")
        else:
            print(f"No such name on the list: '{delete_person}'. Please mind it is CASE SENSITIVE!")
            return
    

    def update_boxer(self, name_to_update):
        """Updates data for a boxer"""
        name_list = COURSOR_SQL.execute("SELECT name FROM boxer_database")
        actual_list_type = [row[0] for row in name_list.fetchall()]

        name_check = False
        for item in actual_list_type:
            if item == name_to_update:
                name_check = True
                break
        
        if not name_check:
            print(f"No such name on the list: '{name_to_update}'. Please note - CASE SENSITIVE!")
            return
        print(f"Updating data for: '{name_to_update}'.")

        upload_for_db = """
            Update boxer_database 
            SET 
            age = ?, 
            height = ?,
            weight = ?,
            weight_class = ?, 
            style = ?,
            ranking = ?,
            wins = ?, 
            losses = ?,
            draws = ?, 
            no_contest = ? 
            WHERE name = ?
        """

        up_boxer_list = get_data_from_user()
        up_boxer_list.insert(len(up_boxer_list), name_to_update)
        COURSOR_SQL.execute(upload_for_db, up_boxer_list)
        CONNECTION_TO_DB.commit()
        print(f"Data updated for: '{name_to_update}.")


    def boxer_list_headings(self: list) -> None:
        """Prints headings of Boxer class into database (only at first run of program)."""    
        if os.path.getsize(FULL_FILE_PATH) < 3: # plik z zapisanymi nagłówkami wazy 8b, czek na pliki poniżej 3b
            boxer_instance = Boxer()
            headers = ", ".join([f"{col} {data_type}" for col, data_type in boxer_instance.ATTRS_TYPES.items()]) # .join zmiania list comprehension na string, łącząc przy użyciu ", "
            create_headers = f"CREATE TABLE boxer_database({headers})"
            COURSOR_SQL.execute(create_headers)
            # Hardcoded = # COURSOR_SQL.execute("""CREATE TABLE boxer_database (name text, age integer, height real, weight real, weight_class text, style text, ranking integer, wins integer, losses integer, draws integer, no_contest integer)""")
        CONNECTION_TO_DB.commit()


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
        '3': lambda: boxer_manager.print_by_line(boxer_manager.read_file_list()),
        '4': lambda: boxer_manager.update_boxer(input("Which boxer do you wish to update? Type name: ")),
        '5': lambda: print("\nGoodbye!") or CONNECTION_TO_DB.close() or sys.exit(0), # "or" w pythonie zwraca wartość pierwszego wyrażenia, które ocenia się jako True. Pierwszy jest print(), który zwraca None - a None jest traktowany jako False. Dlatego wykonywane jest drugie wyrażenie: sys.exit. Gdybyśmy użyli "and" python oczekiwałby, że oba wyrażenia muszą być True żeby wykonać sys.exit(0).
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