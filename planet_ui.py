"""
User Interface (UI) Module
--------------------------
This module contains all functions responsible for handling user interaction, 
including displaying screens, menus, and validating user input for the 
Solar System Explorer application.
"""

def show_title_screen():
    """
    Displays the application's title screen banner.
    """
    print("=====================================")
    print("        SOLAR SYSTEM EXPLORER        ")
    print("=====================================")


def get_username():
    """
    Prompts the user to enter their name and validates the input.
    Ensures the name is not empty and contains only alphabetical characters.
    Returns the validated username (str).
    """
    while True:
        username = input("Enter your name: ").strip()

        if username == "":
            print("\tInvalid input. Name cannot be empty.")
        elif not username.isalpha():
            print("\tInvalid input. Name must contain only letters.")
        else:
            return username  


def show_menu():
    """
    Displays the main application menu and prompts the user for a choice.
    Validates input against predefined choices ("0" to "4").
    Returns the validated user choice (str).
    """
    valid_choices = ["0", "1", "2", "3", "4"]

    while True:
        print("\nMAIN MENU")
        print("1. Search for a planet")
        print("2. List planets with moons")
        print("3. List planets that may support life")
        print("4. Show all planets")
        print("0. Exit program")
        print("\nEnter your choice:")

        choice = input().strip()

        if choice in valid_choices:
            return choice
        else:
            print("\tWrong Key Pressed — try again.")


def exit_message(username):
    """
    Displays the final exit message when the program terminates.
    Args:
        username (str): The name of the user to personalize the goodbye message.
    """
    print("\n\tGoodbye", username + "!")
    print("\tThanks for exploring the Solar System.")
