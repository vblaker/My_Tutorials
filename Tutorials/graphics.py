import turtle

def draw_square(turn_angle):
    window_square = turtle.Screen()
    window_square.bgcolor("red")

    brad = turtle.Turtle()

    brad.right(turn_angle)
    for i in range(0,4):
        brad.forward(100)
        brad.color('yellow')
        brad.right(90)
    #window_square.exitonclick()

def draw_circle():
    window_circle = turtle.Screen()
    window_circle.bgcolor("red")

    angie = turtle.Turtle()
    angie.shape('arrow')
    angie.color('blue')
    angie.circle(100)
    #window_circle.exitonclick()

def draw_triangle():
    window_triangle = turtle.Screen()
    window_triangle.bgcolor("red")

    turdie = turtle.Turtle()
    for i in range(0, 3):
        turdie.forward(100)
        turdie.left(120)
    #window_triangle.exitonclick()

#draw_triangle()
#draw_circle()

num_squares = int(input('Please enter number of squares: '))
for i in range (0,num_squares):
    draw_square(i*360/num_squares)
