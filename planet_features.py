
"""
Planet Data Functions
---------------------
This module contains functions designed to process and display information
from a 2D list of planet data (assumed to be structured: 
[Name, Moon_Count, Atmosphere, Has_Life (1/0), Distance_from_Sun_million_km]).
It includes utilities for searching, detailed display, and filtering.
"""



def find_planet(name, planets):
    """
    Searches the list of planets for a record matching the given name (case-insensitive).
    Returns the index (int) of the planet if found, or -1 otherwise.
    """
    for i in range(len(planets)):
        if planets[i][0].lower() == name.lower():
            return i
    return -1  # planet Not found

def display_planet_info(index, planets):
    """
    Prints a detailed, formatted summary of a planet's attributes.
    The planet is retrieved using the provided index.
    """
    p = planets[index]
    print("\n\tPlanet:", p[0])
    print("\tMoons:", p[1])
    print("\tAtmosphere:", p[2])
    print("\tDistance from Sun:", p[4], "million km")  
    if p[3] == 1:
        print("\tSupports life: YES")
    else:
        print("\tSupports life: NO")

def list_planets_with_moons(planets):
    """
    Prints a list of all planets that have at least one moon.
    """
    print("\n\tPlanets with moons:")
    for p in planets:
        if p[1] > 0:
            print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")

def list_planets_with_life(planets):
    """
    Prints a list of all planets flagged as supporting life (where flag is 1).
    """
    print("\n\tPlanets that may support life:")
    for p in planets:
        if p[3] == 1:
            print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")

def list_all_planets(planets):
    """
    Prints a simple, comprehensive list of all planet names and their distances from the Sun.
    """
    print("\n\tAll planets:")
    for p in planets:
        print(f"\t- {p[0]} (Distance from Sun: {p[4]} million km)")