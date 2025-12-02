def find_planet(name, planets):
    for i in range(len(planets)):
        if planets[i][0].lower() == name.lower():
            return i
    return -1  # Not found

def display_planet_info(index, planets):
    p = planets[index]
    print("\n\tPlanet:", p[0])
    print("\tMoons:", p[1])
    print("\tAtmosphere:", p[2])
    print("\tDistance from Sun:", p[4], "million km")  # new line for distance
    if p[3] == 1:
        print("\tSupports life: YES")
    else:
        print("\tSupports life: NO")

def list_planets_with_moons(planets):
    print("\n\tPlanets with moons:")
    for p in planets:
        if p[1] > 0:
            print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")

def list_planets_with_life(planets):
    print("\n\tPlanets that may support life:")
    for p in planets:
        if p[3] == 1:
            print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")

def list_all_planets(planets):
    print("\n\tAll planets:")
    for p in planets:
        print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")