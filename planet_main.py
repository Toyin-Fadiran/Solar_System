"""
Main Application Logic (Solar System Explorer)
---------------------------------------------
This script serves as the main entry point for the planet data application.
It imports necessary modules, initializes the program sequence, and manages 
the continuous user interaction loop based on the menu choices.
"""

# Import data source and utility modules
from planet_data import planets
import planet_ui
import planet_features
import planet_opencredit

# Initial application setup sequence
planet_ui.show_title_screen()
planet_opencredit.opening_sequence()
username = planet_ui.get_username()

# Main application loop for continuous interaction
while True:
    choice = planet_ui.show_menu()
    

    match choice:
        case "1":
#            print("\n\tEnter planet name:")
            print("Enter planet name:")
            name = input().strip()
            index = planet_features.find_planet(name, planets)
            if index == -1:
                print()
                print("\tSORRY!: Planet not found.")
                print()
            else:
                planet_features.display_planet_info(index, planets)

        case "2":
            planet_features.list_planets_with_moons(planets)

        case "3":
            planet_features.list_planets_with_life(planets)

        case "4":
            planet_features.list_all_planets(planets)

        case "0":
            planet_ui.exit_message(username)
            break

        case _:
            print()
            print("\t   Wrong Key Pressed — try again.")
            print()