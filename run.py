from simple_term_menu import TerminalMenu
from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

# SCOPE sourced from code institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def exits():
    """
    This function prints a message indicating program exit.
    """
    print("Exiting the program.")


def display_sheet_data():
    """
    This function displays the data from the Gsheet.
    """
    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    worksheet = spreadsheet.get_worksheet(0)

    all_rows = worksheet.get_all_values()

    header_row = all_rows[0]
    print(tabulate([header_row], headers="firstrow", tablefmt="fancy_grid"))

    for row in all_rows[1:]:
        print(tabulate([row], tablefmt="fancy_grid"))


def display_sheet_rows(row_indices):
    """
    Display rows in the worksheet based on their indices.
    """
    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    worksheet = spreadsheet.get_worksheet(0)
    values = worksheet.get_all_values()

    for row_index in row_indices:
        print(f"Row {row_index}: {values[row_index - 1]}")


def find_rows_by_input(worksheet, search_value):
    """
    Find all rows in a worksheet containing the specified value.
    """
    values = worksheet.get_all_values()
    matched_rows = [index + 1 for index, row in enumerate(values) if search_value in row]  # noqa
    return matched_rows


def edit_sheet_data(row_index, column_index, new_value):
    """
    This function edits the data in the Gsheet at the specified row and column.
    """
    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    worksheet = spreadsheet.get_worksheet(0)

    column_index = int(column_index)

    # Update the value at the specified cell

    worksheet.update_cell(row_index, column_index, new_value)

    print(f"Updating cell at ({row_index},")
    print("{column_index}) with value: {new_value}")


def show_program_menu():

    """
    This function displays a menu using the TerminalMenu
    class from the simple_term_menu library.
    """
    program_menu_title = ["Welcome to 'Where To Restaurant'", "New users Add New Restaurant First"]  # noqa
    program_menu_items = ["Add New Restaurant", "View Statistics", "Edit Restaurants", "Exit Program"]  # noqa
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
    """
    This function loads valid values from a specified Google Sheets column.
    """

    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE
    )
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open(sheet_name)
    worksheet = spreadsheet.get_worksheet(0)

    valid_values = worksheet.col_values(column_index)
    return valid_values


def view_statistics():
    print("Please input your 'Owner Name' from Add New Restaurants.")
    """
    This function allows the user to view information about the number of
    restaurants of a specific type in a given zip code.
    """
    owner_name = get_valid_owner_name_input()
    valid_owner_names = load_valid_values('survey_q', 1)

    if owner_name in valid_owner_names:
        print(f"'{owner_name}' Welcome Back.")
        zip_code = select_zip_code_list()
        print(f"Zip Code: {zip_code}")

        sheet_name = "stat"
        zip_code_column_index = 0

        credentials = Credentials.from_service_account_file(
            'creds.json', scopes=SCOPE)
        gc = gspread.authorize(credentials)

        spreadsheet = gc.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        filtered_rows = [
            row for row in all_rows if row[zip_code_column_index] == zip_code
        ]
        if not filtered_rows:
            print(f"Sorry no data found for the entered zip code: {zip_code}")
        else:
            # Calculate the row index (adding 1 because list indices start from
            # 0, but Gsheets row indices start from 1)
            row_index = all_rows.index(filtered_rows[0]) + 1

            # Get user input for the restaurant type
            column_name_input = display_restaurant_types_list()

            # Get the header row (assuming it's the first row in the sheet)
            header_row = worksheet.row_values(1)

            try:
                # Find the index of the column with the given name
                column_index_input = header_row.index(column_name_input) + 1

                # Iterate through rows to find the cell with the specified
                # row_index and column_index_input
                # https://realpython.com/python-enumerate/
                # Loop through all_rows with enumeration, starting from 1
                for row_number, row in enumerate(all_rows, start=1):
                    # Check if the value in the specified column
                    # (zip_code_column_index) matches the target zip_code
                    if row[zip_code_column_index] == zip_code:
                        # Check if the current row's index matches
                        # the given row_index
                        if row_index == row_number:
                            # Access the cell at the specified column index
                            # (column_index_input), adjusting to 0-based index
                            cell_at_intersection = row[column_index_input - 1]
                            # Adjust to 0-based index
                            # Print information about the number of restaurants
                            # in the specified zip code
                            print(f"Number of {column_name_input} restaurants")
                            print(f" '{cell_at_intersection}'")
                            print(f"in zip code {zip_code}")
                            break
            except ValueError:
                print(f"Column '{column_name_input}'")
                print("not found in the header row.")
    else:
        print(f"Owner's Name '{owner_name}'")
        print("does not exist.")
        print("Returning to the main menu, and add a new restaurant.")
        print("Viewing Statistics - Not implemented yet.")


def add_new_restaurant():
    """
    This function adds a new restaurant to the Gsheet.
    Collects input for owner name, restaurant type, and zip code.
    Prints the collected information.
    Appends the information to the Gsheet.
    """
    owner_name = get_valid_owner_name_input()
    rest_type = display_restaurant_types_list()
    zip_code = select_zip_code_list()

    print("Owner's Name:", owner_name)
    print("Restaurant Type:", rest_type)
    print("Zip Code:", zip_code)

    export_to_gsheets(owner_name, rest_type, zip_code)
    print("Restaurant added successfully!")

    return_to_menu = input("Press Enter to return to the main menu.\n")
    return show_program_menu()


def valid_owner_name_input(owner_input):
    """
    This function validates the owner name input.
    Ensures that the owner name contains only letters and a single space.
    """
    while owner_input is None or not (
            all((o.isalpha() or (o.isspace() and owner_input.count(o) == 1))
                for o in owner_input) and len(owner_input.strip()) > 0):
        owner_input = input("Invalid input. Please enter a valid owner name: ")

    return owner_input.strip()


