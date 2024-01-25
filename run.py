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

def load_valid_values(sheet_name, column_index):
    # Load existing data from Gsheets
    credentials = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open(sheet_name)
    worksheet = spreadsheet.get_worksheet(0)

    # Get all values in the specified column
    valid_values = worksheet.col_values(column_index)
    return valid_values

def view_statistics():
    # Calls for owner's name input
    owner_name = get_valid_owner_name_input()

    # Load existing data for owner names
    valid_owner_names = load_valid_values('survey_q', 1)

    # Check if the entered owner's name already exists
    if owner_name in valid_owner_names:
        print(f"Owner's Name '{owner_name}' Welcome Back.")
        # Call function to get food type input
        food_type = get_food_type_input()
        print(f"Food Type: {food_type}")
        # Call function to get zip code input
        zip_code = get_zip_code_input()
        print(f"Zip Code: {zip_code}")
    
    else:
        print(f"Owner's Name '{owner_name}' does not exist. Returning to the main menu.")
        print("Viewing Statistics - Not implemented yet.")

def get_food_type_input():
    # Function to get valid food type input from the user
    while True:
        rest_type_input = input("Enter Food Type: ").strip()
        
        # Validation code for food type input
        if any(d.isdigit() or not d.isalnum() for d in rest_type_input.lower()) or len(rest_type_input.strip()) == 0:
            print("Invalid input. Please enter a valid Food Type.")
        else:
            return rest_type_input

def get_zip_code_input():
    # Function to get valid zip code input from the user
    while True:
        zip_code = input("Enter Zip Code: ").strip()

        # Validation code for zip code input
        if len(zip_code.strip()) == 0 or not zip_code.isdigit():
            print("Invalid input. Please enter a valid Zip Code.")
        else:
            return zip_code
def add_new_restaurant():
    owner_name = get_valid_owner_name_input()
    rest_type = get_valid_rest_type_input()
    zip_code = get_valid_zip_code_input()

    print("Owner's Name:", owner_name)
    print("Restaurant Type:", rest_type)
    print("Zip Code:", zip_code)

    export_to_gsheets(owner_name, rest_type, zip_code)
    print("Restaurant added successfully!")



def valid_owner_name_input(owner_input):
    # https://www.w3schools.com/python/ref_string_isalpha.asp
    # https://www.w3schools.com/python/ref_string_isspace.asp
    # https://www.w3schools.com/python/ref_list_count.asp
    # Allow letters and a single space, but not numbers or special characters
    if not all((o.isalpha() or (o.isspace() and owner_input.count(o) == 1)) for o in owner_input):
        return False
    
    if len(owner_input.strip()) == 0:
        return False
    
    return True

def get_valid_owner_name_input():
    owner_input = input("Enter owner's name: ")
    owner_input = owner_input.strip() 

    if valid_owner_name_input(owner_input):
        return owner_input
    else:
        print("Invalid Owner's Name. Please try again.")

def validate_rest_type_input(rest_type_input):
    # https://www.w3schools.com/python/ref_string_isdigit.asp
    # https://www.w3schools.com/python/ref_string_isalnum.asp
    #
    # When inputting your restaurant, no excess space, numbers, special characters (e.g., ()/&!)
    if any(d.isdigit() or not d.isalnum() for d in rest_type_input):
        return False
    # .strip()) == 0: credited to Mentor 
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
            print("Invalid input. Please enter a valid Zip Code.")
# https://spreadsheetpoint.com/python-google-sheets/
def export_to_gsheets(owner_name, rest_type, zip_code):
    # # https://spreadsheetpoint.com/python-google-sheets/
    credentials = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
    # https://snyk.io/advisor/python/gspread/functions/gspread.authorize
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    spreadsheet = spreadsheet.get_worksheet(0)
    # Append the values to Google Sheets
    # https://stackoverflow.com/questions/60793155/gspread-append-row-appending-data-to-different-column
    spreadsheet.append_row([owner_name, rest_type, zip_code])

# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    selected_option = None

    while selected_option != 1:  
        
        selected_option = show_program_menu()

        if selected_option == 1:
                    add_new_restaurant()
        elif selected_option == 0:
                    view_statistics()

print("Exiting the program.")

