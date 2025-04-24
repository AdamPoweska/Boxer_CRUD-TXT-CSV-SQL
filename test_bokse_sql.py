import unittest

import io
from contextlib import redirect_stdout

from bokser_sql import *
from bokser_functions import *

# bokser_functions tests
class TestBokserFunctions(unittest.TestCase):

    def test_validate_name_correct(self):
        name = 'John'
        check = validate_name(name)
        self.assertTrue(check)

    def test_validate_name_not_correct_empty(self):
        name = ''
        check = validate_name(name)
        self.assertFalse(check)

    def test_validate_name_not_correct_to_long(self):
        name = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        check = validate_name(name)
        self.assertFalse(check)

    def test_validate_name_not_correct_int(self):
        name = 1326
        check = validate_name(str(name))
        self.assertFalse(check)

    def test_validate_name_not_correct_int_as_str(self):
        name = '1326'
        check = validate_name(name)
        self.assertFalse(check)

    def test_validate_age_ok(self):
        age = '25'
        check = validate_age(age)
        self.assertTrue(check)

    def test_validate_age_too_low(self):
        age = '5'
        check = validate_age(age)
        self.assertFalse(check)

    def test_validate_age_to_high(self):
        age = '100'
        check = validate_age(age)
        self.assertFalse(check)

    def test_validate_age_str(self):
        age = 'abc'
        check = validate_age(age)
        self.assertFalse(check)

    def test_validate_age_not_full_num(self):
        age = '25.5'
        check = validate_age(age)
        self.assertFalse(check)

    def test_validate_fights_ok(self):
        fights = '25'
        check = validate_fights(fights)
        self.assertTrue(check)

    def test_validate_fights_letters(self):
        fights = 'abc'
        check = validate_fights(fights)
        self.assertFalse(check)

    def test_validate_fights_to_high(self):
        fights = '1001'
        check = validate_fights(fights)
        self.assertFalse(check)

    def test_validate_fights_not_full_num(self):
        fights = '10.5'
        check = validate_fights(fights)
        self.assertFalse(check)


class TestBoxer(unittest.TestCase):

    def test_print_by_line_correct(self):
        boxer = Boxer()
        
        temporary_file = io.StringIO() # tworzy tymczasowy obiekt rozpoznawany przez pytona jako plik ale istniejący w pamięci
        with redirect_stdout(temporary_file): #redirect_stdout przechwyca wszystko co byłoby pokazane jako print (sys.stdout) i przekazuje do tymczasowego bufora 
            boxer.print_by_line(boxer.read_file_list())
        
        output = temporary_file.getvalue() # getvalue zwraca cały zapisany tekst jako jeden string, jest to metoda obiektów .io

        self.assertIn("Many Paquiao", output)

    def test_print_by_line_not_correct(self):
        boxer = Boxer()
        
        temporary_file = io.StringIO() 
        with redirect_stdout(temporary_file): 
            boxer.print_by_line(boxer.read_file_list())
        
        output = temporary_file.getvalue()

        self.assertNotIn("XXX", output)


if __name__ == '__main__':
    unittest.main()
