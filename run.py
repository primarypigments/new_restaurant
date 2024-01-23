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