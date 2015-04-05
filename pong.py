# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randint(3,5), random.randint(1,5)]
    if not direction:
        ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle2_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel   
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bounce off walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # determine whether ball and gutters collide
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (ball_pos[1] < paddle1_pos) or (ball_pos[1] > paddle1_pos + PAD_HEIGHT):
            spawn_ball(RIGHT)
            score2 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
    if ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS:
        if (ball_pos[1] < paddle2_pos) or (ball_pos[1] > paddle2_pos + PAD_HEIGHT):
            spawn_ball(LEFT)
            score1 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel < 0 or paddle1_pos + paddle1_vel >= HEIGHT-1-PAD_HEIGHT :
        pass
    else:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel < 0 or paddle2_pos + paddle2_vel >= HEIGHT-1-PAD_HEIGHT:
        pass
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    paddle1_polygon = [(0, paddle1_pos), 
                   (0, paddle1_pos + PAD_HEIGHT), 
                   (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), 
                   (PAD_WIDTH, paddle1_pos)]
    paddle2_polygon = [(WIDTH-1, paddle2_pos), 
                   (WIDTH-1, paddle2_pos + PAD_HEIGHT), 
                   (WIDTH-1-PAD_WIDTH, paddle2_pos + PAD_HEIGHT), 
                   (WIDTH-1-PAD_WIDTH, paddle2_pos)]
    
    canvas.draw_polygon(paddle1_polygon, 2, "Red", "Yellow")
    canvas.draw_polygon(paddle2_polygon, 2, "Red", "Yellow")   
    
    # draw scores
    sscore1 = str(score1)
    sscore2 = str(score2)
    canvas.draw_text(("Shak: " + sscore1 + " Salope: " + sscore2), (235, 50), 20, "White") 
    if score1 == 5:
        canvas.draw_text("Sous mon bite", (0, 200), 100, "Yellow")
    if score2 == 5:
        canvas.draw_text("Tu es la proprietaire :(", (0, 200), 60, "Yellow")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    speed = 5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = speed
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -speed
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = speed
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -speed
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()