def get_valid_owner_name_input():
    """
    This function retrieves valid owner name input from the user.
    """
    owner_input = input("Enter owner's name: \n").strip()
    while not owner_input or not valid_owner_name_input(owner_input):
        print("Invalid Owner's Name. Please try again.")
        owner_input = input("Enter owner's name: \n").strip()

    return valid_owner_name_input(owner_input).lower()


def export_to_gsheets(owner_name, rest_type, zip_code):
    """
    This function appends data to a Gsheet.
    Uses the gspread library to authenticate and
    append a new row to a Google Sheet.
    """
    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    spreadsheet = spreadsheet.get_worksheet(0)
    spreadsheet.append_row([owner_name.lower(), rest_type, zip_code])


def get_column_index_input():
    """
    Prompt the user for input to select a column index.
    """
    while True:
        index_input = input("1 is New Owner, 2 Restaurant Type, 3 Zip Code\n")

        if not any(char.isspace() for char in index_input):
            return index_input
        else:
            print("Spaces are not allowed. Please enter 1, 2, or 3.")


def get_new_input(index_input):
    """
    Takes a column index as input and returns
    corresponding user input based on the index.
    """
    valid_indices = ['1', '2', '3']

    while index_input not in valid_indices or index_input.startswith("0"):
        print("Invalid input. Please enter 1, 2, or 3")
        print("without spaces and not starting with 0.")
        index_input = input("1 is New Owner, 2 Restaurant Type, 3 Zip Code\n").strip()  # noqa
        index_input = index_input.replace(" ", "")

    if index_input == '1':
        new_owner_name = get_valid_owner_name_input()
        return new_owner_name
    elif index_input == '2':
        new_restaurant_type = display_restaurant_types_list()
        return new_restaurant_type
    elif index_input == '3':
        new_zip_code = select_zip_code_list()
        return new_zip_code


def select_zip_code_list():
    """
    Displays a list of zip codes and prompts the user to select one.
    """
    zip_codes = [
        "77001", "77002", "77003", "77004",
        "77005", "77006", "77007", "77008",
        "77009", "77010"
    ]

    print("Select a Zip Code:")
    for index, zip_code in enumerate(zip_codes, start=1):
        print(f"{index}. {zip_code}")

    while True:
        try:
            owner_input = input("Enter the Zip Code of your choice (1-10): ")

            if owner_input.startswith("0"):
                print("Invalid input. Cannot start with 0.")
                print("Please enter a valid number.")
                continue

            if " " in owner_input:
                print("Invalid input. Spaces are not allowed.")
                print("Please enter a valid number.")
                continue

            owner_choice = int(owner_input)

            if 1 <= owner_choice <= 10:
                return zip_codes[owner_choice - 1]
            else:
                print(" Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input.")
            print("Please enter a valid number between 1 and 10.")


def display_restaurant_types_list():
    """
    Displays a list of restaurant types and prompts the user to select one.
    """
    restaurant_types = [
        "Fast Food Chains",
        "Casual Dining",
        "Pizza Places",
        "Coffee Shops",
        "Steakhouses",
        "Seafood",
        "Mexican",
        "Italian",
        "Asian Cuisine",
        "Barbecue Joints",
        "Diners",
        "Food Trucks",
        "Buffet",
        "Brewpubs",
        "Vegetarian and Vegan"
    ]

    print("Select a Restaurant Type:")
    for index, restaurant_type in enumerate(restaurant_types, start=1):
        print(f"{index}. {restaurant_type}")

    while True:
        try:
            owner_choice = input("Enter 1-15 for desired restaurant type:/n ")

            if owner_choice.startswith("0"):
                print("Invalid input.")
                print("Cannot start with 0. Please enter a valid number.")
                continue

            if " " in owner_choice:
                print("Invalid input. Spaces are not allowed.")
                print("Please enter a valid number.")
                continue

            owner_choice = int(owner_choice)

            if 1 <= owner_choice <= 15:
                return restaurant_types[owner_choice - 1]
            else:
                print("Invalid choice.")
                print("Please enter a number between 1 and 15.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def edit_restaurants():
    """
    This function edits data in survey_q gsheet based on user input.
    """
    credentials = Credentials.from_service_account_file(
        'creds.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open('survey_q')
    worksheet = spreadsheet.get_worksheet(0)
    display_sheet_data()

    search_value = get_valid_owner_name_input()

    matched_rows = find_rows_by_input(worksheet, search_value)

    if not matched_rows:
        print(f"No rows found with the value '{search_value}'. Exiting.")
        return

    print(f"Found {len(matched_rows)} row(s) with the value '{search_value}'.")

    display_sheet_rows(matched_rows)

    column_index = get_column_index_input()
    new_value = get_new_input(column_index)

    for row_index in matched_rows:
        edit_sheet_data(row_index, column_index, new_value)

    display_sheet_data()
    print("Exiting to Menu.")


if __name__ == "__main__":
    """
    Executes the main logic of the script when run as the main program.
    Initializes variables.
    Enters an infinite loop displaying the program menu.
    Calls appropriate functions based on the user's menu selection.
    """
    quitting = False

    while not quitting:
        selected_option = show_program_menu()

        if selected_option == 0:
            add_new_restaurant()
        elif selected_option == 1:
            view_statistics()
        elif selected_option == 2:
            edit_restaurants()
        elif selected_option == 3:
            quitting = True

    print("Exiting the program.")
