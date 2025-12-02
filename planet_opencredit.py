"""
Opening Sequence Module (planet_opencredit)
------------------------------------------
This module contains the function to display an animated graphical
opening sequence for the Solar System Explorer application using the 
Python 'turtle' library. It visually represents the Sun, planet orbits, 
and a simple movement animation before the main application begins.
"""

import turtle # Graphics library for drawing
import time # Module for time-based pauses in animation

def opening_sequence():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Solar System Explorer")

    # --- Title Text Setup ---
    title = turtle.Turtle()
    title.hideturtle()
    title.penup()
    title.goto(0, 250)  # Position near the top center
    title.write("SOLAR SYSTEM", align="center", font=("Arial", 24, "bold"))

   # --- Draw the Sun (Center Object) ---
    sun = turtle.Turtle()
    sun.hideturtle()
    sun.color("orange")
    sun.shape("circle")
    sun.shapesize(3) # Set Sun size
    sun.goto(0, 0) # Move to screen center
    sun.showturtle()

   # --- Planet Configuration Data ---
    planet_colors = ["blue", "red", "green", "purple"]
    planet_distances = [80, 120, 160, 200] # Define orbit radius

    # --- Draw Orbits (Concentric Circles) ---
    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.penup()
    orbit.color("gray")
    for distance in planet_distances:
        orbit.goto(0, -distance)  # Start drawing from the bottom edge of the circle
        orbit.pendown()
        orbit.circle(distance)     # Draw the circular orbit
        orbit.penup()

    # --- Draw Planets ---
    planets = []
    for i in range(len(planet_colors)):
        p = turtle.Turtle()
        p.hideturtle()
        p.color(planet_colors[i])
        p.shape("circle")
        p.shapesize(1.5)
        p.penup()
        p.goto(planet_distances[i], 0) # Position planet at the right edge of its orbit
        p.showturtle()
        planets.append(p)

   # --- Simple Orbit Animation --
    for _ in range(36):
        for i, p in enumerate(planets): # Loop 36 times (10 degrees of rotation each time)
            # Rotate each planet around the Sun. Inner planets move faster (10 + 0*2)
            p.right(10 + i*2)
        time.sleep(0.05) # Pause for smooth animation effect

    # Close turtle window and return to CLI
    screen.bye()
