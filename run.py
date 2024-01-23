from simple_term_menu import TerminalMenu
import gspread
from google.oauth2.service_account import Credentials

# SCOPE scourced from code institue 
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
# https://pypi.org/project/simple-term-menu/ used for folowwing code
def show_program_menu():
    program_menu_title = "Select an option:"
    program_menu_items = ["View Statistics", "Add New Restaurant"]
    program_menu_cursor = " -> "
    program_menu_cursor_style = ("fg_purple", "bold")
    program_menu_style = ("bg_yellow", "fg_gray")

    program_menu = TerminalMenu(program_menu_items, title=program_menu_title, menu_cursor=program_menu_cursor, menu_cursor_style=program_menu_cursor_style, menu_highlight_style= program_menu_style)

    selected_index = program_menu.show()
    return selected_index

def validate_owner_name_input(owner_input):
    # Allow letters and a single space, but not numbers or special characters
    if not all((o.isalpha() or (o.isspace() and owner_input.count(o) == 1)) for o in owner_input):
        return False
    
    if len(owner_input.strip()) == 0:
        return False
    
    return True

    def get_valid_owner_name_input():
    while True:
        owner_input = input("Enter owner's name: ")
        owner_input = owner_input.strip() 

        if validate_owner_name_input(owner_input):
            return owner_input
        else:
            print("Invalid Owner's Name. Please try again.")

def validate_rest_type_input(rest_type_input):
    # When inputting your restaurant, no excess space, numbers, special characters (e.g., ()/&!)
    if any(d.isdigit() or not d.isalnum() for d in rest_type_input):
        return False
    
    if len(rest_type_input.strip()) == 0: 
        return False
    
    return True

def get_valid_rest_type_input():
    while True:
        rest_type_input = input("Enter Restaurant Type: ")
        rest_type_input = rest_type_input.strip()  

        if validate_rest_type_input(rest_type_input):
            return rest_type_input
        else:
            print("Invalid Restaurant Type. Please try again.")

def validate_zip_code(zip_code):
    # Check if the zip code is not empty
    if len(zip_code.strip()) == 0:
        return False

    # Check if the zip code consists only digits
    if not zip_code.isdigit():
        return False

    return True

def get_valid_zip_code_input():
    while True:
        zip_code_input = input("Enter Zip Code: ")
        zip_code_input = zip_code_input.strip()

        if validate_zip_code(zip_code_input):
            return zip_code_input
        else:
            print("Invalid input. Please enter a valid zip code.")
