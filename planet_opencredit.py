import turtle
import time

def opening_sequence():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Solar System Explorer")

    # Write title at the top
    title = turtle.Turtle()
    title.hideturtle()
    title.penup()
    title.goto(0, 250)  # move near top of window
    title.write("SOLAR SYSTEM", align="center", font=("Arial", 24, "bold"))

    # Draw the Sun
    sun = turtle.Turtle()
    sun.hideturtle()
    sun.color("orange")
    sun.shape("circle")
    sun.shapesize(3)
    sun.penup()
    sun.goto(0, 0)
    sun.showturtle()

    # Planet properties
    planet_colors = ["blue", "red", "green", "purple"]
    planet_distances = [80, 120, 160, 200]

    # Draw orbits as concentric circles
    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.penup()
    orbit.color("gray")
    for distance in planet_distances:
        orbit.goto(0, -distance)  # move to bottom of circle
        orbit.pendown()
        orbit.circle(distance)     # draw orbit
        orbit.penup()

    # Draw planets
    planets = []
    for i in range(len(planet_colors)):
        p = turtle.Turtle()
        p.hideturtle()
        p.color(planet_colors[i])
        p.shape("circle")
        p.shapesize(1.5)
        p.penup()
        p.goto(planet_distances[i], 0)
        p.showturtle()
        planets.append(p)

    # Optional: simple orbit animation
    for _ in range(36):
        for i, p in enumerate(planets):
            p.right(10 + i*2)
        time.sleep(0.05)

    # Close turtle window and return to CLI
    screen.bye()
