from planet_data import planets
import planet_ui
import planet_features
import planet_opencredit

planet_ui.show_title_screen()
planet_opencredit.opening_sequence()
username = planet_ui.get_username()

while True:
    choice = planet_ui.show_menu()

    match choice:
        case "1":
            print("\n\tEnter planet name:")
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