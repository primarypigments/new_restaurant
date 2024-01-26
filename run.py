from simple_term_menu import TerminalMenu
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# SCOPE sourced from code institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# https://pypi.org/project/simple-term-menu/ used for following code
def show_program_menu():
    program_menu_title = "Select an option:"
    program_menu_items = ["View Statistics", "Add New Restaurant"]
    program_menu_cursor = " -> "
    program_menu_cursor_style = ("fg_purple", "bold")
    program_menu_style = ("bg_yellow", "fg_gray")

    program_menu = TerminalMenu(
        program_menu_items,
        title=program_menu_title,
        menu_cursor=program_menu_cursor,
        menu_cursor_style=program_menu_cursor_style,
        menu_highlight_style=program_menu_style
    )

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
# allowing the user to view information about the number of 
# restaurants of a specific type in a given zip code
def view_statistics():
    owner_name = get_valid_owner_name_input()
    valid_owner_names = load_valid_values('survey_q', 1)

    if owner_name in valid_owner_names:
        print(f"Owner's Name '{owner_name}' Welcome Back.")
        # food_type = get_food_type_input()
        # print(f"Food Type: {food_type}")
        zip_code = get_zip_code_input()
        print(f"Zip Code: {zip_code}")

        # Load data from Gsheets
        sheet_name = "stat"
        zip_code_column_index = 0

        # Load existing data from Gsheets
        credentials = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
        gc = gspread.authorize(credentials)

        spreadsheet = gc.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(0)

        # Get all rows from the Gsheet
        all_rows = worksheet.get_all_values()

        # Find the row index that matches the entered zip code
        filtered_rows = [row for row in all_rows if row[zip_code_column_index] == zip_code]
        if not filtered_rows:
            print(f"No data found for the entered zip code: {zip_code}")
        else:
            # Calculate the row index (adding 1 because list indices srt from 0, but Gsheets row indices start from 1)
            row_index = all_rows.index(filtered_rows[0]) + 1

            # Get user input for the restaurant type
            column_name_input = input("Enter Restaurant Type: ")

            # Get the header row (assuming it's the first row in the sheet)
            header_row = worksheet.row_values(1)

            try:
                # Find the index of the column with the given name
                column_index_input = header_row.index(column_name_input) + 1

                # Iterate through rows to find the cell with the specified row_index and column_index_input
                # https://realpython.com/python-enumerate/
                # Loop through all_rows with enumeration, starting from 1
                for row_number, row in enumerate(all_rows, start=1):
                    # Check if the value in the specified column (zip_code_column_index) matches the target zip_code
                    if row[zip_code_column_index] == zip_code:
                        # Check if the current row's index matches the given row_index
                        if row_index == row_number:
                             # Access the cell at the specified column index (column_index_input), adjusting to 0-based index
                            cell_at_intersection = row[column_index_input - 1]  # Adjust to 0-based index
                             # Print information about the number of restaurants in the specified zip code
                            print(f"Number of {column_name_input} restaurants '{cell_at_intersection}' in zip code {zip_code}")
                            break

            except ValueError:
                print(f"Column '{column_name_input}' not found in the header row.")

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

    # Prompt to return to the main menu
    return_to_menu = input("Press Enter to return to the main menu.")
    if return_to_menu:
        return show_program_menu()
    else:
        print("Invalid input. Returning to the main menu.")
        return show_program_menu()

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

