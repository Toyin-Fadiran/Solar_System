def show_title_screen():
    print("=====================================")
    print("        SOLAR SYSTEM EXPLORER        ")
    print("=====================================")


def get_username():
    while True:
        username = input("Enter your name: ").strip()

        if username == "":
            print("\tInvalid input. Name cannot be empty.")
        elif not username.isalpha():
            print("\tInvalid input. Name must contain only letters.")
        else:
            return username  


def show_menu():
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
    print("\n\tGoodbye", username + "!")
    print("\tThanks for exploring the Solar System.")
